from django.contrib import admin

# Register your models here.
from .models import Mode, FullChan


class ModeAdmin(admin.ModelAdmin):
    list_display = ('author', 'comment', 'stime', 'archived')


class FullChanAdmin(admin.ModelAdmin):
    list_display = ('chan_name', 'is_current')
    search_fields = ['chan_name']


admin.site.register(Mode, ModeAdmin)
admin.site.register(FullChan, FullChanAdmin)
