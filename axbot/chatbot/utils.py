import hashlib
import hmac
import json

import requests
from django.conf import settings
from django.core.cache import caches


def convert_keys(obj, p):
    if isinstance(obj, dict):
        for k in obj.keys():
            convert_keys(obj[k], p)
            try:
                tempkey = p.sub('_', k)
                obj[tempkey] = obj.pop(k)
            except Exception:
                pass
    elif isinstance(obj, list):
        for item in obj:
            try:
                convert_keys(item, p)
            except Exception:
                # print(k, v, "\t<<>> Error")
                pass

    return obj


def get_apitoken(refresh_token):
    try:
        token_cache_name = settings.AX_TOKEN_CACHE
    except AttributeError:
        token_cache_name = 'default'

    token_cache = caches[token_cache_name]
    token_hash = hashlib.sha256(refresh_token.encode())
    cache_key = 'AX_API_ID_TOKEN_{}'.format(token_hash.hexdigest())
    id_token = token_cache.get(cache_key)
    if id_token is None:
        response = token_exchange(refresh_token)
        id_token = response['id_token']
        expires_in = response['expires_in']
        token_cache.set(cache_key, id_token, 0.7 * expires_in)
    return id_token


def token_exchange(refresh_token):
    response = requests.post(
        url='https://api.ax-semantics.com/v3/token-exchange/',
        data=json.dumps({
            'refresh_token': refresh_token,
        }),
        headers={'Content-Type': 'application/json'},
    )
    return response.json()


def signature_valid(secret, request):
    try:
        raw_data = request.body
        signature_header = request.META['HTTP_X_MYAX_SIGNATURE'].replace('sha1=', '')
        signature_content = hmac.new(
            key=secret.encode('utf-8'),
            msg=raw_data,
            digestmod=hashlib.sha1,
        ).hexdigest()
    except AttributeError:
        pass
    except KeyError:
        pass
    except Exception:
        raise
    else:
        return bool(signature_header == signature_content)
    return False
