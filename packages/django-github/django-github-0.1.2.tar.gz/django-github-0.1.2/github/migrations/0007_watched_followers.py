# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding M2M table for field followers on 'GithubUser'
        db.create_table('github_user_followers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_githubuser', models.ForeignKey(orm['github.githubuser'], null=False)),
            ('to_githubuser', models.ForeignKey(orm['github.githubuser'], null=False))
        ))
        db.create_unique('github_user_followers', ['from_githubuser_id', 'to_githubuser_id'])

        # Adding M2M table for field following on 'GithubUser'
        db.create_table('github_user_following', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_githubuser', models.ForeignKey(orm['github.githubuser'], null=False)),
            ('to_githubuser', models.ForeignKey(orm['github.githubuser'], null=False))
        ))
        db.create_unique('github_user_following', ['from_githubuser_id', 'to_githubuser_id'])

        # Adding M2M table for field watchers on 'Project'
        db.create_table('github_project_watchers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm['github.project'], null=False)),
            ('githubuser', models.ForeignKey(orm['github.githubuser'], null=False))
        ))
        db.create_unique('github_project_watchers', ['project_id', 'githubuser_id'])


    def backwards(self, orm):
        
        # Removing M2M table for field followers on 'GithubUser'
        db.delete_table('github_user_followers')

        # Removing M2M table for field following on 'GithubUser'
        db.delete_table('github_user_following')

        # Removing M2M table for field watchers on 'Project'
        db.delete_table('github_project_watchers')


    models = {
        'github.blob': {
            'Meta': {'ordering': "['-commit__created', 'commit__project__title', 'path']", 'object_name': 'Blob'},
            'commit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'blobs'", 'to': "orm['github.Commit']"}),
            'data': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mime_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'path': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sha': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'size': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'github.commit': {
            'Meta': {'ordering': "['-created']", 'object_name': 'Commit'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'commits'", 'null': 'True', 'to': "orm['github.GithubUser']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'commits'", 'to': "orm['github.Project']"}),
            'sha': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tree': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'github.gist': {
            'Meta': {'ordering': "('-created',)", 'object_name': 'Gist'},
            'code': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'filename': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'gist_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['github.Language']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'github.githubuser': {
            'Meta': {'ordering': "('login',)", 'object_name': 'GithubUser', 'db_table': "'github_user'"},
            'blog': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'company': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'followers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'followers_rel_+'", 'to': "orm['github.GithubUser']"}),
            'followers_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'following': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'following_rel_+'", 'to': "orm['github.GithubUser']"}),
            'following_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'login': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'public_gist_count': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'public_repo_count': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'})
        },
        'github.language': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Language'},
            'extension': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'mime_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        },
        'github.project': {
            'Meta': {'ordering': "('title',)", 'unique_together': "(('user', 'slug'),)", 'object_name': 'Project'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'github_repo': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['github.GithubUser']", 'null': 'True', 'blank': 'True'}),
            'watchers': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'watched'", 'symmetrical': 'False', 'to': "orm['github.GithubUser']"})
        }
    }

    complete_apps = ['github']
