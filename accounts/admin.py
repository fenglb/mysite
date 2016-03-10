#-*- coding=utf-8 -*-
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from datetime import date, datetime

from .models import CustomUser, PersonInCharge, Orgnization
from eguard.eguardcrawler import checkUserExist

# Register your models here.
class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label=u'密码', widget=forms.PasswordInput)
    password2 = forms.CharField(label=u'确认密码', widget=forms.PasswordInput)
    class Meta:
        model = CustomUser
        fields = ('username', 'surname','position', 'identify', 'phone_number', 'email', 'person_in_charge' )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(u"密码不一致，请重新输入!")
        return password2
    def clean_person_in_charge(self):
        person_in_charge = self.cleaned_data.get("person_in_charge")
        return person_in_charge

    def clean_identify(self):
        position = self.cleaned_data.get("position")
        if position == "visit":
            users = CustomUser.objects.filter( position="visit" ).filter( create_time__year=datetime.now().year )
            date_str = datetime.now().strftime("%Y%m")
            identify = "T"+date_str+"{:03}".format(len(users))
        else:
            surname = self.cleaned_data.get("surname")
            identify = self.cleaned_data.get("identify")

            if not identify:
                raise forms.ValidationError(u"厦大学生或者教工必须输入学号/教工号！")

            # login school service to comfirm the information
            if not checkUserExist( surname, identify ):
                raise forms.ValidationError(u"姓名和学号/教工号不匹配！")

        return identify

    def getDefaultExpiredDate(self):
        position = self.cleaned_data.get("position")
        start_years = datetime.now().year
        if position == "visit":
            years = 1
        else:
            identify = self.cleaned_data.get("identify")
            if identify.isdigit():
                if len(identify) == 14: # 学生
                    start_years = int(identify[3:7])
                    if identify[7:9] == "01":
                        years = 4
                    elif identify[7:9] == "11":
                        years = 3
                    elif identify[7:9] == "22":
                        years = 4
                    else:
                        years = 1
                else: # 教工
                    years = 100
            else:
                years = 1
        return date(start_years+years, 7, 1)

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.expired_time = self.getDefaultExpiredDate()
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class OrgnizationForm( forms.ModelForm ):
    class Meta:
        model = Orgnization
        fields = ( 'name', 'department', 'address')

    def save(self, commit=True):
        org_name = self.cleaned_data.get("name")
        org_department = self.cleaned_data.get("department")
        org_address    = self.cleaned_data.get("address")
        try:
            org = Orgnization.objects.get(name=org_name, department=org_department)
        except Orgnization.DoesNotExist:
            org = Orgnization(name=org_name, department=org_department)

        setattr(org, 'address', self.cleaned_data['address'])
             
        if commit:
            org.save()

        return org

class OrgnizationAdmin( admin.ModelAdmin ):
    list_display = ( 'name', 'department' )
    fields = ('name', 'department', 'address')

class PersonInChargeForm( forms.ModelForm ):

    titles = forms.ChoiceField(label=u"职位", choices=PersonInCharge.titles_choice ) 
    class Meta:
        model = PersonInCharge
        fields = ( 'phone_number0', 'email0', 'titles')

    def save(self, surname, commit=True):
        try:
            person_in_charge = PersonInCharge.objects.get(surname0=surname)
        except PersonInCharge.DoesNotExist:
            person_in_charge = PersonInCharge(surname0=surname)

        for field in self.cleaned_data:
            setattr(person_in_charge, field, self.cleaned_data[field])

        if commit:
            person_in_charge.save()
        return person_in_charge
    
class PersonInChargeAdmin( admin.ModelAdmin ):
    list_display = ('surname0', 'phone_number0', 'email0', 'orgnization')
    fields = ('surname0', 'phone_number0', 'email0', 'titles', 'orgnization')
    search_fields = ('surname0',)

class UserInforForm( forms.ModelForm ):
    
    class Meta:
        model = CustomUser
        fields = ('phone_number', 'email', 'profile_image', 'user_bio', 'person_in_charge' )

class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ('username', 'surname', 'identify', 'phone_number', 'email', 'person_in_charge', 'position', 'is_staff')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

class CustomUserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username', 'surname', 'identify', 'phone_number', 'email', 'position', 'person_in_charge', 'is_staff', 'is_active', 'is_expired')
    list_filter = ('person_in_charge',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('surname','title', 'identify', 'position', 'person_in_charge', 'expired_time', 'profile_image', 'user_bio')}),
        ('Contract', {'fields': ('phone_number','email')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'title', 'surname', 'position',  'identify', 'phone_number', 'email','person_in_charge', 'expired_time', 'password1', 'password2' )}
        ),
    )
    search_fields = ('surname', 'username')
    ordering = ('person_in_charge',)

    #filter_horizontal = ('groups', 'user_permissions')
    #def  has_add_permission( self, request):
    #    return True

# Now register the new UserAdmin...
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Orgnization, OrgnizationAdmin )
admin.site.register(PersonInCharge, PersonInChargeAdmin )
