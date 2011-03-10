import csv

from fish import ProgressFish
from django.db import transaction

from monitoring.models import *

REQUIRED = ('site', 'taxon', 'year', 'mean', 'stderror')

@transaction.commit_on_success
def import_data(path, project, protocol_name, unit_name, unit_suffix, **kwargs):
    for kwarg in REQUIRED:
        if kwarg not in kwargs:
            raise KeyError('import data requires a "%s" keyword argument' \
                % (kwarg, ))
        try:
            protocol = Protocol.objects.get(name=protocol_name)
            MeanDensity.objects.filter(protocol=protocol).delete()
            print "Protocol %s already exists. Removed old records" % (
                protocol_name, )
        except:
            unit = Unit(name=unit_name, suffix=unit_suffix)
            unit.save()
            protocol = Protocol(
                name=protocol_name, 
                unit=unit, 
                code="rpc", 
                project=project)
            protocol.save()
            print "Protocol %s created." % (protocol_name, )

        fish = ProgressFish(total=file_len(path) - 1)
        reader = csv.DictReader(open(path))
        for row in reader:
            fish.animate(amount=reader.line_num - 1)
            code = None
            taxon = Taxon.objects.get(
                code=row[kwargs['taxon']], project=project)
            site = SamplingSite.objects.get(
                code=row[kwargs['site']].upper(), project=project)
            md = MeanDensity(
                protocol=protocol,
                site=site,
                taxon=taxon,
                year=int(row[kwargs['year']]),
                mean=float(row[kwargs['mean']]),
                stderror=float(row[kwargs['stderror']])
            )
            md.save()
        return reader.line_num - 1

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1
    