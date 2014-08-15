from suds.client import Client
from suds.wsse import Security, UsernameToken
from suds import sudsobject
from classes import PaymentInfo, BillInfo, AccountInfo, OfferInfo


def call_soap():
    end_url = "http://happed3.na.directenergy.corp:10127/services/{0}?wsdl"

    premise_service = "Peace8PremiseService"
    custom_service = "CustomService"

    client = Client(end_url.format(custom_service), username='oamuser', password='oam_tpc8')

    security = Security()
    token = UsernameToken('oamuser', 'oam_tpc8')
    security.tokens.append(token)
    client.set_options(wsse=security)

    print client

    call = client.factory.create('Call')
    #premise = client.factory.create('ns2:Premise')

    #premise = client.service.getPremiseByPremiseNumber("5791")

    #print premise
    call.methodName = 'getOfferInfo'
    call.param1 = '653498899'
    call.param2 = 5791

    r = client.service.getCustomRecords(call)

    for result in r.Results[1:]:
        abc = sudsobject.asdict(result)

        offr = OfferInfo(**abc)

        print offr.end_date

call_soap()
