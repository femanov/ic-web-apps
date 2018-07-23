from django.contrib import admin

# Register your models here.
from .models import Mode, ModeData, FullChan


class ModeAdmin(admin.ModelAdmin):
    list_display = ('comment', 'stime')


class ModeDataAdmin(admin.ModelAdmin):
    list_display = ('fullchan', 'mode', 'utime', 'value', 'available')
    search_fields = ['fullchan']


class FullChanAdmin(admin.ModelAdmin):
    list_display = ('chan_name', 'is_current')
    search_fields = ['chan_name']



admin.site.register(Mode, ModeAdmin)
admin.site.register(ModeData, ModeDataAdmin)
admin.site.register(FullChan, FullChanAdmin)
