from django.contrib import admin
from django import forms
# Register your models here.
from .models import Dev, Devtype, Namesys, Chan, DevTree, DevTreeItem, MetaData, CAccessType, CProtocol

from .models import Sys
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
    filter_horizontal = ('chans', 'metadata')


# class SysAdmin(admin.ModelAdmin):
#     list_display = ('name', 'label', 'parent', 'ord', 'description', 'dev_count')
#     filter_horizontal = ('devs',)


class SysAdmin(TreeAdmin):
    form = movenodeform_factory(Sys)
    filter_horizontal = ('devs',)


class NamesysAdmin(admin.ModelAdmin):
    list_display = ('label', 'name', 'soft', 'def_soft')
    search_fields = ['label', 'name']


class DevAdmin(admin.ModelAdmin):
    list_display = ('label', 'name', 'ord', 'description', 'namesys', 'meta_count', 'enabled')
    list_filter = ['enabled', 'metadata', 'namesys', 'devtype']
    search_fields = ['label', 'name', 'description']
    filter_horizontal = ('devtype', 'metadata')


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
admin.site.register(CAccessType, ChanAccessAdmin)
admin.site.register(CProtocol, ChanProtocolAdmin)
admin.site.register(DevTree, DevTreeAdmin)
admin.site.register(DevTreeItem, DevTreeItemAdmin)
admin.site.register(MetaData, MetaDataAdmin)
