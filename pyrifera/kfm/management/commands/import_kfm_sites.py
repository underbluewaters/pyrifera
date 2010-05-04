from django.core.management.base import BaseCommand, AppCommand
from optparse import make_option
from monitoring.models import SamplingSite, Project
import csv
from django.contrib.gis.geos import Point, fromstr

class Command(BaseCommand):
    option_list = AppCommand.option_list
    help = "Loads kfm sites from a csv file. Requires a path to a csv files."
    args = '[path]'
    
    def handle(self, path, *args, **options):
        """Assumes a csv file with headers, comma delimiters, and quoted 
        values. Values accessed by keys SiteName, SiteCode, Latitude, 
        Longitude. Coordinates in degress decimal minutes.
        
        This command will not overwrite sites with the same name and project.
        """
        reader = csv.DictReader(open(path))
        count = 0
        for row in reader:
            count += 1
            kfm = Project.objects.get(name="NPS Kelp Forest Monitoring")
            point = Point(ddm2dd("-" + row['Longitude']), ddm2dd(row['Latitude']))
            print point.wkt
            site = SamplingSite(name=row['SiteName'], code=row["SiteCode"],
                point=point, project=kfm)
            site.save()
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