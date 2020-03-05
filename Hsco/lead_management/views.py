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

def lead_manager_view(request):
    return render(request,'lead_management/lead_manager.html')

def lead_follow_up_histroy(request):
    return render(request,'lead_management/lead_history.html')

def lead_delete_product(request):
    return render(request,'lead_management/lead_delete_product.html')

def lead_analytics(request):
    return render(request,'lead_management/analytics.html')

def lead_employee_graph(request):
    return render(request,'lead_management/lead_employee_graph.html')