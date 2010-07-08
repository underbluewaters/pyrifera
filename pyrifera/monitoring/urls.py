from django.conf.urls.defaults import *
from django.conf import settings
urlpatterns = patterns('',
    url(r'^sites/', 'monitoring.views.sites', {}),
)