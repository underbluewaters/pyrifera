from django.conf.urls.defaults import *
from django.conf import settings
urlpatterns = patterns('',
    (r'^jsonsearch/', 'monitoring.views.json_search'),
    (r'^sites/(\d+)', 'monitoring.views.sites'),
    (r'^sites_nl/(\d+)', 'monitoring.views.sites_nl'),
    (r'^site/(\d+)/', 'monitoring.views.site'),
    (r'^search/(\d+)/', 'monitoring.views.search'),
    (r'^projects/', 'monitoring.views.projects'),
    (r'^species_lists/(\d+)/', 'monitoring.views.species_lists'),
    (r'^streamgraphs/(\d+)/(\d+)/', 'monitoring.views.streamgraph'),
    (r'^proportional_symbols/(\d+)/(\d+)/', 'monitoring.views.proportional_symbols'),
    (r'^site_data/(\d+)/(\d+)/', 'monitoring.views.species_site_data'),
)