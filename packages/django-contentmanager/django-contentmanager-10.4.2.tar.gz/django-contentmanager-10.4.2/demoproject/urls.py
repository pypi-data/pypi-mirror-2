from django.conf.urls.defaults import *

from django.conf import settings
from django.contrib import admin
admin.autodiscover()

from contentmanager import autodiscover
autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^contentmanager/', include('contentmanager.urls')),
)

# this is for serving static files in development
if settings.DEBUG:
    import os
    # get the static path from settings
    static_url = settings.MEDIA_URL
    if static_url.startswith('/'):
        static_url = static_url.lstrip('/')
        urlpatterns += patterns(
            '',
            (r'^%s(?P<path>.*)$' % static_url, 'django.views.static.serve',
             {'document_root': settings.MEDIA_ROOT}),
            )
