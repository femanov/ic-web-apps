# Generated by Django 2.0.2 on 2018-07-05 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accdb', '0011_auto_20180705_0950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chan',
            name='saveble',
            field=models.BooleanField(default='True'),
        ),
        migrations.AlterField(
            model_name='dev',
            name='enabled',
            field=models.BooleanField(default='True'),
        ),
        migrations.AlterField(
            model_name='fullchan',
            name='is_current',
            field=models.BooleanField(default='False'),
        ),
        migrations.AlterField(
            model_name='mode',
            name='archived',
            field=models.BooleanField(default='False'),
        ),
        migrations.AlterField(
            model_name='modedata',
            name='available',
            field=models.BooleanField(default='False'),
        ),
    ]