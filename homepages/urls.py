from django.conf.urls import url

from homepages.views import home, about, labs, insts, service, contact, appoint, post

urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^(?P<slug>[-\w\d]+),(?P<post_id>\d+)/$', post, name='post'),
    url(r'^about/$', about, name='about'),
    url(r'^labs/$', labs, name='labs'),
    url(r'^insts/', insts, name='insts'),
    url(r'^service/$', service, name='service'),
    url(r'^contact/$', contact, name='contact'),
    url(r'^appoint/$', appoint, name='appoint'),
    ]
