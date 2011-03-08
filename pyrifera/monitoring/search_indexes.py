from haystack.indexes import *
from haystack import site
from monitoring.models import Taxon

class TaxonIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    protocol = CharField(model_attr='project')
    
    
site.register(Taxon, TaxonIndex)
