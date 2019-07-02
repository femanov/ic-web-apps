from django.contrib.postgres.fields import JSONField
from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class FullChan(models.Model):
    protocol = models.CharField(max_length=50, default='')
    chan_name = models.CharField(max_length=1024, default='')
    cur_chan_name = models.CharField(max_length=1024, default='')
    access = models.CharField(max_length=10, default='')
    #namesys_id = models.IntegerField(default=0)
    dev_id = models.IntegerField(default=0)
    chan_id = models.IntegerField(default=0)
    is_current = models.BooleanField(default=False)
    systems = ArrayField(models.IntegerField(), default=list)

    class Meta:
        db_table = 'fullchan'
        constraints = [
            models.UniqueConstraint(fields=["chan_name", "dev_id", "chan_id"], name='fchan_uniq')
        ]


class TestMode(models.Model):
    comment = models.CharField(max_length=1024)
    author = models.CharField(max_length=50, default='')
    stime = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)
    data = JSONField(default=dict)

    class Meta:
        db_table = 'test_mode'


class Mode(models.Model):
    comment = models.CharField(max_length=1024)
    author = models.CharField(max_length=50, default='')
    stime = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)
    info = JSONField(default=dict)

    def __str__(self):
        return self.comment

    class Meta:
        db_table = 'mode'


class ModeData(models.Model):
    mode = models.ForeignKey(Mode, on_delete=models.CASCADE)
    utime = models.BigIntegerField()
    value = models.FloatField(default=0)
    available = models.BooleanField(default=False)
    fullchan = models.ForeignKey(FullChan, on_delete=models.SET_DEFAULT, default=1)

    def __str__(self):
        return str(self.mode) + " : " + str(self.fullchan)

    class Meta:
        db_table = 'modedata_t'


class ModeMark(models.Model):
    mode = models.ForeignKey(Mode, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100, unique=True)
    comment = models.CharField(max_length=1024)
    author = models.CharField(max_length=100, default='')

    class Meta:
        db_table = 'modemark'
