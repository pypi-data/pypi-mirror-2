
from south.db import db
from django.db import models
from github.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Commit'
        db.create_table('github_commit', (
            ('id', orm['github.Commit:id']),
            ('project', orm['github.Commit:project']),
            ('sha', orm['github.Commit:sha']),
            ('tree', orm['github.Commit:tree']),
            ('created', orm['github.Commit:created']),
            ('name', orm['github.Commit:name']),
            ('message', orm['github.Commit:message']),
            ('url', orm['github.Commit:url']),
        ))
        db.send_create_signal('github', ['Commit'])
        
        # Adding model 'Project'
        db.create_table('github_project', (
            ('id', orm['github.Project:id']),
            ('title', orm['github.Project:title']),
            ('slug', orm['github.Project:slug']),
            ('description', orm['github.Project:description']),
            ('github_repo', orm['github.Project:github_repo']),
            ('created', orm['github.Project:created']),
        ))
        db.send_create_signal('github', ['Project'])
        
        # Adding model 'Blob'
        db.create_table('github_blob', (
            ('id', orm['github.Blob:id']),
            ('commit', orm['github.Blob:commit']),
            ('name', orm['github.Blob:name']),
            ('path', orm['github.Blob:path']),
            ('size', orm['github.Blob:size']),
            ('mime_type', orm['github.Blob:mime_type']),
            ('data', orm['github.Blob:data']),
            ('sha', orm['github.Blob:sha']),
        ))
        db.send_create_signal('github', ['Blob'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Commit'
        db.delete_table('github_commit')
        
        # Deleting model 'Project'
        db.delete_table('github_project')
        
        # Deleting model 'Blob'
        db.delete_table('github_blob')
        
    
    
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
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }
    
    complete_apps = ['github']
