from django.shortcuts import render, render_to_response, redirect
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth import login as auth_login
from django.contrib.auth import authenticate
from django.db.models import Q
try:
    from django.contrib.sites.shortcuts import get_current_site
except ImportError:
    from django.contrib.sites.models import get_current_site

from .admin import UserCreationForm, UserInforForm, PersonInChargeForm, OrgnizationForm
from .models import CustomUser, PersonInCharge, Orgnization
from eguard.admin import EntranceAppointmentForm
from eguard.models import Entrance, EntranceAppointment
from schedule.admin import InstrumentAppointmentForm
from schedule.models import Instrument, InstrumentAppointment, SampleAppointment
from eguard.eguardcrawler import checkUserExist

import uuid
import json
import time
from datetime import date, datetime
from mail.sendmail import sendEmail

# Create your views here.

def getActiveCode( email ):
    email_code = uuid.uuid5( uuid.NAMESPACE_DNS, email+str(time.time())).hex
    return email_code

def verifyUserMail(request, username, email_code ):
    try:
        user = CustomUser.objects.get(username=username)
    except (CustomUser.DoesNotExist, ValueError):
        return render_to_response('accounts/register_activated_fail.html')

    if user.is_active:
        return HttpResponseRedirect('/accounts/login/')
    elif email_code == user.email_code:
        user.is_active = True
        user.save()
        return render_to_response('accounts/register_activated.html')


def login(request):
    context = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth_login(request, user)
                return HttpResponseRedirect( request.POST['next'] )
            else:
                context['errors'] = '您的用户没有激活！请激活！'
        else:
            context['errors'] = '您的密码和用户名不匹配！'
    return render( request, 'accounts/login.html', context )

@login_required
def profile(request):
    today = date.today()
    if request.user.is_superuser:
        samples = SampleAppointment.objects.all().order_by("-created_time").filter(Q(start_time__gte=today)| Q(has_approved=None))
    else:
        samples = SampleAppointment.objects.all().order_by("-created_time").filter(user=request.user)

    trains = InstrumentAppointment.objects.all().order_by("-created_datetime").filter(Q(target_datetime__gte=today)|Q(has_approved=None))
    entrances = EntranceAppointment.objects.all().order_by("-created_datetime").filter(Q(created_datetime__gte=today)|Q(has_approved=None))

    return render(request, "accounts/profile.html", {'samples': samples, "trains": trains, "entrances": entrances} )

def getPersonInChargeInfo( request, surname ):
    values = {}
    if request.method == 'GET':
        try:
            person_in_charge = PersonInCharge.objects.get(surname0=surname)
        except PersonInCharge.DoesNotExist:
            person_in_charge = None
        fields = PersonInChargeForm.Meta.fields
        values = {}
        for field in fields:
            if person_in_charge:
                values[field] = getattr( person_in_charge, field )
            else: values[field] = ""
        fields =  OrgnizationForm.Meta.fields
        for field in fields:
            if person_in_charge:
                values[field] = getattr( person_in_charge.orgnization, field )
            else: values[field] = ""
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
    doors = Entrance.objects.all()
    instruments = Instrument.objects.all()
    has_permission_entrance = Entrance.objects.filter( user=request.user )
    has_permission_instrument = Instrument.objects.filter( user=request.user )
    has_appointed_entrance = EntranceAppointment.objects.filter( user=request.user )
    has_appointed_instrument = InstrumentAppointment.objects.filter( user=request.user )

    if request.method == 'POST':
        if item=="eguard":
            door_list = request.POST.getlist('entrance')
            if door_list:
                door_appintment = EntranceAppointment(user=request.user)
                door_appintment.reason = request.POST['reason']
                door_appintment.expired_time = request.POST['expired_time']
                door_appintment.save()
                for door_id in door_list:
                    door = Entrance.objects.get(id=door_id)
                    door_appintment.entrance.add(door)
            return HttpResponseRedirect("/accounts/apermission")
        if item=="instr":
            instr_list = request.POST.getlist('instrument')
            if instr_list:
                instr_appintment = InstrumentAppointment(user=request.user)
                instr_appintment.target_datetime = request.POST['target_datetime']
                instr_appintment.times = request.POST['times']
                instr_appintment.save()
                for dev_id in instr_list:
                    dev = Instrument.objects.get(id=dev_id)
                    instr_appintment.instrument.add(dev)
            return HttpResponseRedirect("/accounts/apermission")

    return render(request, "accounts/apermission.html", {
                            'has_permission_instrument': has_permission_instrument,
                            'has_permission_entrance': has_permission_entrance,
                            'has_appointed_instrument': has_appointed_instrument,
                            'has_appointed_entrance': has_appointed_entrance,
                            'doors': doors, 'instruments': instruments,
                              })

def checkUsername(request,name):
    values = {}
    if request.method == "GET":
        try:
            user = CustomUser.objects.get(username=name)
            values['exist'] = True
        except CustomUser.DoesNotExist:
            values['exist'] = False
    return HttpResponse(json.dumps(values, ensure_ascii=False))

def getDefaultExpiredDate(identify):
    years = 1
    position = "visit"
    start_years = datetime.now().year
    if identify.isdigit():
        if len(identify) == 14: # 学生
            start_years = int(identify[3:7])
            if identify[7:9] == "01":
                years = 5
            elif identify[7:9] == "11":
                years = 3
            elif identify[7:9] == "22":
                years = 4
            else:
                years = 1
            position = "student"
        else: # 教工
            years = 100
            position = "staff"
    return date(start_years+years, 7, 1),position

@csrf_protect
def register(request):

    if request.method == 'POST':
        errors = {}

        surname      = request.POST['surname']
        if not surname: errors['surname'] = "请输入您的真实名字！"
        username     = request.POST['username']
        if not username: errors['username'] = "请提供一个用户名！"
        identify     = request.POST['identify']
        phone_number = request.POST['phone_number']
        if not phone_number: errors['phone_number'] = "请提供一个联系电话！"
        email        = request.POST['email']
        if not email: errors['email'] = "请提供一个有效的邮箱地址！"
        password1    = request.POST['password1']
        if not password1: errors['password'] = "密码不能为空！"
        password2    = request.POST['password2']

        pi_name         = request.POST['pi_name']
        if not pi_name: errors['pi_name'] = "输入您课题组组长或者经费负责人的姓名！"
        pi_phone_number = request.POST['pi_phone_number']
        if not pi_phone_number: errors['pi_phone_number'] = "输入您课题组组长或者经费负责人的联系电话！"
        pi_email        = request.POST['pi_email']
        if not pi_email: errors['pi_email'] = "输入您课题组组长或者经费负责人的邮箱！"

        org_name    = request.POST['orgnization']
        if not org_name: errors['org_name'] = "输入您单位名称！"
        department  = request.POST['department']
        if not department: errors['department'] = "输入您的部门！"
        address     = request.POST['address']
        if not address: errors['address'] = "输入您的单位地址！"

        if password1 and password2 and password1 != password2:
            errors['password'] = "密码不一致，请重新输入！"

        matched = checkUserExist(surname, identify)
        if identify and not matched:
            errors['identify'] = "姓名和卡号不匹配，如果您没有厦大一卡通，请留空！"
        else:
            user = CustomUser.objects.get(surname=surname, identify=identify)
            if user:
                errors['identify'] = "这个姓名和卡号已经注册过。您可以通过邮箱找回密码！"

        email_code = getActiveCode( email )
        site = get_current_site(request)
        html_content = render_to_string( 'accounts/send_email.html', 
            {'email_code': email_code, 'username': username, 'site': site} )
        subject, from_email, to_email = '您注册了厦门大学高场核磁中心网站', settings.DEFAULT_FROM_EMAIL, email
        if ( not sendEmail(  to_email, from_email, subject, html_content ) ):
            errors['email'] = "您输入电子邮箱无效，请重新输入！"
        if ( not errors ):

            orgnization,created = Orgnization.objects.get_or_create(name=org_name, department=department)
            orgnization.address = address
            orgnization.save()

            pi,created = PersonInCharge.objects.get_or_create(surname0=pi_name)
            pi.phone_number0 = pi_phone_number
            pi.email0 = pi_email
            pi.orgnization = orgnization
            pi.save()
            if not identify:
                users = CustomUser.objects.filter(position="visit").filter(create_time__year=datetime.now().year)
                date_str = datetime.now().strftime("%Y%m%d")
                identify = "T"+date_str+"{:03}".format(len(users))

            user = CustomUser(username=username,
                surname=surname,identify=identify,
                phone_number=phone_number,email=email,
                email_code=email_code)
            user.person_in_charge = pi
            user.expired_time, user.position = getDefaultExpiredDate(identify)
            user.set_password(password1)
            user.save()
            return render(request, "accounts/register_done.html", {'email': user.email})
        else:
            return render(request, "accounts/register.html", {
                "surname": surname,
                "username": username,
                "identify": identify,
                "phone_number": phone_number,
                "email": email,
                "pi_name": pi_name,
                "pi_phone_number": pi_phone_number,
                "pi_email": pi_email,
                "orgnization": org_name,
                "department": department,
                "address": address,
                "errors": errors,
                },)
    return render(request, "accounts/register.html", )

def register_done(request):
    return render(request, "accounts/register_done.html")

def activeUser(request):

    errors = None
    if request.method == 'POST':
        username=request.POST.get('username', None)
        surname =request.POST.get('surname', None)
        #identify =request.POST.get('identify', None)
        phone_number =request.POST.get('phone_number', None)
        email =request.POST.get('email', None)

        user = CustomUser.objects.get(username=username)

        if user.is_active:
            errors = "您的用户已经激活，请直接<a href='/accounts/login/'>登录</a>！如果您忘记密码，请<a href='/password_reset/recover/'>重设密码</a>!"
            return render(request, "accounts/active.html", {'errors': errors,})

        if user:
            if user.surname == surname:
                #if user.identify == identify:
                email_code = getActiveCode( email )
                user.email_code = email_code
                user.email = email
                site = get_current_site( request )
                html_content = render_to_string( 'accounts/send_email.html', {'email_code': email_code, 'pk': user.id, 'site': site } )
                subject, from_email, to_email = '您注册了厦门大学高场核磁中心网站', settings.DEFAULT_FROM_EMAIL, user.email
                if ( sendEmail(  to_email, from_email, subject, html_content ) ):
                    user.email = email
                    user.phone_number = phone_number
                    user.save()
                else:
                    errors = "您输入电子邮箱无效(%s)，请重新输入！" % email
                #else:
                #    errors = "您输入的学号/教工卡 (%s) 有误" % identify
            else:
                errors = "您输入的真实姓名(%s)有误" % surname
            return render(request, "accounts/active.html", {'errors':errors, 'email': user.email})
        else:
            errors = "您输入的用户名有误 %s" % username
    else:
        errors = "有错误"

    return render(request, "accounts/active.html", {'errors': errors,})
