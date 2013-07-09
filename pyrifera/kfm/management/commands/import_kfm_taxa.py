from django.core.management.base import BaseCommand, AppCommand
from optparse import make_option
from monitoring.models import Taxon, Project
import csv
from django.contrib.gis.geos import Point, fromstr
from django.db import transaction
from monitoring.data_import import highlightError

class Command(BaseCommand):
    option_list = AppCommand.option_list
    help = "Loads kfm taxa from a csv file. Requires a path to a csv files."
    args = '[path]'
    
    @transaction.commit_on_success
    def handle(self, path, *args, **options):
        """Assumes a csv file with headers, comma delimiters, and quoted 
        values. Values accessed by keys Species, Species Name, CommonName.
        
        SpeciesName will be split for genus and species
        
        This command will not overwrite taxa with the same "Species" and 
        Project. It will update that taxon with new names only if those 
        existing fields are blank.
        """
        kfm = Project.objects.get(name="NPS Kelp Forest Monitoring")
        f = open(path)
        reader = csv.DictReader(open(path))
        count = 0
        for row in reader:
            count += 1
            code = None
            species = ''
            genus = ''
            common_name = ''
            scientific_name = ''
            code = str(row['Species'])
            common_name = row['CommonName']
            sp = row['Species Name'].split(' ')
            if len(sp) >= 2:
                species = sp[1]
                if species in ('Spp.', 'Spp', 'SPP', 'SPP.', 'spp', 'spp.'):
                    genus = sp[0]
            scientific_name = row['Species Name']
            if code == None or len(code) < 1:
                highlightError(reader, f, row, 'Species')
                raise ValueError("Species code not defined")
            taxa = Taxon.objects.filter(project=kfm, code=code)
            try:
                if len(taxa):
                    taxon = taxa[0]
                    if taxon.common_name is '':
                        taxon.common_name = common_name                    
                    if taxon.scientific_name is '':
                        taxon.scientific_name = scientific_name
                    if taxon.genus is '':
                        taxon.genus = genus
                    taxon.full_clean()
                    taxon.save()
                else:
                    taxon = Taxon(
                        code=code, 
                        project=kfm, 
                        common_name=common_name, 
                        scientific_name=scientific_name, 
                        genus=genus)
                    taxon.save()
            except:
                highlightError(reader, f, row)
                raise

            
        print "done. added or modified %s taxa" % (count, )


def to_unicode_or_bust(obj, encoding='utf-8'):
    if isinstance(obj, basestring):
        if not isinstance(obj, unicode):
            obj = unicode(obj, encoding)
    return obj