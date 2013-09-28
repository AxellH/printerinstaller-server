from django.conf.urls import patterns, url

from printers import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^(?P<printerlist_id>\d+)/$', views.detail, name='detail'), 
    url(r'^(?P<printerlist_name>[^/]+)/$', views.getlist, name='getlist'),    
)