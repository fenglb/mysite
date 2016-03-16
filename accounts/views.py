from django.shortcuts import render, render_to_response, redirect
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
try:
    from django.contrib.sites.shortcuts import get_current_site
except ImportError:
    from django.contrib.sites.models import get_current_site

from .admin import UserCreationForm, UserInforForm, PersonInChargeForm, OrgnizationForm
from .models import CustomUser, PersonInCharge
from eguard.admin import EntranceAppointmentForm
from eguard.models import Entrance, EntranceAppointment
from schedule.admin import InstrumentAppointmentForm
from schedule.models import Instrument, InstrumentAppointment, SampleAppointment

import uuid
import json
import time
import smtplib

# Create your views here.

def getActiveCode( email ):
    email_code = uuid.uuid5( uuid.NAMESPACE_DNS, email+str(time.time())).hex
    return email_code

def send_email( user, email_code, site ):
    email = user.email

    html_content = render_to_string( 'accounts/send_email.html', {'email_code': email_code, 'pk': user.id, 'site': site } )
    subject, from_email, to_email = '您注册了厦门大学高场核磁中心网站', 'tonyfeng@xmu.edu.cn', email
    text_content = 'tmp'
    msg = EmailMultiAlternatives( subject, text_content, from_email, [to_email] )
    msg.attach_alternative( html_content, 'text/html' )
    try:
        msg.send()
        return 1
    except smtplib.SMTPException:
        return 0

def verifyUserMail(request, pk, email_code ):
    try:
        pk = int(pk)
        user = CustomUser.objects.get(id=pk)
    except (CustomUser.DoesNotExist, ValueError):
        return render_to_response('accounts/register_activated_fail.html')

    if user.is_active:
        return HttpResponseRedirect('/accounts/login/')
    elif email_code == user.email_code:
        user.is_active = True
        user.save()
        return render_to_response('accounts/register_activated.html')


@login_required
def profile(request):
    samples = SampleAppointment.objects.all().order_by("-created_time")

    trains = InstrumentAppointment.objects.all().order_by("-created_datetime")
    entrances = EntranceAppointment.objects.all().order_by("-created_datetime")

    return render(request, "accounts/profile.html", {'samples': samples, "trains": trains, "entrances": entrances} )

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
    if request.user.person_in_charge:
        org_form = OrgnizationForm( request.POST or None, instance=request.user.person_in_charge.orgnization )
    else:
        org_form = OrgnizationForm( request.POST or None )

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
    
    eform = EntranceAppointmentForm(request.POST or None, initial={'expired_time': request.user.expired_time} )
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
            user = form.save( commit=False )
            email_code = getActiveCode( user.email )
            user.email_code = email_code
            user.save()
            site = get_current_site(request)
            if ( send_email( user, email_code, site ) != 1 ):
                user.delete()
                form.errors['email'] = "您输入电子邮箱无效，请重新输入！"
                return render(request, "accounts/register.html", {'form':form, },)
            else:
                return render(request, "accounts/register_done.html", {'email': user.email})
    else:
        form = UserCreationForm()

    return render(request, "accounts/register.html", {'form':form, },)

def register_done(request):
    return render(request, "accounts/register_done.html")

def activeUser(request):

    errors = None
    if request.method == 'POST':
        username=request.POST.get('username', None)
        surname =request.POST.get('surname', None)
        identify =request.POST.get('identify', None)
        phone_number =request.POST.get('phone_number', None)
        email =request.POST.get('email', None)

        user = CustomUser.objects.get(username=username)

        if user:
            if user.surname == surname:
                if user.identify == identify:
                    email_code = getActiveCode( email )
                    user.email_code = email_code
                    site = get_current_site( request )
                    if ( send_email( user, email_code, site ) == 1 ):
                        user.email = email
                        user.phone_number = phone_number
                        user.save()
                    else:
                        errors = "您输入电子邮箱无效(%s)，请重新输入！" % email
                else:
                    errors = "您输入的学号/教工卡 (%s) 有误" % identify
            else:
                errors = "您输入的真实姓名(%s)有误" % surname
            return render(request, "accounts/active.html", {'errors':errors, 'email': user.email})
        else:
            errors = "您输入的用户名有误 %s" % username
    else:
        errors = "有错误"

    return render(request, "accounts/active.html", {'errors': errors,})
