# Generated by Django 2.1.1 on 2018-09-02 10:28

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accmode', '0003_auto_20180718_0854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fullchan',
            name='systems',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), default=list, size=None),
        ),
    ]