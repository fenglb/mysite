# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-27 08:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0009_instrumentappointment_has_approved'),
    ]

    operations = [
        migrations.AddField(
            model_name='instrumentappointment',
            name='feedback',
            field=models.TextField(blank=True, max_length=300, null=True, verbose_name='\u53cd\u9988\u4fe1\u606f'),
        ),
    ]
