#-*-coding=utf-8 -*-
from django import forms
from django.contrib import admin
from .models import Experiment, Sample, Instrument, InstrumentAppointment, SampleAppointment
from .tz import cntoutc

from django.utils import timezone
from datetime import datetime, timedelta
# Register your models here.

def checkOverwrite( start, stop, instrument ):
    num = 0
    start = cntoutc( start )
    stop  = cntoutc( stop)
    experiments = Experiment.objects.filter(instrument=instrument)
    for exp in experiments:
        start0 = exp.start_time
        stop0  = exp.stop_time()
        if start <= start0 and stop > start0:
            num += 1
        if start < stop0 and stop >= stop0:
            num += 1
        if start >= start0 and stop <= stop0:
            num += 1

    return bool(num)

class ExperimentCreationForm(forms.ModelForm):
    class Meta:
        model = Experiment
        fields = ('user', 'instrument', 'start_time', 'times', 'measure_type' )

    def clean_start_time(self):
        start_time = self.cleaned_data.get('start_time')
        #start_time0 = datetime.strptime(start_time, "%Y-%m-%d %H:%M")
        if ( int(start_time.strftime("%U")) - int(datetime.today().strftime("%U")) > 1):
            raise forms.ValidationError(u"预约开始时间限制在这周内.")

        if ( start_time < timezone.now() ):
            raise forms.ValidationError(u"预约开始时间已经过去，请重新选择！")
        return start_time
    def clean_times(self):
        start_time = self.cleaned_data.get('start_time')
        times = self.cleaned_data.get('times')
        instrument = self.cleaned_data.get('instrument')

        if ( checkOverwrite( start_time, start_time+timedelta(hours=times), instrument ) ):
            raise forms.ValidationError(u"您申请的时间内包含其他人的实验，请另选择时间！")
        return times

    def save(self, commit=True):
        exp = super(ExperimentCreationForm, self).save(commit=False)
        if commit:
            exp.save()
        return exp

class ExperimentAdmin(admin.ModelAdmin):
    add_form = ExperimentCreationForm

    list_display = ('surname', 'instrument', 'start_time', 'stop_time', 'times')

    def surname(self, obj):
        return u'{0} [{1}]'.format(obj.user.surname, obj.user.person_in_charge.surname0)

    surname.short_description = u"用户"

class SampleAdmin( admin.ModelAdmin ):
    list_display = ('name', 'solvent', 'concentration', 'molecular_weight')

class SampleForm( forms.ModelForm ):
    class Meta:
        model = Sample
        fields = ('name', 'solvent', 'concentration', 'molecular_weight', 'structure', 'others', 'upload')
    def save(self, commit=True):
        isNull = True
        for field in self.Meta.fields:
            value = self.cleaned_data.get(field)
            if value:
                isNull = False
        if isNull:
            return None
        sample = super(SampleForm, self).save(commit=False)
        if commit:
            sample.save()
        return sample

class SampleAppointmentAdmin( admin.ModelAdmin ):
    list_display = ('user', 'sample', 'instrument', 'start_time', 'stop_time', 'has_approved' )

class SampleAppointmentForm( forms.ModelForm ):
    class Meta:
        model = SampleAppointment
        fields = ('user', 'sample', 'instrument', 'start_time', 'times', 'measure_type')
    def save(self, commit=True):
        sampleapp = super(SampleAppointmentForm, self).save(commit=False)
        if commit:
            sampleapp.save()
        return sampleapp

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
admin.site.register(SampleAppointment, SampleAppointmentAdmin)
admin.site.register(Experiment, ExperimentAdmin)
admin.site.register(Instrument, InstrumentAdmin)
admin.site.register(InstrumentAppointment, InstrumentAppointmentAdmin)
