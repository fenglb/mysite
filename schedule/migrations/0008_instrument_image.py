# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-27 02:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0007_instrument_instrumentappointment'),
    ]

    operations = [
        migrations.AddField(
            model_name='instrument',
            name='image',
            field=models.ImageField(default=b'/media/images/default.png', upload_to=b'images', verbose_name='\u7167\u7247'),
        ),
    ]
