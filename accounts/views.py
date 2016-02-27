#-*- coding: utf-8 -*-
from django.shortcuts import render, render_to_response
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from .admin import UserCreationForm, UserInforForm, PersonInChargeForm, OrgnizationForm
from .models import CustomUser, PersonInCharge
from eguard.admin import EntranceAppointmentForm
from eguard.models import Entrance, EntranceAppointment
from schedule.admin import InstrumentAppointmentForm
from schedule.models import Instrument, InstrumentAppointment

import uuid
import json
import time

# Create your views here.

def getActiveCode( email ):
    email_code = uuid.uuid5( uuid.NAMESPACE_DNS, email+str(time.time())).hex
    return email_code

def send_email( user ):
    email = user.email
    if isinstance( email, unicode ):
        email = email.encode( 'utf-8' )

    html_content = render_to_string( 'accounts/send_email.html', {'email_code': getActiveCode( email ) } )
    subject, from_email, to_email = u'您注册了厦门大学高场核磁中心网站', 'tonyfeng@xmu.edu.cn', email
    text_content = 'asssskkj'
    msg = EmailMultiAlternatives( subject, text_content, from_email, [to_email] )
    msg.attach_alternative( html_content, 'text/html' )
    msg.send()
    return HttpResponse( u'请查看您注册使用邮箱%0激活用户，完成注册'.format(email) )

def verifyUserMail( request, pk, email_code ):
    try:
        pk = int(pk)
        user = CustomUser.objects.get(id=pk)
    except (CustomUser.DoesNotExist, ValueError):
        return render_to_response('accounts/register_done.html')

    if user.is_active:
        return HttpResponseRedirect('/accounts/login/')
    elif email_code == user.email_code:
        user.is_active = True
        user.save()
        return render_to_response('accounts/register_done.html')


@login_required
def profile(request):
    return render(request, "accounts/profile.html")

@login_required
def getPersonInChargeInfo( request, surname ):
    if request.method == 'GET':
        try:
            person_in_charge = PersonInCharge.objects.get(surname0=surname)
        except PersonInCharge.DoesNotExist:
            person_in_charge = None
        fields = PersonInChargeForm.Meta.fields
        values = {}
        for field in fields:
            values[field] = getattr( person_in_charge, field )
        fields =  OrgnizationForm.Meta.fields
        for field in fields:
            values[field] = getattr( person_in_charge.orgnization, field )

    return HttpResponse(json.dumps(values, ensure_ascii=False))

@login_required
def userinfo(request):

    user_form = UserInforForm( request.POST or None, instance=request.user )
    pi_form = PersonInChargeForm( request.POST or None, instance=request.user.person_in_charge )
    org_form = OrgnizationForm( request.POST or None, instance=request.user.person_in_charge.orgnization )
    person_in_charge = request.user.person_in_charge.surname0

    if request.method == 'POST':

        is_valid = user_form.is_valid() and pi_form.is_valid() and org_form.is_valid()

        if is_valid:
            person_in_charge = request.POST.get("surname0")
            user = user_form.save(commit=False)
            pi   = pi_form.save(person_in_charge, commit=False)
            org  = org_form.save()
            pi.orgnization = org
            pi.save()
            user.person_in_charge = pi
            user.save()
            return HttpResponseRedirect("/accounts/profile")

    return render(request, "accounts/userinfo.html", {'userform': user_form, 'piform': pi_form, 'orgform': org_form,})

@login_required
def apermission(request, item=None):
    
    eform = EntranceAppointmentForm(request.POST or None )
    iform = InstrumentAppointmentForm(request.POST or None )

    has_permission_entrance = Entrance.objects.filter( user=request.user )
    has_permission_instrument = Instrument.objects.filter( user=request.user )
    has_appointed_entrance = EntranceAppointment.objects.filter( user=request.user )
    has_appointed_instrument = InstrumentAppointment.objects.filter( user=request.user )

    if request.method == 'POST':
        if item=="eguard" and eform.is_valid():
            eform.save()
            return HttpResponseRedirect("/accounts/apermission")
        if item=="instr" and iform.is_valid():
            iform.save()
            return HttpResponseRedirect("/accounts/apermission")

    return render(request, "accounts/apermission.html", {'eform': eform, 'iform': iform, 
                            'has_permission_instrument': has_permission_instrument,
                            'has_permission_entrance': has_permission_entrance,
                            'has_appointed_instrument': has_appointed_instrument,
                            'has_appointed_entrance': has_appointed_entrance,
                              })

@csrf_protect
def register(request):

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_email( user )
            return HttpResponseRedirect("/accounts/register_done")
        #else:
        #    return HttpResponse(u'注册用户时发生错误，请返回重新注册！')
    else:
        form = UserCreationForm()

    return render(request, "accounts/register.html", {'form':form, },)

def register_done(request):
    return render(request, "accounts/register_done.html")
