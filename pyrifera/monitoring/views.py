# Create your views here.
from monitoring.models import *
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
import json

def projects(request):
    """Renders a kml file representing projects."""
    projects = Project.objects.all().order_by('name')
    return render_to_response('monitoring/projects.kml', {
            "projects": projects
        }, mimetype="application/vnd.google-earth.kml+xml")
            
def streamgraph(request, site_pk, protocol_pk):
    """Renders a kml file representing sites."""
    site = get_object_or_404(SamplingSite, pk=site_pk)
    protocol = get_object_or_404(Protocol, pk=protocol_pk)
    project = protocol.project
    data = []
    for taxon in site.taxa:
        a = []
        for val in site.mean_densities.filter(taxon=taxon, protocol=protocol).order_by('year', 'taxon').values_list('mean', flat=True):
            a.append(round(val, 4))
        if len(a) > 0:
            data.append(a)
    
    data = json.dumps(data)
    print data
    return render_to_response('monitoring/streamgraph.html', {
        'site': site,
        'project': project,
        'protocol': protocol,
        'data': data
        }, context_instance=RequestContext(request))

def site(request, pk):
    site = get_object_or_404(SamplingSite, pk=pk)
    return render_to_response('monitoring/site.html', {'site': site}, 
        context_instance=RequestContext(request))
    
def species_lists(request, pk):
    site = get_object_or_404(SamplingSite, pk=pk)
    return render_to_response('monitoring/species_lists.html', {
            'site': site, 
            'protocols': site.protocols.all()
        }, context_instance=RequestContext(request))
    