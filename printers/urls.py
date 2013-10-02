from django.conf.urls import patterns, url
from printers import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    
    url(r'^add_printer/$', views.add_printer,{}, name='add_printer'),    
    url(r'^edit_printer/(?P<printer_id>\d+)/', views.edit_printer,{}, name='edit_printer'),
    url(r'^del_printer/(?P<id>\d+)/$', views.del_printer, name='del_printer'),
        
    url(r'^add_printerlist/$', views.add_printerlist, name='add_printerlist'), 
    url(r'^edit_printerlist/(?P<printerlist_id>\d+)/$', views.edit_printerlist, name='edit_printerlist'),
    
    url(r'^printer_details/(?P<id>\d+)/$', views.printer_details, name='printer_details'), 
    url(r'^printerlist_details/(?P<id>\d+)/$', views.printerlist_details, name='printerlist_details'), 
    url(r'^del_printerlist/(?P<id>\d+)/$', views.del_printerlist, name='del_printerlist'),
    
    url(r'^(?P<name>[^/]+)/$', views.getlist, name='getlist'),    
)