# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-02 07:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0017_auto_20160302_1520'),
    ]

    operations = [
        migrations.AddField(
            model_name='sampleappointment',
            name='measure_type',
            field=models.TextField(blank=True, help_text='\u5b9e\u9a8c\u6d4b\u91cf\u7c7b\u578b\uff0cC13\uff0cH1\uff0c HSQC\uff0cHMBC\u7b49', null=True, verbose_name='\u5b9e\u9a8c\u7c7b\u578b'),
        ),
        migrations.AlterField(
            model_name='sample',
            name='name',
            field=models.CharField(default=b'2016030224', max_length=100, verbose_name='\u540d\u79f0'),
        ),
    ]
