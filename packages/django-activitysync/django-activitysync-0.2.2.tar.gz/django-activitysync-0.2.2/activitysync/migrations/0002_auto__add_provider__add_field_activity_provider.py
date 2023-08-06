# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Provider'
        db.create_table('activitysync_provider', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('prefix', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=500)),
            ('sourceid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20, primary_key=True, db_index=True)),
        ))
        db.send_create_signal('activitysync', ['Provider'])

        # Adding field 'Activity.provider'
        db.add_column('activitysync_activity', 'provider', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['activitysync.Provider'], null=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting model 'Provider'
        db.delete_table('activitysync_provider')

        # Deleting field 'Activity.provider'
        db.delete_column('activitysync_activity', 'provider_id')


    models = {
        'activitysync.activity': {
            'Meta': {'ordering': "('-pub_date',)", 'object_name': 'Activity'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'guid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '500'}),
            'provider': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['activitysync.Provider']", 'null': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {}),
            'published': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        },
        'activitysync.provider': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Provider'},
            'link': ('django.db.models.fields.URLField', [], {'max_length': '500'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'prefix': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'sourceid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20', 'primary_key': 'True', 'db_index': 'True'})
        }
    }

    complete_apps = ['activitysync']
