
from south.db import db
from django.db import models
from github.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'User'
        db.create_table('github_user', (
            ('id', orm['github.user:id']),
            ('login', orm['github.user:login']),
            ('name', orm['github.user:name']),
            ('company', orm['github.user:company']),
            ('location', orm['github.user:location']),
            ('email', orm['github.user:email']),
            ('blog', orm['github.user:blog']),
            ('following_count', orm['github.user:following_count']),
            ('followers_count', orm['github.user:followers_count']),
            ('public_gist_count', orm['github.user:public_gist_count']),
            ('public_repo_count', orm['github.user:public_repo_count']),
        ))
        db.send_create_signal('github', ['User'])
        
        # Adding field 'Project.user'
        db.add_column('github_project', 'user', orm['github.project:user'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'User'
        db.delete_table('github_user')
        
        # Deleting field 'Project.user'
        db.delete_column('github_project', 'user_id')
        
    
    
    models = {
        'github.blob': {
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
            'created': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'commits'", 'to': "orm['github.Project']"}),
            'sha': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tree': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'github.project': {
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'github_repo': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '50', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['github.User']", 'null': 'True'})
        },
        'github.user': {
            'blog': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'company': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'followers_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'following_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'login': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'public_gist_count': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'public_repo_count': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'})
        }
    }
    
    complete_apps = ['github']
