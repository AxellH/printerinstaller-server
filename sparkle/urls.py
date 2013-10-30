from django.conf.urls import patterns, url
from sparkle import views


urlpatterns = patterns('sparkle.views',
    url(r'^$', views.index, name='index'),
    url(r'^appcast/add/$', views.appcast_add,{}, name='appcast_add'),    
    url(r'^appcast/edit/(?P<appcast_id>\d+)/', views.appcast_edit,{}, name='appcast_edit'),
    url(r'^(?P<name>[^/]+)/appcast.xml$', 'appcast', name='sparkle_application_appcast'),
)
