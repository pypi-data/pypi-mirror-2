
from south.db import db
from django.db import models
from github.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Language'
        db.create_table('github_language', (
            ('id', orm['github.language:id']),
            ('name', orm['github.language:name']),
            ('slug', orm['github.language:slug']),
            ('language_code', orm['github.language:language_code']),
            ('mime_type', orm['github.language:mime_type']),
            ('extension', orm['github.language:extension']),
        ))
        db.send_create_signal('github', ['Language'])
        
        # Adding model 'Gist'
        db.create_table('github_gist', (
            ('id', orm['github.gist:id']),
            ('title', orm['github.gist:title']),
            ('slug', orm['github.gist:slug']),
            ('language', orm['github.gist:language']),
            ('filename', orm['github.gist:filename']),
            ('description', orm['github.gist:description']),
            ('code', orm['github.gist:code']),
            ('created', orm['github.gist:created']),
            ('gist_id', orm['github.gist:gist_id']),
        ))
        db.send_create_signal('github', ['Gist'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Language'
        db.delete_table('github_language')
        
        # Deleting model 'Gist'
        db.delete_table('github_gist')
        
    
    
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
            'github_repo': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'blank': 'True'}),
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'public_gist_count': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'public_repo_count': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'})
        }
    }
    
    complete_apps = ['github']
