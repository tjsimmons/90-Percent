from suds.client import Client
from suds.wsse import Security, UsernameToken
from suds import sudsobject
from classes import PaymentInfo, BillInfo, AccountInfo, OfferInfo, AddressInfo
from models import Address

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

def call_soap():
    end_url = "http://happed3.na.directenergy.corp:10127/services/{0}?wsdl"

    financial_service = "FinancialService"
    premise_service = "Peace8PremiseService"
    custom_service = "CustomService"

    peace_client = Client(end_url.format(premise_service))
    custom_client = Client(end_url.format(custom_service))

    security = Security()
    token = UsernameToken('oamuser', 'oam_tpc8')
    security.tokens.append(token)

    peace_client.set_options(wsse=security)
    custom_client.set_options(wsse=security)

    premise = peace_client.factory.create('ns2:Premise')

    premise = peace_client.service.getPremiseByPremiseNumber("5791")

    #print premise

    address_info = AddressInfo(**sudsobject.asdict(premise))

    address = Address(street_name=address_info.streetDescription.strip(), street_number=address_info.houseNumber.strip(),
        city=address_info.townDescription.strip(), postal=address_info.postalZone.strip(), state="TX")

    print address.street_name

    """custom_call = custom_client.factory.create('Call')
    custom_call.methodName = 'getOfferInfo'
    custom_call.param1 = '653498899'
    custom_call.param2 = 5791

    r = custom_client.service.getCustomRecords(custom_call)

    for result in r.Results[1:]:
        abc = sudsobject.asdict(result)

        offr = OfferInfo(**abc)

        #print offr.end_date"""

call_soap()
