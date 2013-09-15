import csv

from progressbar import ProgressBar
from django.db import transaction
from django.db.models import Q
from termcolor import colored

from monitoring.models import *
import linecache

REQUIRED = ('site', 'taxon', 'year', 'mean', 'stderror')

import sys

def printLines(f, start, end, problem, problem_text=False):
    while start < end:
        output = False
        if start == problem:
            output = "%s >>\t%s" % (start, 
                linecache.getline(f.name, start)) 
            if problem_text:
                idx = output.index(problem_text)
                coutput = colored(output[0:idx], 'yellow', attrs=['reverse'])
                coutput += colored(output[idx:idx+len(problem_text)], 'red', attrs=['reverse'])
                coutput += colored(output[idx+len(problem_text):], 'yellow', attrs=['reverse'])
                output = coutput
            else:
                output = colored(output, 'yellow', attrs=['reverse'])
        else:
            if start > 1:
                output = str(start) + "\t" + linecache.getline(f.name, start)
        if output:
            sys.stdout.write(output)
        start = start + 1

def highlightError(reader, f, row, column='unknown'):
    print """

Error found in '%s', line %d, column '%s':
\n\t%s
    """ % (f.name, reader.line_num, column, ",".join(reader.fieldnames))
    problem_text = False
    if column and column != 'unknown':
        problem_text = row[column]
    printLines(f, reader.line_num - 5, reader.line_num + 5, reader.line_num, problem_text)
    print "\n"


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

        f = open(path, 'r')
        reader = csv.DictReader(f)
        progress = ProgressBar(maxval=file_len(path) - 1).start()
        for row in reader:
            progress.update(reader.line_num - 1)
            code = None
            try:
                taxon = Taxon.objects.get(
                    code=row[kwargs['taxon']], project=project)
            except Taxon.DoesNotExist:
                highlightError(reader, f, row, kwargs['taxon'])
                raise
            except:
                highlightError(reader, row, f)
                raise
            try:
                site = SamplingSite.objects.get(
                    code=row[kwargs['site']].upper(), project=project)
            except SamplingSite.DoesNotExist:
                highlightError(reader, f, row, kwargs['site'])
                raise
            except:
                highlightError(reader, f, row)
                raise

            if 'stderror' in kwargs:
                try:
                    stderror = float(row[kwargs['stderror']])
                except ValueError, e:
                    highlightError(reader, f, row, kwargs['stderror'])
                    raise    
            else:
                stderror = None
            try:
                year = int(row[kwargs['year']])
            except ValueError, e:
                highlightError(reader, f, row, kwargs['year'])
                raise
            try:
                mean = float(row[kwargs['mean']])
            except ValueError, e:
                highlightError(reader, f, row, kwargs['mean'])
                raise
            try:
                md = MeanDensity(
                    protocol=protocol,
                    site=site,
                    taxon=taxon,
                    year=year,
                    mean=mean,
                    stderror=stderror
                )
                md.save()
            except:
                highlightError(reader, f, row)
                raise

        progress.finish()
        return reader.line_num - 1

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

@transaction.commit_on_success
def remove_taxa(protocol_name, taxa):
    protocol = Protocol.objects.get(name=protocol_name)
    print 'removing erroneous taxa...'
    for name in taxa:
        print name
        taxon = Taxon.objects.get(Q(scientific_name=name) | Q(common_name=name))
        MeanDensity.objects.filter(protocol=protocol, taxon=taxon).delete()
    print 'removed data in %s for %s taxa' % (protocol.name, len(taxa))