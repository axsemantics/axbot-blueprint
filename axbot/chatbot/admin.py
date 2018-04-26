from django.contrib import admin
from.models import AxResponse


class AxResponseAdmin(admin.ModelAdmin):
    list_display = ('ax_uid', 'ax_text', 'ax_error', 'ax_error_message', "modified", "df_UserSessionId", "created")
admin.site.register(AxResponse, AxResponseAdmin)

# Register your models here.
