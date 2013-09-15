from django.core.management.base import BaseCommand, AppCommand
from optparse import make_option
from monitoring.models import Project, SamplingSite, WaterTemperature
import csv
from django.db import transaction
from datetime import datetime
from decimal import *
from progressbar import ProgressBar
from monitoring.data_import import highlightError

sites = dict()

class Command(BaseCommand):
    option_list = AppCommand.option_list
    help = "Loads kfm temperature data from a csv file. \
        Requires a path to a csv files."
    args = '[path]'
    
    @transaction.commit_on_success
    def handle(self, path, *args, **options):
        """Assumes a csv file with headers, comma delimiters, and quoted 
        values. Values accessed by keys SiteCode, Date, and AvgOfTemperatureC.
        
        Will remove any existing records for the project.
                
        """
        kfm = Project.objects.get(name="NPS Kelp Forest Monitoring")
        WaterTemperature.objects.filter(site__project=kfm).delete()
        f = open(path)
        reader = csv.DictReader(f)
        count = 0
        progress = ProgressBar(maxval=file_len(path) - 1).start()
        for row in reader:
            try:
                progress.update(reader.line_num - 1)
                count += 1
                sitecode = str(row['SiteCode'])
                datet = datetime.strptime(row['Date'], "%m/%d/%Y %H:%M:%S")
                celsius = Decimal(row['AvgOfTemperatureC'])
                site = getSite(sitecode, kfm)
                if site:
                    temp = WaterTemperature(
                        site=site, 
                        date=datet,
                        celsius=celsius)
                    temp.save()
            except:
                highlightError(reader, f, row)
                raise
        
        progress.finish()    
        print "done. added %s temperature records" % (count, )


def getSite(sitecode, project):
    if(sitecode in sites.keys()):
        return sites[sitecode]
    else:
        try:
            site = SamplingSite.objects.get(project=project, code=sitecode)
            sites[sitecode] = site
            return site
        except:
            return False
            
def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1
