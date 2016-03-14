from django.conf.urls import url

from eguard.views import dealAppoint

urlpatterns = [
    url(r'^$', dealAppoint, name='dealAppoint'),
    ]
