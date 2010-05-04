# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding unique constraint on 'SamplingSite', fields ['project', 'name']
        db.create_unique('monitoring_samplingsite', ['project_id', 'name'])
    
    
    def backwards(self, orm):
        
        # Removing unique constraint on 'SamplingSite', fields ['project', 'name']
        db.delete_unique('monitoring_samplingsite', ['project_id', 'name'])
    
    
    models = {
        'monitoring.project': {
            'Meta': {'object_name': 'Project'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'homepage': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'monitoring.samplingsite': {
            'Meta': {'unique_together': "(('name', 'project'),)", 'object_name': 'SamplingSite'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['monitoring.Project']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }
    
    complete_apps = ['monitoring']
