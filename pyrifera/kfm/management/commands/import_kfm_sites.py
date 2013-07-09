from django.core.management.base import BaseCommand, AppCommand
from optparse import make_option
from monitoring.models import SamplingSite, Project
import csv
from django.contrib.gis.geos import Point, fromstr
from django.db import transaction
from monitoring.data_import import highlightError

class Command(BaseCommand):
    option_list = AppCommand.option_list
    help = "Loads kfm sites from a csv file. Requires a path to a csv files."
    args = '[path]'
    
    @transaction.commit_on_success
    def handle(self, path, *args, **options):
        """Assumes a csv file with headers, comma delimiters, and quoted 
        values. Values accessed by keys SiteName, SiteCode, Latitude, 
        Longitude. Coordinates in degress decimal minutes.
        
        This command will not overwrite sites with the same name and project.
        """
        f = open(path)
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            count += 1
            kfm = Project.objects.get(name="NPS Kelp Forest Monitoring")
            try:
                lng = ddm2dd("-" + row['Longitude'])
            except ValueError:
                highlightError(reader, f, row, 'Longitude')
                raise
            except:
                highlightError(reader, f, row)
                raise
            try:
                lat = ddm2dd(row['Latitude'])
            except ValueError:
                highlightError(reader, f, row, 'Latitude')
                raise
            except:
                highlightError(reader, f, row)
                raise
            try:
                point = Point(lng, lat)
                site = SamplingSite(name=row['SiteName'], code=row["SiteCode"],
                    point=point, project=kfm)
                site.save()
            except:
                highlightError(reader, f, row)
                raise
        print "done. added %s sites" % (count, )

def ddm2dd(ddm):
    """ 
    >>> ddm2dd("33 28.791")
    33.47985
    """
    parts = ddm.split(' ')
    if(int(parts[0]) < 1):
        return int(parts[0]) - float(parts[1]) / 60.0
    else:
        return int(parts[0]) + float(parts[1]) / 60.0