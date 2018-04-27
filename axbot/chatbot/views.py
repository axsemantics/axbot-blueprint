import json
import re
from time import sleep
from uuid import uuid4

import requests
from django.conf import settings
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from .models import AxResponse
from .utils import convert_keys, get_apitoken, signature_valid


class AxWebhook(View):
    webhooksecret = None

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(AxWebhook, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        isvalid = signature_valid(self.get_webhooksecret(), request)
        if not isvalid:
            return HttpResponse(status=403)

        body_unicode = request.body.decode(request.encoding or 'utf-8')
        body = json.loads(body_unicode)
        error = bool(body.get('error'))

        AxResponse.objects.create(
            ax_uid=body['uid'],
            ax_error=error,
            ax_text=body['text'] if not error else None,
        )

        return HttpResponse(status=201)

    def get_webhooksecret(self):
        if self.webhooksecret is None:
            return settings.AX_WEBHOOKSECRET
        return self.webhooksecret


class Ax(View):
    instant_id = None
    refresh_token = None

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(Ax, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        body = self.preprocessing(request, body)
        ax_instant_request = self.generate_ax_text(request, body)
        if ax_instant_request is None:
            return HttpResponse(status=408)

        # dialogflow response json format
        response_data = self.postprocessing(request, ax_instant_request)
        return HttpResponse(
            json.dumps(response_data), content_type='application/json')

    def preprocessing(self, request, obj):
        p = re.compile(r'[^a-zA-Z\d]')
        convert_keys(obj, p)
        return obj

    def postprocessing(self, request, ax_instant_request):
        # to use other message objects see:
        # https://dialogflow.com/docs/reference/agent/message-objects
        texttosend = ax_instant_request.ax_text
        response_data = {
            'speech': texttosend,
            'displayText': texttosend,
            'data': {},
            'contextOut': [],
            'source': 'webhook',
        }
        return response_data

    def get_instant_id(self, request):
        if self.instant_id is None:
            return settings.AX_INSTANT_ID
        return self.instant_id

    def generate_ax_text(self, request, obj):
        uuid = uuid4()
        instant_id = self.get_instant_id(request)
        uid = str(uuid)
        url = 'https://api.ax-semantics.com/v2/instant/{id}/generate-content/{uid}/'.format(
            id=instant_id,
            uid=uid,
        )
        payload = json.dumps(obj)
        apitoken = self.get_apitoken(request)
        headers = {
            'authorization': 'JWT {}'.format(apitoken),
            'content-type': 'application/json',
        }
        response = requests.post(
            url=url,
            data=payload,
            headers=headers,
        )
        assert response.status_code < 300
        ax_instant_request = None
        for _ in range(30):
            sleep(0.1)
            try:
                ax_instant_request = AxResponse.objects.get(ax_uid=uid)
            except AxResponse.DoesNotExist:
                continue
            break
        return ax_instant_request

    def get_apitoken(self, request):
        refresh_token = self.get_refresh_token(request)
        return get_apitoken(refresh_token)

    def get_refresh_token(self, request):
        return self.refresh_token or settings.AX_REFRESH_TOKEN
