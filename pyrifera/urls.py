from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
import monitoring

admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', 'lingcod.common.views.map', {'template_name': 'common/map_ext.html'}, name="map"),
    (r'^tests/', 'django.views.generic.simple.direct_to_template', {'template': 'common/tests.html', 'extra_context': {'api_key': settings.GOOGLE_API_KEY}}),
    (r'^', include('monitoring.urls')),
    (r'^', include('lingcod.common.urls')),
)

# Useful for serving files when using the django dev server
urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True }),
)