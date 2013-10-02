from django.conf.urls import patterns, url
from printers import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    
    url(r'^printer/add/$', views.add_printer,{}, name='add_printer'),    
    url(r'^printer/edit/(?P<printer_id>\d+)/', views.edit_printer,{}, name='edit_printer'),
    url(r'^printer/delete/(?P<id>\d+)/$', views.del_printer, name='del_printer'),
    url(r'^printer/details/(?P<id>\d+)/$', views.printer_details, name='printer_details'), 
        
    url(r'^printerlist/add/$', views.add_printerlist, name='add_printerlist'), 
    url(r'^printerlist/edit/(?P<printerlist_id>\d+)/$', views.edit_printerlist, name='edit_printerlist'),
    url(r'^printerlist/delete/(?P<id>\d+)/$', views.del_printerlist, name='del_printerlist'),
    url(r'^printerlist/details/(?P<id>\d+)/$', views.printerlist_details, name='printerlist_details'), 
    
    url(r'^(?P<name>[^/]+)/$', views.getlist, name='getlist'),    
)