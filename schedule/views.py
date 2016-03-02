#-*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .admin import ExperimentCreationForm
from .models import Experiment, Instrument
from accounts.models import PersonInCharge
from .tz import cnfromutc

from django.conf import settings

import os, pytz, json
from datetime import timedelta
from .colorlist import textcolor, bordercolor, colorlist
# Create your views here.

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
            event={}
            if instrument=='all':
                event['title'] = "{0} {1}".format(exp.user.get_full_name(), exp.instrument.short_name)
            else:
                event['title'] = "{0}[{1}]".format(exp.user.get_full_name(), exp.user.person_in_charge.surname0.encode('utf-8'))
            start = exp.start_time
            event['start'] = cnfromutc( start ).strftime("%Y-%m-%dT%H:%M:%S%z")
            end = cnfromutc( exp.start_time+timedelta(hours=exp.times) )
            event['end'] = end.strftime("%Y-%m-%dT%H:%M:%S%z")
            group_id = PersonInCharge.objects.get(surname0=exp.user.person_in_charge.surname0).id % len(bordercolor)
            event['borderColor'] = bordercolor[group_id]
            if instrument=='all':
                event['color'] = colorlist[exp.instrument.id]
            # 0 --> 500MHz , 1 --> 600MHz, 2 --> 850MHz, 3 --> MS
            event['textColor'] = textcolor
            data.append(event)
    return HttpResponse(json.dumps(data, ensure_ascii=False))
