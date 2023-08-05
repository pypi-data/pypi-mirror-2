# -*- coding: utf-8 -*-
from south.db import db

from django.db import models

from experiments.models import *

class Migration:    
    def forwards(self, orm):
        # Adding model 'AnonymousVisitor'
        db.create_table('experiments_anonymousvisitor', (
            ('id', orm['experiments.anonymousvisitor:id']),
            ('created', orm['experiments.anonymousvisitor:created']),
        ))
        db.send_create_signal('experiments', ['AnonymousVisitor'])
        
        # Adding model 'GoalRecord'
        db.create_table('experiments_goalrecord', (
            ('id', orm['experiments.goalrecord:id']),
            ('created', orm['experiments.goalrecord:created']),
            ('anonymous_visitor', orm['experiments.goalrecord:anonymous_visitor']),
            ('goal_type', orm['experiments.goalrecord:goal_type']),
        ))
        db.send_create_signal('experiments', ['GoalRecord'])
        
        # Adding model 'GoalType'
        db.create_table('experiments_goaltype', (
            ('id', orm['experiments.goaltype:id']),
            ('name', orm['experiments.goaltype:name']),
        ))
        db.send_create_signal('experiments', ['GoalType'])
        
        # Adding field 'Participant.anonymous_visitor'
        db.add_column('experiments_participant', 'anonymous_visitor', orm['experiments.participant:anonymous_visitor'])
        
        # Changing field 'Participant.user'
        # (to signature: django.db.models.fields.related.ForeignKey(to=orm['auth.User'], null=True))
        db.alter_column('experiments_participant', 'user_id', orm['experiments.participant:user'])
        
        # Creating unique_together for [anonymous_visitor, experiment] on Participant.
        db.create_unique('experiments_participant', ['anonymous_visitor_id', 'experiment_id'])
    
    def backwards(self, orm):    
        # Deleting unique_together for [anonymous_visitor, experiment] on Participant.
        db.delete_unique('experiments_participant', ['anonymous_visitor_id', 'experiment_id'])
        
        # Deleting model 'AnonymousVisitor'
        db.delete_table('experiments_anonymousvisitor')
        
        # Deleting model 'GoalRecord'
        db.delete_table('experiments_goalrecord')
        
        # Deleting model 'GoalType'
        db.delete_table('experiments_goaltype')
        
        # Deleting field 'Participant.anonymous_visitor'
        db.delete_column('experiments_participant', 'anonymous_visitor_id')
        
        # Changing field 'Participant.user'
        # (to signature: django.db.models.fields.related.ForeignKey(to=orm['auth.User']))
        db.alter_column('experiments_participant', 'user_id', orm['experiments.participant:user'])
    
    models = {
        'auth.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'experiments.anonymousvisitor': {
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'experiments.dailyreport': {
            'control_score': ('django.db.models.fields.FloatField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'experiment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['experiments.Experiment']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'test_score': ('django.db.models.fields.FloatField', [], {})
        },
        'experiments.experiment': {
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'experiments.goalrecord': {
            'anonymous_visitor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['experiments.AnonymousVisitor']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'goal_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['experiments.GoalType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'experiments.goaltype': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'unique': 'True'})
        },
        'experiments.participant': {
            'Meta': {'unique_together': "(('user', 'experiment'), ('anonymous_visitor', 'experiment'))"},
            'anonymous_visitor': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['experiments.AnonymousVisitor']", 'null': 'True'}),
            'enrollment_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'experiment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['experiments.Experiment']"}),
            'group': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'})
        }
    }
    
    complete_apps = ['experiments']
