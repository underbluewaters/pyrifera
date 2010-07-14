from django.contrib.gis import admin
from monitoring.models import SamplingSite, Project, Taxon

class SamplingSiteAdmin(admin.GeoModelAdmin):
    pass
    
class ProjectAdmin(admin.GeoModelAdmin):
    pass
    
class TaxonAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(SamplingSite, SamplingSiteAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Taxon, TaxonAdmin)