from django.db import models
from eguard.eguardcrawler import EntranceGuard
from datetime import datetime, timedelta
from accounts.models import CustomUser

# Create your models here.

class Entrance(models.Model):
    #    ('D500', '靠500M核磁室门'),
    #    ('D102', '值班室大门'),
    #    ('D103', '值班室里门'),
    #    ('D600', '靠600M核磁室门')
    name = models.CharField(max_length=100, verbose_name='门禁', default='值班室大门')
    code = models.CharField(max_length=4, verbose_name='编号', default='D102')
    user = models.ManyToManyField(CustomUser, verbose_name='授权者', blank=True) #授权者

    def __str__(self):
        return self.name

class EntranceAppointment(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name='申请人')
    entrance = models.ManyToManyField( Entrance, verbose_name='门禁', help_text='进出核磁中心请同时申请“值班室大门”，“值班室里门”；而其他申请请根据需求来。通过按住Ctrl来实现多选！')
    reason   = models.TextField( max_length=300, blank=True, null=True, verbose_name='申请理由', help_text='请给出申请理由，不然可能会导致申请不通过！' )
    created_datetime = models.DateTimeField( auto_now_add=True )
    expired_time = models.DateField( default=datetime.now()+timedelta(days=100*365), verbose_name='失效日期' )
    has_approved = models.NullBooleanField(verbose_name='是否赞同', help_text='空着表示未处理', null=True, blank=True)
    feedback = models.TextField(max_length=300, verbose_name='反馈信息', null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.has_approved:
            eguard = EntranceGuard()
            for ent in self.entrance.all():
                eguard.doEntranceUserCreated( self.user.identify, ent.code )
                ent.user.add( self.user )
                ent.save()
        super(EntranceAppointment, self).save(*args, **kwargs)

    def __str__(self):
        all_entrances = ",".join( [door.name for door in self.entrance.all()] )
        strforback = '[{0}]申请开通[{1}], 有效期到[{2}]'.format(self.user.surname, all_entrances, self.expired_time.strftime("%Y-%m-%d") )
        return strforback
    
class Event(models.Model):
    entrance = models.ForeignKey( Entrance, verbose_name='门号' )
    user    = models.ForeignKey( CustomUser, verbose_name='出入者' )
    datetime = models.DateTimeField(verbose_name='时间')

    def getUserSurname(self):
        return self.user.surname
    getUserSurname.short_description = '出入者'
    def __str__(self):
        sentance = '{0}在{1}进入"{2}"'.format(self.user.surname, self.datetime.strftime("%Y-%m-%d %H:%M"), self.entrance.name )
        return sentance
