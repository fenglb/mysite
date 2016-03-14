from django.contrib import admin
from django import forms
from .models import Entrance, Event, EntranceAppointment
# Register your models here.
class EntranceAppointmentForm( forms.ModelForm ):
    all_entrances = ( (ent.code, ent.name) for ent in Entrance.objects.all() )
    #entrance = forms.MultipleChoiceField( label=u'门禁', widget=forms.CheckboxSelectMultiple, choices=all_entrances, help_text=u"进出中心请同时申请“值班室大门”和“值班室里门”，500M核磁使用者申请“值班室大门”和“靠500M核磁室门”，其他请根据需求申请门禁" )
    class Meta:
        model = EntranceAppointment
        fields = '__all__'

class EntranceAppointmentAdmin( admin.ModelAdmin ):
    list_display = ('__str__', 'expired_time', 'has_approved')
    filter_horizontal = ('entrance',)

class EntranceAdmin( admin.ModelAdmin ):
    filter_horizontal = ('user',)

class EventAdmin( admin.ModelAdmin ):
    list_display = ['getUserSurname', 'entrance', 'datetime']

admin.site.register(Event, EventAdmin)
admin.site.register(EntranceAppointment, EntranceAppointmentAdmin)
admin.site.register(Entrance, EntranceAdmin)
