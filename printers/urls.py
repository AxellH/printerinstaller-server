from django.conf.urls import patterns, url
from printers import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    
    url(r'^printer/add/$', views.printer_add,{}, name='printer_add'),    
    url(r'^printer/edit/(?P<printer_id>\d+)/', views.printer_edit,{}, name='printer_edit'),
    url(r'^printer/delete/(?P<id>\d+)/$', views.printer_delete, name='printer_delete'),
    url(r'^printer/details/(?P<id>\d+)/$', views.printer_details, name='printer_details'), 
        
    url(r'^printerlist/add/$', views.printerlist_add, name='printerlist_add'), 
    url(r'^printerlist/edit/(?P<printerlist_id>\d+)/$', views.printerlist_edit, name='printerlist_edit'),
    url(r'^printerlist/delete/(?P<id>\d+)/$', views.printerlist_delete, name='printerlist_delete'),
    url(r'^printerlist/details/(?P<id>\d+)/$', views.printerlist_details, name='printerlist_details'), 
    
    url(r'^options/add/$', views.options_add,{}, name='options_add'),    
    url(r'^options/list/', views.options_list,{}, name='options_list'), 
    url(r'^options/delete/(?P<id>\d+)/$', views.options_delete, name='options_delete'),
       
    url(r'^(?P<name>[^/]+)/$', views.getlist, name='getlist'),    
)