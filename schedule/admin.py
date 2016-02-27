#-*-coding=utf-8 -*-
from django import forms
from django.contrib import admin
from .models import Experiment, Sample, Instrument, InstrumentAppointment
from .tz import cntoutc

from django.utils import timezone
from datetime import datetime
# Register your models here.

def checkNoExp( start, stop, instrument ):
    # START lte start
    # STOP gte start
    num = 0
    start = cntoutc( start )
    stop  = cntoutc( stop)
    exps = Experiment.objects.filter(instrument=instrument) \
            .filter(start_time__lte=start).filter(stop_time__gt=start)
    num += len(exps)

    # START gte stop
    # STOP lt stop
    exps = Experiment.objects.filter(instrument=instrument) \
            .filter(start_time__lt=stop).filter(stop_time__gte=stop)
    num += len(exps)
    # START gte start
    # STOP lte stop
    exps = Experiment.objects.filter(instrument=instrument) \
            .filter(start_time__gte=start).filter(stop_time__lte=stop)
    num += len(exps)

    return bool(num)

class ExperimentCreationForm(forms.ModelForm):
    class Meta:
        model = Experiment
        fields = ('user', 'instrument', 'start_time', 'times', 'measure_type', 'sample')

    def clean_start_time(self):
        start_time = self.cleaned_data.get('start_time')
        #start_time0 = datetime.strptime(start_time, "%Y-%m-%d %H:%M")
        if ( int(start_time.strftime("%U")) - int(datetime.today().strftime("%U")) > 1):
            raise forms.ValidationError(u"预约开始时间限制在这周内.")

        if ( start_time < now ):
            raise forms.ValidationError(u"预约开始时间已经过去，请重新选择！")
        return start_time

    def save(self, request, commit=True):
        exp = super(ExperimentCreationForm, self).save(commit=False)
        exp.user = request.user
        if commit:
            exp.save()
        return exp

class ExperimentAdmin(admin.ModelAdmin):
    add_form = ExperimentCreationForm

    list_display = ('surname', 'instrument', 'start_time', 'times')

    def surname(self, obj):
        return u'{0} [{1}]'.format(obj.user.surname, obj.user.person_in_charge.surname0)

    surname.short_description = u"用户"

class SampleAdmin( admin.ModelAdmin ):
    list_display = ('name', 'solvent', 'concentration', 'molecular_weight')
    
class InstrumentAppointmentForm( forms.ModelForm ):
    class Meta:
        model = InstrumentAppointment
        fields = ('user', 'instrument', 'target_datetime')
class InstrumentAppointmentAdmin(admin.ModelAdmin):
    list_display = ("__str__", "target_datetime", "has_approved")

class InstrumentAdmin( admin.ModelAdmin ):
    list_display = ('name', )
    filter_horizontal = ('user',)

admin.site.register(Sample, SampleAdmin)
admin.site.register(Experiment, ExperimentAdmin)
admin.site.register(Instrument, InstrumentAdmin)
admin.site.register(InstrumentAppointment, InstrumentAppointmentAdmin)
