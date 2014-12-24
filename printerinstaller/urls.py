from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from printers.api_views import OptionViewSet, PrinterViewSet

router = DefaultRouter()
router.register(r'options', OptionViewSet)
router.register(r'printers', PrinterViewSet)


urlpatterns = patterns('',
    url(r'^api/', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$', 'django.contrib.auth.views.login',name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout_then_login',name='logout'),
    url(r'^changepassword/$', 'django.contrib.auth.views.password_change',name='change_password'),
    url(r'^changepassword/done/$', 'django.contrib.auth.views.password_change_done',name='password_change_done'),
    )

# a test needs to be done to check wether the sparkle url's should be included.
if settings.HOST_SPARKLE_UPDATES:
    urlpatterns += patterns('',
        url(r'^sparkle/', include('sparkle.urls'))
        )
# then we can add the rest of the url patterns which are sparse.
urlpatterns += patterns('',
    url(r'^', include('printers.urls'),name='printers'),
    )

if settings.SERVE_FILES and not settings.RUNNING_ON_APACHE:
    urlpatterns += patterns('',
    # static files
    url(r'^static/(?P<path>.*)$' ,  'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    url(r'^files/private/*' , RedirectView.as_view(url=u'/%s', permanent=False), name='nowhere'),
    url(r'^files/(?P<path>.*)$' , 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    # (r'^ppds/(?P<path>.*)$',    'django.views.static.serve', {'document_root': settings.MEDIA_ROOT+'/ppds'}),
)

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]
