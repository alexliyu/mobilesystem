# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'TopicType'
        db.create_table('forum_topictype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('forum', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['forum.Forum'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=100, db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')(default='')),
        ))
        db.send_create_signal('forum', ['TopicType'])

        # Adding field 'Topic.topic_type'
        db.add_column('forum_topic', 'topic_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['forum.TopicType'], null=True, blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting model 'TopicType'
        db.delete_table('forum_topictype')

        # Deleting field 'Topic.topic_type'
        db.delete_column('forum_topic', 'topic_type_id')


    models = {
        'attachments.attachment': {
            'Meta': {'object_name': 'Attachment'},
            'activated': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'date_uploaded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '255'}),
            'file_size': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_img': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'num_downloads': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'org_filename': ('django.db.models.fields.TextField', [], {}),
            'suffix': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '8', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
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
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'forum.category': {
            'Meta': {'object_name': 'Category'},
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'forum.config': {
            'Meta': {'object_name': 'Config'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'forum.forum': {
            'Meta': {'object_name': 'Forum'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forum.Category']"}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_post': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'num_posts': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'num_topics': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '110', 'db_index': 'True'}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'forum.forumuserprofile': {
            'Meta': {'object_name': 'LBForumUserProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_activity': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'last_posttime': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'signature': ('django.db.models.fields.CharField', [], {'max_length': '1000', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'forum_profile'", 'unique': 'True', 'to': "orm['auth.User']"}),
            'userrank': ('django.db.models.fields.CharField', [], {'default': "'Junior Member'", 'max_length': '30'})
        },
        'forum.post': {
            'Meta': {'object_name': 'Post'},
            'attachments': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['attachments.Attachment']", 'symmetrical': 'False', 'blank': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'edited_by': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'format': ('django.db.models.fields.CharField', [], {'default': "'bbcode'", 'max_length': '20'}),
            'has_attachments': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'has_imgs': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'posted_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'poster_ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'topic': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forum.Topic']"}),
            'topic_post': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'forum.topic': {
            'Meta': {'object_name': 'Topic'},
            'closed': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'created_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'forum': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forum.Forum']"}),
            'has_attachments': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'has_imgs': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'hidden': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_post': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'last_reply_on': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'level': ('django.db.models.fields.SmallIntegerField', [], {'default': '30'}),
            'need_replay': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'need_reply_attachments': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'num_replies': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'num_views': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'posted_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'sticky': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '999'}),
            'topic_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forum.TopicType']", 'null': 'True', 'blank': 'True'}),
            'updated_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'})
        },
        'forum.topictype': {
            'Meta': {'object_name': 'TopicType'},
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'forum': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forum.Forum']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '100', 'db_index': 'True'})
        }
    }

    complete_apps = ['forum']
