# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-08 08:10
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_auto_20160308_1053'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='email_code',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='expired_time',
            field=models.DateField(default=datetime.datetime(2116, 2, 13, 16, 10, 20, 588485), verbose_name='\u5931\u6548\u65e5\u671f'),
        ),
    ]
