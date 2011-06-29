# Create your views here.
from monitoring.models import *
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
import json
from symbolizers import ScaledImageGChartSymbolizer
from settings import MEDIA_URL, MEDIA_ROOT
import operator
from haystack.query import SearchQuerySet, SQ
from django.http import HttpResponse
import Image, ImageFont, ImageDraw

def projects(request):
    """Renders a kml file representing projects."""
    projects = Project.objects.all().order_by('name')
    return render_to_response('monitoring/projects.kml', {
            "projects": projects
        }, mimetype="application/vnd.google-earth.kml+xml")

def sites(request, project_pk):
    """Renders a kml file with all sites for a given project."""
    project = get_object_or_404(Project, pk=project_pk)
    return render_to_response('monitoring/sites.kml', {
        'project': project,
        'MEDIA_URL': MEDIA_URL,
    }, mimetype="application/vnd.google-earth.kml+xml")

def autocomplete(request):
    """Returns an array of matching terms"""
    from django.utils.safestring import mark_safe
    query = request.GET.get('q', '')
    results = SearchQuerySet().filter(reduce(operator.__and__, [SQ(text__startswith=word.strip()) | SQ(text__icontains=word.strip()) | SQ(text=word.strip()) for word in query.split(' ')]))
    results = results[0:10]
    return HttpResponse(mark_safe('\n'.join([str(r.text.strip()) for r in results])), mimetype="text/plain")
    # return HttpResponse(json.dumps({'query': query, 'suggestions':[r.text for r in results]}), mimetype='application/json')


def autocomplete2(request):
    """Returns the number of matches, offsets, and html representations of 
    the result set.
    """
    from django.utils.safestring import mark_safe
    query = request.GET.get('q', '')
    offset = int(request.GET.get('offset', 0));
    count = int(request.GET.get('count', 10));
    results = SearchQuerySet().filter(reduce(operator.__and__, [SQ(text__startswith=word.strip()) | SQ(text__icontains=word.strip()) | SQ(text=word.strip()) for word in query.split(' ')])).order_by('name')
    n = results.count()
    if n < count:
        offset2 = offset + n
    else:
        offset2 = offset + count
    if offset2 > n:
        offset2 = n
    results = results[offset:offset2]
    return HttpResponse(json.dumps({
        'count': n,
        'offset': offset,
        'offset2': offset2,
        'results': [ r.html for r in results ],
    }), mimetype="text/json")
    


def sites_nl(request, project_pk):
    """Renders an empty networklink pointed at monitoring.views.sites."""
    project = get_object_or_404(Project, pk=project_pk)
    return render_to_response('monitoring/sites_nl.kml', {
        'project': project,
    }, mimetype="application/vnd.google-earth.kml+xml")

def search(request, project_pk):
    """
    Renders a search box that can be added to the sidebar for selecting taxa. 
    """
    project = get_object_or_404(Project, pk=project_pk)
    offset = int(request.GET.get('offset', 0))
    return render_to_response('monitoring/search.html', {
        'project': project,
        'MEDIA_URL': MEDIA_URL,
        'taxa': project.taxa()[offset:int(offset)+10],
        'offset': offset,
        'offset2': offset + 10,
        'count': project.taxa().count(),
    })
    
            
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
    years = MeanDensity.objects.values_list('year', flat=True).distinct('year').order_by('year')
    return render_to_response('monitoring/site.html', {
        'site': site,
        'temperatures': ", ".join([("{'date':new Date('%s'), 'celsius': %s}" % (t.date.ctime(), t.celsius)) for t in site.watertemperature_set.all().order_by('date')]),
        'min_year': years[0],
        'max_year': years[len(years) - 1],
        }, 
        context_instance=RequestContext(request))
    
def species_lists(request, pk):
    site = get_object_or_404(SamplingSite, pk=pk)
    protocols = site.protocols.all()
    return render_to_response('monitoring/species_lists.html', {
            'site': site, 
            'protocols': protocols
        }, context_instance=RequestContext(request))
        
def protocol_species_list(request, site_pk, protocol_pk):
    site = get_object_or_404(SamplingSite, pk=protocol_pk)
    protocol = get_object_or_404(Protocol, pk=site_pk)
    return render_to_response('monitoring/protocol_species_list.html', {
            'site': site, 
            'protocol': protocol,
            'means': site.all_means_json(protocol),
        }, context_instance=RequestContext(request))    

from django.views.decorators.cache import cache_page
from lingcod.kmlapp.views import create_kmz

# @cache_page(60 * 60 * 24 * 30)
def proportional_symbols(request, pk, protocol_pk):
    taxon = get_object_or_404(Taxon, pk=pk)
    protocol = get_object_or_404(Protocol, pk=protocol_pk)
    observations = MeanDensity.objects.filter(taxon=taxon, protocol=protocol).order_by(
        'year').select_related('site')
    # symbolizer = ColladaSymbolizer(observations)
    symbolizer = ScaledImageGChartSymbolizer(observations)
    sites = taxon.project.sites.all()
    # template = 
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
        
def chart(request, pk):
    site = get_object_or_404(SamplingSite, pk=pk)
    return render_to_response('monitoring/chart.html', {
        'site': site,
        }, 
        context_instance=RequestContext(request))
        
        
def taxon_records(request, pk, protocol_pk, site_pk):
    print pk, protocol_pk, site_pk
    taxon = get_object_or_404(Taxon, pk=pk)
    site = get_object_or_404(SamplingSite, pk=site_pk)
    protocol = get_object_or_404(Protocol, pk=protocol_pk)
    records = [{
        'taxon': taxon.pk,
        'scientific_name': taxon.scientific_name,
        'common_name': taxon.common_name,
        'mean': record.mean,
        'stderror': record.stderror,
        'n': record.n,
        'protocol': protocol.name,
        'site': site.name,
        'year': record.year,
        'unit': protocol.unit.name,
        'unit_suffix': protocol.unit.suffix,
    } for record in MeanDensity.objects.filter(protocol=protocol, taxon=taxon, site=site).order_by('year')]
    return HttpResponse(json.dumps(records), mimetype="text/json")
    
def taxon_overlay(request, pk):
    taxon = get_object_or_404(Taxon, pk=pk)
    fontfile = MEDIA_ROOT + 'Didact_Gothic/DidactGothic.ttf'
    im = Image.new("RGBA", (400, 210), (0,0,0,0))
    dr = ImageDraw.Draw(im)
    font = ImageFont.truetype('arial.ttf', 24)
    dr.text((10,10), 'Hi There '+taxon.name(), fill='#ffccff', font=font)
    response = HttpResponse(mimetype="image/png")
    im.save(response, "PNG")
    return response