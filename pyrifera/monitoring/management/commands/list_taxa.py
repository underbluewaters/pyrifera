from optparse import make_option
from os.path import join

from django.core.management.base import BaseCommand, AppCommand
from monitoring.models import Protocol

class Command(BaseCommand):
    option_list = AppCommand.option_list
    help = "Imports all data from a base path. Assumes certain file names."
    args = '[protocolname]'
    
    def handle(self, protocol_name, *args, **options):
        protocol = Protocol.objects.get(name=protocol_name)
        print "\n%s (%s taxa)" % (protocol_name, protocol.taxa.count())
        print "taxon.pk\ttaxon.name()\n============================"
        for taxon in protocol.taxa.order_by('scientific_name'):
            print taxon.pk, '\t\t', taxon.name()
        print "\n"
