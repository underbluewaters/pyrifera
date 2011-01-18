from django.conf.urls.defaults import *
from django.conf import settings
urlpatterns = patterns('',
    (r'^sites/(\d+)/', 'monitoring.views.site'),
    (r'^projects/', 'monitoring.views.projects'),
    (r'^species_lists/(\d+)/', 'monitoring.views.species_lists'),
    (r'^streamgraphs/(\d+)/(\d+)/', 'monitoring.views.streamgraph'),
    (r'^proportional_symbols/(\d+)/(\d+)/', 'monitoring.views.proportional_symbols'),
    (r'^site_data/(\d+)/(\d+)/', 'monitoring.views.species_site_data'),
)