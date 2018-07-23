from django.contrib import admin
from django import forms
# Register your models here.
from .models import Sys, Dev, Devtype, Namesys, Chan, DevTree, DevTreeItem, MetaData

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
    filter_horizontal = ('chans', 'metadata')


class SysAdmin(admin.ModelAdmin):
    list_display = ('name', 'label', 'parent', 'ord', 'description', 'dev_count')
    filter_horizontal = ('devs',)


class SysMPAdmin(TreeAdmin):
    form = movenodeform_factory(SysMP)
    filter_horizontal = ('devs',)


class NamesysAdmin(admin.ModelAdmin):
    list_display = ('label', 'name', 'soft', 'def_soft')
    search_fields = ['label', 'name']


class DevAdmin(admin.ModelAdmin):
    list_display = ('label', 'name', 'ord', 'description', 'namesys', 'meta_count', 'enabled')
    list_filter = ['enabled', 'sys', 'namesys', 'devtype']
    search_fields = ['label', 'name', 'description']
    filter_horizontal = ('devtype', 'metadata')


class ChanAdmin(admin.ModelAdmin):
    list_display = ('label', 'name', 'access', 'units',
                    'dtype', 'dsize', 'protocol', 'ord', 'savable',)
    list_filter = ['protocol']
    search_fields = ['label', 'name']



class DevTreeAdmin(admin.ModelAdmin):
    list_display = ('name',)


class DevTreeItemAdmin(admin.ModelAdmin):
    list_display = ('devtree', 'dev', 'parent')


class MetaDataAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Sys, SysAdmin)
admin.site.register(SysMP, SysMPAdmin)

admin.site.register(Dev, DevAdmin)
admin.site.register(Devtype, DevtypeAdmin)
admin.site.register(Namesys, NamesysAdmin)
admin.site.register(Chan, ChanAdmin)
admin.site.register(DevTree, DevTreeAdmin)
admin.site.register(DevTreeItem, DevTreeItemAdmin)
admin.site.register(MetaData, MetaDataAdmin)
