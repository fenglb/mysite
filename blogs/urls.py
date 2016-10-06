from django.conf.urls import url, include
from . import views
from .feeds import BlogPostFeed

urlpatterns = [
    url('^$', views.home),
    url('^(?P<page>\d+)/$', views.home),
    url(r'^(?P<md5>\w{32})/$', views.blogpost, name='blogpost'),
    url('^archive/$', views.archive),
    url('^about/$', views.about),
    url('^projects/$', views.projects),
    url('^talks/$', views.talks),
    url('^article/(?P<freshness>.*)/$', views.article),
    url('^rss/$', BlogPostFeed()),
]
