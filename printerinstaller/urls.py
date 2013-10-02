from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the next line to enable the admin:
    url(r'^printers/admin/', include(admin.site.urls)),
    url(r'^printers/login/$', 'django.contrib.auth.views.login',name='login'),
    url(r'^printers/logout/$', 'django.contrib.auth.views.logout_then_login',name='logout'),
    url(r'^printers/changepassword/$', 'django.contrib.auth.views.password_change',name='change_password'),
    url(r'^printers/changepassword/done/$', 'django.contrib.auth.views.password_change_done'),
    url(r'^printers/', include('printers.urls'),name='home'),
)
