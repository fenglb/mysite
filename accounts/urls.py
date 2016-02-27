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
from accounts.views import register, register_done, verifyUserMail, profile, userinfo, apermission, getPersonInChargeInfo
from django.contrib.auth.views import login, logout, password_change, password_change_done

urlpatterns = [
    url(r'^register/$', register, name='register'),
    url(r'^register_done/$', register_done),
    url(r'^profile/$', profile, name='profile'),
    url(r'^userinfo/$', userinfo, name='userinfo'),
    url(r'^apermission/$', apermission, name='apermission'),
    url(r'^apermission/(\w+)$', apermission, name='apermission'),
    url(r'^verifymail/(?P<pk>\d+)/(\w+)$', verifyUserMail ),
    url(r'^getpi/(\w+)$', getPersonInChargeInfo, name='getpi'),

    url(r'^login/$', login,
        name='login', kwargs={'template_name': 'accounts/login.html'}),

    url(r'^logout/$', logout,
        name='logout', kwargs={'next_page': '/'}),

    url(r'^password_change/$', password_change,
        name='password_change', 
        kwargs={'template_name': 'accounts/password_change_form.html', 
                'post_change_redirect': 'accounts:password_change_done',}),

    url(r'^password_change_done/$', 
        password_change_done,
        name='password_change_done', 
        kwargs={'template_name': 'accounts/password_change_done.html'}),
]
