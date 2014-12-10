# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Option'
        db.create_table(u'printers_option', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('option', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200, blank=True)),
        ))
        db.send_create_signal(u'printers', ['Option'])

        # Adding model 'Printer'
        db.create_table(u'printers_printer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('model', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('ppd_file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('protocol', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'printers', ['Printer'])

        # Adding M2M table for field option on 'Printer'
        m2m_table_name = db.shorten_name(u'printers_printer_option')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('printer', models.ForeignKey(orm[u'printers.printer'], null=False)),
            ('option', models.ForeignKey(orm[u'printers.option'], null=False))
        ))
        db.create_unique(m2m_table_name, ['printer_id', 'option_id'])

        # Adding model 'PrinterList'
        db.create_table(u'printers_printerlist', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'printers', ['PrinterList'])

        # Adding M2M table for field printer on 'PrinterList'
        m2m_table_name = db.shorten_name(u'printers_printerlist_printer')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('printerlist', models.ForeignKey(orm[u'printers.printerlist'], null=False)),
            ('printer', models.ForeignKey(orm[u'printers.printer'], null=False))
        ))
        db.create_unique(m2m_table_name, ['printerlist_id', 'printer_id'])


    def backwards(self, orm):
        # Deleting model 'Option'
        db.delete_table(u'printers_option')

        # Deleting model 'Printer'
        db.delete_table(u'printers_printer')

        # Removing M2M table for field option on 'Printer'
        db.delete_table(db.shorten_name(u'printers_printer_option'))

        # Deleting model 'PrinterList'
        db.delete_table(u'printers_printerlist')

        # Removing M2M table for field printer on 'PrinterList'
        db.delete_table(db.shorten_name(u'printers_printerlist_printer'))


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
            'model': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'option': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['printers.Option']", 'symmetrical': 'False', 'blank': 'True'}),
            'ppd_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
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