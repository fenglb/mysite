# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-06 08:51
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eguard', '0012_auto_20161006_1650'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entranceappointment',
            name='expired_time',
            field=models.DateField(default=datetime.datetime(2116, 9, 12, 16, 51, 4, 761392), verbose_name='失效日期'),
        ),
    ]
