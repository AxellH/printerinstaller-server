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

if settings.HOST_SPARKLE_UPDATES[0]:
    SPARKLE_URLS = url(r'^%ssparkle/'% sub_path, include('sparkle.urls'))
else:
    # not ideal, but this can't be blank so we'll just trump it.
    SPARKLE_URLS = url(r'^%s'% sub_path, include('printers.urls'),name='home')



urlpatterns = patterns('',
    url(r'^%sadmin/'% sub_path, include(admin.site.urls)),
    url(r'^%slogin/$'% sub_path, 'django.contrib.auth.views.login',name='login'),
    url(r'^%slogout/$'% sub_path, 'django.contrib.auth.views.logout_then_login',name='logout'),
    url(r'^%schangepassword/$'% sub_path, 'django.contrib.auth.views.password_change',name='change_password'),
    url(r'^%schangepassword/done/$'% sub_path, 'django.contrib.auth.views.password_change_done'),
    SPARKLE_URLS,
    url(r'^%s'% sub_path, include('printers.urls'),name='home'),
)

# if settings.DEBUG:+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
