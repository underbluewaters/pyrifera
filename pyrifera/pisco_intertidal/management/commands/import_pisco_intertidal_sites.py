from django.core.management.base import BaseCommand, AppCommand
from optparse import make_option
from monitoring.models import SamplingSite, Project
import csv
from django.contrib.gis.geos import Point, fromstr

class Command(BaseCommand):
    option_list = AppCommand.option_list
    help = """Loads pisco intertidal sites from a csv file. Requires a path 
    to a csv file."""
    args = '[path]'
    
    def handle(self, path, *args, **options):
        """Assumes a csv file with headers, comma delimiters, and quoted 
        strings. Values accessed by keys site_code, full_sitename, 
        longitude(dd), latitude(dd). Coordinates in decimal degrees.
        
        This command will not overwrite sites with the same name and project.
        """
        reader = csv.DictReader(open(path))
        count = 0
        for row in reader:
            count += 1
            project = Project.objects.get(name="PISCO Intertidal")
            point = Point(float(row['longitude(dd)']), 
                float(row['latitude(dd)']))
            site = SamplingSite(name=row['full_sitename'], code=row["site_code"],
                point=point, project=project)
            site.save()
        print "done. added %s sites" % (count, )