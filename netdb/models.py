from django.db import models

class Domain(models.Model):
    name = models.CharField(max_length=255)
    admin_mail = models.CharField(max_length=255, default='emanov@inp.nsk.su')
    dns_serial = models.IntegerField(default=20)
    dns_options = models.TextField(default='', blank=True)
    nameservers = models.TextField(default='', blank=True)
    static_records = models.TextField(default='', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'domain'


class Net(models.Model):
    name = models.CharField(max_length=300)
    ip = models.GenericIPAddressField(protocol='IPv4')
    mask = models.IntegerField(default=24)
    domain = models.ForeignKey(Domain, default=1, on_delete=models.CASCADE)
    description = models.TextField(default='', blank=True)
    dhcp_options = models.TextField(default='', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'net'
        ordering = ['ip', 'name']


class Host(models.Model):
    name = models.CharField(max_length=300)
    ip = models.GenericIPAddressField(protocol='IPv4')
    mac = models.CharField(max_length=17)
    net = models.ForeignKey(Net, default=1, on_delete=models.CASCADE)
    location = models.CharField(max_length=300, default='', blank=True)
    aliases = models.CharField(max_length=300, default='', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'host'
        ordering = ['ip', 'name']
