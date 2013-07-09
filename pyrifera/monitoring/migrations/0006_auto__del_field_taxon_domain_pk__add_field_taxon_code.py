# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Deleting field 'Taxon.domain_pk'
        db.delete_column('monitoring_taxon', 'domain_pk')

        # Adding field 'Taxon.code'
        db.add_column('monitoring_taxon', 'code', self.gf('django.db.models.fields.CharField')(default=datetime.date(2010, 7, 14), max_length=100, blank=False, unique=True), keep_default=False)
    
    
    def backwards(self, orm):
        
        # Adding field 'Taxon.domain_pk'
        db.add_column('monitoring_taxon', 'domain_pk', self.gf('django.db.models.fields.CharField')(default=datetime.date(2010, 7, 14), max_length=100, blank=True), keep_default=False)

        # Deleting field 'Taxon.code'
        db.delete_column('monitoring_taxon', 'code')
    
    
    models = {
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
            'code': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'False', 'unique': 'True'}),
            'common_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'genus': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'species': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }
    
    complete_apps = ['monitoring']
