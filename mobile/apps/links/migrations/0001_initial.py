# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Links'
        db.create_table('links_links', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('link_title', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('link_url', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('addTime', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('links', ['Links'])


    def backwards(self, orm):
        
        # Deleting model 'Links'
        db.delete_table('links_links')


    models = {
        'links.links': {
            'Meta': {'object_name': 'Links'},
            'addTime': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link_title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'link_url': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['links']
