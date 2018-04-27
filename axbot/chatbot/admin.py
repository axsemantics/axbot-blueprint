from django.contrib.admin import ModelAdmin, register

from .models import AxResponse


@register(AxResponse)
class AxResponseAdmin(ModelAdmin):
    list_display = ('ax_uid', 'ax_text', 'ax_error', 'ax_error_message', "modified", "df_UserSessionId", "created")
