# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Debtor.firstname'
        db.alter_column(u'details_debtor', 'firstname', self.gf('django.db.models.fields.CharField')(max_length=20, null=True))

    def backwards(self, orm):

        # Changing field 'Debtor.firstname'
        db.alter_column(u'details_debtor', 'firstname', self.gf('django.db.models.fields.CharField')(default=None, max_length=20))

    models = {
        u'details.address': {
            'Meta': {'object_name': 'Address'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 8, 13, 0, 0)'}),
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
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 8, 13, 0, 0)'}),
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
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 8, 13, 0, 0)'})
        },
        u'details.payment': {
            'Meta': {'object_name': 'Payment'},
            'channel': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'date_received': ('django.db.models.fields.DateField', [], {}),
            'debtor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['details.Debtor']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 8, 13, 0, 0)'}),
            'payment_amt': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'})
        },
        u'details.premise': {
            'Meta': {'object_name': 'Premise'},
            'address': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['details.Address']", 'null': 'True'}),
            'debtor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['details.Debtor']"}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'esiid': ('django.db.models.fields.CharField', [], {'max_length': '24', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 8, 13, 0, 0)'}),
            'premnum': ('django.db.models.fields.IntegerField', [], {}),
            'rate': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['details.Rate']", 'null': 'True'}),
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
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 8, 13, 0, 0)'}),
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
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 8, 13, 0, 0)'}),
            'offer': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '4'})
        },
        u'details.reading': {
            'Meta': {'object_name': 'Reading'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_num': ('django.db.models.fields.IntegerField', [], {}),
            'last_modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 8, 13, 0, 0)'}),
            'read_date': ('django.db.models.fields.DateField', [], {}),
            'read_method': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'reading': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['details']