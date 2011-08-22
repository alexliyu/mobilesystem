# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'sms_history.sms_users'
        db.delete_column('sms_sms_history', 'sms_users_id')

        # Adding M2M table for field sms_users on 'sms_history'
        db.create_table('sms_sms_history_sms_users', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('sms_history', models.ForeignKey(orm['sms.sms_history'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('sms_sms_history_sms_users', ['sms_history_id', 'user_id'])

        # Deleting field 'sms_list.sms_users'
        db.delete_column('sms_sms_list', 'sms_users_id')

        # Adding M2M table for field sms_users on 'sms_list'
        db.create_table('sms_sms_list_sms_users', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('sms_list', models.ForeignKey(orm['sms.sms_list'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('sms_sms_list_sms_users', ['sms_list_id', 'user_id'])


    def backwards(self, orm):
        
        # User chose to not deal with backwards NULL issues for 'sms_history.sms_users'
        raise RuntimeError("Cannot reverse this migration. 'sms_history.sms_users' and its values cannot be restored.")

        # Removing M2M table for field sms_users on 'sms_history'
        db.delete_table('sms_sms_history_sms_users')

        # User chose to not deal with backwards NULL issues for 'sms_list.sms_users'
        raise RuntimeError("Cannot reverse this migration. 'sms_list.sms_users' and its values cannot be restored.")

        # Removing M2M table for field sms_users on 'sms_list'
        db.delete_table('sms_sms_list_sms_users')


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
            'sms_users': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False'}),
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
            'sms_users': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False'}),
            'stat': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'})
        }
    }

    complete_apps = ['sms']
