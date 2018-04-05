from django.contrib import admin

# Register your models here.
from .models import Host, Net, Domain


class HostAdmin(admin.ModelAdmin):
    list_display = ('name', 'ip', 'mac', 'location', 'net')
    list_filter = ['net']
    search_fields = ('name', 'ip', 'mac', 'location')


class NetAdmin(admin.ModelAdmin):
    list_display = ('name', 'ip', 'mask')


class DomainAdmin(admin.ModelAdmin):
    list_display = ('name', )


admin.site.register(Host, HostAdmin)
admin.site.register(Net, NetAdmin)
admin.site.register(Domain, DomainAdmin)
