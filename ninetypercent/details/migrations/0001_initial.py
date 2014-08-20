# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Address'
        db.create_table(u'details_address', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 8, 19, 0, 0))),
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
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 8, 19, 0, 0))),
            ('debtornum', self.gf('django.db.models.fields.IntegerField')()),
            ('firstname', self.gf('django.db.models.fields.CharField')(max_length=20, null=True)),
            ('surname', self.gf('django.db.models.fields.CharField')(max_length=30, null=True)),
            ('company_code', self.gf('django.db.models.fields.CharField')(max_length=4, null=True)),
            ('on_ebill', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=12, null=True)),
            ('email_address', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('aav', self.gf('django.db.models.fields.CharField')(max_length=4, null=True)),
            ('current_balance', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=4)),
            ('overdue_balance', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=4)),
            ('statement_due', self.gf('django.db.models.fields.DateField')(null=True)),
            ('statement_amount', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=4)),
        ))
        db.send_create_signal(u'details', ['Debtor'])

        # Adding model 'Premise'
        db.create_table(u'details_premise', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 8, 19, 0, 0))),
            ('premnum', self.gf('django.db.models.fields.IntegerField')()),
            ('debtor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['details.Debtor'])),
            ('esiid', self.gf('django.db.models.fields.CharField')(max_length=24, null=True)),
            ('start_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('end_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('address', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['details.Address'], null=True)),
            ('reading', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['details.Reading'], null=True)),
        ))
        db.send_create_signal(u'details', ['Premise'])

        # Adding model 'Rate'
        db.create_table(u'details_rate', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 8, 19, 0, 0))),
            ('premise', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['details.Premise'])),
            ('offer', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('rate', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=4)),
            ('effective_from', self.gf('django.db.models.fields.DateField')()),
            ('effective_to', self.gf('django.db.models.fields.DateField')(null=True)),
        ))
        db.send_create_signal(u'details', ['Rate'])

        # Adding model 'PTJ'
        db.create_table(u'details_ptj', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 8, 19, 0, 0))),
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
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 8, 19, 0, 0))),
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
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 8, 19, 0, 0))),
            ('debtor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['details.Debtor'], null=True)),
            ('date_received', self.gf('django.db.models.fields.DateField')()),
            ('payment_amt', self.gf('django.db.models.fields.DecimalField')(max_digits=10, decimal_places=2)),
            ('channel', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'details', ['Payment'])

        # Adding model 'Reading'
        db.create_table(u'details_reading', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('last_modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 8, 19, 0, 0))),
            ('reading', self.gf('django.db.models.fields.IntegerField')()),
            ('read_date', self.gf('django.db.models.fields.DateField')()),
            ('read_method', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('invoice_num', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'details', ['Reading'])


    def backwards(self, orm):
        # Deleting model 'Address'
        db.delete_table(u'details_address')

        # Deleting model 'Debtor'
        db.delete_table(u'details_debtor')

        # Deleting model 'Premise'
        db.delete_table(u'details_premise')

        # Deleting model 'Rate'
        db.delete_table(u'details_rate')

        # Deleting model 'PTJ'
        db.delete_table(u'details_ptj')

        # Deleting model 'Invoice'
        db.delete_table(u'details_invoice')

        # Deleting model 'Payment'
        db.delete_table(u'details_payment')

        # Deleting model 'Reading'
        db.delete_table(u'details_reading')


    models = {
        u'details.address': {
            'Meta': {'object_name': 'Address'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 8, 19, 0, 0)'}),
            'postal': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'street_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'street_number': ('django.db.models.fields.IntegerField', [], {})
        },
        u'details.debtor': {
            'Meta': {'object_name': 'Debtor'},
            'aav': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True'}),
            'company_code': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True'}),
            'current_balance': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4'}),
            'debtornum': ('django.db.models.fields.IntegerField', [], {}),
            'email_address': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 8, 19, 0, 0)'}),
            'on_ebill': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'overdue_balance': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True'}),
            'statement_amount': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '4'}),
            'statement_due': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True'})
        },
        u'details.invoice': {
            'Meta': {'object_name': 'Invoice'},
            'debtor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['details.Debtor']", 'null': 'True'}),
            'due_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_amt': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '10', 'decimal_places': '2'}),
            'invoice_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'invoice_num': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 8, 19, 0, 0)'})
        },
        u'details.payment': {
            'Meta': {'object_name': 'Payment'},
            'channel': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'date_received': ('django.db.models.fields.DateField', [], {}),
            'debtor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['details.Debtor']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 8, 19, 0, 0)'}),
            'payment_amt': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'})
        },
        u'details.premise': {
            'Meta': {'object_name': 'Premise'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['details.Address']", 'null': 'True'}),
            'debtor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['details.Debtor']"}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'esiid': ('django.db.models.fields.CharField', [], {'max_length': '24', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 8, 19, 0, 0)'}),
            'premnum': ('django.db.models.fields.IntegerField', [], {}),
            'reading': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['details.Reading']", 'null': 'True'}),
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
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 8, 19, 0, 0)'}),
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
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 8, 19, 0, 0)'}),
            'offer': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'premise': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['details.Premise']"}),
            'rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '4'})
        },
        u'details.reading': {
            'Meta': {'object_name': 'Reading'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_num': ('django.db.models.fields.IntegerField', [], {}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 8, 19, 0, 0)'}),
            'read_date': ('django.db.models.fields.DateField', [], {}),
            'read_method': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'reading': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['details']