# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-24 10:29
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20160223_1543'),
    ]

    operations = [
        migrations.RenameField(
            model_name='personincharge',
            old_name='email',
            new_name='email0',
        ),
        migrations.RenameField(
            model_name='personincharge',
            old_name='phone_number',
            new_name='phone_number0',
        ),
        migrations.RenameField(
            model_name='personincharge',
            old_name='surname',
            new_name='surname0',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='expired_time',
            field=models.DateField(default=datetime.datetime(2116, 1, 31, 18, 29, 17, 569433), verbose_name='\u5931\u6548\u65e5\u671f'),
        ),
    ]
