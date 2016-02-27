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
from .views import index, getEvent, create_experiment, setAppointment, manual, viewAppointment

urlpatterns = [
    url(r'^$', index, name="index"),
    url(r'^getEvent/$', getEvent, name="getEvent"),
    url(r'^getEvent/(\w+)/$', getEvent, name="getEvent"),
    url(r'^setAppointment/(\w+)/$', setAppointment, name="setAppointment"),
    url(r'^create_experiment/$', create_experiment, name="create_experiment"),
    url(r'^viewAppointment/(\w+)/$', viewAppointment, name="viewAppointment"),
    url(r'^manual/$', manual, name="manual"),
]
