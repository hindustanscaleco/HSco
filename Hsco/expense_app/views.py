from django.shortcuts import render

# Create your views here.

def expense_dashboard(request):
    return render(request,"expense_app/expense_dashboard.html")

def add_expense(request):
    return render(request,"expense_app/add_expense.html")

def expense_product(request):
    return render(request,"expense_app/expense_product.html")

def vendor_master(request):
    return render(request,"expense_app/vendor_master.html")

def expense_details(request):
    return render(request,'expense_app/expense_details.html')

def expense_report(request):
    return render(request,'expense_app/expense_report.html')

def expense_report_dashboard(request):
    return render(request,'expense_app/expense_report_dashboard.html')

def expense_master(request):
    return render(request,'expense_app/expense_master.html')

def expense_type_sub_master(request):
    return render(request,'expense_app/expense_type_sub_master.html')

def expense_type_sub_sub_master(request):
    return render(request,'expense_app/expense_type_sub_sub_master.html')