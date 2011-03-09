from django.contrib.gis import admin
from monitoring.models import *

    
admin.site.register(SamplingSite)
admin.site.register(Project)
admin.site.register(Taxon)
admin.site.register(Protocol)
admin.site.register(Unit)

admin.site.register(ExcludedSearchTerms)
admin.site.register(ExcludedAffix)