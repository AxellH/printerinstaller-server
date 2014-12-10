from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

if settings.RUNNING_ON_APACHE:
    sub_path = ''
else:        
    sub_path = settings.SUB_PATH

urlpatterns = patterns('',
    url(r'^%sadmin/'% sub_path, include(admin.site.urls)),
    url(r'^%slogin/$'% sub_path, 'django.contrib.auth.views.login',name='login'),
    url(r'^%slogout/$'% sub_path, 'django.contrib.auth.views.logout_then_login',name='logout'),
    url(r'^%schangepassword/$'% sub_path, 'django.contrib.auth.views.password_change',name='change_password'),
    url(r'^%schangepassword/done/$'% sub_path, 'django.contrib.auth.views.password_change_done',name='password_change_done'),
    )

# a test needs to be done to check wether the sparkle url's should be included.
if settings.HOST_SPARKLE_UPDATES:
    urlpatterns += patterns('',
        url(r'^%ssparkle/'% sub_path, include('sparkle.urls'))
        )
# then we can add the rest of the url patterns which are sparse.
urlpatterns += patterns('',
    url(r'^%s'% sub_path, include('printers.urls'),name='printers'),
    url(r'^%s$'% sub_path, 'printers.views.index', name='home'),
    ) 

if settings.SERVE_FILES and not settings.RUNNING_ON_APACHE:
    urlpatterns += patterns('',
    (r'^static/(?P<path>.*)$',  'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    (r'^sparkle/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT+'/sparkle'}),
    (r'^ppds/(?P<path>.*)$',    'django.views.static.serve', {'document_root': settings.MEDIA_ROOT+'/ppds'}),
)
