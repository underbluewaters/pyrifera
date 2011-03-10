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


paths = (
    'KFM Site Information.txt',                 # 0
    'KFM Species Name.txt',                     # 1
    'videos.txt',                               # 2
    'KFM Temperature 1993-2010.txt',            # 3
    'KFM 1 m Quadrata Summary 1982-2010.txt',   # 4
    'KFM 5 m Quadrata Summary 1996-2010.txt',   # 5
    'KFM RPCs Summary 1982-2010.txt',           # 6
)

class Command(BaseCommand):
    option_list = AppCommand.option_list
    help = "Imports all data from a base path. Assumes certain file names."
    args = '[path prefix]'
    
    def handle(self, path, prefix, *args, **options):
        print "Importing sites"
        ImportSites().execute(join(path, paths[0]))
        print "Importing Taxa"
        ImportTaxa().execute(join(path, paths[1]))
        print "Importing Videos"
        ImportVideos().execute(prefix, join(path, paths[2]))
        print "Importing Quad 1m"
        ImportQuad1m().execute(join(path, paths[4]))
        print "Importing Quad 5m"
        ImportQuad5m().execute(join(path, paths[5]))
        print "Importing RPC"
        ImportRpc().execute(join(path, paths[6]))
        print "Importing Temperature Data"
        ImportTemp().execute(join(path, paths[3]))
        print "Done"