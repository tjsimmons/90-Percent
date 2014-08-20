from django.shortcuts import render, redirect

from models import Debtor, Premise

from peace_webservices import call_soap

def details(request, debtornum):
    debtor = Debtor.objects.get(debtornum=debtornum)
    premises = Premise.objects.filter(debtor=debtor).order_by("-start_date")

    return render(request, 'details.html', {"debtor": debtor, "premises": premises})

def home(request):
    return render(request, 'base.html')

def search(request):
    debtor = call_soap(int(request.POST['debtornum']))

    return redirect(debtor)
