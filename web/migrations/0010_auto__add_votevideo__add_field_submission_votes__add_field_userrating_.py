# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'VoteVideo'
        db.create_table(u'web_votevideo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('example', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web.Submission'])),
            ('vote', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'web', ['VoteVideo'])

        # Adding field 'Submission.votes'
        db.add_column(u'web_submission', 'votes',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'UserRating.VideoRating'
        db.add_column(u'web_userrating', 'VideoRating',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'VoteVideo'
        db.delete_table(u'web_votevideo')

        # Deleting field 'Submission.votes'
        db.delete_column(u'web_submission', 'votes')

        # Deleting field 'UserRating.VideoRating'
        db.delete_column(u'web_userrating', 'VideoRating')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'web.atom': {
            'Meta': {'ordering': "['name']", 'object_name': 'Atom'},
            'base_category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'child_atoms'", 'to': u"orm['web.BaseCategory']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'summary': ('django.db.models.fields.TextField', [], {'default': "'There is no summary added at this time.'"})
        },
        u'web.atomcategory': {
            'Meta': {'ordering': "['name']", 'object_name': 'AtomCategory'},
            'child_atoms': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['web.Atom']", 'symmetrical': 'False', 'blank': 'True'}),
            'child_categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'parent_categories'", 'blank': 'True', 'to': u"orm['web.AtomCategory']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'parent_class': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.Class']"})
        },
        u'web.basecategory': {
            'Meta': {'ordering': "['name']", 'object_name': 'BaseCategory'},
            'child_categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'parent_categories'", 'blank': 'True', 'to': u"orm['web.BaseCategory']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'summary': ('django.db.models.fields.TextField', [], {'default': "'There is no summary added at this time.'"})
        },
        u'web.bugreport': {
            'Meta': {'ordering': "['subject']", 'object_name': 'BugReport'},
            'cc_myself': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'web.class': {
            'Meta': {'ordering': "['name']", 'object_name': 'Class'},
            'allowed_users': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'allowed_classes'", 'blank': 'True', 'to': u"orm['auth.User']"}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'author'", 'to': u"orm['auth.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'N'", 'max_length': '1'}),
            'students': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'enrolled_classes'", 'blank': 'True', 'to': u"orm['auth.User']"}),
            'summary': ('django.db.models.fields.TextField', [], {'default': "'There is no summary added at this time.'"})
        },
        u'web.example': {
            'Meta': {'object_name': 'Example'},
            'atom': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'example_set'", 'to': u"orm['web.Atom']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'example_set'", 'to': u"orm['auth.User']"}),
            'votes': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'web.exposition': {
            'Meta': {'ordering': "['title']", 'object_name': 'Exposition'},
            'atom': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.Atom']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'exposition_set'", 'to': u"orm['auth.User']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'votes': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'web.lecturenote': {
            'Meta': {'object_name': 'LectureNote'},
            'atom': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'lecturenote_set'", 'to': u"orm['web.Atom']"}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'lecturenote_set'", 'to': u"orm['auth.User']"}),
            'votes': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'web.submission': {
            'Meta': {'object_name': 'Submission'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'video_owner'", 'to': u"orm['auth.User']"}),
            'tags': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'tags'", 'symmetrical': 'False', 'to': u"orm['web.Atom']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'video': ('django.db.models.fields.CharField', [], {'max_length': '400', 'blank': 'True'}),
            'votes': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'web.userrating': {
            'ExampleRating': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'ExpoRating': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'LecNoteRating': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'Meta': {'object_name': 'UserRating'},
            'VideoRating': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'VoteDown': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'VoteUp': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rating': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'ratingUser'", 'to': u"orm['auth.User']"})
        },
        u'web.vote': {
            'Meta': {'object_name': 'Vote'},
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rating': ('django.db.models.fields.IntegerField', [], {}),
            'submission': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'votes_s'", 'to': u"orm['web.Submission']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'v_category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'votes_s'", 'to': u"orm['web.VoteCategory']"})
        },
        u'web.votecategory': {
            'Meta': {'ordering': "['name']", 'object_name': 'VoteCategory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'web.voteexample': {
            'Meta': {'object_name': 'VoteExample'},
            'example': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.Example']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'vote': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'web.voteexposition': {
            'Meta': {'object_name': 'VoteExposition'},
            'example': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.Exposition']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'vote': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'web.votelecturenote': {
            'Meta': {'object_name': 'VoteLectureNote'},
            'example': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.LectureNote']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'vote': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'web.votevideo': {
            'Meta': {'object_name': 'VoteVideo'},
            'example': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['web.Submission']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'vote': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['web']