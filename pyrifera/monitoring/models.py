import os
import re

from django.contrib.gis.db import models
from django.template.loader import render_to_string
from django.template import Context, Template
from django.utils import simplejson
from django.db.models import Avg, Sum, Min, Max

from monitoring import memoized

SITE_STYLE = 'monitoring/site_style.kml'


class Project(models.Model):
    """A research project."""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    homepage = models.URLField(blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    app_label = models.CharField(max_length=100, blank=True, null=True)
    
    def __unicode__(self):
        return self.name
    
    def style_url(self):
        return "#default_site_stylemap"
    
    def styles(self):
        styles = ''
        if self.module:
            templates = (
                SITE_STYLE,
            )
            for t in templates:
                path = self.has_style(t)
                if path:
                    try:
                        f = open(path)
                        t = Template(f.read())
                        rendered = t.render(Context({'project': self}))
                        styles = ''.join((styles, rendered,))
                    except:
                        pass
        return styles
    
    @memoized
    def has_style(self, template_name):
        if self.module:
            path = os.path.join(self.module.__path__[0], 
                'templates', template_name)
            if os.path.exists(path):
                return path
        return False
    
    @property
    @memoized
    def module(self):
        """Returns the module of the app specified in the app_label property.
        
        """
        if self.app_label:
            return __import__(self.app_label)
        else:
            return False
    
    def taxa(self):
        return self.taxon_set.all().order_by('scientific_name')

class SiteManager(models.GeoManager):
    
    def with_extras(self):
        return self.select_related('project')
        

class SamplingSite(models.Model):
    name = models.CharField(max_length=100)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Project, db_index=True, related_name='sites')
    description = models.TextField(blank=True)
    point = models.PointField(geography=True)
    code = models.CharField(max_length=100, blank=True)

    objects = SiteManager()
    
    class Meta:
        unique_together = (("name", "project"),)
    
    def __unicode__(self):
        return self.name
    
    def style_url(self):
        if self.project.has_style(SITE_STYLE):
            return "#%s_site_stylemap" % (self.project.app_label)
        else:
            return "#default_site_stylemap"

    def years_sampled(self):
        """Returns all years that the site has been sampled."""
        if not hasattr(self, '_years_sampled'):
            self._years_sampled = self.mean_densities.order_by('year'
                ).values_list('year', flat=True).distinct('year')
        return self._years_sampled
    
    def earliest(self):
        """Earliest sampling date"""
        return self.years_sampled()[0]
    
    def latest(self):
        """Earliest sampling date"""
        return list(self.years_sampled())[-1]

    @property
    def taxa(self):
        """Returns all taxa that have a density value at this site."""
        ids = self.mean_densities.values_list('taxon').distinct()
        return Taxon.objects.filter(pk__in=ids)

    @property
    def observed_taxa(self):
        """Returns all taxa that have been observed at this site 
        (counts of zero not included).
        """
        ids = self.mean_densities.filter(mean__gt=0).values_list('taxon')
        return Taxon.objects.filter(pk__in=ids.distinct())
    
    @property
    def protocols(self):
        """Returns all protocols that have been used at the site."""
        return Protocol.objects.filter(
            pk__in=self.mean_densities.values_list('protocol').distinct()
                ).order_by('name')

    def first_video(self):
        return [self.videos.all()[0]]
      
    def all_means_json(self, protocol):
        results = {}
        results['All Years'] = []
        counted_taxa = Taxon.objects.filter(
            pk__in=self.mean_densities.filter(
                protocol=protocol, site=self).values_list('taxon').distinct())
        for taxon in counted_taxa:
            record = MeanDensity.objects.filter(taxon=taxon, site=self).aggregate(min_year=Min('year'), max_year=Max('year'), avg=Avg('mean'), sum_n=Sum('n'))
            if record['avg'] > 0:
                results['All Years'].append({
                    'taxon': taxon.pk,
                    'scientific_name': taxon.scientific_name,
                    'common_name': taxon.common_name,
                    'mean': record['avg'],
                    'stderror': None,
                    'n': record['sum_n'],
                    'protocol': protocol.name,
                    'site': self.name,
                    'min_year': record['min_year'],
                    'max_year': record['max_year'],
                })
        for record in MeanDensity.objects.filter(protocol=protocol, site=self).select_related('taxon'):
            if record.mean > 0:
                if record.year not in results:
                    results[record.year] = []
                results[record.year].append({
                    'taxon': record.taxon.pk,
                    'scientific_name': record.taxon.scientific_name,
                    'common_name': record.taxon.common_name,
                    'mean': record.mean,
                    'stderror': record.stderror,
                    'n': record.n,
                    'protocol': protocol.name,
                    'site': self.name,
                    'year': record.year,
                })
            
            
        return simplejson.dumps(results)
    
class Taxon(models.Model):
    """Represents a particular species. 
    Also represents concepts like blue rockfish recruit(<10cm) and 
    blue rockfish. 
    It's difficult to require specific names like genus and species for this
    model since often this information isn't a part of the datasets that are
    being imported. It's easier to just treat these more like tags for data
    
    """
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    common_name = models.CharField(db_index=True, max_length=200, blank=True)
    genus = models.CharField(db_index=True, max_length=200, blank=True)
    species = models.CharField(max_length=200, blank=True)
    scientific_name = models.CharField(max_length=200, blank=True)
    code = models.CharField(max_length=100, blank=True)
    # for when you need to mention "This species was added to our lists
    # in 2003 because we decided to split Kelp Bass into Kelp Bass recruits 
    # and adults"
    notes = models.TextField(blank=True)
    project = models.ForeignKey('Project')

    def __unicode__(self):
        return self.name()
        
    def name(self):
        """Formats an easy to read name, prefering a species binomial."""
        if self.scientific_name:
            return self.scientific_name
        if self.genus and self.species:
            return "%s %s" % (self.genus, self.species)
        if self.common_name:
            return self.common_name
        if self.genus:
            return "%s spp." % (self.genus, )
    
    def clean(self):
        from django.core.exceptions import ValidationError
        # Must specify genus or common_name
        if self.common_name is '' and self.genus is '' and \
            self.scientific_name is '':
            raise ValidationError('Taxon %s must have a common_name, '+
                'genus or scientific_name.' % (self.code))
    
    def protocols(self):
        return Protocol.objects.filter(pk__in=MeanDensity.objects.filter(
            taxon=self).values_list('protocol', flat=True).distinct())
    
    def image_search_term(self):
        name = self.name()
        for excluded in ExcludedAffix.objects.all():
            name = re.split('(?i)\W'+excluded.affix.replace('.', '\\.') + '\W', name)[0]
            name = re.split('(?i)\W'+excluded.affix.replace('.', '\\.') + '$', name)[0]
        for excluded in ExcludedSearchTerm.objects.all():
            name = name.replace(excluded.term.replace('.', '\\.'), '')
        return name.strip()


class Unit(models.Model):
    u"""Describes the unit used in the sampling protocol, 
    for example: "# per m\u00B2". 
    
    Suffix is attached to the end of numbers in the UI. As in the above 
    example a record of 4 would be displayed as "4 per m\u00B2"
    
    """
    name = models.CharField(max_length=10)
    suffix = models.CharField(max_length=10)

    def __unicode__(self):
        return self.name


class Protocol(models.Model):
    """Describes a sampling protocol used to collect DensityObservations 
    and other types of data.
    
    """
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    unit = models.ForeignKey(Unit)
    url = models.URLField(blank=True)
    code = models.CharField(max_length=20)
    project = models.ForeignKey('Project')

    def __unicode__(self):
        return "%s - %s" % (self.project.name, self.name)

    def sites(self):
        return mean_densities.select_related('site').distinct()
    
    @property
    def taxa(self):
        """Returns all taxa observed with this protocol."""
        return Taxon.objects.filter(
            pk__in=self.mean_densities.filter(
                protocol=self).values_list('taxon').distinct())                

class MeanDensity(models.Model):
    """Observation of density or count at a particular site, date, taxon, and
    protocol.
    
    """
    protocol = models.ForeignKey('Protocol', db_index=True, blank=False, 
        related_name="mean_densities")
    site = models.ForeignKey('SamplingSite', blank=False, 
        related_name="mean_densities")
    taxon = models.ForeignKey('Taxon', db_index=True, blank=False,
        related_name="mean_densities")
    year = models.IntegerField(db_index=True, blank=False)
    month = models.IntegerField(blank=True, null=True)
    day = models.IntegerField(blank=True, null=True)
    mean = models.FloatField(blank=False)
    stderror = models.FloatField(blank=False)
    n = models.IntegerField(blank=True, null=True)
    
    def __unicode__(self):
        return "%d %s %s %s: %d %s" % (self.year, self.site.name, 
        self.protocol.name, self.taxon, self.mean, self.protocol.unit)
    
    def json_string(self):
        return ("{date: new Date(%s, 6, 1), mean: %s, stderror: %s, n: %s}" % (self.year, self.mean, self.stderror, self.n)).replace('None', 'null')

def records_to_json(queryset):
    results = []
    min_year = 100000
    max_year = 0
    min_mean = 0
    max_mean = 0
    for record in queryset.select_related('taxon', 'site', 'protocol', 
        'protocol__unit', 'protocol__project').order_by('taxon', 'year'):
        results.append({
            'taxon': record.taxon.pk,
            'scientific_name': record.taxon.scientific_name,
            'common_name': record.taxon.common_name,
            'mean': record.mean,
            'stderror': record.stderror,
            'year': record.year,
            'month': record.month,
            'day': record.day,
            'n': record.n,
            'protocol': record.protocol.name,
            'site': record.site.name,
            'project': record.protocol.project.name,
        })
        
        if record.year < min_year:
            min_year = record.year
        if record.year > max_year:
            max_year = record.year
        if record.mean < min_mean:
            min_mean = record.mean
        if record.mean > max_mean:
            max_mean = record.mean
    
    return simplejson.dumps({
        'min_year': min_year,
        'max_year': max_year,
        'min_mean': min_mean,
        'max_mean': max_mean,
        'records': results,
    })
    
class Video(models.Model):
    """Represents a video of a particular site on a given year.
    """
    site = models.ForeignKey('SamplingSite', blank=False, related_name='videos')
    year = models.IntegerField(blank=False)
    url = models.URLField(blank=False, verify_exists=True)
    full_thumbnail = models.URLField(null=True, verify_exists=True)
    
    class Meta:
        ordering = ('-year', )
        
class WaterTemperature(models.Model):
    """Represents a recording of water temperature at a given site and date
    in degrees celsius.
    """
    site = models.ForeignKey('SamplingSite', blank=False)
    date = models.DateTimeField(db_index=True, blank=False)
    celsius = models.DecimalField(blank=False, max_digits=5, decimal_places=3)
    
    
class ExcludedSearchTerm(models.Model):
    """Used to exclude terms from use in image search. For example, you may 
    want to exclude "Acid Weed" for obvious reasons. 
    "Miscellaneous" is also a good one to exclude.
    """
    term = models.CharField(max_length=200, blank=False)

    def __str__(self):
        return self.term

class ExcludedAffix(models.Model):
    """Use to exclude endings of names from image search term. For example, 
    "Macrocystis pyrifera Adult (> 30cm)". In this case we can store Adult. 
    Any excluded Affix and text following it will be removed from the Taxon 
    image_search_term.
    """
    affix = models.CharField(max_length=200, blank=False)
    
    def __str__(self):
        return self.affix
    