# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-12 02:51
from __future__ import unicode_literals

import datetime
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_auto_20160308_1610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(default='unkown@xmu.edu.cn', help_text='有效邮箱，用于认证通知', max_length=255, verbose_name='邮箱'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='expired_time',
            field=models.DateField(default=datetime.date(2116, 2, 17), verbose_name='失效日期'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='phone_number',
            field=models.CharField(default='05920000000', help_text='格式为05922186874或者手机号码', max_length=18, verbose_name='电话号码'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='position',
            field=models.CharField(choices=[('student', '厦大学生'), ('staff', '厦大教师'), ('visit', '其他')], default='student', max_length=7, verbose_name='身份'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='profile_image',
            field=models.ImageField(default='/media/profile/default.png', upload_to='profile', verbose_name='个人照片'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(help_text='纯数字和字母', max_length=30, unique=True, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z]*$', message='只有[0-9a-z-A-Z]字符可以.')], verbose_name='用户名'),
        ),
        migrations.AlterField(
            model_name='personincharge',
            name='email0',
            field=models.EmailField(default='unkown@xmu.edu.cn', help_text='有效邮箱，用于认证通知', max_length=255, verbose_name='邮箱'),
        ),
        migrations.AlterField(
            model_name='personincharge',
            name='phone_number0',
            field=models.CharField(default='05920000000', help_text='格式为05922186874或者手机号码', max_length=18, verbose_name='电话号码'),
        ),
        migrations.AlterField(
            model_name='personincharge',
            name='titles',
            field=models.CharField(choices=[('PI', '课题组负责人'), ('FL', '经费负责人'), ('OL', '公司领导')], default='PI', max_length=3, verbose_name='职务'),
        ),
    ]
