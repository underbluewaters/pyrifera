# encoding: utf-8
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from monitoring.models import Project

class Migration(DataMigration):
    
    def forwards(self, orm):
        "Write your forwards methods here."
        project = Project(name="PISCO Intertidal")
        project.save()
    
    
    def backwards(self, orm):
        "Write your backwards methods here."
        project = Project.objects.get(name="PISCO Intertidal")
        project.delete()
    
    models = {
        
    }
    
    complete_apps = ['pisco_intertidal']
