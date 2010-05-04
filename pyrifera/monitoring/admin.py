from django.contrib.gis import admin
from monitoring.models import SamplingSite, Project

class SamplingSiteAdmin(admin.GeoModelAdmin):
    pass
    
class ProjectAdmin(admin.GeoModelAdmin):
    pass
    
admin.site.register(SamplingSite, SamplingSiteAdmin)
admin.site.register(Project, ProjectAdmin)