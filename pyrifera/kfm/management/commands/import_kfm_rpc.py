from django.core.management.base import BaseCommand, AppCommand
from optparse import make_option
from monitoring.models import *
import csv
from django.contrib.gis.geos import Point, fromstr
from django.db import transaction
from datetime import datetime

PROTOCOL_NAME = 'Random Point Contact'

class Command(BaseCommand):
    option_list = AppCommand.option_list
    help = "Loads kfm rpc data from a csv file. Requires a path to the file."
    args = '[path]'
    
    @transaction.commit_on_success
    def handle(self, path, *args, **options):
        """Assumes a csv file with headers, comma delimiters, and quoted 
        values. Values accessed by keys SiteCode, Species, Year, Mean, and 
        "Std Error"
        
        This command _will_ overwrite existing observations.
        """
        kfm = Project.objects.get(name="NPS Kelp Forest Monitoring")
        try:
            rpc = Protocol.objects.get(name=PROTOCOL_NAME)
            print "Protocol %s already exists." % (PROTOCOL_NAME, )
        except:
            unit = Unit(name='% cover')
            unit.save()
            rpc = Protocol(
                name="Random Point Contact", 
                unit=unit, 
                code="rpc", 
                project=kfm)
            rpc.save()
            print "Protocol %s created." % (PROTOCOL_NAME, )
                
        reader = csv.DictReader(open(path))
        count = 0
        for row in reader:
            count += 1
            code = None
            print 'Looking for Taxon %s' % (row['Species'])
            taxon = Taxon.objects.get(code=row['Species'], project=kfm)
            print 'Looking for Site %s' % (row['SiteCode'])
            site = SamplingSite.objects.get(code=row['SiteCode'].upper(), 
                project=kfm)
            md = MeanDensity(
                protocol=rpc,
                site=site,
                taxon=taxon,
                year=int(row['Year']),
                mean=float(row['Mean']),
                stderror=float(row['Std Error'])
            )
            md.save()
            
        #     species = ''
        #     genus = ''
        #     common_name = ''
        #     scientific_name = ''
        #     code = str(row['Species'])
        #     common_name = row['CommonName']
        #     sp = row['Species Name'].split(' ')
        #     if len(sp) >= 2:
        #         species = sp[1]
        #         if species in ('Spp.', 'Spp', 'SPP', 'SPP.', 'spp', 'spp.'):
        #             genus = sp[0]
        #         scientific_name = row['Species Name']
        # taxa = Taxon.objects.filter(project=kfm, code=code)
        # if len(taxa):
        #     taxon = taxa[0]
        #     taxon.common_name = common_name
        #     taxon.scientific_name = scientific_name
        #     taxon.genus = genus
        #     taxon.full_clean()
        #     taxon.save()
        # else:
        #     taxon = Taxon(
        #         code=code, 
        #         project=kfm, 
        #         common_name=common_name, 
        #         scientific_name=scientific_name, 
        #         genus=genus)
        #     taxon.save()
        #     
        # print "done. added or modified %s taxa" % (count, )
