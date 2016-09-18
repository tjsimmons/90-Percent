from datetime import datetime, date, timedelta
import logging

from suds.client import Client
from suds.wsse import Security, UsernameToken
from suds import sudsobject
from suds.xsd.doctor import ImportDoctor, Import
from classes import OfferInfo
from models import Debtor, Rate, Premise, Address, BillingAddress, Reading

"""
And now, a programming note.
** expands dictionary objects (e.g., {"key": "value", "foo": bar"}) into named parameters when expanded into a method
So, baz(**dict) becomes baz(key=value, foo=bar)
It's kinda handy.

When defining a method, bar(*args, **kwargs)
*args will take any number of arguments
**kwargs will take any number of named arguments

So, the two paragraphs above work in conjunction to create nice, generic methods
"""

FINANCIAL_SERVICE = "FinancialService"
CUSTOMER_DETAIL_SERVICE = "CustomerDetailService"
PREMISE_SERVICE = ""
READING_SERVICE = "UtilityUsageService"
CUSTOM_SERVICE = "CustomService"
END_URL = ""

def get_customer_details(debtornum):
    debtor, created = Debtor.objects.get_or_create(debtornum=debtornum)

    if debtor.last_modified < datetime.now() - timedelta(days=1) or created or not debtor.retrieved:
        print "Calling webservices -", str(datetime.now())
        # Doctor is a SUDS class that fixes broken schemas. In this case, we need to let the client know about the Peace8.Peace.Com schema
        imp = Import('http://peace8.peace.com/')
        doctor = ImportDoctor(imp)
        debtor_client = setup_soap(CUSTOMER_DETAIL_SERVICE, doctor=doctor)
        financial_client = setup_soap(FINANCIAL_SERVICE)

        print 'Getting debtor details -', str(datetime.now())
        debtor_details = debtor_client.service.getCustomerDetail(debtornum)

        print 'Getting financial details -', str(datetime.now())
        financial_details = financial_client.service.getAccountBalance(debtornum)

        if len(debtor_details.consumers) > 0:
            # we have at least one consumer
            consumer = debtor_details.consumers[0][0]   # of our array of consumers, get the first consumer, then the first detail object within that
        else:
            consumer = None

        # high level debtor stuff
        debtor.company_code = debtor_details.companyCode
        debtor.on_ebill = 'Y' if debtor_details.EBill == True else 'N'

        # financial stuff
        debtor.current_balance = financial_details.currentBalance
        debtor.overdue_balance = financial_details.currentOverdueBalance
        debtor.statement_due = financial_details.lastStatementDueDate
        debtor.statement_amount = financial_details.lastStatementClosingBalance

        if debtor.overdue_balance > 0:
            debtor.past_due = True
        else:
            debtor.past_due = False

        # person specific stuff
        if consumer:
            debtor.firstname = consumer.firstName
            debtor.surname = consumer.surname
            debtor.phone_number = consumer.homePhone
            debtor.email_address = consumer.email
            debtor.aav = consumer.password
            debtor.critical_care = True if consumer.criticalCare == "Y" or consumer.life_support == "Y" else False

        # billing address
        bill_address, created = BillingAddress.objects.get_or_create(address_line1=debtor_details.billAddress.addressLine1.strip(), address_line2=debtor_details.billAddress.addressLine2.strip(),
            address_line3=debtor_details.billAddress.addressLine3.strip(), address_name=debtor_details.billAddress.addresseName.strip(), postal=debtor_details.billAddress.postalZone.strip())

        debtor.billing_address = bill_address

        # get the premise stuff now
        snippets = consumer.premiseDetails[0] # same as consumer. it's a tuple, with one part actually holding the premises

        for snippet in snippets:
            get_premise_details(debtor, snippet.premiseNumber, snippet.status)

        # save the debtor changes
        debtor.retrieved = True

        debtor.save()

    print 'Finished -', str(datetime.now())

    return debtor

def get_premise_details(debtor, premnum, status):
    print 'Getting premise details for', premnum, str(datetime.now())
    custom_client = setup_soap(CUSTOM_SERVICE)
    premise_client = setup_soap(PREMISE_SERVICE)
    reading_client = setup_soap(READING_SERVICE)

    # create a list of rates so we can sort, and add the latest to the premise
    rates = []

    # get the offer details
    offer_call = custom_client.factory.create('Call')
    offer_call.methodName = 'getOfferInfo'
    offer_call.param1 = debtor.debtornum
    offer_call.param2 = premnum

    premise, created = Premise.objects.get_or_create(premnum=premnum, debtor=debtor)

    # since it's getCustomRecords, we need to loop through starting with record 1 (not 0, that's headers)
    # Results is the array object it's returned in
    # this is for Offers
    print 'Getting offer info for premise -', str(datetime.now())
    r = custom_client.service.getCustomRecords(offer_call)

    if r != "":     # apparently, getCustomRecords returns an empty string if nothing is found
        for result in r.Results[1:]:
            offer_info = OfferInfo(**sudsobject.asdict(result))

            rate, created = Rate.objects.get_or_create(offer=offer_info.offer.strip())

            rate.rate = offer_info.price

            if offer_info.start_date:
                rate.effective_from = datetime.strptime(offer_info.start_date, "%m/%d/%y")

            if offer_info.end_date:
                rate.effective_to = datetime.strptime(offer_info.end_date, "%m/%d/%y")

            rates.append(rate)

    # get the latest rate
    rates = sorted(rates, key=lambda x: x.effective_from, reverse=True)
    latest_rate = None

    if len(rates) > 0:
        rates[0].save() # just save the latest
        latest_rate = rates[0]

    # now get the latest reading.
    # since i can't find a field in any service to give me last read date
    # we're going to get every reading for the premise, from 1-1-2012 through today
    # then just take the latest. If it's slow, I'll have to rethink
    print 'Getting readings for premise -', str(datetime.now())
    soap_readings = reading_client.service.getReadingForPremise(premnum, datetime(2012, 01, 01).isoformat(), datetime.now().isoformat())
    readings = []

    print 'Finding latest reading -', str(datetime.now())
    if soap_readings.totalNumOfRecordsFound > 0:
        for service_object in soap_readings.readingForPremise.services:    # this object is a nightmare. just go with me on it.
            for service_detail in service_object[1]:
                for service in service_detail[1]:
                    if service.serviceNumber == 1:
                        for reading_details in service.readings:
                            for reading_detail in reading_details[1]:
                                for reading_object in reading_detail[1]:
                                    reading = Reading(reading=reading_object.reading, read_date=reading_object.readDate, read_method=reading_object.readMethod)

                                    readings.append(reading)

    readings = sorted(readings, key=lambda x:x.read_date, reverse=True)
    latest_reading = None

    if len(readings) > 0:
        readings[0].save()  # only save our latest one
        latest_reading = readings[0]

    # now the Premise info
    print 'Getting premise info -', str(datetime.now())
    soap_premise = premise_client.service.getPremiseByPremiseNumber(premnum)

    premise_address, created = Address.objects.get_or_create(street_name=soap_premise.streetDescription.strip(), street_number=soap_premise.houseNumber.strip(),
        city=soap_premise.townDescription.strip(), state="TX", postal=soap_premise.postalZone.strip())

    premise.address = premise_address
    premise.esiid = None    # add later
    premise.start_date = date(1900, 1, 1)
    premise.end_date = date(2099, 12, 31)
    premise.status = status
    premise.reading = latest_reading
    premise.rate = latest_rate

    premise.save()

def setup_soap(service, doctor=None):
    #logging.basicConfig(level=logging.INFO)
    #logging.getLogger('suds.client').setLevel(logging.DEBUG)

    client = Client(END_URL.format(service), doctor=doctor)

    security = Security()
    token = UsernameToken('foo', 'bar')
    security.tokens.append(token)

    client.set_options(wsse=security)

    return client

def call_soap(debtornum):
    debtor = get_customer_details(debtornum)

    return debtor
