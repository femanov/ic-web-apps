# Generated by Django 2.0.2 on 2018-03-16 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accdb', '0004_auto_20180315_1122'),
    ]

    operations = [
        migrations.CreateModel(
            name='SysTestMP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('path', models.CharField(max_length=255, unique=True)),
                ('depth', models.PositiveIntegerField()),
                ('numchild', models.PositiveIntegerField(default=0)),
                ('ord', models.IntegerField(default=0)),
                ('name', models.CharField(default='', max_length=100)),
                ('label', models.CharField(default='', max_length=100)),
                ('description', models.CharField(blank=True, default='', max_length=1024, null=True)),
                ('devs', models.ManyToManyField(blank=True, to='accdb.Dev')),
            ],
            options={
                'db_table': 'systest_mp',
            },
        ),
    ]
