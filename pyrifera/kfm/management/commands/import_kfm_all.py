from optparse import make_option
from os.path import join

from django.core.management.base import BaseCommand, AppCommand

from kfm.management.commands.import_kfm_sites import Command as ImportSites
from kfm.management.commands.import_kfm_taxa import Command as ImportTaxa
from kfm.management.commands.import_kfm_videos import Command as ImportVideos
from kfm.management.commands.import_kfm_temp import Command as ImportTemp
from kfm.management.commands.import_kfm_quad_1m import Command as ImportQuad1m
from kfm.management.commands.import_kfm_quad_5m import Command as ImportQuad5m
from kfm.management.commands.import_kfm_rpc import Command as ImportRpc
from kfm.management.commands.import_kfm_band import Command as ImportBand
from kfm.management.commands.import_kfm_fish_transects import Command as ImportFishTransect
from kfm.management.commands.kfm_remove_taxa import Command as RemoveTaxa
from haystack.management.commands.rebuild_index import Command as RebuildIndex
from django.core.cache import cache
from distutils.util import strtobool

from monitoring.models import *

paths = (
    'KFM Site Information.txt',                 # 0
    'KFM Species Name.txt',                     # 1
    'videos.txt',                               # 2
    'KFM Temperature.txt',                      # 3
    'KFM 1 m Quadrat Summary.txt',              # 4
    'KFM 5 m Quadrat Summary.txt',              # 5
    'KFM RPCs Summary.txt',                     # 6
    'KFM BandTransect Summary.txt',             # 7
    'KFM Fish Transect 1 Normalized.txt',       # 8
)

class Command(BaseCommand):
    option_list = AppCommand.option_list
    help = """
    Imports all data from a base path. Assumes certain file names.
    example usage:
        python manage.py import_kfm_all ./path-to-data-dir http://kfm-videos.underbluewaters.net
    """
    args = '[path prefix]'
    
    def handle(self, path, prefix, *args, **options):
        

        print "Importing new data will destroy the current database. Proceed? [y/N]"
        try:
            confirm = strtobool(raw_input()) is 1
        except:
            confirm = False
        if confirm:

            print "Deleting old data"
            MeanDensity.objects.all().delete()
            Protocol.objects.all().delete()
            Taxon.objects.all().delete()
            SamplingSite.objects.all().delete()
            WaterTemperature.objects.all().delete()
            Video.objects.all().delete()

            print "Importing sites"
            ImportSites().execute(join(path, paths[0]))
            print "Importing Taxa"
            ImportTaxa().execute(join(path, paths[1]))
            print "Importing Videos"
            ImportVideos().execute(prefix, join(path, paths[2]))

            print """
Now for the slow part.
Importing Quad (1 & 5m), RPC, Band Tansect, Fish, and Temperature Data
            """
            print "Importing Quad 1m"
            ImportQuad1m().execute(join(path, paths[4]))
            print "Importing Quad 5m"
            ImportQuad5m().execute(join(path, paths[5]))
            print "Importing RPC"
            ImportRpc().execute(join(path, paths[6]))
            print "Importing Band Transect"
            ImportBand().execute(join(path, paths[7]))
            print "Importing Fish Transect"
            ImportFishTransect().execute(join(path, paths[8]))
            print "Importing Temperature Data"
            ImportTemp().execute(join(path, paths[3]))
            RemoveTaxa().execute()
            print "Must now rebuild search index"
            RebuildIndex().execute()
            print "Clearing caches"
            cache.clear()
            print "Done"
        else:
            print "cancelled"
            return