# Generated by Django 2.0.2 on 2018-07-13 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accdb', '0017_fullchan_cur_chan_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='devtype',
            name='devmeta',
            field=models.ManyToManyField(blank=True, to='accdb.DevMeta'),
        ),
    ]
