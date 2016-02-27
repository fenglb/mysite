#-*- coding: utf-8 -*-
from django.db import models
# Create your models here.
from accounts.models import CustomUser
from tz import cnfromutc

class Sample( models.Model ):
    
    name = models.CharField( verbose_name=u'名称', max_length = 100 )
    solvent = models.CharField( verbose_name=u'氘代试剂', blank=True, null=True, max_length = 30 )
    concentration = models.FloatField( verbose_name=u'浓度/ML', blank=True, null=True )
    molecular_weight = models.FloatField( verbose_name=u'分子量', blank=True, null=True )
    structure = models.CharField( verbose_name=u'化学式', blank=True, null =True, max_length = 1000 )
    others   = models.TextField(verbose_name=u'其他', blank=True, null=True)

    def __str__(self):
        return self.name.encode('utf-8')

class Instrument(models.Model):
    name = models.CharField( verbose_name=u'名称', max_length = 100 )
    introduct = models.TextField(verbose_name=u'介绍', blank=True, null=True)
    user = models.ManyToManyField(CustomUser, verbose_name=u'授权者', blank=True) #授权者
    def __str__(self):
        return self.name.encode('utf-8')

class InstrumentAppointment(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name=u'申请人')
    instrument = models.ManyToManyField( Instrument, verbose_name=u'仪器' )
    target_datetime = models.DateTimeField(verbose_name=u'预定日期', help_text=u'请选择一个预定时间，等待管理员确定！', null=True, blank=True)
    created_datetime = models.DateTimeField( auto_now_add=True )
    def __str__(self):
        all_instrument = u",".join( [inst.name for inst in self.instrument.all()] )
        strforback = u'[{0}]申请[{1}]培训'.format(self.user.surname, all_instrument )
        return strforback.encode('utf-8')


class Experiment(models.Model):
    """
    create experiment
    """ 
    INSTRUMENT_TYPE = (
        ('500MHz', '500MHz NMR'),
        ('600MHz', '600MHz NMR'),
        ('850MHz', '850MHz NMR'),
        ('MS', 'QTop MS'),
    )
    user = models.ForeignKey( CustomUser, verbose_name=u'用户' )
    measure_type = models.TextField(verbose_name=u'实验类型', blank=True, null=True , help_text=u'实验测量类型，C13，H1， HSQC，HMBC等')

    instrument = models.CharField(verbose_name=u'仪器类型', max_length=6, choices=INSTRUMENT_TYPE, default='600Mhz')

    sample = models.ForeignKey( Sample, null=True, blank=True, verbose_name=u'样品参数')
    start_time = models.DateTimeField(verbose_name=u'起始时间', help_text=u'实验预约起始时间')
    times  = models.IntegerField( verbose_name=u'实验用时/小时', help_text=u'实验预估用时，请参考不同实验估计用时！' )

    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return u"Id: {0}".format(self.id)
