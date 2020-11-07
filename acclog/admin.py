from django.contrib import admin

# Register your models here.
from .models import LogChan, LogData


class LogChanAdmin(admin.ModelAdmin):
    pass


admin.site.register(LogChan, LogChanAdmin)

