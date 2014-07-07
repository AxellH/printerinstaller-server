# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Application'
        db.create_table(u'sparkle_application', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'sparkle', ['Application'])

        # Adding model 'Version'
        db.create_table(u'sparkle_version', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sparkle.Application'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('short_version', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('dsa_signature', self.gf('django.db.models.fields.CharField')(max_length=80, null=True, blank=True)),
            ('length', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('release_notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('minimum_system_version', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('published', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('update', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'sparkle', ['Version'])

        # Adding model 'SystemProfileReport'
        db.create_table(u'sparkle_systemprofilereport', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ip_address', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'sparkle', ['SystemProfileReport'])

        # Adding model 'SystemProfileReportRecord'
        db.create_table(u'sparkle_systemprofilereportrecord', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('report', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sparkle.SystemProfileReport'])),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=80)),
        ))
        db.send_create_signal(u'sparkle', ['SystemProfileReportRecord'])


    def backwards(self, orm):
        # Deleting model 'Application'
        db.delete_table(u'sparkle_application')

        # Deleting model 'Version'
        db.delete_table(u'sparkle_version')

        # Deleting model 'SystemProfileReport'
        db.delete_table(u'sparkle_systemprofilereport')

        # Deleting model 'SystemProfileReportRecord'
        db.delete_table(u'sparkle_systemprofilereportrecord')


    models = {
        u'sparkle.application': {
            'Meta': {'object_name': 'Application'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'sparkle.systemprofilereport': {
            'Meta': {'object_name': 'SystemProfileReport'},
            'added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'})
        },
        u'sparkle.systemprofilereportrecord': {
            'Meta': {'object_name': 'SystemProfileReportRecord'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sparkle.SystemProfileReport']"}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '80'})
        },
        u'sparkle.version': {
            'Meta': {'object_name': 'Version'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sparkle.Application']"}),
            'dsa_signature': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'length': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'minimum_system_version': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'published': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'release_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'short_version': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'update': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['sparkle']