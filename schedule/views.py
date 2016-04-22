from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .admin import ExperimentCreationForm, SampleAppointmentForm, SampleForm
from .models import Experiment, Instrument, InstrumentAppointment, SampleAppointment
from accounts.models import PersonInCharge
from .tz import cnfromutc

from django.conf import settings

import os, pytz, json
from datetime import timedelta, datetime
from .colorlist import textcolor, bordercolor, colorlist
# Create your views here.

@login_required
def dealSampleAppoint(request):
    if request.method == 'POST':
        appointment = get_object_or_404(SampleAppointment, id=request.POST['sample'])
        appointment.has_approved = request.POST.get('check', False)
        if ( appointment.has_approved ):
            appointment.start_time = datetime.strptime(request.POST['start_time'], "%Y-%m-%d %H:%M:%S" )
            appointment.times = float(request.POST['times'])
        appointment.feedback = request.POST['feedback']
        appointment.save()
    return redirect( reverse("accounts:profile") )

@login_required
def dealInstrumentAppoint(request):
    if request.method == 'POST':
        appointment = get_object_or_404(InstrumentAppointment, id=request.POST['train'])
        appointment.has_approved = request.POST.get('check', False)
        if ( appointment.has_approved ):
            appointment.target_datetime = datetime.strptime(request.POST['start_time'], "%Y-%m-%d %H:%M:%S")
            appointment.times = float(request.POST['times'])
        appointment.feedback = request.POST['feedback']
        appointment.save()
    return redirect( reverse("accounts:profile") )

@login_required
def sample(request):
    app_form = SampleAppointmentForm( request.POST or None, initial={'user': request.user, 'instrument': 1} )
    sample_form = SampleForm( request.POST or None )
    if request.method == 'POST':
        is_valid = app_form.is_valid() and sample_form.is_valid()
        if is_valid:
            sample = sample_form.save()
            app = app_form.save(commit=False)
            app.sample = sample
            app.save()
            return HttpResponseRedirect("/accounts/profile")
    return render(request, 'schedule/sample.html', {'appform': app_form, 'sampleform': sample_form})
    
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
