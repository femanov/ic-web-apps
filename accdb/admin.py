from django.contrib import admin
from django import forms
# Register your models here.
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from .models import Dev, Devtype, Namesys, Chan, DevTree, DevTreeItem, MetaData, AccessType, Protocol
from .models import Sys



class DevtypeForm(forms.ModelForm):
    class Meta:
        fields = ['name', 'description', 'chans']
        model = Devtype
        widgets = {
            'chans': forms.SelectMultiple(attrs={'size': 30})
        }


class DevtypeAdmin(admin.ModelAdmin):
    search_fields = ['name', 'description']
    filter_horizontal = ('chans', 'metadata')


class SysAdmin(TreeAdmin):
    form = movenodeform_factory(Sys)
    filter_horizontal = ('devs',)


class NamesysAdmin(admin.ModelAdmin):
    list_display = ('label', 'name', 'soft', 'def_soft')
    search_fields = ['label', 'name']


class DevAdmin(admin.ModelAdmin):
    list_display = ('label', 'name', 'ord', 'description', 'namesys', 'meta_count', 'enabled', 'get_syss')
    list_filter = ['enabled', 'metadata', 'sys', 'namesys', 'devtype']
    search_fields = ['label', 'name', 'description']
    filter_horizontal = ('devtype', 'metadata',)

    def get_syss(self, obj):
        return [x.name for x in obj.sys.all()]

class ChanAdmin(admin.ModelAdmin):
    list_display = ('label', 'name', 'access_type', 'units',
                    'dtype', 'dsize', 'cprotocol', 'ord', 'savable',)
    list_filter = ['cprotocol', 'devtype']
    search_fields = ['label', 'name']


class ChanAccessAdmin(admin.ModelAdmin):
    list_display = ('access', 'savable', 'direct_loadable')


class ChanProtocolAdmin(admin.ModelAdmin):
    list_display = ('protocol',)


class DevTreeAdmin(admin.ModelAdmin):
    list_display = ('name',)


class DevTreeItemAdmin(admin.ModelAdmin):
    list_display = ('devtree', 'dev', 'parent')


class MetaDataAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Sys, SysAdmin)

admin.site.register(Dev, DevAdmin)
admin.site.register(Devtype, DevtypeAdmin)
admin.site.register(Namesys, NamesysAdmin)
admin.site.register(Chan, ChanAdmin)
admin.site.register(AccessType, ChanAccessAdmin)
admin.site.register(Protocol, ChanProtocolAdmin)
admin.site.register(DevTree, DevTreeAdmin)
admin.site.register(DevTreeItem, DevTreeItemAdmin)
admin.site.register(MetaData, MetaDataAdmin)
