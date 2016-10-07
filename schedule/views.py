from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .admin import ExperimentCreationForm, SampleAppointmentForm, SampleForm
from .models import Experiment, Instrument, InstrumentAppointment, SampleAppointment, Sample
from accounts.models import PersonInCharge
from .tz import cnfromutc, cntoutc

from django.conf import settings

import os, pytz, json
from datetime import timedelta, datetime
from .colorlist import textcolor, bordercolor, colorlist
from mail.sendmail import sendEmail
# Create your views here.

@login_required
def dealSampleAppoint(request):
    if request.method == 'POST':
        appointment = get_object_or_404(SampleAppointment, id=request.POST['sample'])
        appointment.has_approved = bool(request.POST.get('check', False))

        has_changed_start_time = False
        has_changed_times = False
        if ( appointment.has_approved ):
            start_time = datetime.strptime(request.POST['start_time']+"+0800", "%Y-%m-%d %H:%M:%S%z" )
            if (appointment.start_time - start_time).seconds > 60:
                has_changed_start_time = True
                appointment.start_time = start_time
            times = float(request.POST['times'])
            if  appointment.times != times:
                has_changed_times = True
                appointment.times = times
        appointment.feedback = request.POST['feedback']

        #send the mail to the user of this appoint
        if appointment.has_approved:
            subject = "您的核磁送样申请通过了,请于%s准时送样！" % cnfromutc(appointment.start_time).strftime("%m-%d %H:%M")
            if has_changed_start_time:
                subject = "您的核磁送样申请时间被改为%s, 请注意送样时间！" % appointment.start_time.strftime("%m-%d %H:%M")
            condition="通过"
        else:
            subject = "您核磁送样申请被拒绝,详细原因请看内容!"
            condition="被拒绝"
        content = """{username}:\n
        \t您在核磁仪器{inst}上从{start_time}的{times}个机时的申请{cond}了.\n
        反馈意见:{feedback}\n
        有什么问题请联系核磁中心管理员mailto:tonyfeng@xmu.edu.cn,电话2186874.
        """.format(username=appointment.user.surname, 
            inst=appointment.instrument,
            start_time=cnfromutc(appointment.start_time).strftime("%m-%d %H:%M"),
            times=appointment.times,
            feedback=appointment.feedback,
            cond=condition
            )

        if sendEmail([appointment.user.email], settings.DEFAULT_FROM_EMAIL, subject, content):
            appointment.feedback += ", 邮件已发送！"
        else:
            appointment.feedback += ", 邮件发送失败！"
        
        appointment.save()
    return redirect( reverse("accounts:profile") )

@login_required
def dealInstrumentAppoint(request):
    if request.method == 'POST':
        appointment = get_object_or_404(InstrumentAppointment, id=request.POST['train'])
        appointment.has_approved = bool(request.POST.get('check', False))
        if ( appointment.has_approved ):
            appointment.target_datetime = datetime.strptime(request.POST['start_time'], "%Y-%m-%d %H:%M:%S")
            appointment.times = float(request.POST['times'])
        appointment.feedback = request.POST['feedback']

        #send the mail to the user of this appoint
        appointment.save()
    return redirect( reverse("accounts:profile") )

@login_required
def sample(request):
    #app_form = SampleAppointmentForm( request.POST or None, initial={'user': request.user, 'instrument': 1} )
    #sample_form = SampleForm( request.POST or None )
    instruments = Instrument.objects.all()

    if request.method == 'POST':
        checked_instrument_id = request.POST['instrument']
        if checked_instrument_id:
            checked_instrument = Instrument.objects.get(id=checked_instrument_id)
            sample_app = SampleAppointment(user=request.user)
            sample_app.instrument = checked_instrument
            sample_app.start_time = request.POST['start_time']
            sample_app.times = request.POST['times']
            sample_app.measure_type = request.POST['measure_type']
            
            null_sample = True
            sample_name = request.POST['name']
            if sample_name:
                null_sample = False
            sample_solvent = request.POST['solvent']
            if sample_solvent:
                null_sample = False
            sample_concentration = request.POST['concentration']
            if sample_concentration:
                null_sample = False
            sample_mw = request.POST['molecular_weight']
            if sample_mw:
                null_sample = False
            sample_structure = request.POST['structure']
            if sample_structure:
                null_sample = False
            sample_others = request.POST['others']
            if sample_others:
                null_sample = False
            if not null_sample:
                sample = Sample(name=sample_name,
                                solvent=sample_solvent,
                                concentration=sample_concentration,
                                molecular_weight=sample_mw,
                                structure=sample_structure,
                                others=sample_others
                )
                sample.save()
                sample_app.sample = sample
            sample_app.save()

        return HttpResponseRedirect("/accounts/profile")

    return render(request, 'schedule/sample.html', {
                'instruments': instruments,
                })
    
def viewSchedule(request, instrument=None):
    is_perm = False

    if request.user.is_authenticated() and instrument:
        user = Instrument.objects.filter(short_name=instrument, user=request.user)
        if user:
            is_perm = True
        inst = Instrument.objects.get(short_name=instrument)
        form = ExperimentCreationForm(initial={'user':request.user, 'instrument':inst})

        if request.method == 'POST':
            form = ExperimentCreationForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect("/schedule/view/{0}/".format(instrument))
        return render(request, 'schedule/index.html', 
                {'instrument': instrument, 'is_perm': is_perm, 'form': form})
    else:
        return render(request, 'schedule/index.html', 
                {'instrument': instrument, 'is_perm': is_perm, })



def getEvent(request, instrument):
    if request.method == 'GET':
        if instrument=='all':
            experiments = Experiment.objects.all()
        else:
            experiments = Experiment.objects.filter(instrument__short_name=instrument)
        data = []
        for exp in experiments:
            person_in_charge_name = ''
            event={}
            if instrument=='all':
                event['title'] = "{0} {1}".format(exp.user.get_full_name(), exp.instrument.short_name)
            else:
                if exp.user.person_in_charge:
                    person_in_charge_name = exp.user.person_in_charge.surname0
                else:
                    person_in_charge_name = 'NONE'
                event['title'] = "{0}[{1}]".format(exp.user.get_full_name(), person_in_charge_name)
            start = exp.start_time
            event['start'] = cnfromutc( start ).strftime("%Y-%m-%dT%H:%M:%S%z")
            end = cnfromutc( exp.start_time+timedelta(hours=exp.times) )
            event['end'] = end.strftime("%Y-%m-%dT%H:%M:%S%z")
            try:
                group_id = PersonInCharge.objects.get(surname0=person_in_charge_name).id % len(bordercolor)
            except PersonInCharge.DoesNotExist:
                group_id = len(bordercolor) - 1
            event['borderColor'] = bordercolor[group_id]
            if instrument=='all':
                event['color'] = colorlist[exp.instrument.id]
            # 0 --> 500MHz , 1 --> 600MHz, 2 --> 850MHz, 3 --> MS
            event['textColor'] = textcolor
            data.append(event)
    return HttpResponse(json.dumps(data, ensure_ascii=False))
