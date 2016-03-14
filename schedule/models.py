from django.db import models
# Create your models here.
from accounts.models import CustomUser
from .tz import cnfromutc
from datetime import timedelta, datetime

class Sample( models.Model ):
    
    name = models.CharField( verbose_name='名称', max_length = 100, blank=True, null=True )
    solvent = models.CharField( verbose_name='氘代试剂', blank=True, null=True, max_length = 30 )
    concentration = models.FloatField( verbose_name='浓度/mM', blank=True, null=True )
    molecular_weight = models.FloatField( verbose_name='分子量', blank=True, null=True )
    structure = models.CharField( verbose_name='化学式', blank=True, null =True, max_length = 1000 )
    others   = models.TextField(verbose_name='其他', blank=True, null=True)
    upload   = models.FileField(upload_to='samples/', blank=True, null=True)

    def __str__(self):
        return self.name

class Instrument(models.Model):
    name = models.CharField( verbose_name='名称', max_length = 100 )
    short_name = models.CharField( verbose_name='简称', max_length = 100, unique=True )
    introduct = models.TextField(verbose_name='介绍', blank=True, null=True)
    user = models.ManyToManyField(CustomUser, verbose_name='授权者', blank=True) #授权者
    image = models.ImageField(upload_to="images", blank=False, null=False, verbose_name='照片', default="/media/images/default.png")
    def __str__(self):
        return self.name

class SampleAppointment( models.Model ):
    user = models.ForeignKey( CustomUser, verbose_name='用户' )
    sample = models.ForeignKey( Sample, null=True, blank=True, verbose_name='样品参数')

    instrument = models.ForeignKey(Instrument, verbose_name='选择仪器')

    start_time = models.DateTimeField(verbose_name='起始时间', help_text='实验预约起始时间')
    times  = models.FloatField( verbose_name='实验用时/小时', help_text='实验预估用时，请参考不同实验估计用时！' )
    measure_type = models.TextField(verbose_name='实验类型', blank=True, null=True , help_text='实验测量类型，C13，H1， HSQC，HMBC等')

    created_time = models.DateTimeField(auto_now_add=True)
    has_approved = models.NullBooleanField(verbose_name='是否赞同', help_text='空着表示未处理', null=True, blank=True)
    feedback = models.TextField(max_length=300, verbose_name='反馈信息', null=True, blank=True)

    def stop_time(self):
        return self.start_time + timedelta(hours=self.times)
    stop_time.short_description = "结束时间"

    def save(self, *args, **kwargs):
        if self.has_approved:
            new_experiment = Experiment(user=self.user)
            new_experiment.measure_type = "送样测试:" + self.measure_type
            new_experiment.start_time = self.start_time
            new_experiment.times = self.times
            new_experiment.instrument = self.instrument
            new_experiment.save()

        super(SampleAppointment, self).save(*args, **kwargs)

    def __str__(self):
        return "{0}[{1}]在“{2}”上申请从{3}到{4}的送样实验".format(self.user, self.user.person_in_charge, self.instrument.short_name, cnfromutc(self.start_time).strftime("%m-%d %H:%M"), cnfromutc(self.stop_time()).strftime("%m-%d %H:%M"))

class InstrumentAppointment(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name='申请人')
    instrument = models.ManyToManyField( Instrument, verbose_name='仪器', help_text='通过按住Ctrl来实现多选！' )
    target_datetime = models.DateTimeField(verbose_name='预定日期', help_text='请选择一个预定时间，等待管理员确定！', null=True, blank=True)
    times   = models.FloatField(verbose_name='用时/小时', help_text='预估培训使用时间,如果不需要培训把这个数值设置为0.', default=0.5)
    created_datetime = models.DateTimeField( auto_now_add=True )
    has_approved = models.NullBooleanField(verbose_name='是否赞同', help_text='空着表示未处理', null=True, blank=True)
    feedback = models.TextField(max_length=300, verbose_name='反馈信息', null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.has_approved:
            for inst in self.instrument.all():
                inst.user.add( self.user )
                inst.save()
                if self.times < 0.1: continue
                new_experiment = Experiment(user=self.user)
                new_experiment.measure_type = "仪器培训"
                new_experiment.start_time = self.target_datetime
                new_experiment.times = self.times
                new_experiment.instrument = inst
                new_experiment.save()
        super(InstrumentAppointment, self).save(*args, **kwargs)

    def __str__(self):
        all_instrument = ",".join( [inst.name for inst in self.instrument.all()] )
        target_datetime = cnfromutc(self.target_datetime).strftime("%Y-%m-%d %H:%m")
        strforback = '[{0}]申请[{1}]预计在{2}培训'.format(self.user.surname, all_instrument, target_datetime )
        return strforback


class Experiment(models.Model):
    """
    create experiment
    """ 
    user = models.ForeignKey( CustomUser, verbose_name='用户' )
    measure_type = models.TextField(verbose_name='实验类型', blank=True, null=True , help_text='实验测量类型，C13，H1， HSQC，HMBC等')

    instrument = models.ForeignKey(Instrument, verbose_name='选择仪器')

    start_time = models.DateTimeField(verbose_name='起始时间', help_text='实验预约起始时间')
    times  = models.FloatField( verbose_name='实验用时/小时', help_text='实验预估用时，请参考不同实验估计用时！' )

    created_time = models.DateTimeField(auto_now_add=True)

    def stop_time(self):
        return self.start_time + timedelta(hours=self.times)
    stop_time.short_description = "结束时间"

    def __str__(self):
        return "{0}[{1}]在“{2}”上预约从{3}到{4}的实验".format(self.user, self.user.person_in_charge, self.instrument.short_name, cnfromutc(self.start_time).strftime("%m-%d %H:%M"), cnfromutc(self.stop_time()).strftime("%m-%d %H:%M"))
