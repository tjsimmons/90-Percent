from django.shortcuts import render, redirect

from utilities import get_details
from models import Debtor, Invoice, Premise, Payment

def details(request, debtornum):
    debtor = Debtor.objects.get(debtornum__exact=debtornum)
    premises = Premise.objects.filter(debtor=debtor).order_by("-start_date")
    invoice = Invoice.objects.get(debtor__exact=debtor)
    payment = Payment.objects.get(debtor__exact=debtor)

    return render(request, 'details.html', {"debtor": debtor, "premises": premises, "invoice": invoice, "payment": payment})

def home(request):
    return render(request, 'base.html')

def search(request):
    info = get_details(int(request.POST['debtornum']))

    return redirect(info)
