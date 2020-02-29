from django.shortcuts import render
from .forms import Customer_detailForm

# Create your views here.

def lead_home(request):
    return render(request,'lead_management/lead_home.html',)

def view_lead(request):
    form = Customer_detailForm()
    context={
        'form':form
    }
    return render(request, 'lead_management/view_lead.html',context)

def lead_report(request):
    return render(request,'lead_management/report_lead.html')