from django.conf.urls import patterns, url
from sparkle import views


urlpatterns = patterns('sparkle.views',
    url(r'^$', views.index, name='index'),
    url(r'^privatekey/add/$', views.private_key_add,{}, name='private_key_add'),
    url(r'^privatekey/edit/(?P<id>\d+)/', views.private_key_edit,{}, name='private_key_edit'),
    url(r'^version/add/$', views.version_add,{}, name='version_add'),
    url(r'^version/delete/(?P<id>\d+)/', views.version_delete,{}, name='version_delete'),    
    url(r'^version/edit/(?P<id>\d+)/', views.version_edit,{}, name='version_edit'),
    url(r'^version/activate/(?P<id>\d+)/', views.version_activate,{}, name='version_activate'),
    url(r'^(?P<name>[^/]+)/appcast.xml$', 'appcast', name='sparkle_application_appcast'),
)
