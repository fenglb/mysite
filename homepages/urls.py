from django.conf.urls import url

from homepages.views import home, about, labs, insts, service, contact, appoint, post, map

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^(?P<md5>\w{32})/$', post, name='post'),
    url(r'^about/$', about, name='about'),
    url(r'^labs/$', labs, name='labs'),
    url(r'^insts/', insts, name='insts'),
    url(r'^service/$', service, name='service'),
    url(r'^contact/$', contact, name='contact'),
    url(r'^appoint/$', appoint, name='appoint'),
    url(r'^map/$', map, name='map'),
    ]
