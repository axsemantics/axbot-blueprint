from django.db import models
from django_extensions.db.models import TimeStampedModel


class AxResponse(TimeStampedModel):
    ax_uid = models.UUIDField(unique=True)
    ax_text = models.TextField(null=False, blank=True)
    ax_error = models.BooleanField()
    # captures ax error model, that can be boolean or text
    ax_error_message = models.TextField(null=False, blank=True)

    # SessionId passed from and to Dialogflow
    df_UserSessionId = models.TextField(null=False, blank=True)
