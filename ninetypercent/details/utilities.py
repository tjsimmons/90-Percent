from datetime import datetime
from cx_Oracle import connect

from models import Debtor, Premise, Rate, Address, Invoice, PTJ, Payment, Reading

def get_database_connection():
    db_connect = connect('foo', 'bar', 'baz')
    db_cursor = db_connect.cursor()

    return (db_connect, db_cursor)

def close_database_connection(connection):
    db, cursor = connection

    db.close()

def get_debtor_details(debtor, connection):
    connect, cursor = connection

    query = Debtor.get_query(debtor.debtornum)

    details = cursor.execute(query).fetchone()

    if details:
        debtor.firstname = details[0]
        debtor.surname = details[1]
        debtor.company_code = details[2]
        debtor.on_ebill = details[3]
        debtor.phone_number = details[4]
        debtor.email_address = details[5]

    debtor.save()

def get_address_details(premise, connection):
    connect, cursor = connection
    query = Address.get_query(premise.premnum)

    row = cursor.execute(query).fetchone()

    address = Address()
    address.street_name = row[0]
    address.street_number = row[1]
    address.city = row[2]
    address.state = row[3]
    address.postal = row[4]
    address.save()

    return address

def get_last_rate(debtor, premise, connection):
    connect, cursor = connection
    rate_query = Rate.get_query(debtor.debtornum, premise.premnum)


    row = cursor.execute(rate_query).fetchone()

    rate = Rate()
    rate.offer = row[0]
    rate.rate = row[1]
    rate.effective_from = row[2]
    rate.effective_to = row[3]
    rate.save()

    return rate

def get_last_reading(debtor, premise, connection):
    connect, cursor = connection

    query = Reading.get_query(debtor.debtornum, premise.premnum)

    row = cursor.execute(query).fetchone()

    reading, created = Reading.objects.get_or_create(reading=row[0], read_date=row[1], read_method=row[2], invoice_num=row[3])

    return reading

def get_premises(debtor, connection):
    connect, cursor = connection
    premises = []

    query = Premise.get_query(debtor.debtornum)

    for row in cursor.execute(query).fetchall():
        try:
            premise = Premise.objects.get(premnum__exact=row[0])
        except Premise.DoesNotExist:
            premise = Premise()

        premise.premnum = row[0]
        premise.debtor = debtor
        premise.esiid = row[1]
        premise.start_date = row[2]
        premise.status = row[3]
        premise.address = get_address_details(premise, connection)
        premise.rate = get_last_rate(debtor, premise, connection)
        premise.reading = get_last_reading(debtor, premise, connection)
        premise.end_date = row[4]
        premise.save()

        premises.append(premise)

    return premises

def get_last_payment(debtor, connection):
    connect, cursor = connection

    query = Payment.get_query(debtor.debtornum)

    row = cursor.execute(query).fetchone()

    payment, created = Payment.objects.get_or_create(debtor=debtor, date_received=row[0], payment_amt=row[1], channel=row[2])

def get_last_invoice(debtor, connection):
    connect, cursor = connection

    query = Invoice.get_query(debtor.debtornum)

    row = cursor.execute(query).fetchone()

    invoice, created = Invoice.objects.get_or_create(invoice_num__exact=row[0])
    invoice.debtor = debtor
    invoice.invoice_num = row[0]
    invoice.invoice_date = row[1]
    invoice.invoice_amt = row[2]
    invoice.due_date = row[3]
    invoice.save()

def get_recent_ptjs(debtor, connection):
    connect, cursor = connection

    query = PTJ.get_query(debtor.debtornum)

    for row in cursor.execute(query).fetchall():
        try:
            ptj = PTJ.objects.get(ptj_number__exact=row[0])
        except PTJ.DoesNotExist:
            ptj = PTJ()

        try:
            premise, created = Premise.objects.get_or_create(premnum=row[5])
        except:
            premise = None

        ptj.ptj_number = row[0]
        ptj.debtor = debtor
        ptj.premise = premise
        ptj.type_code = row[1]
        ptj.class_code = row[2]
        ptj.subclass_code = row[3]
        ptj.status_code = row[4]
        ptj.date_logged = row[6]
        ptj.date_status = row[7]
        ptj.save()

def get_details(debtornum):
    connection = get_database_connection()

    try:
        debtor = Debtor.objects.get(debtornum__exact=debtornum)
        created = False
    except Debtor.DoesNotExist:
        debtor = Debtor(debtornum=debtornum)
        created = True

    if created or (datetime.now() - debtor.last_modified).days > 0:
        # been more than a day since we updated, let's update the info, or a new debtor
        #get_debtor_details(debtor, connection)
        pass

    get_debtor_details(debtor, connection)

    # get our premises for the debtor
    get_premises(debtor, connection)

    # get our invoices for the debtor
    get_last_invoice(debtor, connection)

    get_last_payment(debtor, connection)

    # and PTJs, maybe???
    #get_recent_ptjs(debtor, connection)

    close_database_connection(connection)

    return debtor
