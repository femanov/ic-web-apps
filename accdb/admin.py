from django.contrib import admin
from django import forms
# Register your models here.
from treebeard.admin import TreeAdmin
from treebeard.forms import movenodeform_factory

from .models import Dev, Devtype, Namesys, Chan, DevTree, DevTreeItem, MetaData, AccessType, Protocol
from .models import Sys, Bridge



class DevtypeForm(forms.ModelForm):
    class Meta:
        fields = ['name', 'description', 'chans']
        model = Devtype
        widgets = {
            'chans': forms.SelectMultiple(attrs={'size': 30})
        }

@admin.register(Devtype)
class DevtypeAdmin(admin.ModelAdmin):
    search_fields = ['name', 'description']
    filter_horizontal = ('chans', 'metadata')

@admin.register(Sys)
class SysAdmin(TreeAdmin):
    form = movenodeform_factory(Sys)
    filter_horizontal = ('devs',)

@admin.register(Namesys)
class NamesysAdmin(admin.ModelAdmin):
    list_display = ('label', 'name', 'soft', 'def_soft')
    search_fields = ['label', 'name']

@admin.register(Dev)
class DevAdmin(admin.ModelAdmin):
    list_display = ('label', 'name', 'ord', 'description', 'namesys', 'meta_count', 'enabled', 'get_syss')
    list_filter = ['enabled', 'metadata', 'sys', 'namesys', 'devtype']
    search_fields = ['label', 'name', 'description']
    filter_horizontal = ('devtype', 'metadata',)

    def get_syss(self, obj):
        return [x.name for x in obj.sys.all()]

@admin.register(Chan)
class ChanAdmin(admin.ModelAdmin):
    list_display = ('label', 'name', 'access_type', 'units',
                    'dtype', 'dsize', 'cprotocol', 'ord', 'savable',)
    list_filter = ['cprotocol', 'devtype']
    search_fields = ['label', 'name']

@admin.register(AccessType)
class ChanAccessAdmin(admin.ModelAdmin):
    list_display = ('access', 'savable', 'direct_loadable')

@admin.register(Protocol)
class ChanProtocolAdmin(admin.ModelAdmin):
    list_display = ('protocol',)

@admin.register(DevTree)
class DevTreeAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(DevTreeItem)
class DevTreeItemAdmin(admin.ModelAdmin):
    list_display = ('devtree', 'dev', 'parent')

@admin.register(MetaData)
class MetaDataAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Bridge)
class BridgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'namesys')
    autocomplete_fields = ('namesys',)
    filter_horizontal = ('devs',)