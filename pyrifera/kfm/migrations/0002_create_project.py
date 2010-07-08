# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from monitoring.models import Project

class Migration(DataMigration):
    
    def forwards(self, orm):
        "Write your forwards methods here."
        kfm = Project(name="NPS Kelp Forest Monitoring", app_label="kfm")
        kfm.save()
    
    
    def backwards(self, orm):
        "Write your backwards methods here."
        kfm = Project.objects.get(name="NPS Kelp Forest Monitoring")
        kfm.delete()
    
    models = {
        
    }
    
    complete_apps = ['kfm']
