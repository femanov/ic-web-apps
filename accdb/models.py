from django.db.models import JSONField
from django.db import models
from django.db.models import Count
from treebeard.mp_tree import MP_Node


# better to move this in separate place?
dtypes = {
    'int8': 'b',
    'uint8': '+b',
    'int16': 'h',
    'uint16': '+h',
    'int32': 'i',
    'uint32': '+i',
    'int': 'i',
    'int64': 'q',
    'uint64': '+q',
    'float': 's',
    'double': 'd',
    'text': 't',
    'utext': 'u',
    '': 'd',
}


class Namesys(models.Model):
    name = models.CharField(max_length=300)
    label = models.CharField(max_length=100)
    soft = models.BooleanField(default=False)
    def_soft = models.BooleanField(default=False)
    info = JSONField(default=dict)

    def cx_host(self):
        return self.name.split(':')[0]

    def cx_srvnum(self):
        return self.name.split(':')[1].split('.')[0]

    def __str__(self):
        return f"{self.label} ({self.name})"

    class Meta:
        db_table = 'namesys'
        ordering = ['name', ]


class AccessType(models.Model):
    access = models.CharField(max_length=10, default='r')
    savable = models.BooleanField(default=True)
    direct_loadable = models.BooleanField(default=True)
    load_implemented = models.BooleanField(default=True)

    def __str__(self):
        return self.access

    class Meta:
        db_table = 'caccess_type'


class Protocol(models.Model):
    protocol = models.CharField(max_length=10)

    def __str__(self):
        return self.protocol

    class Meta:
        db_table = 'cprotocol'


class Chan(models.Model):
    DT_CHOICES = [
        ('int8', 'int8'),
        ('int16', 'int16'),
        ('int32', 'int32'),
        ('int64', 'int64'),
        ('uint8', 'uint8'),
        ('uint16', 'uint16'),
        ('uint32', 'uint32'),
        ('uint64', 'uint64'),
        ('float', 'float'),
        ('double', 'double'),
        ('text', 'text'),
        ('utext', 'utext'),
    ]
    name = models.CharField(max_length=100, blank=True, default='')
    units = models.CharField(max_length=100, blank=True, default='')
    label = models.CharField(max_length=100, blank=True, default='')
    dtype = models.CharField(max_length=100, blank=True, choices=DT_CHOICES, default='int32')
    dsize = models.IntegerField(default=1)
    params = models.CharField(max_length=200, blank=True, default='')
    ord = models.IntegerField(default=1)
    savable = models.BooleanField(default=True)
    access_type = models.ForeignKey(AccessType, on_delete=models.SET_NULL, default=4, blank=True, null=True)
    cprotocol = models.ForeignKey(Protocol, on_delete=models.SET_NULL, default=1, blank=True, null=True)

    def cx_str_for_dt(self, num):
        u = f" units:{self.units}" if len(self.units) > 0 else ''
        return f"{self.name} {num} {self.params}{u}"

    def cx_type_sig(self):
        return f"{dtypes[self.dtype]}{self.dsize}"

    def __str__(self):
        return self.label

    class Meta:
        db_table = 'chan'
        ordering = ['ord', 'label', 'name', ]


class MetaData(models.Model):
    name = models.CharField(max_length=100)
    data = JSONField(default=dict)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'metadata'


class Devtype(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1024, blank=True, default='')
    soft = models.BooleanField(default=False)
    driver = models.CharField(max_length=100, blank=True, default='')
    chans = models.ManyToManyField(Chan, blank=True)
    metadata = models.ManyToManyField(MetaData, blank=True)

    def cx_str(self):
        cs = self.chans.all()
        cgs = {}
        for x in cs:
            ts = x.cx_type_sig()
            if ts in cgs:
                cgs[ts].append(x)
            else:
                cgs[ts] = [x]
        cg_ts = [f"w{len(cgs[x])}{x}" for x in cgs]
        dt_strs = [f"devtype {self.name} {','.join(cg_ts)}{' {'}"]
        c_count = 0
        for x in cgs:
            for c in cgs[x]:
                dt_strs.append(c.cx_str_for_dt(c_count))
                c_count += 1
        dt_strs.append('}')
        return '\n'.join(dt_strs)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'devtype'
        ordering = ['name', ]


class DevManager(models.Manager):
    def get_queryset(self):
        return super(DevManager, self).get_queryset().annotate(metacount=Count('metadata'))


class Dev(models.Model):
    name = models.CharField(max_length=100, blank=True, default='')
    label = models.CharField(max_length=100)
    description = models.CharField(max_length=1024, blank=True, default='')
    namesys = models.ForeignKey(Namesys, on_delete=models.SET_NULL, blank=True, null=True)
    devtype = models.ManyToManyField(Devtype)
    enabled = models.BooleanField(default=True)
    ord = models.IntegerField(default=0)
    metadata = models.ManyToManyField(MetaData, blank=True)
    params = models.CharField(max_length=200, blank=True, default='')
    objects = DevManager()

    def meta_count(self):
        return self.metacount

    def __str__(self):
        try:
            ret = f"{self.namesys.label}:{self.label}"
        except:
            ret = f"none:{self.label}"
        return ret

    class Meta:
        db_table = 'dev'
        ordering = ['ord']


class SysManager(models.Manager):
    def get_queryset(self):
        return super(SysManager, self).get_queryset().annotate(devcount=Count('devs'))


class Sys(MP_Node):
    node_order_by = ['ord']
    ord = models.IntegerField()
    name = models.CharField(max_length=100, default='')
    label = models.CharField(max_length=100, default='')
    description = models.CharField(max_length=1024, default='', blank=True, null=True)
    devs = models.ManyToManyField(Dev, related_name='sys', blank=True)

    def dev_count(self):
        return self.devcount

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'sys'


class AutoLoad(models.Model):
    name = models.CharField(max_length=100, default='')
    enabled = models.BooleanField(default=True)
    mark_name = models.CharField(max_length=4, default='')
    signal_chan = models.CharField(max_length=100, default='')
    syss = models.ManyToManyField(Sys, blank=True)
    access_types = models.ManyToManyField(AccessType, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "autoload"


# some data about device hierarchic structures like
# possibly need to switch to MP_node
class DevTree(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'devtree'


class DevTreeItem(models.Model):
    devtree = models.ForeignKey(DevTree, on_delete=models.CASCADE)
    dev = models.ForeignKey(Dev, on_delete=models.SET_NULL, null=True)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.dev.name

    class Meta:
        db_table = 'devtreeitem'


class Bridge(models.Model):
    name = models.CharField(max_length=100, blank=True, default='')
    namesys = models.ForeignKey(Namesys, on_delete=models.SET_NULL, blank=True, null=True)
    devs = models.ManyToManyField(Dev, blank=True)
    readonly = models.BooleanField(default=False)
    on_update = models.BooleanField(default=False)
    savable = models.BooleanField(default=True)


    class Meta:
        db_table = 'bridge'


class SrvMirror(models.Model):
    name = models.CharField(max_length=100, blank=True, default='')
    description = models.CharField(max_length=1024, default='', blank=True, null=True)
    source = models.ForeignKey(Namesys, on_delete=models.SET_NULL, blank=True, null=True)
    readonly = models.BooleanField(default=False)
    on_update = models.BooleanField(default=False)
    savable = models.BooleanField(default=True)

    def cx_host(self):
        return self.name.split(':')[0]

    def cx_srvnum(self):
        return self.name.split(':')[1].split('.')[0]


    class Meta:
        db_table = 'srvmirror'
