# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'sms_list'
        db.create_table('sms_sms_list', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default='', max_length=50)),
            ('content', self.gf('django.db.models.fields.TextField')(default='', max_length=200)),
            ('creat_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('sms_id', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('stat', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=1)),
            ('errors', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('sms_users', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('sms', ['sms_list'])

        # Adding model 'sms_history'
        db.create_table('sms_sms_history', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default='', max_length=50)),
            ('content', self.gf('django.db.models.fields.TextField')(default='', max_length=500)),
            ('creat_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('sms_id', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('sms_users', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('stat', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=1)),
            ('errors', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('sms', ['sms_history'])


    def backwards(self, orm):
        
        # Deleting model 'sms_list'
        db.delete_table('sms_sms_list')

        # Deleting model 'sms_history'
        db.delete_table('sms_sms_history')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'sms.sms_history': {
            'Meta': {'object_name': 'sms_history'},
            'content': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '500'}),
            'creat_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'errors': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sms_id': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'sms_users': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'stat': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'})
        },
        'sms.sms_list': {
            'Meta': {'object_name': 'sms_list'},
            'content': ('django.db.models.fields.TextField', [], {'default': "''", 'max_length': '200'}),
            'creat_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'errors': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sms_id': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'sms_users': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'stat': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'})
        }
    }

    complete_apps = ['sms']
