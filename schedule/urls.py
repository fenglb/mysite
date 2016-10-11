"""nmrcen URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from .views import viewSchedule, getEvent, sample, dealInstrumentAppoint, dealSampleAppoint, delSampleAppoint, updateSampleAppoint, delExpriment, updateExpriment

urlpatterns = [
    url(r'^$', viewSchedule, name="view"),
    url(r'^dealSample/$', dealSampleAppoint, name="dealSampleAppoint"),
    url(r'^dealInstr/$', dealInstrumentAppoint, name="dealInstrumentAppoint"),
    url(r'^view/(\w+)/$', viewSchedule, name="view"),
    url(r'^sample/$', sample, name="sample"),
    url(r'^getEvent$', getEvent, name="getEvent"),
    url(r'^getEvent/(\w+)/$', getEvent, name="getEvent"),
    url(r'^delSample/(\d+)/$', delSampleAppoint, name="delSample"),
    url(r'^updateSample/$', updateSampleAppoint, name="updateSample"),
    url(r'^delExp/(\d+)/$', delExpriment, name="delExp"),
    url(r'^updateExp/$', updateExpriment, name="updateExp"),
]
