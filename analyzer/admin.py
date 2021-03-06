from django.contrib import admin
from .models import S3AccessLog


class S3AccessLogAdmin(admin.ModelAdmin):
    list_display = ['bucket_owner', 'bucket_name', 'request_datetime', 'remote_ip', 'requesta', 'request_id', 'operation', 'request_key', 'request_uri', 'http_status', 'error_code', 'bytes_sent', 'object_size', 'total_time', 'turn_around_time', 'referrer', 'user_agent', 'version_id', ]
    fieldsets = [(None, {'fields': list_display})]
    list_filter = ['bucket_name', 'bucket_owner', 'version_id', 'referrer', 'http_status', 'error_code', 'operation', ]
    search_fields = list_display


admin.site.register(S3AccessLog, S3AccessLogAdmin)
