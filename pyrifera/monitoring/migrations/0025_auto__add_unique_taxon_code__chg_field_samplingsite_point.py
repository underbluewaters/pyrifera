# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'Taxon', fields ['code']
        db.create_unique(u'monitoring_taxon', ['code'])


        # Changing field 'SamplingSite.point'
        db.alter_column(u'monitoring_samplingsite', 'point', self.gf('django.contrib.gis.db.models.fields.PointField')(geography=True))

    def backwards(self, orm):
        # Removing unique constraint on 'Taxon', fields ['code']
        db.delete_unique(u'monitoring_taxon', ['code'])


        # Changing field 'SamplingSite.point'
        db.alter_column(u'monitoring_samplingsite', 'point', self.gf('django.contrib.gis.db.models.fields.PointField')())

    models = {
        u'monitoring.excludedaffix': {
            'Meta': {'object_name': 'ExcludedAffix'},
            'affix': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'monitoring.excludedsearchterm': {
            'Meta': {'object_name': 'ExcludedSearchTerm'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'term': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'monitoring.meandensity': {
            'Meta': {'object_name': 'MeanDensity'},
            'day': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mean': ('django.db.models.fields.FloatField', [], {}),
            'month': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'n': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'protocol': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mean_densities'", 'to': u"orm['monitoring.Protocol']"}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mean_densities'", 'to': u"orm['monitoring.SamplingSite']"}),
            'stderror': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'taxon': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mean_densities'", 'to': u"orm['monitoring.Taxon']"}),
            'year': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'})
        },
        u'monitoring.project': {
            'Meta': {'object_name': 'Project'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'homepage': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'monitoring.protocol': {
            'Meta': {'object_name': 'Protocol'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['monitoring.Project']"}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['monitoring.Unit']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'monitoring.samplingsite': {
            'Meta': {'unique_together': "(('name', 'project'),)", 'object_name': 'SamplingSite'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {'geography': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sites'", 'to': u"orm['monitoring.Project']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'monitoring.taxon': {
            'Meta': {'object_name': 'Taxon'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'common_name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '200', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'genus': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['monitoring.Project']"}),
            'scientific_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'species': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'monitoring.unit': {
            'Meta': {'object_name': 'Unit'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '14'}),
            'suffix': ('django.db.models.fields.CharField', [], {'max_length': '14'})
        },
        u'monitoring.video': {
            'Meta': {'ordering': "('-year',)", 'object_name': 'Video'},
            'full_thumbnail': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'videos'", 'to': u"orm['monitoring.SamplingSite']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        },
        u'monitoring.watertemperature': {
            'Meta': {'object_name': 'WaterTemperature'},
            'celsius': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '3'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['monitoring.SamplingSite']"})
        }
    }

    complete_apps = ['monitoring']