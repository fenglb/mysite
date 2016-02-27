#-*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .admin import ExperimentCreationForm
from .models import Experiment
from accounts.models import PersonInCharge
from .tz import cnfromutc

from django.conf import settings

import os, pytz, json
from datetime import timedelta
from .colorlist import textcolor, bordercolor, colorlist
# Create your views here.

def index(request):
    return render(request, 'schedule/index.html' )

def manual(request):

    userManual = open( os.path.join( settings.BASE_DIR, 'static/manual/usermanual.md' ), 'r' ).read()
    anonymousManual = open( os.path.join( settings.BASE_DIR, 'static/manual/anonymousmanual.md' ), 'r' ).read()
    
    return render( request, 'schedule/manual.html', {'userManual': userManual, 'anonymousManual': anonymousManual,})

@login_required
def create_experiment(request):
    form = ExperimentCreationForm(initial={})
    instrument = request.POST.get('instrument', "600MHz")

    if request.method == 'POST':
        form = ExperimentCreationForm(request.POST)
        if form.is_valid():
            instrument = request.POST['instrument']
            form.save(request=request)
            return HttpResponseRedirect("/schedule/setAppointment/{0}/".format(instrument))
    return render(request, 'schedule/appointment.html', {'form': form, 'instrument':instrument, })

@login_required
def setAppointment(request, instrument):

    form = ExperimentCreationForm(initial={})

    return render(request, 'schedule/appointment.html', {'form':form, 'instrument': instrument} )

def viewAppointment(request, instrument):

    return render(request, 'schedule/index.html', {'instrument': instrument, })

def getEvent(request, instrument=None):
    if request.method == 'GET':
        if not instrument:
            experiments = Experiment.objects.all()
        else:
            experiments = Experiment.objects.filter(instrument=instrument)
        data = []
        for exp in experiments:
            event={}
            event['title'] = "{0} {1}".format(exp.user.get_full_name(), exp.instrument.name.encode('utf-8'))
            start = exp.start_time
            event['start'] = cnfromutc( start ).strftime("%Y-%m-%dT%H:%M:%S")
            end = cnfromutc( exp.start_time+timedelta(hours=exp.times) )
            event['end'] = end.strftime("%Y-%m-%dT%H:%M:%S")
            group_id = PersonInCharge.objects.get(surname0=exp.user.person_in_charge.surname0).id % len(bordercolor)
            event['borderColor'] = bordercolor[group_id]
            event['color'] = colorlist[exp.instrument.id]
            # 0 --> 500MHz , 1 --> 600MHz, 2 --> 850MHz, 3 --> MS
            event['textColor'] = textcolor
            data.append(event)
    return HttpResponse(json.dumps(data, ensure_ascii=False))
