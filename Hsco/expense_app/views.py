from django.shortcuts import render
from .models import Expense_Type_Sub_Master, Expense_Type_Sub_Sub_Master, Vendor
from django.shortcuts import render, redirect
from user_app.models import SiteUser

# Create your views here.

def expense_dashboard(request):
    return render(request,"expense_app/expense_dashboard.html")

def add_expense(request):
    expense_masters = Expense_Type_Sub_Sub_Master.objects.all()
    context={
        'expense_masters' : expense_masters,
    }
    return render(request,"expense_app/add_expense.html", context)

def expense_product(request):
    return render(request,"expense_app/expense_product.html")

def vendor_master(request):
    if request.method == 'POST' or request.method == 'FILES' :
        expense_type_master = request.POST.get('expense_type_master')
        expense_type_sub_master = request.POST.get('expense_type_sub_master')
        expense_type_sub_sub_master = request.POST.get('expense_type_sub_sub_master')
        name = request.POST.get('name')
        phone_no = request.POST.get('phone_no')
        total_basic_amount = request.POST.get('total_basic_amount')
        pf = request.POST.get('pf')
        gst = request.POST.get('gst')
        sgst_per = request.POST.get('sgst_per')
        sgst_amt = request.POST.get('sgst_amt')
        cgst_per = request.POST.get('cgst_per')
        cgst_amt = request.POST.get('cgst_amt')
        igst_per = request.POST.get('igst_per')
        igst_amt = request.POST.get('igst_amt')
        discount_per = request.POST.get('discount_per')
        discount_amt = request.POST.get('discount_amt')
        gst_no = request.POST.get('gst_no')
        date_of_payment = request.POST.get('date_of_payment')
        total_amount = request.POST.get('total_amount')
        name_of_payee = request.POST.get('name_of_payee')
        po_issued = request.FILES.get('po_issued')
        bill_copy = request.FILES.get('bill_copy')
        voucher_no = request.POST.get('voucher_no')
        payment_type = request.POST.get('payment_type')
        
        if gst == "on":
            gst = True
        else:
            gst = False
            
        item = Vendor()

        item.user_id = SiteUser.objects.get(id=request.user.id)
        item.expense_type_sub_sub_master_id = Expense_Type_Sub_Sub_Master.objects.get(id=expense_type_sub_sub_master)
        item.name = name
        item.phone_no = phone_no
        item.total_basic_amount = total_basic_amount
        item.pf = pf
        item.gst = gst
        item.sgst_per = sgst_per
        item.sgst_amt = sgst_amt
        item.cgst_per = cgst_per
        item.cgst_amt = cgst_amt
        item.igst_per = igst_per
        item.igst_amt = igst_amt
        item.discount_per = discount_per
        item.discount_amt = discount_amt
        item.gst_no = gst_no
        if date_of_payment != None and date_of_payment != '':
            item.date_of_payment = date_of_payment
        item.total_amount = total_amount
        item.name_of_payee = name_of_payee
        item.po_issued = po_issued
        item.bill_copy = bill_copy
        item.voucher_no = voucher_no
        item.payment_type = payment_type
        item.save()
        return redirect('/expense_master/')  

    return render(request,"expense_app/vendor_master.html")

def expense_details(request):
    return render(request,'expense_app/expense_details.html')

def expense_report(request):
    return render(request,'expense_app/expense_report.html')

def expense_report_dashboard(request):
    return render(request,'expense_app/expense_report_dashboard.html')

def expense_master(request):
    expense_masters = Expense_Type_Sub_Sub_Master.objects.all()
    context={
        'expense_masters' : expense_masters,
    }
    return render(request,'expense_app/expense_master.html', context)

def expense_type_sub_master(request):
    if request.method == 'POST' or request.method == 'FILES' :
        expense_type_master = request.POST.get('expense_type_master')
        expense_type_sub_master = request.POST.get('expense_type_sub_master')
        notes = request.POST.get('notes')
        
        item = Expense_Type_Sub_Master()

        item.user_id = SiteUser.objects.get(id=request.user.id)
        item.expense_type_master = expense_type_master
        item.expense_type_sub_master = expense_type_sub_master
        item.notes = notes
        item.save()
        return redirect('/expense_master/')  

    return render(request,'expense_app/expense_type_sub_master.html')

def expense_type_sub_sub_master(request):
    sub_master = Expense_Type_Sub_Master.objects.all()
    context = {
        'sub_master': sub_master,
    }
    if request.method == 'POST' or request.method == 'FILES' :
        expense_type_sub_master = request.POST.get('expense_type_sub_master')
        expense_type_sub_sub_master = request.POST.get('expense_type_sub_sub_master')
        notes = request.POST.get('notes')
        
        item = Expense_Type_Sub_Sub_Master()

        item.user_id = SiteUser.objects.get(id=request.user.id)
        item.expense_type_sub_master_id = Expense_Type_Sub_Master.objects.get(id=expense_type_sub_master)
        item.expense_type_sub_sub_master = expense_type_sub_sub_master
        item.notes = notes
        item.save()
        return redirect('/expense_master/')  
    return render(request,'expense_app/expense_type_sub_sub_master.html', context)

def load_expense_sub_master(request):
    expense_type_master = request.GET.get('expense_type_master')

    expense_type_sub_masters = Expense_Type_Sub_Master.objects.filter(expense_type_master=expense_type_master)
    return render(request, 'AJAX_dropdowns/expense_sub_master_dropdown.html', {'expense_type_sub_masters': expense_type_sub_masters})

def load_expense_sub_sub_master(request):
    expense_type_sub_master = request.GET.get('expense_type_sub_master')

    expense_type_sub_sub_masters = Expense_Type_Sub_Sub_Master.objects.filter(expense_type_sub_master_id=expense_type_sub_master)
    return render(request, 'AJAX_dropdowns/expense_sub_sub_master_dropdown.html', {'expense_type_sub_sub_masters': expense_type_sub_sub_masters})

