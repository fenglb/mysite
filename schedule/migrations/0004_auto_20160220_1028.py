# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-20 02:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0003_auto_20160220_0948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sample',
            name='concentration',
            field=models.FloatField(blank=True, null=True, verbose_name='\u6d53\u5ea6/ML'),
        ),
        migrations.AlterField(
            model_name='sample',
            name='molecular_weight',
            field=models.FloatField(blank=True, null=True, verbose_name='\u5206\u5b50\u91cf'),
        ),
        migrations.AlterField(
            model_name='sample',
            name='name',
            field=models.CharField(max_length=100, verbose_name='\u540d\u79f0'),
        ),
        migrations.AlterField(
            model_name='sample',
            name='others',
            field=models.TextField(blank=True, null=True, verbose_name='\u5176\u4ed6'),
        ),
        migrations.AlterField(
            model_name='sample',
            name='solvent',
            field=models.CharField(blank=True, max_length=30, null=True, verbose_name='\u6c18\u4ee3\u8bd5\u5242'),
        ),
        migrations.AlterField(
            model_name='sample',
            name='structure',
            field=models.CharField(blank=True, max_length=1000, null=True, verbose_name='\u5316\u5b66\u5f0f'),
        ),
    ]
