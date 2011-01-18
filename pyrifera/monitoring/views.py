# Create your views here.
from monitoring.models import *
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
import json
from symbolizers import ColladaSymbolizer, ScaledImageSymbolizer

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
    data = records_to_json(site.mean_densities.filter(protocol=protocol))
    project = protocol.project
    # data = []
    # for taxon in site.taxa:
    #     a = []
    #     for val in site.mean_densities.filter(taxon=taxon, protocol=protocol).order_by('year', 'taxon').values_list('mean', flat=True):
    #         a.append(round(val, 4))
    #     if len(a) > 0:
    #         data.append(a)
    # 
    # data = json.dumps(data)
    # print data
    return render_to_response('monitoring/streamgraph.html', {
        'site': site,
        'project': project,
        'protocol': protocol,
        'data': data
        }, context_instance=RequestContext(request))

def site(request, pk):
    site = get_object_or_404(SamplingSite, pk=pk)
    # streamgraph_data = "{"
    # for protocol in site.protocols.all():
    #     streamgraph_data = streamgraph_data + ("'%s': %s" % (protocol.name, records_to_json(site.mean_densities.filter(protocol=protocol))))
    # streamgraph_data = streamgraph_data + "}"
    return render_to_response('monitoring/site.html', {
        'site': site,
        # 'streamgraph_data': streamgraph_data,
        }, 
        context_instance=RequestContext(request))
    
def species_lists(request, pk):
    site = get_object_or_404(SamplingSite, pk=pk)
    return render_to_response('monitoring/species_lists.html', {
            'site': site, 
            'protocols': site.protocols.all()
        }, context_instance=RequestContext(request))

def proportional_symbols(request, pk, protocol_pk):
    taxon = get_object_or_404(Taxon, pk=pk)
    protocol = get_object_or_404(Protocol, pk=protocol_pk)
    observations = MeanDensity.objects.filter(taxon=taxon, protocol=protocol).order_by(
        'year').select_related('site')
    symbolizer = ColladaSymbolizer(observations)
    symbolizer = ScaledImageSymbolizer(observations)
    return render_to_response('monitoring/proportional_symbols.kml', {
            "taxon": taxon,
            "protocol": protocol,
            "observations": observations,
            'symbolizer': symbolizer,
        }, mimetype="application/vnd.google-earth.kml+xml", 
        context_instance=RequestContext(request))

def species_site_data(request, taxon_pk, site_pk):
    taxon = get_object_or_404(Taxon, pk=taxon_pk)
    site = get_object_or_404(SamplingSite, pk=site_pk)
    observations = MeanDensity.objects.filter(taxon=taxon).order_by(
        'year').select_related('site')
    return render_to_response('monitoring/species_site_data.html', {
            "taxon": taxon,
            "site": site,
            "observations": observations
        }, context_instance=RequestContext(request))
