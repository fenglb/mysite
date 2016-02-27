#-*- coding=utf-8 -*-
from django.contrib import admin
from django import forms
from .models import Entrance, Event, EntranceAppointment
# Register your models here.
class EntranceAppointmentForm( forms.ModelForm ):
    all_entrances = ( (ent.code, ent.name) for ent in Entrance.objects.all() )
    entrance = forms.MultipleChoiceField( label=u'门禁', widget=forms.CheckboxSelectMultiple, choices=all_entrances )
    class Meta:
        model = EntranceAppointment
        fields = '__all__'

class EntranceAppointmentAdmin( admin.ModelAdmin ):
    filter_horizontal = ('entrance',)

class EntranceAdmin( admin.ModelAdmin ):
    filter_horizontal = ('user',)

class EventAdmin( admin.ModelAdmin ):
    list_display = ['getUserSurname', 'entrance', 'datetime']

admin.site.register(Event, EventAdmin)
admin.site.register(EntranceAppointment, EntranceAppointmentAdmin)
admin.site.register(Entrance, EntranceAdmin)
