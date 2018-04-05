from django.contrib import admin
from django import forms
# Register your models here.
from .models import Sys, Dev, Devtype, Namesys, Chan, Mode, ModeData, DevTree, DevTreeItem, DevMeta, FullChan

from .models import SysMP
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

class DevtypeForm(forms.ModelForm):
    class Meta:
        fields = ['name', 'description', 'chans']
        model = Devtype
        widgets = {
            'chans': forms.SelectMultiple(attrs={'size': 30})
        }


class DevtypeAdmin(admin.ModelAdmin):
    #form = DevtypeForm
    search_fields = ['name', 'description']
    filter_horizontal = ('chans',)


class SysAdmin(admin.ModelAdmin):
    list_display = ('name', 'label', 'parent', 'ord', 'description', 'dev_count')
    filter_horizontal = ('devs',)


class SysTestMPAdmin(TreeAdmin):
    form = movenodeform_factory(SysMP)
    filter_horizontal = ('devs',)


class NamesysAdmin(admin.ModelAdmin):
    list_display = ('label', 'name', 'soft')
    search_fields = ['label', 'name']


class DevAdmin(admin.ModelAdmin):
    list_display = ('label', 'name', 'ord', 'description', 'namesys', 'meta_count')
    list_filter = ['enabled', 'sys', 'namesys', 'devtype']
    search_fields = ['label', 'name', 'description']
    filter_horizontal = ('devtype', 'devmeta')


class ChanAdmin(admin.ModelAdmin):
    list_display = ('label', 'name', 'access', 'units',
                    'dtype', 'dsize', 'protocol', 'ord', 'handle')
    list_filter = ['protocol']
    search_fields = ['label', 'name']


class ModeAdmin(admin.ModelAdmin):
    list_display = ('comment', 'stime')


class ModeDataAdmin(admin.ModelAdmin):
    list_display = ('fullchan', 'mode', 'utime', 'value', 'available')
    search_fields = ['fullchan']


class DevTreeAdmin(admin.ModelAdmin):
    list_display = ('name',)


class DevTreeItemAdmin(admin.ModelAdmin):
    list_display = ('devtree', 'dev', 'parent')


class DevMetaAdmin(admin.ModelAdmin):
    list_display = ('name',)


class FullChanAdmin(admin.ModelAdmin):
    list_display = ('chan_name', 'is_current')
    search_fields = ['chan_name']



admin.site.register(Mode, ModeAdmin)
admin.site.register(ModeData, ModeDataAdmin)
admin.site.register(Sys, SysAdmin)
admin.site.register(SysMP, SysTestMPAdmin)

admin.site.register(Dev, DevAdmin)
admin.site.register(Devtype, DevtypeAdmin)
admin.site.register(Namesys, NamesysAdmin)
admin.site.register(Chan, ChanAdmin)
admin.site.register(DevTree, DevTreeAdmin)
admin.site.register(DevTreeItem, DevTreeItemAdmin)
admin.site.register(DevMeta, DevMetaAdmin)
admin.site.register(FullChan, FullChanAdmin)
