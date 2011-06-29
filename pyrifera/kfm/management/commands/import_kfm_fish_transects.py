from optparse import make_option

from django.core.management.base import BaseCommand, AppCommand

from monitoring.models import Project
from monitoring.data_import import import_data

class Command(BaseCommand):
    option_list = AppCommand.option_list
    help = "Loads kfm fish transect data from a csv file. Requires a path to \
        the file."
    args = '[path]'
    
    def handle(self, path, *args, **options):
        """Assumes a csv file with headers, comma delimiters, and quoted 
        values. Values accessed by keys SiteCode, Species, Year, and 
        SumOfCountA
        
        This command _will_ overwrite existing observations.
        """
        kfm = Project.objects.get(name="NPS Kelp Forest Monitoring")
        saved = import_data(path, kfm, 'Fish Transect', u"# per transect",
            u"per transect",
            site='SiteCode', 
            taxon='Species', 
            year='Year', 
            mean='SumOfCountA')
        print "Save %d records." % (saved, )