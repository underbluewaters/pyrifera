from django.core.management.base import BaseCommand, AppCommand
from optparse import make_option
from monitoring.models import SamplingSite, Project, Video
import csv
from django.contrib.gis.geos import Point, fromstr
from django.db import transaction
import re
from urlparse import urljoin
from monitoring.data_import import printLines, highlightError

class Command(BaseCommand):
    option_list = AppCommand.option_list
    help = "Loads kfm videos from a list of files and a url prefix."
    args = '[prefix] [path]'
    
    @transaction.commit_on_success
    def handle(self, prefix, path, *args, **options):
        """Videos are assumed to be all listed in the file specified by the 
        `path` argument, and available under the same directory specified by 
        the path prefix. List of files can be generated like so:
         
        $ ls > list.txt
        
        File names should take the form of "sitecode year.mp4".
        
        Prefix will be joined with the file name to create the full url to the
        video.
        """
        count = 0
        r = re.compile("(\w+) (\d+).mp4")
        f = open(path)
        i = 0
        for line in f:
            i += 1
            match = r.match(line)
            if match:
                site, year = match.groups()
                site = site[2:]
                try:
                    site = SamplingSite.objects.get(code=site)
                except SamplingSite.DoesNotExist:
                    printLines(f, i - 5, i + 5, i)
                    raise
                except:
                    printLines(f, i - 5, i + 5, i)
                    raise

                url = urljoin(prefix, line)
                video = Video(site=site, year=int(year), url=url, 
                    full_thumbnail=url.strip()+'.jpg')
                video.save()
                count += 1
        print "saved %s videos" % (count, )