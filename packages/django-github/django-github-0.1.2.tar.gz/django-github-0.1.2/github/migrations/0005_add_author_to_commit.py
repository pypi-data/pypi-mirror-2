
from south.db import db
from django.db import models
from github.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'Commit.author'
        db.add_column('github_commit', 'author', orm['github.commit:author'])
        
        # Changing field 'Project.user'
        # (to signature: django.db.models.fields.related.ForeignKey(to=orm['github.User'], null=True, blank=True))
        db.alter_column('github_project', 'user_id', orm['github.project:user'])
        
        # Changing field 'Project.github_repo'
        # (to signature: django.db.models.fields.CharField(max_length=255, blank=True))
        db.alter_column('github_project', 'github_repo', orm['github.project:github_repo'])
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'Commit.author'
        db.delete_column('github_commit', 'author_id')
        
        # Changing field 'Project.user'
        # (to signature: django.db.models.fields.related.ForeignKey(to=orm['github.User'], null=True))
        db.alter_column('github_project', 'user_id', orm['github.project:user'])
        
        # Changing field 'Project.github_repo'
        # (to signature: django.db.models.fields.CharField(max_length=255))
        db.alter_column('github_project', 'github_repo', orm['github.project:github_repo'])
        
    
    
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
            'author': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'related_name': "'commits'", 'to': "orm['github.User']"}),
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
        'github.language': {
            'extension': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'mime_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        },
        'github.project': {
            'Meta': {'unique_together': "(('user', 'slug'),)"},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'github_repo': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['github.User']", 'null': 'True', 'blank': 'True'})
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'public_gist_count': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'public_repo_count': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'})
        }
    }
    
    complete_apps = ['github']
