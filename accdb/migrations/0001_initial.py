# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-24 05:38
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=100)),
                ('access', models.CharField(max_length=10)),
                ('units', models.CharField(blank=True, default='', max_length=100)),
                ('protocol', models.CharField(max_length=100)),
                ('label', models.CharField(blank=True, default='', max_length=100)),
                ('dtype', models.CharField(blank=True, default='', max_length=100)),
                ('dsize', models.IntegerField(default=1)),
                ('ord', models.IntegerField(default=1)),
                ('handle', models.CharField(default='double', max_length=1000)),
                ('saveble', models.IntegerField(default=1)),
            ],
            options={
                'db_table': 'chan',
                'ordering': ['label', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Dev',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=100)),
                ('label', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, default='', max_length=1024)),
                ('enabled', models.IntegerField(default=1)),
                ('ord', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'dev',
                'ordering': ['ord'],
            },
        ),
        migrations.CreateModel(
            name='DevMeta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('data', django.contrib.postgres.fields.jsonb.JSONField(default={})),
            ],
            options={
                'db_table': 'devmeta',
            },
        ),
        migrations.CreateModel(
            name='DevTree',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'devtree',
            },
        ),
        migrations.CreateModel(
            name='DevTreeItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dev', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accdb.Dev')),
                ('devtree', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accdb.DevTree')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accdb.DevTreeItem')),
            ],
            options={
                'db_table': 'devtreeitem',
            },
        ),
        migrations.CreateModel(
            name='Devtype',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.CharField(blank=True, default='', max_length=1024)),
                ('soft', models.IntegerField(default=0)),
                ('chans', models.ManyToManyField(blank=True, to='accdb.Chan')),
            ],
            options={
                'db_table': 'devtype',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='FullChan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('protocol', models.CharField(default='', max_length=1024)),
                ('chan_name', models.CharField(default='', max_length=1024)),
                ('namesys_id', models.IntegerField(default=0)),
                ('dev_id', models.IntegerField(default=0)),
                ('chan_id', models.IntegerField(default=0)),
                ('is_current', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'fullchan',
            },
        ),
        migrations.CreateModel(
            name='Mode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=1024)),
                ('author', models.CharField(default='', max_length=100)),
                ('stime', models.DateTimeField(auto_now_add=True)),
                ('archived', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'mode',
            },
        ),
        migrations.CreateModel(
            name='ModeData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('utime', models.BigIntegerField()),
                ('value', models.FloatField(default=0)),
                ('available', models.IntegerField(default=0)),
                ('fullchan', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='accdb.FullChan')),
                ('mode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accdb.Mode')),
            ],
            options={
                'db_table': 'modedata',
            },
        ),
        migrations.CreateModel(
            name='ModeMark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('comment', models.CharField(max_length=1024)),
                ('author', models.CharField(default='', max_length=100)),
                ('mode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accdb.Mode')),
            ],
            options={
                'db_table': 'modemark',
            },
        ),
        migrations.CreateModel(
            name='Namesys',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('label', models.CharField(max_length=100)),
                ('soft', models.IntegerField(default=0)),
            ],
            options={
                'db_table': 'namesys',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Sys',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('label', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=1024)),
                ('ord', models.IntegerField(default=0)),
                ('devs', models.ManyToManyField(blank=True, to='accdb.Dev')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='accdb.Sys')),
            ],
            options={
                'db_table': 'sys',
                'ordering': ['ord'],
            },
        ),
        migrations.AddField(
            model_name='dev',
            name='devmeta',
            field=models.ManyToManyField(blank=True, to='accdb.DevMeta'),
        ),
        migrations.AddField(
            model_name='dev',
            name='devtype',
            field=models.ManyToManyField(to='accdb.Devtype'),
        ),
        migrations.AddField(
            model_name='dev',
            name='namesys',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accdb.Namesys'),
        ),
    ]
