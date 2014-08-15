# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Rate'
        db.create_table(u'details_rate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 8, 5, 0, 0))),
            ('offer', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('rate', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=4)),
            ('effective_from', self.gf('django.db.models.fields.DateField')()),
            ('effective_to', self.gf('django.db.models.fields.DateField')(null=True)),
        ))
        db.send_create_signal(u'details', ['Rate'])

        # Adding model 'Address'
        db.create_table(u'details_address', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 8, 5, 0, 0))),
            ('street_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('street_number', self.gf('django.db.models.fields.IntegerField')()),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('postal', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal(u'details', ['Address'])

        # Adding model 'Debtor'
        db.create_table(u'details_debtor', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 8, 5, 0, 0))),
            ('debtornum', self.gf('django.db.models.fields.IntegerField')()),
            ('firstname', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('surname', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('company_code', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('on_ebill', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=12, null=True)),
            ('email_address', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
        ))
        db.send_create_signal(u'details', ['Debtor'])

        # Adding model 'Premise'
        db.create_table(u'details_premise', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 8, 5, 0, 0))),
            ('premnum', self.gf('django.db.models.fields.IntegerField')()),
            ('debtor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['details.Debtor'])),
            ('esiid', self.gf('django.db.models.fields.CharField')(max_length=24, null=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('end_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['details.Address'], null=True)),
            ('rate', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['details.Rate'], null=True)),
        ))
        db.send_create_signal(u'details', ['Premise'])

        # Adding model 'PTJ'
        db.create_table(u'details_ptj', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 8, 5, 0, 0))),
            ('ptj_number', self.gf('django.db.models.fields.IntegerField')()),
            ('debtor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['details.Debtor'], null=True)),
            ('premise', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['details.Premise'], null=True)),
            ('date_logged', self.gf('django.db.models.fields.DateTimeField')()),
            ('date_status', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('type_code', self.gf('django.db.models.fields.CharField')(max_length=2, null=True)),
            ('class_code', self.gf('django.db.models.fields.CharField')(max_length=10, null=True)),
            ('subclass_code', self.gf('django.db.models.fields.CharField')(max_length=2, null=True)),
            ('status_code', self.gf('django.db.models.fields.CharField')(max_length=2, null=True)),
        ))
        db.send_create_signal(u'details', ['PTJ'])

        # Adding model 'Invoice'
        db.create_table(u'details_invoice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 8, 5, 0, 0))),
            ('debtor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['details.Debtor'], null=True)),
            ('invoice_num', self.gf('django.db.models.fields.CharField')(max_length=10, null=True)),
            ('invoice_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('invoice_amt', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=2)),
            ('due_date', self.gf('django.db.models.fields.DateField')(null=True)),
        ))
        db.send_create_signal(u'details', ['Invoice'])

        # Adding model 'Payment'
        db.create_table(u'details_payment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 8, 5, 0, 0))),
            ('debtor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['details.Debtor'], null=True)),
            ('date_received', self.gf('django.db.models.fields.DateField')()),
            ('payment_amt', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('channel', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'details', ['Payment'])


    def backwards(self, orm):
        # Deleting model 'Rate'
        db.delete_table(u'details_rate')

        # Deleting model 'Address'
        db.delete_table(u'details_address')

        # Deleting model 'Debtor'
        db.delete_table(u'details_debtor')

        # Deleting model 'Premise'
        db.delete_table(u'details_premise')

        # Deleting model 'PTJ'
        db.delete_table(u'details_ptj')

        # Deleting model 'Invoice'
        db.delete_table(u'details_invoice')

        # Deleting model 'Payment'
        db.delete_table(u'details_payment')


    models = {
        u'details.address': {
            'Meta': {'object_name': 'Address'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 8, 5, 0, 0)'}),
            'postal': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'street_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'street_number': ('django.db.models.fields.IntegerField', [], {})
        },
        u'details.debtor': {
            'Meta': {'object_name': 'Debtor'},
            'company_code': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'debtornum': ('django.db.models.fields.IntegerField', [], {}),
            'email_address': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 8, 5, 0, 0)'}),
            'on_ebill': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'details.invoice': {
            'Meta': {'object_name': 'Invoice'},
            'debtor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['details.Debtor']", 'null': 'True'}),
            'due_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_amt': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2'}),
            'invoice_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'invoice_num': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 8, 5, 0, 0)'})
        },
        u'details.payment': {
            'Meta': {'object_name': 'Payment'},
            'channel': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'date_received': ('django.db.models.fields.DateField', [], {}),
            'debtor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['details.Debtor']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 8, 5, 0, 0)'}),
            'payment_amt': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'})
        },
        u'details.premise': {
            'Meta': {'object_name': 'Premise'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['details.Address']", 'null': 'True'}),
            'debtor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['details.Debtor']"}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'esiid': ('django.db.models.fields.CharField', [], {'max_length': '24', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 8, 5, 0, 0)'}),
            'premnum': ('django.db.models.fields.IntegerField', [], {}),
            'rate': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['details.Rate']", 'null': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'})
        },
        u'details.ptj': {
            'Meta': {'object_name': 'PTJ'},
            'class_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'date_logged': ('django.db.models.fields.DateTimeField', [], {}),
            'date_status': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'debtor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['details.Debtor']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 8, 5, 0, 0)'}),
            'premise': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['details.Premise']", 'null': 'True'}),
            'ptj_number': ('django.db.models.fields.IntegerField', [], {}),
            'status_code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'subclass_code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'}),
            'type_code': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True'})
        },
        u'details.rate': {
            'Meta': {'object_name': 'Rate'},
            'effective_from': ('django.db.models.fields.DateField', [], {}),
            'effective_to': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 8, 5, 0, 0)'}),
            'offer': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '4'})
        }
    }

    complete_apps = ['details']