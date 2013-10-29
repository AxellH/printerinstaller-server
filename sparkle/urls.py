from django.conf.urls.defaults import *
from django.conf.urls import patterns, url
from sparkle import views


urlpatterns = patterns('sparkle.views',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<name>[^/]+)/appcast.xml$', 'appcast', name='sparkle_application_appcast'),
)
