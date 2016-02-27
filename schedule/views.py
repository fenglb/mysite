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

INSTRUMENT_TYPE = ( '500MHz', '600MHz', '850MHz', 'MS' )

def index(request):
    try:
        groups = request.user.groups.all()
        grouplist = [group.name for group in groups ]
    except AttributeError:
        grouplist = []

    grouplist = list(set(grouplist) & set(INSTRUMENT_TYPE))
    return render(request, 'schedule/index.html', {'grouplist': grouplist,})

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

    groups = request.user.groups.all()
    grouplist = [group.name for group in groups ]
    grouplist = list(set(grouplist) & set(INSTRUMENT_TYPE))
    if instrument not in grouplist:
        return render(request, 'schedule/index.html', {'grouplist': grouplist,})

    form = ExperimentCreationForm(initial={})

    grouplist.remove(instrument)
    return render(request, 'schedule/appointment.html', {'form':form, 'instrument': instrument, 'grouplist': grouplist})

def viewAppointment(request, instrument):

    try:
        groups = request.user.groups.all()
        grouplist = [group.name for group in groups ]
    except AttributeError:
        grouplist = []

    grouplist = list(set(grouplist) & set(INSTRUMENT_TYPE))
    return render(request, 'schedule/index.html', {'instrument': instrument, 'grouplist': grouplist,})

def getEvent(request, instrument=None):
    if request.method == 'GET':
        if not instrument:
            experiments = Experiment.objects.all()
        else:
            experiments = Experiment.objects.filter(instrument=instrument)
        data = []
        for exp in experiments:
            event={}
            if not instrument:
                event['title'] = "{0} {1}".format(exp.user.get_full_name(), exp.instrument)
            else:
                event['title'] = "{0} {1}".format(exp.user.get_full_name(), exp.name.encode('utf-8'))
            start = cnfromutc(exp.start_time)
            event['start'] = start.strftime("%Y-%m-%dT%H:%M:%S")
            end = cnfromutc( exp.start_time+timedelta(hours=exp.times) )
            event['end'] = end.strftime("%Y-%m-%dT%H:%M:%S")
            groud_id = PersonInCharge.objects.get(surname=exp.user.person_in_charge).id % len(colorlist)
            event['color'] = colorlist[groud_id]
# 0 --> 500MHz , 1 --> 600MHz, 2 --> 850MHz, 3 --> MS
            event['borderColor'] = bordercolor[INSTRUMENT_TYPE.index( exp.instrument )]

            event['textColor'] = textcolor
            data.append(event)
    return HttpResponse(json.dumps(data, ensure_ascii=False))
