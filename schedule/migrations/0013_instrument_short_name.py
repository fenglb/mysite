# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-28 02:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0012_auto_20160227_2116'),
    ]

    operations = [
        migrations.AddField(
            model_name='instrument',
            name='short_name',
            field=models.CharField(default='unkown', max_length=100, verbose_name='\u7b80\u79f0'),
            preserve_default=False,
        ),
    ]
