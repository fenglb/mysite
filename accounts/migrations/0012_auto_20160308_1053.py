# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-08 02:53
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20160227_2016'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='title',
            field=models.CharField(blank=True, max_length=50, verbose_name='\u804c\u79f0'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='expired_time',
            field=models.DateField(default=datetime.datetime(2116, 2, 13, 10, 53, 12, 470208), verbose_name='\u5931\u6548\u65e5\u671f'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_staff',
            field=models.BooleanField(default=False, verbose_name='NMRCEN_Man'),
        ),
    ]
