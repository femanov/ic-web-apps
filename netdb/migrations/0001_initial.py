# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-24 05:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('dns_serial', models.IntegerField(default=20)),
                ('dns_options', models.TextField(blank=True, default='')),
                ('nameservers', models.TextField(blank=True, default='')),
                ('static_records', models.TextField(blank=True, default='')),
            ],
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('ip', models.GenericIPAddressField(protocol='IPv4')),
                ('mac', models.CharField(max_length=17)),
                ('location', models.CharField(blank=True, default='', max_length=300)),
            ],
            options={
                'db_table': 'host',
                'ordering': ['ip', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Net',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('ip', models.GenericIPAddressField(protocol='IPv4')),
                ('mask', models.IntegerField(default=24)),
                ('dns_serial', models.IntegerField(default=20)),
                ('description', models.TextField(blank=True, default='')),
                ('dhcp_options', models.TextField(blank=True, default='')),
                ('dns_options', models.TextField(blank=True, default='')),
                ('domain', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='netdb.Domain')),
            ],
            options={
                'db_table': 'net',
                'ordering': ['ip', 'name'],
            },
        ),
        migrations.AddField(
            model_name='host',
            name='net',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='netdb.Net'),
        ),
    ]
