from optparse import make_option

from django.core.management.base import BaseCommand, AppCommand

from monitoring.models import Project
from monitoring.data_import import import_data, remove_taxa

class Command(BaseCommand):
    option_list = AppCommand.option_list
    help = "Removes records for certain taxa/protocol combinations that are \
    erroneous."
    args = ''
    
    def handle(self, *args, **options):
        remove_taxa('Quadrat: 1 Meter', [
            'Aplysia californica',
            'Crassedoma giganteum',
            # Should these be included? It's the only protocol that has them
            # 'Dictyoneuropsis reticulata/Agarum fimbriatum adult',
            # 'Dictyoneuropsis reticulata/Agarum fimbriatum juvenile',
            'Haliotis rufescens',
            'Kelletia kelletii',
            # Lots of data for this urchin, but sporadic and I remember David 
            # mentioning removing it
            'Lytechinus anamesus',
            'Pycnopodia helianthoides',        
        ])
        
        remove_taxa('Quadrat: 5 Meter', [
        ])
        
        remove_taxa('Band Transect', [
        ])
        
        remove_taxa('Fish Transect', [
        ])