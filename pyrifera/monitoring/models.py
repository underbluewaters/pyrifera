from django.contrib.gis.db import models
import os
from django.template.loader import render_to_string
from django.template import Context, Template
from monitoring import memoized

SITE_STYLE = 'monitoring/site_style.kml'

# Create your models here.
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
            path = os.path.join(
                self.module.__path__[0], 'templates', template_name)
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
    

class SiteManager(models.GeoManager):
    
    def with_extras(self):
        return self.select_related('project')
        

class SamplingSite(models.Model):
    name = models.CharField(max_length=100)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Project, related_name='sites')
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
            

class Taxon(models.Model):
    """Represents a particular species. 
    Also represents concepts like blue rockfish recruit(<10cm) and 
    blue rockfish. 
    """
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    common_name = models.CharField(max_length=200, blank=True)
    genus = models.CharField(max_length=200, blank=True)
    species = models.CharField(max_length=200, blank=True)
    scientific_name = models.CharField(max_length=200, blank=True)
    code = models.CharField(max_length=100, blank=True)
    # for when you need to mention "This species was added to our lists
    # in 2003 because we decided to split Kelp Bass into Kelp Bass recruits 
    # and adults"
    notes = models.TextField(blank=True)
    project = models.ForeignKey('Project')

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

    def __unicode__(self):
        return self.name()
    
    def clean(self):
        from django.core.exceptions import ValidationError
        # Must specify genus or common_name
        if self.common_name is '' and self.genus is '':
            raise ValidationError('Taxon must have a common_name or genus.')