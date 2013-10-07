from django.conf.urls import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

if settings.RUNNING_ON_APACHE:
    #The Apache WSGIScriptAlias handles the subpathing so here it's blank
    sub_path = ''
else:
    sub_path="printers/"
    
urlpatterns = patterns('',
    url(r'^%sadmin/'% sub_path, include(admin.site.urls)),
    url(r'^%slogin/$'% sub_path, 'django.contrib.auth.views.login',name='login'),
    url(r'^%slogout/$'% sub_path, 'django.contrib.auth.views.logout_then_login',name='logout'),
    url(r'^%schangepassword/$'% sub_path, 'django.contrib.auth.views.password_change',name='change_password'),
    url(r'^%schangepassword/done/$'% sub_path, 'django.contrib.auth.views.password_change_done'),
    url(r'^%s'% sub_path, include('printers.urls'),name='home'),
)