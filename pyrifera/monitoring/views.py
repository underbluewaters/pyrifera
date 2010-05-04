# Create your views here.
from monitoring.models import Project
from django.shortcuts import render_to_response

def sites(request):
    """Renders a kml file representing sites."""
    projects = Project.objects.all()
    return render_to_response('monitoring/sites.kml', {"projects": projects},
            mimetype="application/vnd.google-earth.kml+xml")