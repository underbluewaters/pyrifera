# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Changing field 'Unit.suffix'
        db.alter_column('monitoring_unit', 'suffix', self.gf('django.db.models.fields.CharField')(max_length=14))

        # Changing field 'Unit.name'
        db.alter_column('monitoring_unit', 'name', self.gf('django.db.models.fields.CharField')(max_length=14))
    
    
    def backwards(self, orm):
        
        # Changing field 'Unit.suffix'
        db.alter_column('monitoring_unit', 'suffix', self.gf('django.db.models.fields.CharField')(max_length=10))

        # Changing field 'Unit.name'
        db.alter_column('monitoring_unit', 'name', self.gf('django.db.models.fields.CharField')(max_length=10))
    
    
    models = {
        'monitoring.excludedaffix': {
            'Meta': {'object_name': 'ExcludedAffix'},
            'affix': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'monitoring.excludedsearchterm': {
            'Meta': {'object_name': 'ExcludedSearchTerm'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'term': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'monitoring.meandensity': {
            'Meta': {'object_name': 'MeanDensity'},
            'day': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mean': ('django.db.models.fields.FloatField', [], {}),
            'month': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'n': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'protocol': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mean_densities'", 'to': "orm['monitoring.Protocol']"}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mean_densities'", 'to': "orm['monitoring.SamplingSite']"}),
            'stderror': ('django.db.models.fields.FloatField', [], {}),
            'taxon': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mean_densities'", 'to': "orm['monitoring.Taxon']"}),
            'year': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'})
        },
        'monitoring.project': {
            'Meta': {'object_name': 'Project'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'homepage': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'monitoring.protocol': {
            'Meta': {'object_name': 'Protocol'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['monitoring.Project']"}),
            'unit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['monitoring.Unit']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'monitoring.samplingsite': {
            'Meta': {'unique_together': "(('name', 'project'),)", 'object_name': 'SamplingSite'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sites'", 'to': "orm['monitoring.Project']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'monitoring.taxon': {
            'Meta': {'object_name': 'Taxon'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'common_name': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '200', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'genus': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['monitoring.Project']"}),
            'scientific_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'species': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'monitoring.unit': {
            'Meta': {'object_name': 'Unit'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '14'}),
            'suffix': ('django.db.models.fields.CharField', [], {'max_length': '14'})
        },
        'monitoring.video': {
            'Meta': {'object_name': 'Video'},
            'full_thumbnail': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'videos'", 'to': "orm['monitoring.SamplingSite']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        },
        'monitoring.watertemperature': {
            'Meta': {'object_name': 'WaterTemperature'},
            'celsius': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '3'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['monitoring.SamplingSite']"})
        }
    }
    
    complete_apps = ['monitoring']
