from django.contrib.postgres.fields import JSONField
from django.db import models
from django.db.models import Count
from treebeard.mp_tree import MP_Node

# Create your models here.
class Namesys(models.Model):
    name = models.CharField(max_length=300)
    label = models.CharField(max_length=100)
    soft = models.BooleanField(default=False)
    def_soft = models.BooleanField(default=False)

    def __str__(self):
        return self.label

    class Meta:
        db_table = 'namesys'
        ordering = ['id', ]


class Chan(models.Model):
    name = models.CharField(max_length=100, blank=True, default='')
    access = models.CharField(max_length=10, default='r')
    units = models.CharField(max_length=100, blank=True, default='')
    protocol = models.CharField(max_length=100)
    label = models.CharField(max_length=100, blank=True, default='')
    dtype = models.CharField(max_length=100, blank=True, default='')
    dsize = models.IntegerField(default=1)
    ord = models.IntegerField(default=1)
    savable = models.BooleanField(default=True)

    def __str__(self):
        return self.label

    class Meta:
        db_table = 'chan'
        ordering = ['label', 'name', ]


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
    chans = models.ManyToManyField(Chan, blank=True)
    metadata = models.ManyToManyField(MetaData, blank=True)

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
    objects = DevManager()

    def meta_count(self):
        return self.metacount

    def __str__(self):
        return self.label

    class Meta:
        db_table = 'dev'
        ordering = ['ord', ]


class SysManager(models.Manager):
    def get_queryset(self):
        return super(SysManager, self).get_queryset().annotate(devcount=Count('devs'))


class Sys(MP_Node):
    node_order_by = ['ord']
    ord = models.IntegerField()
    name = models.CharField(max_length=100, default='')
    label = models.CharField(max_length=100, default='')
    description = models.CharField(max_length=1024, default='', blank=True, null=True)
    devs = models.ManyToManyField(Dev, blank=True)

    def dev_count(self):
        return self.devcount

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'sys'


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
