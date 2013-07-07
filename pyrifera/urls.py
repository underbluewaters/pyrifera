from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from monitoring.models import Project
from django.conf.urls import patterns
from django.views.generic import TemplateView

import monitoring

admin.autodiscover()

class TestView(TemplateView):
    template_name = "common/tests.html"

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['api_key'] = settings.GOOGLE_API_KEY

urlpatterns = patterns('',

    url(r'^$', 'lingcod.common.views.map', {'template_name': 'common/map_ext.html', 'extra_context': {'projects': Project.objects}}, name="map"),
    (r'^tests/', TestView.as_view()),
    (r'^', include('monitoring.urls')),
    (r'^', include('lingcod.common.urls')),
)

# Useful for serving files when using the django dev server
urlpatterns += patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True }),
)