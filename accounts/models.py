from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser, PermissionsMixin,
    )
from django.contrib.auth.models import Group
from django.core.validators import RegexValidator
from django.utils import timezone
from datetime import datetime, timedelta
# Create your models here.

class CustomUserManager( BaseUserManager ):
    def create_user( self, username, surname, email, identify, phone_number, password, position, person_in_charge):
        """
        """
        user = self.model(
            email      = self.normalize_email(email),
            surname    = surname,
            identify   = identify,
            phone_number = phone_number,
            person_in_charge= person_in_charge,
            position = position
            )
        user.set_password(password)
        user.username = username
        user.save(using=self._db)

        return user

    def create_superuser( self, username, surname, email, identify, phone_number, password ):
        position = "staff"
        orgnization = Orgnization()
        orgnization.name = "厦门大学"
        orgnization.department = "化学化工学院"
        orgnization.address = "厦门市思明区思明南路220号"
        orgnization.save()

        person_in_charge = PersonInCharge()
        person_in_charge.surname = surname
        person_in_charge.phone_number = phone_number
        person_in_charge.email = email
        person_in_charge.orgnization = orgnization
        person_in_charge.save()

        user = self.create_user( username, surname, email, identify, phone_number, password, position, person_in_charge ) 
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class Orgnization( models.Model ):
    name       = models.CharField( verbose_name='单位名称', max_length=250 )
    department = models.CharField( verbose_name='部门', max_length=100 )
    address    = models.CharField( verbose_name='地址', max_length=250 )

    def __str__(self):
        full_name = self.name+self.department
        return full_name



class PersonInCharge( models.Model ):
    surname0      = models.CharField( unique=True, verbose_name='姓名', help_text='用户的真实姓名', max_length=30)
    phonenumeric = RegexValidator(r'^\+?1?\d{9,15}$', message='格式为05922186874或者手机号码')
    phone_number0 = models.CharField( verbose_name='电话号码', help_text='格式为05922186874或者手机号码', max_length=18, default='05920000000' )
    email0 = models.EmailField( verbose_name='邮箱', help_text='有效邮箱，用于认证通知', max_length=255, default='unkown@xmu.edu.cn')
    titles_choice = (
        ('PI', '课题组负责人'),
        ('FL', '经费负责人'),
        ('OL', '公司领导')
    )
    titles = models.CharField( verbose_name='职务', max_length=3, choices=titles_choice, default='PI')
    orgnization = models.ForeignKey( Orgnization, verbose_name='单位', null=True, blank=True )

    def __str__(self):
        return self.surname0

class CustomUser( AbstractBaseUser, PermissionsMixin ):

    alphanumeric = RegexValidator(r'^[0-9a-zA-Z]*$', message='只有[0-9a-z-A-Z]字符可以.')
    username     = models.CharField( verbose_name='用户名', help_text='纯数字和字母', unique=True, max_length=30, validators=[alphanumeric])
    surname      = models.CharField( verbose_name='姓名', help_text='用户的真实姓名', max_length=30)
    identify     = models.CharField( verbose_name='学号/教工号', help_text='厦大学生号或者教工号，非厦大学生或者教师不用填', max_length=30, unique=True, null=True, blank=True )
    phonenumeric = RegexValidator(r'^\+?1?\d{9,15}$', message='格式为05922186874或者手机号码')
    phone_number = models.CharField( verbose_name='电话号码', help_text='格式为05922186874或者手机号码', max_length=18, default="05920000000" )
    position_choice = (
                ('student', "厦大学生"),
                ('staff',   "厦大教师"),
                ('visit',   "其他"),
    )
    position     = models.CharField( verbose_name='身份', max_length=7, choices=position_choice, default='student' )
    person_in_charge = models.ForeignKey( PersonInCharge, verbose_name='负责人', help_text='课题组负责人, 导师或者领导，里面找不到暂时不用填写，登录以后请修改个人资料！', null=True, blank=True )
    create_time  = models.DateTimeField(auto_now_add=True)
    expired_time = models.DateField( default=(timezone.now()+timedelta(days=100*365)).date(), verbose_name='失效日期' )

    email = models.EmailField( verbose_name='邮箱', help_text='有效邮箱，用于认证通知', max_length=255, default="unkown@xmu.edu.cn")
    email_code = models.CharField( max_length=50, null=True, blank=True )

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['surname', 'identify', 'phone_number', 'email']

    is_active = models.BooleanField(verbose_name='活跃', default=False, null=False)
    is_staff = models.BooleanField(verbose_name='NMRCEN_Man', default=False, null=False)
    title = models.CharField(verbose_name='职称', max_length=50, blank=True, null=False)

    profile_image = models.ImageField(upload_to="profile", blank=False, null=False, verbose_name='个人照片', default="/media/profile/default.png")
    user_bio = models.TextField(verbose_name='自我介绍', max_length=600,blank=True)

    def get_full_name(self):
        return self.surname

    def get_position_name(self):
        return dict(self.position_choice)[self.position]

    def is_expired(self):
        if not self.expired_time:
            self.expired_time = (timezone.now() + timedelta(days=100*365)).date()
        return timezone.now().date() > self.expired_time
    is_expired.boolean = True
    is_expired.short_description= '过期'

    def get_short_name(self):
        return self.surname

    def __str__(self):
        return self.surname
