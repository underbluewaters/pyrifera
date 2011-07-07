from optparse import make_option

from django.core.management.base import BaseCommand, AppCommand

from monitoring.models import Project
from monitoring.data_import import import_data, remove_taxa

class Command(BaseCommand):
    option_list = AppCommand.option_list
    help = "Loads kfm 1 meter quad data from a csv file. Requires a path to \
        the file."
    args = '[path]'
    
    def handle(self, path, *args, **options):
        """Assumes a csv file with headers, comma delimiters, and quoted 
        values. Values accessed by keys SiteCode, Species, Year, Mean, and 
        "Std Error"
        
        This command _will_ overwrite existing observations.
        """
        kfm = Project.objects.get(name="NPS Kelp Forest Monitoring")
        saved = import_data(path, kfm, 'Quadrat: 1 Meter', u"# per m\u00B2",
            u"per m\u00B2",
            site='SiteCode', 
            taxon='Species', 
            year='Year', 
            mean='Mean', 
            stderror='Std Error')
        print "Save %d records." % (saved, )