# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-02 09:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0019_auto_20160302_1714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sample',
            name='name',
            field=models.CharField(max_length=100, verbose_name='\u540d\u79f0'),
        ),
    ]
