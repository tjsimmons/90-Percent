from django.db import models
from datetime import datetime

# Create your models here.
class Common(models.Model):
    last_modified = models.DateTimeField(default=datetime.now())

    # meta info for the class.
    # abstract = True means it's an abstract class
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # always make sure we update timestamp on save
        # basically a trigger
        self.last_modified = datetime.now()

        # make sure we actually save
        super(Common, self).save(*args, **kwargs)

class Address(Common):
    street_name = models.CharField(max_length=50)
    street_number = models.IntegerField()
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=2)
    postal = models.CharField(max_length=10)

class BillingAddress(Common):
    address_line1 = models.CharField(max_length=50)
    address_line2 = models.CharField(max_length=50)
    address_line3 = models.CharField(max_length=50)
    address_name = models.CharField(max_length=100)
    postal = models.CharField(max_length=10)

class Debtor(Common):
    debtornum = models.IntegerField()
    firstname = models.CharField(max_length=20, null=True)
    surname = models.CharField(max_length=30, null=True)
    company_code = models.CharField(max_length=4, null=True)
    billing_address = models.ForeignKey(BillingAddress, null=True)
    on_ebill = models.CharField(max_length=1, null=True)
    phone_number = models.CharField(max_length=12, null=True)
    email_address = models.CharField(max_length=50, null=True)
    aav = models.CharField(max_length=4, null=True)
    current_balance = models.DecimalField(max_digits=10, decimal_places=4, null=True)
    overdue_balance = models.DecimalField(max_digits=10, decimal_places=4, null=True)
    statement_due = models.DateField(null=True)
    statement_amount = models.DecimalField(max_digits=10, decimal_places=4, null=True)

    def get_absolute_url(self):
        return "/details/%s/" % self.debtornum

class Premise(Common):
    premnum = models.IntegerField()
    debtor = models.ForeignKey(Debtor)
    esiid = models.CharField(max_length=24, null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    status = models.CharField(max_length=1, null=True)
    address = models.ForeignKey(Address, null=True)
    reading = models.ForeignKey("Reading", null=True)

class Rate(Common):
    premise = models.ForeignKey(Premise)
    offer = models.CharField(max_length=30)
    rate = models.DecimalField(max_digits=5, decimal_places=4, null=True)
    effective_from = models.DateField(null=True)
    effective_to = models.DateField(null=True)

class PTJ(Common):
    ptj_number = models.IntegerField()
    debtor = models.ForeignKey(Debtor, null=True)
    premise = models.ForeignKey(Premise, null=True)
    date_logged = models.DateTimeField()
    date_status = models.DateTimeField(null=True)
    type_code = models.CharField(max_length=2, null=True)
    class_code = models.CharField(max_length=10, null=True)
    subclass_code = models.CharField(max_length=2, null=True)
    status_code = models.CharField(max_length=2, null=True)


class Invoice(Common):
    debtor = models.ForeignKey(Debtor, null=True)
    invoice_num = models.CharField(max_length=10, null=True)
    invoice_date = models.DateField(null=True)
    invoice_amt = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    due_date = models.DateField(null=True)

class Payment(Common):
    debtor = models.ForeignKey(Debtor, null=True)
    date_received = models.DateField()
    payment_amt = models.DecimalField(max_digits=10, decimal_places=2)
    channel = models.CharField(max_length=20)

class Reading(Common):
  reading = models.IntegerField()
  read_date = models.DateField()
  read_method = models.CharField(max_length=1)
  invoice_num = models.IntegerField()
