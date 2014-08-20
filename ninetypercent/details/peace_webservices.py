from datetime import datetime
import logging

from suds.client import Client
from suds.wsse import Security, UsernameToken
from suds import sudsobject
from suds.xsd.doctor import ImportDoctor, Import
from classes import OfferInfo
from models import Debtor, Rate, Premise, Address, BillingAddress

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
PREMISE_SERVICE = "Peace8PremiseService"
CUSTOM_SERVICE = "CustomService"
END_URL = "http://happed3.na.directenergy.corp:10127/services/{0}?wsdl"

def get_customer_details(debtornum):
    # Doctor is a SUDS class that fixes broken schemas. In this case, we need to let the client know about the Peace8.Peace.Com schema
    imp = Import('http://peace8.peace.com/')
    doctor = ImportDoctor(imp)

    debtor_client = setup_soap(CUSTOMER_DETAIL_SERVICE, doctor=doctor)
    financial_client = setup_soap(FINANCIAL_SERVICE)

    debtor_details = debtor_client.service.getCustomerDetail(debtornum)
    financial_details = financial_client.service.getAccountBalance(debtornum)

    if len(debtor_details.consumers) > 0:
        # we have at least one consumer
        consumer = debtor_details.consumers[0][0]   # of our array of consumers, get the first consumer, then the first detail object within that
    else:
        consumer = None

    debtor, created = Debtor.objects.get_or_create(debtornum=debtornum)

    # high level debtor stuff
    debtor.company_code = debtor_details.companyCode
    debtor.on_ebill = 'Y' if debtor_details.EBill == True else 'N'

    # financial stuff
    debtor.current_balance = financial_details.currentBalance
    debtor.overdue_balance = financial_details.currentOverdueBalance
    debtor.statement_due = financial_details.lastStatementDueDate
    debtor.statement_amount = financial_details.lastStatementClosingBalance

    # person specific stuff
    if consumer:
        debtor.firstname = consumer.firstName
        debtor.surname = consumer.surname
        debtor.phone_number = consumer.homePhone
        debtor.email_address = consumer.email
        debtor.aav = consumer.password

    # billing address
    bill_address, created = BillingAddress.objects.get_or_create(address_line1=debtor_details.billAddress.addressLine1.strip(), address_line2=debtor_details.billAddress.addressLine2.strip(),
        address_line3=debtor_details.billAddress.addressLine3.strip(), address_name=debtor_details.billAddress.addresseName.strip(), postal=debtor_details.billAddress.postalZone.strip())

    debtor.billing_address = bill_address

    # save the debtor changes
    debtor.save()

    # get the premise stuff now
    snippets = consumer.premiseDetails[0] # same as consumer. it's a tuple, with one part actually holding the premises

    for snippet in snippets:
        get_premise_details(debtor, snippet.premiseNumber)

    return debtor

def get_premise_details(debtor, premnum):
    custom_client = setup_soap(CUSTOM_SERVICE)
    peace_client = setup_soap(PREMISE_SERVICE)

    # get the offer details
    offer_call = custom_client.factory.create('Call')
    offer_call.methodName = 'getOfferInfo'
    offer_call.param1 = debtor.debtornum
    offer_call.param2 = premnum

    premise, created = Premise.objects.get_or_create(premnum=premnum, debtor=debtor)

    # since it's getCustomRecords, we need to loop through starting with record 1 (not 0, that's headers)
    # Results is the array object it's returned in
    # this is for Offers
    r = custom_client.service.getCustomRecords(offer_call)

    if r != "":     # apparently, getCustomRecords returns an empty string if nothing is found
        for result in r.Results[1:]:
            offer_info = OfferInfo(**sudsobject.asdict(result))

            rate, created = Rate.objects.get_or_create(offer=offer_info.offer.strip(), premise=premise)

            rate.rate = offer_info.price

            if offer_info.start_date:
                rate.effective_from = datetime.strptime(offer_info.start_date, "%m/%d/%y")

            if offer_info.end_date:
                rate.effective_to = datetime.strptime(offer_info.end_date, "%m/%d/%y")

            rate.save()

    # now the Premise info
    soap_premise = peace_client.service.getPremiseByPremiseNumber(premnum)

    premise.save()

def setup_soap(service, doctor=None):
    #logging.basicConfig(level=logging.INFO)
    #logging.getLogger('suds.client').setLevel(logging.DEBUG)

    client = Client(END_URL.format(service), doctor=doctor)

    security = Security()
    token = UsernameToken('oamuser', 'oam_tpc8')
    security.tokens.append(token)

    client.set_options(wsse=security)

    return client

def call_soap(debtornum):
    debtor = get_customer_details(debtornum)

    return debtor
    # premise service
    """premise = peace_client.factory.create('ns2:Premise')

    premise = peace_client.service.getPremiseByPremiseNumber("5791")

    #print premise

    address_info = AddressInfo(**sudsobject.asdict(premise))

    address = Address(street_name=address_info.streetDescription.strip(), street_number=address_info.houseNumber.strip(),
        city=address_info.townDescription.strip(), postal=address_info.postalZone.strip(), state="TX")

    print address.street_name"""

    """custom_call = custom_client.factory.create('Call')
    custom_call.methodName = 'getOfferInfo'
    custom_call.param1 = '653498899'
    custom_call.param2 = 5791

    r = custom_client.service.getCustomRecords(custom_call)

    for result in r.Results[1:]:
        abc = sudsobject.asdict(result)

        offr = OfferInfo(**abc)

        #print offr.end_date"""
