from haystack.indexes import *
from haystack import site
from monitoring.models import Taxon

class TaxonIndex(SearchIndex):
    text = CharField(document=True, use_template=True)
    name = CharField(model_attr='name')
    protocol = CharField(model_attr='project')
    html = CharField(use_template=True, template_name='monitoring/search_result.html')
    
    
site.register(Taxon, TaxonIndex)
