# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'Unit'
        db.create_table('monitoring_unit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('monitoring', ['Unit'])

        # Adding model 'Protocol'
        db.create_table('monitoring_protocol', (
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['monitoring.Project'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('unit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['monitoring.Unit'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('monitoring', ['Protocol'])

        # Adding model 'MeanDensity'
        db.create_table('monitoring_meandensity', (
            ('protocol', self.gf('django.db.models.fields.related.ForeignKey')(related_name='mean_densities', to=orm['monitoring.Protocol'])),
            ('taxon', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['monitoring.Taxon'])),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['monitoring.SamplingSite'])),
            ('stddev', self.gf('django.db.models.fields.FloatField')()),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('n', self.gf('django.db.models.fields.IntegerField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('mean', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('monitoring', ['MeanDensity'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'Unit'
        db.delete_table('monitoring_unit')

        # Deleting model 'Protocol'
        db.delete_table('monitoring_protocol')

        # Deleting model 'MeanDensity'
        db.delete_table('monitoring_meandensity')
    
    
    models = {
        'monitoring.meandensity': {
            'Meta': {'object_name': 'MeanDensity'},
            'date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mean': ('django.db.models.fields.FloatField', [], {}),
            'n': ('django.db.models.fields.IntegerField', [], {}),
            'protocol': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'mean_densities'", 'to': "orm['monitoring.Protocol']"}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['monitoring.SamplingSite']"}),
            'stddev': ('django.db.models.fields.FloatField', [], {}),
            'taxon': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['monitoring.Taxon']"})
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
            'common_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'genus': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }
    
    complete_apps = ['monitoring']
