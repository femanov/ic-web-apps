from django.contrib import admin

# Register your models here.
from .models import Mode, FullChan, ModeMark


@admin.register(Mode)
class ModeAdmin(admin.ModelAdmin):
    list_display = ('author', 'comment', 'stime', 'archived')

@admin.register(FullChan)
class FullChanAdmin(admin.ModelAdmin):
    list_display = ('chan_name', 'is_current')
    search_fields = ['chan_name']


@admin.register(ModeMark)
class ModeMarkAdmin(admin.ModelAdmin):
    list_display = ('name', 'mode', 'comment', 'author')

