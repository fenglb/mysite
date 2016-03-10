#-*- coding=utf-8-*-
from django.db import models
from datetime import datetime, timedelta
from accounts.models import CustomUser

# Create your models here.

class Entrance(models.Model):
    #    ('D500', u'靠500M核磁室门'),
    #    ('D102', u'值班室大门'),
    #    ('D103', u'值班室里门'),
    #    ('D600', u'靠600M核磁室门')
    name = models.CharField(max_length=100, verbose_name=u'门禁', default=u'值班室大门')
    code = models.CharField(max_length=4, verbose_name=u'编号', default='D102')
    user = models.ManyToManyField(CustomUser, verbose_name=u'授权者', blank=True) #授权者

    def __str__(self):
        return self.name.encode('utf-8')

class EntranceAppointment(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name=u'申请人')
    entrance = models.ManyToManyField( Entrance, verbose_name=u'门禁', help_text=u'进出核磁中心请同时申请“值班室大门”，“值班室里门”；而其他申请请根据需求来。通过按住Ctrl来实现多选！')
    reason   = models.TextField( max_length=300, blank=True, null=True, verbose_name=u'申请理由', help_text=u'请给出申请理由，不然可能会导致申请不通过！' )
    created_datetime = models.DateTimeField( auto_now_add=True )
    expired_time = models.DateField( default=datetime.now()+timedelta(days=100*365), verbose_name=u'失效日期' )
    has_approved = models.NullBooleanField(verbose_name='是否赞同', help_text=u'空着表示未处理', null=True, blank=True)
    feedback = models.TextField(max_length=300, verbose_name=u'反馈信息', null=True, blank=True)

    def __str__(self):
        all_entrances = u",".join( [door.name for door in self.entrance.all()] )
        strforback = u'[{0}]申请开通[{1}], 有效期到[{2}]'.format(self.user.surname, all_entrances, self.expired_time.strftime("%Y-%m-%d") )
        return strforback.encode('utf-8')
    
class Event(models.Model):
    entrance = models.ForeignKey( Entrance, verbose_name=u'门号' )
    user    = models.ForeignKey( CustomUser, verbose_name=u'出入者' )
    datetime = models.DateTimeField(verbose_name=u'时间')

    def getUserSurname(self):
        return self.user.surname.encode('utf-8')
    getUserSurname.short_description = u'出入者'
    def __str__(self):
        sen = u'{0}在{1}进入"{2}"'.format(self.user.surname, self.datetime.strftime("%Y-%m-%d %H:%M"), self.entrance.name )
        return sen.encode('utf-8')
