from django.db import models
from django.contrib.postgres.fields import ArrayField, JSONField


class LogChan(models.Model):
    protocol = models.CharField(max_length=50, default='')
    chan_name = models.CharField(max_length=1024, default='')
    cur_chan_name = models.CharField(max_length=1024, default='')
    dtype = models.CharField(max_length=20, default='double')
    log_type = models.CharField(max_length=20, default='double')  # JSONField(default=dict)
    dev_id = models.IntegerField(default=0)
    chan_id = models.IntegerField(default=0)
    is_current = models.BooleanField(default=False)

    class Meta:
        db_table = 'logchan'
        constraints = [
            models.UniqueConstraint(fields=["chan_name", "dev_id", "chan_id"], name='logchan_uniq')
        ]


class LogData(models.Model):
    log_chan = models.ForeignKey(LogChan, on_delete=models.CASCADE)
    stime = models.DateTimeField(auto_now_add=True)
    data = JSONField(default=dict)

    class Meta:
        db_table = 'logdata'
