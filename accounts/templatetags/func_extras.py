from django import template
register = template.Library()
from datetime import date, datetime, timedelta
from schedule.tz import cnfromutc, navicetoaware

@register.filter(name='isAfterToday')
def isAfterToday(day):
    day = cnfromutc(day)
    today = date.today()
    return day.date() > today

@register.filter(name='isMoreThan12Hours')
def isMoreThan12Hours(dt):
    now = datetime.now()
    moreThan12Hours = now + timedelta(hours=12)
    return cnfromutc(dt) >= navicetoaware(moreThan12Hours)

@register.filter(name='isAfterNow')
def isAfterNow(dt, delta=0):
    now = datetime.now() + timedelta(hours=delta)
    return cnfromutc(dt) >= navicetoaware(now)

@register.filter(name='isBeforeToday')
def isBeforeToday(day):
    day = cnfromutc(day)
    today = date.today()
    return day.date() < today

@register.filter(name='isBeforeNow')
def isBeforeNow(dt):
    now = datetime.now()
    return cnfromutc(dt) < navicetoaware(now)

    
