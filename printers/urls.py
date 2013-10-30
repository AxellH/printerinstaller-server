from django.conf.urls import patterns, url
from printers import views as pviews
from sparkle import views as sviews


urlpatterns = patterns('',
    url(r'^$', pviews.index, name='index'),
    url(r'^sparkle/$', sviews.index, name='su-index'),
    
    url(r'^printer/add/$', pviews.printer_add,{}, name='printer_add'),    
    url(r'^printer/edit/(?P<printer_id>\d+)/', pviews.printer_edit,{}, name='printer_edit'),
    url(r'^printer/delete/(?P<id>\d+)/$', pviews.printer_delete, name='printer_delete'),
    url(r'^printer/details/(?P<id>\d+)/$', pviews.printer_details, name='printer_details'), 
        
    url(r'^printerlist/add/$', pviews.printerlist_add, name='printerlist_add'), 
    url(r'^printerlist/edit/(?P<printerlist_id>\d+)/$', pviews.printerlist_edit, name='printerlist_edit'),
    url(r'^printerlist/delete/(?P<id>\d+)/$', pviews.printerlist_delete, name='printerlist_delete'),
    url(r'^printerlist/details/(?P<id>\d+)/$', pviews.printerlist_details, name='printerlist_details'), 
    
    url(r'^options/add/$', pviews.options_add,{}, name='options_add'),    
    url(r'^options/list/', pviews.options_list,{}, name='options_list'), 
    url(r'^options/delete/(?P<id>\d+)/$', pviews.options_delete, name='options_delete'),
       
    url(r'^(?P<name>[^/]+)/$', pviews.getlist, name='getlist'),    
)