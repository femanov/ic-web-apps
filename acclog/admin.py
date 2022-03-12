from django.contrib import admin

# Register your models here.
from .models import LogChan, LogData


@admin.register(LogChan)
class LogChanAdmin(admin.ModelAdmin):
    search_fields = ['chan_name', 'cur_chan_name']



