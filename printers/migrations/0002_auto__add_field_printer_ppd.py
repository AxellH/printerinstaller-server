# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Printer.ppd'
        db.add_column(u'printers_printer', 'ppd',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Printer.ppd'
        db.delete_column(u'printers_printer', 'ppd')


    models = {
        u'printers.option': {
            'Meta': {'object_name': 'Option'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'option': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200', 'blank': 'True'})
        },
        u'printers.printer': {
            'Meta': {'object_name': 'Printer'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'option': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['printers.Option']", 'symmetrical': 'False', 'blank': 'True'}),
            'ppd': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'ppd_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'protocol': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'printers.printerlist': {
            'Meta': {'object_name': 'PrinterList'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'printer': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['printers.Printer']", 'symmetrical': 'False', 'blank': 'True'})
        }
    }

    complete_apps = ['printers']