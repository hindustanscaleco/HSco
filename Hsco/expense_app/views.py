import io

from django.core.files.base import ContentFile
from django.shortcuts import render
from django.template.loader import get_template

from .models import Expense_Type_Sub_Master, Expense_Type_Sub_Sub_Master, Vendor, Expense, Expense_Product , Bill
from django.shortcuts import render, redirect
from user_app.models import SiteUser
from django.http import HttpResponse, JsonResponse
from customer_app.models import type_purchase,main_model,sub_model,sub_sub_model
from stock_management_system_app.models import Godown, Product
from purchase_app.views import check_admin_roles
from django.db.models import Q, F, Min, Avg
from django.contrib import messages
from lead_management.models import Pi_section
from purchase_app.models import Purchase_Details,Product_Details
from .utils import render_to_pdf
from datetime import datetime
# Create your views here.
today_month = datetime.now().month


def expense_dashboard(request):
    if check_admin_roles(request):  # For ADMIN
        expense_list = Expense.objects.filter(Q(user_id__name=request.user.name)|Q(user_id__group__icontains=request.user.name),
                        user_id__is_deleted=False, entry_date__month=today_month).order_by('-id')
            
    else:  # For EMPLOYEE
        expense_list = Expense.objects.filter(user_id=request.user.pk, entry_date__month=today_month).order_by('-id')
            
    #filter by company type (sales or scales)
    if request.method == 'GET' and 'company_type' in request.GET:
        company_type = request.GET.get('company_type')

        if check_admin_roles(request):  # For ADMIN
            expense_list = Expense.objects.filter(Q(user_id__name=request.user.name)|Q(user_id__group__icontains=request.user.name),
                                                        user_id__is_deleted=False,our_company_name__icontains=company_type).order_by('-id')

        else:  # For EMPLOYEE
            expense_list = Expense.objects.filter(user_id=request.user.pk,our_company_name__icontains=company_type).order_by('-id')

        context = {
            'expense_list':expense_list,
        }
        return render(request,"expense_app/load_expense_company_type.html", {'expense_list':expense_list,})

    # search by options
    if request.method == 'POST' :
        if'submit1' in request.POST:
            start_date = request.POST.get('date1')
            end_date = request.POST.get('date2')
            if check_admin_roles(request):  # For ADMIN
                expense_list = Expense.objects.filter(Q(user_id__name=request.user.name)|Q(user_id__group__icontains=request.user.name),
                                                            user_id__is_deleted=False,entry_date__range=[start_date, end_date]).order_by('-id')

            else:  # For EMPLOYEE
                expense_list = Expense.objects.filter(user_id=request.user.pk,entry_date__range=[start_date, end_date]).order_by('-id')

            context = {
                'expense_list': expense_list,
                'search_msg': 'Search result for date range: '+start_date+' TO '+end_date,
            }
            return render(request, 'expense_app/expense_dashboard.html', context)
        elif 'submit2' in request.POST:
            contact = request.POST.get('contact')
            if check_admin_roles(request):  # For ADMIN
                expense_list = Expense.objects.filter(Q(user_id__name=request.user.name)|Q(user_id__group__icontains=request.user.name),
                                                            user_id__is_deleted=False,vendor__phone_no__icontains=contact).order_by('-id')

            else:  # For EMPLOYEE
                expense_list = Expense.objects.filter(user_id=request.user.pk,vendor__phone_no__icontains=contact).order_by('-id')

            context = {
                'expense_list': expense_list,
                'search_msg': 'Search result for Vendor Contact No: ' + contact,
            }
            return render(request, 'expense_app/expense_dashboard.html', context)

        elif 'submit3' in request.POST:
            email = request.POST.get('email')

            if check_admin_roles(request):  # For ADMIN
                expense_list = Expense.objects.filter(Q(user_id__name=request.user.name)|Q(user_id__group__icontains=request.user.name),
                                                            user_id__is_deleted=False,vendor__email_id__icontains=email).order_by('-id')

            else:  # For EMPLOYEE
                expense_list = Expense.objects.filter(user_id=request.user.pk,vendor__email_id__icontains=email).order_by('-id')

            context = {
                'expense_list': expense_list,
                'search_msg': 'Search result for Vendor Email ID: ' + email,
            }
            return render(request, 'expense_app/expense_dashboard.html', context)
        elif 'submit4' in request.POST:
            name = request.POST.get('name')
            
            if check_admin_roles(request):  # For ADMIN
                expense_list = Expense.objects.filter(Q(user_id__name=request.user.name)|Q(user_id__group__icontains=request.user.name),
                                                            user_id__is_deleted=False,vendor__name__icontains=name).order_by('-id')

            else:  # For EMPLOYEE
                expense_list = Expense.objects.filter(user_id=request.user.pk,vendor__name__icontains=name).order_by('-id')

            context = {
                'expense_list': expense_list,
                'search_msg': 'Search result for Vendor Name: ' +name,
            }
            return render(request, 'expense_app/expense_dashboard.html', context)

        elif  'submit5' in request.POST:
            company = request.POST.get('company')
            
            if check_admin_roles(request):  # For ADMIN
                expense_list = Expense.objects.filter(Q(user_id__name=request.user.name)|Q(user_id__group__icontains=request.user.name),
                                                            user_id__is_deleted=False,vendor__company_name__icontains=company).order_by('-id')

            else:  # For EMPLOYEE
                expense_list = Expense.objects.filter(user_id=request.user.pk,vendor__company_name__icontains=company).order_by('-id')

            context = {
                'expense_list': expense_list,
                'search_msg': 'Search result for Company Name: ' + company,
            }
            return render(request, 'expense_app/expense_dashboard.html', context)
        elif request.method=='POST' and 'submit6' in request.POST:
            id = request.POST.get('id')
            if check_admin_roles(request):  # For ADMIN
                expense_list = Expense.objects.filter(Q(user_id__name=request.user.name)|Q(user_id__group__icontains=request.user.name),
                                                            user_id__is_deleted=False,id=id).order_by('-id')

            else:  # For EMPLOYEE
                expense_list = Expense.objects.filter(user_id=request.user.pk,id=id).order_by('-id')

            context = {
                'expense_list': expense_list,
                'search_msg': 'Search result for Expense ID. : ' + str(id),
            }
            return render(request, 'expense_app/expense_dashboard.html', context)
        
    context={
        'expense_list': expense_list,
    }
    return render(request,"expense_app/expense_dashboard.html", context)

def add_expense(request):
    expense_masters = Expense_Type_Sub_Sub_Master.objects.all()
    context={
        'expense_masters' : expense_masters,
    }
    # get vendor list according to expense sub sub master
    if request.method == 'GET' and 'expense_type_sub_sub_master' in request.GET:
        expense_type_sub_sub_master_id = request.GET.get('expense_type_sub_sub_master')
        vendors_list = Vendor.objects.filter(expense_type_sub_sub_master_id=expense_type_sub_sub_master_id)
        context={
            'vendors_list' : vendors_list,
            'expense_masters' : expense_masters,
        }
        context.update(context)
        return render(request, 'expense_app/load_vendor_list_expense.html', context)
    if request.method == 'POST' or request.method == 'FILES' :
        expense_type_master = request.POST.get('expense_type_master')
        expense_type_sub_master = request.POST.get('expense_type_sub_master')
        expense_type_sub_sub_master = request.POST.get('expense_type_sub_sub_master')
        name = request.POST.get('name')
        notes = request.POST.get('notes')
        our_company_name = request.POST.get('our_company_name')
        bill_no = request.POST.get('bill_no')
        bill_date = request.POST.get('bill_date')
        total_basic_amount = request.POST.get('total_basic_amount')
        pf = request.POST.get('pf')
        gst = request.POST.get('gst')

        sgst_per = request.POST.get('sgst_per')
        cgst_per = request.POST.get('cgst_per')
        igst_per = request.POST.get('igst_per')
        tds_per = request.POST.get('tds_per')
        discount_per = request.POST.get('discount_per')
        sgst_amt = request.POST.get('sgst_amt')
        cgst_amt = request.POST.get('cgst_amt')
        igst_amt = request.POST.get('igst_amt')
        tds_amt = request.POST.get('tds_amt')
        discount_amt = request.POST.get('discount_amt')

        total_amount = request.POST.get('total_amount')
        gst_no = request.POST.get('gst_no')
        date_of_payment = request.POST.get('date_of_payment')
        name_of_payee = request.POST.get('name_of_payee')
        po_issued = request.FILES.get('po_issued')
        bill_copy = request.FILES.get('bill_copy')
        voucher_no = request.POST.get('voucher_no')
        
        #bank details
        payment_type = request.POST.get('payment_type')
        bank_name = request.POST.get('bank_name')
        cheque_no = request.POST.get('cheque_no')
        cheque_date = request.POST.get('cheque_date')

        neft_bank_name = request.POST.get('neft_bank_name')
        neft_date = request.POST.get('neft_date')
        reference_no = request.POST.get('reference_no')

        credit_pending_amount = request.POST.get('credit_pending_amount')
        credit_authorised_by = request.POST.get('credit_authorised_by')

        if gst == "on":
            gst = True
        else:
            gst = False

        item = Expense()

        item.user_id = SiteUser.objects.get(id=request.user.id)
        item.log_entered_by = request.user.name
        item.expense_type_sub_sub_master_id = Expense_Type_Sub_Sub_Master.objects.get(id=expense_type_sub_sub_master)
        item.vendor  = Vendor.objects.get(id=name)
        item.notes  = notes 
        item.our_company_name  = our_company_name 
        item.bill_no  = bill_no
        if bill_date != None and bill_date != '':
            item.bill_date  = bill_date 
        item.total_basic_amount  = total_basic_amount 
        item.pf  = pf 
        item.gst  = gst 
        item.sgst_per  = sgst_per 
        item.cgst_per  = cgst_per 
        item.igst_per  = igst_per 
        item.tds_per  = tds_per 
        item.discount_per  = discount_per 
        item.sgst_amt  = sgst_amt 
        item.cgst_amt  = cgst_amt 
        item.igst_amt  = igst_amt 
        item.tds_amt  = tds_amt 
        item.discount_amt  = discount_amt 
        item.total_amount  = total_amount 
        item.gst_no  = gst_no 
        if date_of_payment != None and date_of_payment != '':
            item.date_of_payment  = date_of_payment 
        item.name_of_payee   = name_of_payee  
        if po_issued != None and po_issued != '':
            item.po_issued   = po_issued 
        if bill_copy != None and bill_copy != '':
            item.bill_copy   = bill_copy  
        item.voucher_no   = voucher_no  
        item.payment_type   = payment_type  

        item.cheque_no = cheque_no
        item.bank_name = bank_name
        if cheque_date != None and cheque_date != '':
            item.cheque_date = cheque_date

        item.neft_bank_name = neft_bank_name
        item.reference_no = reference_no
        if neft_date != None and neft_date != '':
            item.neft_date = neft_date

        if credit_pending_amount != '':
            item.credit_pending_amount = float(credit_pending_amount)
        item.credit_authorised_by = credit_authorised_by

        item.save()
        if expense_type_master == 'Purchase of Goods':
            return redirect('/expense_product/'+str(item.pk))
        else :  
            return redirect('/expense_dashboard/' )

    
    return render(request,"expense_app/add_expense.html", context)

def expense_product(request, expense_id):
    type_of_purchase_list =type_purchase.objects.all() #1
    if request.user.role == 'Super Admin':
        godowns = Godown.objects.filter(default_godown_purchase=False)

    elif request.user.role == 'Admin':
        godowns = Godown.objects.filter(Q(default_godown_purchase=False)&Q(godown_admin__id = request.user.id ))

    elif request.user.role == 'Manager':
        godowns = Godown.objects.filter(Q(default_godown_purchase=False)&Q(godown_admin__profile_name = request.user.admin))

    else:
        godowns = Godown.objects.filter(Q(default_godown_purchase=False)&Q(godown_admin__profile_name = request.user.admin))

    if request.method == 'POST':
        quantity = float(request.POST.get('quantity'))
        expense_type = request.POST.get('expense_type')
        model_of_purchase = request.POST.get('model_of_purchase')
        type_of_scale = request.POST.get('type_of_scale')
        sub_model = request.POST.get('sub_model')
        sub_sub_model = request.POST.get('sub_sub_model')
        serial_no = request.POST.get('serial_no')
        brand = request.POST.get('brand')
        capacity = request.POST.get('capacity')
        unit = request.POST.get('unit')
        amount = request.POST.get('amount')
        rate = request.POST.get('rate')
        is_last_product_yes = request.POST.get('is_last_product_yes')
        godown = request.POST.get('godown')

        if amount == '' or amount == None:
            amount=0.0

        
        item = Expense_Product()

        item.user_id = SiteUser.objects.get(id=request.user.id)
        item.expense_id = Expense.objects.get(id=expense_id)
        item.godown_id = Godown.objects.get(id=godown)

        item.expense_type = expense_type

        item.type_of_scale = type_of_scale
        item.model_of_purchase = model_of_purchase
        item.sub_model = sub_model
        item.sub_sub_model = sub_sub_model
        item.serial_no = serial_no
        item.brand = brand
        item.capacity = capacity
        item.unit = unit
        item.amount = amount            
        item.rate = rate 
        item.quantity = quantity
        item.log_entered_by = request.user.name

        item.save()

        if is_last_product_yes == 'Yes':
            return redirect('/expense_dashboard/' )
        elif is_last_product_yes == 'No':
            return redirect('/expense_product/'+str(expense_id))  
        
    context={
            'type_purchase':type_of_purchase_list,
            'godowns':godowns,
        }         
    return render(request,"expense_app/expense_product.html",context)

def update_expense_product(request, expense_id, product_id):
    expense_product = Expense_Product.objects.get(id=product_id)
    type_of_purchase_list =type_purchase.objects.all() #1
    if request.user.role == 'Super Admin':
        godowns = Godown.objects.filter(default_godown_purchase=False)

    elif request.user.role == 'Admin':
        godowns = Godown.objects.filter(Q(default_godown_purchase=False)&Q(godown_admin__id = request.user.id ))

    elif request.user.role == 'Manager':
        godowns = Godown.objects.filter(Q(default_godown_purchase=False)&Q(godown_admin__profile_name = request.user.admin))

    else:
        godowns = Godown.objects.filter(Q(default_godown_purchase=False)&Q(godown_admin__profile_name = request.user.admin))

    if request.method == 'POST':
        if 'delete' in request.POST:
            Expense_Product.objects.get(id=product_id).delete()
            messages.success(request, 'Expense Product with ID:-'+str(product_id)+' deleted successfully!')
            return redirect('/expense_details/'+str(expense_id))
        quantity = float(request.POST.get('quantity'))
        expense_type = request.POST.get('expense_type')
        model_of_purchase = request.POST.get('model_of_purchase')
        type_of_scale = request.POST.get('type_of_scale')
        sub_model = request.POST.get('sub_model')
        sub_sub_model = request.POST.get('sub_sub_model')
        serial_no = request.POST.get('serial_no')
        brand = request.POST.get('brand')
        capacity = request.POST.get('capacity')
        unit = request.POST.get('unit')
        amount = request.POST.get('amount')
        rate = request.POST.get('rate')
        is_last_product_yes = request.POST.get('is_last_product_yes')
        godown = request.POST.get('godown')

        if amount == '' or amount == None:
            amount=0.0

        item = Expense_Product.objects.get(id=product_id)

        item.user_id = SiteUser.objects.get(id=request.user.id)
        item.expense_id = Expense.objects.get(id=expense_id)
        item.godown_id = Godown.objects.get(id=godown)

        item.expense_type = expense_type
        if type_of_scale != 'None' and type_of_scale != '':
            item.type_of_scale = type_of_scale
        if model_of_purchase != 'None' and model_of_purchase != '':
            item.model_of_purchase = model_of_purchase
        if sub_model != 'None' and sub_model != '':
            item.sub_model = sub_model
        if sub_sub_model != 'None' and sub_sub_model != '':
            item.sub_sub_model = sub_sub_model
        item.serial_no = serial_no
        item.brand = brand
        item.capacity = capacity
        item.unit = unit
        item.amount = amount            
        item.rate = rate 
        item.quantity = quantity
        item.log_entered_by = request.user.name

        item.save(update_fields=['type_of_scale','model_of_purchase','sub_model','sub_sub_model','serial_no','brand','capacity','unit','amount','rate','quantity','log_entered_by','expense_type','godown_id'])  

        return redirect('/expense_details/'+str(expense_id))  
        
    context={
            'type_purchase':type_of_purchase_list,
            'godowns':godowns,
            'expense_product':expense_product,
        }         
    return render(request,"expense_app/update_expense_product.html",context)


def vendor_master(request):
    if request.method == 'POST' or request.method == 'FILES' :
        expense_type_master = request.POST.get('expense_type_master')
        expense_type_sub_master = request.POST.get('expense_type_sub_master')
        expense_type_sub_sub_master = request.POST.get('expense_type_sub_sub_master')

        name = request.POST.get('name')
        phone_no = request.POST.get('phone_no')
        company_name = request.POST.get('company_name')
        detailed_address = request.POST.get('detailed_address')
        email_id = request.POST.get('email_id')
        hsn_code = request.POST.get('hsn_code')

        gst_no = request.POST.get('gst_no')
        sgst_per = request.POST.get('sgst_per')
        cgst_per = request.POST.get('cgst_per')
        igst_per = request.POST.get('igst_per')
        tds_per = request.POST.get('tds_per')
        notes = request.POST.get('notes')
            
        item = Vendor()

        item.user_id = SiteUser.objects.get(id=request.user.id)
        item.log_entered_by = request.user.name
        item.expense_type_sub_sub_master_id = Expense_Type_Sub_Sub_Master.objects.get(id=expense_type_sub_sub_master)
        item.name = name
        item.phone_no = phone_no
        item.company_name = company_name
        item.detailed_address = detailed_address
        item.email_id = email_id
        item.gst_no = gst_no
        item.sgst_per = sgst_per
        item.cgst_per = cgst_per
        item.igst_per = igst_per
        item.tds_per = tds_per
        item.hsn_code = hsn_code
        item.notes = notes

        item.save()
        return redirect('/expense_dashboard/')  

    return render(request,"expense_app/vendor_master.html")

def expense_details(request, expense_id):
    expense = Expense.objects.get(id=expense_id)
    vendors_list = Vendor.objects.all()
    expense_products = Expense_Product.objects.filter(expense_id=expense_id)
    # get vendor list according to expense sub sub master
    if request.method == 'GET' and 'expense_type_sub_sub_master' in request.GET:
        expense_type_sub_sub_master_id = request.GET.get('expense_type_sub_sub_master')
        vendors_list = Vendor.objects.filter(expense_type_sub_sub_master_id=expense_type_sub_sub_master_id)
        print('venodr list')
        print(vendors_list)
        print('jlkdfsklj')
        context={
            'vendors_list' : vendors_list,
            'expense_masters' : expense_masters,
        }
        context.update(context)
        return render(request, 'expense_app/load_vendor_list_expense.html', context)
    if request.method == 'POST' or request.method == 'FILES' :
        if 'delete' in request.POST:
            Expense.objects.get(id=expense_id).delete()
            messages.success(request, 'Expense with ID:-'+str(expense_id)+' deleted successfully!')
            return redirect('/expense_dashboard/')
        expense_type_master = request.POST.get('expense_type_master')
        expense_type_sub_master = request.POST.get('expense_type_sub_master')
        expense_type_sub_sub_master = request.POST.get('expense_type_sub_sub_master')
        name = request.POST.get('name')
        notes = request.POST.get('notes')
        our_company_name = request.POST.get('our_company_name')
        bill_no = request.POST.get('bill_no')
        bill_date = request.POST.get('bill_date')
        total_basic_amount = request.POST.get('total_basic_amount')
        pf = request.POST.get('pf')
        gst = request.POST.get('gst')

        sgst_per = request.POST.get('sgst_per')
        cgst_per = request.POST.get('cgst_per')
        igst_per = request.POST.get('igst_per')
        tds_per = request.POST.get('tds_per')
        discount_per = request.POST.get('discount_per')
        sgst_amt = request.POST.get('sgst_amt')
        cgst_amt = request.POST.get('cgst_amt')
        igst_amt = request.POST.get('igst_amt')
        tds_amt = request.POST.get('tds_amt')
        discount_amt = request.POST.get('discount_amt')

        total_amount = request.POST.get('total_amount')
        gst_no = request.POST.get('gst_no')
        date_of_payment = request.POST.get('date_of_payment')
        name_of_payee = request.POST.get('name_of_payee')
        po_issued = request.FILES.get('po_issued')
        bill_copy = request.FILES.get('bill_copy')
        voucher_no = request.POST.get('voucher_no')
        
        #bank details
        payment_type = request.POST.get('payment_type')
        bank_name = request.POST.get('bank_name')
        cheque_no = request.POST.get('cheque_no')
        cheque_date = request.POST.get('cheque_date')

        neft_bank_name = request.POST.get('neft_bank_name')
        neft_date = request.POST.get('neft_date')
        reference_no = request.POST.get('reference_no')

        credit_pending_amount = request.POST.get('credit_pending_amount')
        credit_authorised_by = request.POST.get('credit_authorised_by')

        if gst == "on":
            gst = True
        else:
            gst = False

        item = Expense.objects.get(id=expense_id)

        item.user_id = SiteUser.objects.get(id=request.user.id)
        item.log_entered_by = request.user.name
        item.expense_type_sub_sub_master_id = Expense_Type_Sub_Sub_Master.objects.get(id=expense_type_sub_sub_master)
        item.vendor  = Vendor.objects.get(id=name)
        item.notes  = notes 
        item.our_company_name  = our_company_name 
        item.bill_no  = bill_no
        if bill_date != None and bill_date != '':
            item.bill_date  = bill_date 
        item.total_basic_amount  = total_basic_amount 
        item.pf  = pf 
        item.gst  = gst 
        item.sgst_per  = sgst_per 
        item.cgst_per  = cgst_per 
        item.igst_per  = igst_per 
        item.tds_per  = tds_per 
        item.discount_per  = discount_per 
        item.sgst_amt  = sgst_amt 
        item.cgst_amt  = cgst_amt 
        item.igst_amt  = igst_amt 
        item.tds_amt  = tds_amt 
        item.discount_amt  = discount_amt 
        item.total_amount  = total_amount 
        item.gst_no  = gst_no 
        if date_of_payment != None and date_of_payment != '':
            item.date_of_payment  = date_of_payment 
        item.name_of_payee   = name_of_payee  
        if po_issued != None and po_issued != '':
            item.po_issued   = po_issued 
        if bill_copy != None and bill_copy != '':
            item.bill_copy   = bill_copy  
        item.voucher_no   = voucher_no  
        item.payment_type   = payment_type  

        item.cheque_no = cheque_no
        if cheque_date != None and cheque_date != '':
            item.cheque_date = cheque_date

        item.neft_bank_name = neft_bank_name
        item.reference_no = reference_no
        if neft_date != None and neft_date != '':
            item.neft_date = neft_date

        if credit_pending_amount != '' and credit_pending_amount != 'None' and credit_pending_amount != None:
            item.credit_pending_amount = float(credit_pending_amount)
        item.credit_authorised_by = credit_authorised_by

        item.save(update_fields=['expense_type_sub_sub_master_id','vendor','notes','our_company_name','bill_no','bill_date',
        'total_basic_amount','pf','gst','sgst_per','cgst_per','igst_per','tds_per','discount_per','sgst_amt','cgst_amt',
        'igst_amt','tds_amt','discount_amt','total_amount','gst_no','date_of_payment','name_of_payee','po_issued','bill_copy',
        'voucher_no','payment_type','bank_name','cheque_no','cheque_date','neft_bank_name','neft_date',
        'reference_no','credit_pending_amount','credit_authorised_by','log_entered_by',])

        return redirect('/expense_dashboard/')  

    context={
        'expense' : expense,
        'expense_products' : expense_products,
        'vendors_list' : vendors_list,
    }
    return render(request,'expense_app/expense_details.html',context)

def expense_report(request):
    if request.method =='POST':
        selected_expense_list = request.POST.getlist('expense[]')
        selected_product_list = request.POST.getlist('expense_product[]')

        start_date = request.POST.get('date1')
        end_date = request.POST.get('date2')

        string_expense = ','.join(selected_expense_list)
        string_product = ','.join(selected_product_list)

        request.session['start_date'] = start_date
        request.session['end_date'] = end_date
        request.session['selected_expense_list'] = selected_expense_list
        request.session['selected_product_list'] = selected_product_list
        request.session['string_expense'] = string_expense
        request.session['string_product'] = string_product
        return redirect('/final_expense_report/')
    return render(request,'expense_app/expense_report.html')

def final_expense_report(request):
    start_date = request.session.get('start_date')
    end_date = request.session.get('end_date')

    selected_expense_list = ['id'] + request.session.get('selected_expense_list')    
    selected_product_list = request.session.get('selected_product_list')    
    string_expense = request.session.get('string_expense')    
    string_product = request.session.get('string_product')    
    final_row_product = []
    final_row = []
    
    from django.db.models import F
    expense_query = Expense.objects.none()
    
    expense_query = Expense.objects.filter(entry_date__range=(start_date, end_date)).values(*selected_expense_list).order_by('-id')
    print('enumerate(selected_product_list)')
    #if expense is purchase of goods    
    for single_expense in expense_query:
        if single_expense['expense_type_sub_sub_master_id__expense_type_sub_master_id__expense_type_master'] == 'Purchase of Goods':
            single_expense['product details'] = list(Expense_Product.objects.filter(expense_id=single_expense['id']).values(*selected_product_list) )
            # expense_product = Expense_Product.objects.get(expense_id=single_expense['id'])
            # for index,product in enumerate(selected_product_list):
            #     single_expense[product] = expense_product.values(*product)
            #     print(product)
    
    
    
    try:
        del request.session['start_date']
        del request.session['end_date']
        del request.session['selected_expense_list']
        del request.session['selected_product_list']
        del request.session['string_expense']
        del request.session['string_product']
    except:
        pass

    context={
        'final_row':final_row,
        'final_row_product':final_row_product,
        'selected_list':selected_expense_list,
        'expense_query':expense_query,
    }
    return render(request,'expense_app/final_expense_report.html', context)

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
        item.log_entered_by = request.user.name
        item.expense_type_master = expense_type_master
        item.expense_type_sub_master = expense_type_sub_master
        item.notes = notes
        item.save()
        messages.success(request,"Expense Type Sub Master : "+str(expense_type_sub_master)+" created successfully!")
        return redirect('/expense_type_sub_sub_master/')  

    return render(request,'expense_app/expense_type_sub_master.html')

def update_expense_type_sub_master(request, sub_master_id):
    
    sub_master =  Expense_Type_Sub_Master.objects.get(id=sub_master_id)
    if request.method == 'POST' or request.method == 'FILES' :
        if 'delete' in request.POST:
            Expense_Type_Sub_Master.objects.filter(id=sub_master_id).delete()
            messages.success(request,"Expense Sub Master with ID: "+str(sub_master_id)+" deleted successfully!")
            return redirect('/expense_master/')
        expense_type_master = request.POST.get('expense_type_master')
        expense_type_sub_master = request.POST.get('expense_type_sub_master')
        notes = request.POST.get('notes')
        
        item = sub_master

        item.user_id = SiteUser.objects.get(id=request.user.id)
        item.log_entered_by = request.user.name
        item.expense_type_master = expense_type_master
        item.expense_type_sub_master = expense_type_sub_master
        item.notes = notes
        item.save(update_fields=['log_entered_by','notes','expense_type_sub_master','expense_type_master','user_id',])
        return redirect('/expense_master/')  
    context = {
        'sub_master': sub_master,
    }
    return render(request,'expense_app/update_expense_type_sub_master.html',context)

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
        item.log_entered_by = request.user.name
        item.expense_type_sub_master_id = Expense_Type_Sub_Master.objects.get(id=expense_type_sub_master)
        item.expense_type_sub_sub_master = expense_type_sub_sub_master
        item.notes = notes
        item.save()
        messages.success(request,"Expense Type Sub Sub Master : "+str(expense_type_sub_sub_master)+" created successfully!")
        return redirect('/expense_master/')  
    return render(request,'expense_app/expense_type_sub_sub_master.html', context)

def update_expense_type_sub_sub_master(request, sub_sub_master_id):
    sub_master = Expense_Type_Sub_Master.objects.all()
    sub_sub_master =  Expense_Type_Sub_Sub_Master.objects.get(id=sub_sub_master_id)
    context = {
        'sub_master': sub_master,
        'sub_sub_master': sub_sub_master,
    }
    if request.method == 'POST' or request.method == 'FILES' :
        if 'delete' in request.POST:
            Expense_Type_Sub_Sub_Master.objects.filter(id=sub_sub_master_id).delete()
            messages.success(request,"Expense Type Sub Sub Master with ID: "+str(sub_sub_master_id)+" deleted successfully!")
            return redirect('/expense_master/')
        expense_type_sub_master = request.POST.get('expense_type_sub_master')
        expense_type_sub_sub_master = request.POST.get('expense_type_sub_sub_master')
        notes = request.POST.get('notes')
        
        item =sub_sub_master

        item.user_id = SiteUser.objects.get(id=request.user.id)
        item.log_entered_by = request.user.name
        item.expense_type_sub_master_id = Expense_Type_Sub_Master.objects.get(id=expense_type_sub_master)
        item.expense_type_sub_sub_master = expense_type_sub_sub_master
        item.notes = notes
        item.save(update_fields=['user_id','log_entered_by','expense_type_sub_master_id','expense_type_sub_sub_master','notes',])
        return redirect('/expense_master/')  
    return render(request,'expense_app/update_expense_type_sub_sub_master.html', context)


def load_expense_sub_master(request):
    expense_type_master = request.GET.get('expense_type_master')

    expense_type_sub_masters = Expense_Type_Sub_Master.objects.filter(expense_type_master=expense_type_master)
    return render(request, 'AJAX_dropdowns/expense_sub_master_dropdown.html', {'expense_type_sub_masters': expense_type_sub_masters})

def load_expense_sub_sub_master(request):
    expense_type_sub_master = request.GET.get('expense_type_sub_master')

    expense_type_sub_sub_masters = Expense_Type_Sub_Sub_Master.objects.filter(expense_type_sub_master_id__id=expense_type_sub_master)
    return render(request, 'AJAX_dropdowns/expense_sub_sub_master_dropdown.html', {'expense_type_sub_sub_masters': expense_type_sub_sub_masters})

def load_vendor_details(request):
    vendor_id = request.GET.get('vendor_id')

    vendor_detail = list(Vendor.objects.filter(id=vendor_id).values())

    data = {
        'vendor_detail':vendor_detail,
    }
    return JsonResponse(data)

def load_expense_by_company(request):
    company_type = request.GET.get('company_type')
    # if company_type == 'Sales':
    #     expense_list = 
    # elif company_type == 'Scales':
    data = {
        'expense_list':expense_list,
    }
    return JsonResponse(data)


class BytesIOWrapper(object):

    def __init__(self, file, encoding='utf-8', errors='strict'):
        self.file, self.encoding, self.errors = file, encoding, errors
        self.buf = b''
    def readinto(self, buf):
        if not self.buf:
            self.buf = self.file.read(4096).encode(self.encoding, self.errors)
            if not self.buf:
                return 0
        length = min(len(buf), len(self.buf))
        buf[:length] = self.buf[:length]
        self.buf = self.buf[length:]
        return length
    def readable(self):
        return True


def showBill(request,sales_id,bill_company_type):
    purchase_details = Purchase_Details.objects.filter(id=sales_id).values('total_amount','crm_no__company_name','crm_no__customer_gst_no','bill_no','second_person',
                                                                        'sales_person','crm_no__address','po_number','second_contact_no','bill_address','shipping_address',
                                                                        'value_of_goods','bank_name','total_pf','date_of_purchase','reference_no','tax_amount','channel_of_dispatch','payment_mode','round_off_total',
                                                                        'credit_pending_amount','credit_authorised_by','neft_bank_name','neft_date','reference_no','cheque_no','cheque_date','purchase_no','date_of_purchase','bill_no')
    latest_bill_no=0
    try:
        todays_date = str(Bill.objects.get(purchase_id=sales_id, company_type=bill_company_type).entry_date)
    except:
        todays_date = str(datetime.now().strftime("%d-%m-%Y"))
    
    try:
        update_bill_no = Bill.objects.filter(company_type=bill_company_type).latest('id').update_bill_no
    except:
        update_bill_no = ''
        
    try:
        bill_no = Bill.objects.filter(company_type=bill_company_type,purchase_id=sales_id).latest('id').bill_no
    except:
        bill_no = 0

    # if bill already exists
    if Bill.objects.filter(purchase_id=sales_id, company_type=bill_company_type).count() > 0:
        latest_bill_no =  str(Bill.objects.get(purchase_id=sales_id, company_type=bill_company_type).bill_no)
        # elif  Bill.objects.filter(bill_no=bill_no, company_type=bill_company_type).count() > 0 and bill_company_type != '' and bill_company_type != 'None':
        #     latest_bill_no = str(Bill.objects.filter(company_type=bill_company_type).latest('id').bill_no)
    # if bill is not created and updated bill no in latest bill is not empty
    elif (update_bill_no != '' and update_bill_no != None ) and Bill.objects.filter(bill_no=update_bill_no, company_type=bill_company_type).count() == 0 and bill_company_type != '' and bill_company_type != 'None':
        latest_bill_no = str(update_bill_no).zfill(10)
    # if latest bill is none
    elif bill_company_type != '' and bill_company_type != 'None':
        try:
            latest_bill_no = str((int(Bill.objects.filter(company_type=bill_company_type).latest('id').bill_no) + 1)).zfill(10)
        except:
            latest_bill_no = '0000000001'
    elif bill_company_type == '' or bill_company_type == 'None' :
        messages.error(request,'Please select company type - Sales or Scales to generate a bill !')
        return redirect('/update_customer_details/'+str(sales_id))

    products_details = Product_Details.objects.filter(purchase_id=sales_id).values()


    for item in products_details:
        # <<<<<<< development
        #         product = Product.objects.filter(scale_type__name=item['type_of_scale'], main_category__name=item['model_of_purchase'],
        #                                                   sub_category__name=item['sub_model'])[0]

        try:
            product = Product.objects.get(scale_type__name=item['type_of_scale'],
                                          main_category__name=item['model_of_purchase'],
                                          sub_category__name=item['sub_model'],
                                          sub_sub_category__name=item['sub_sub_model'])
        except:
            product = Product.objects.get(scale_type__name=item['type_of_scale'],
                                          main_category__name=item['model_of_purchase'],
                                          sub_category__name=item['sub_model'])

        item['rate'] = product.cost_price
        item['hsn_code'] = product.hsn_code


    for obj in purchase_details:
        # print('sqddqsfwdwffewfewqfefefefeqwe',obj['channel_of_dispatch'])
        if obj['channel_of_dispatch'] == "Franchisee Store":
            obj['shipping_address'] = obj['crm_no__address']
            obj['bill_address'] = obj['crm_no__address']

        if obj['channel_of_dispatch'] != "Franchisee Store" and obj['shipping_address'] == obj['bill_address']:
            obj['shipping_address'] = obj['bill_address']
            # obj['bill_address']=obj['crm_no__address']

        if obj['crm_no__customer_gst_no'] != None:
            if '27' in obj['crm_no__customer_gst_no'] or (
                    len(obj['crm_no__customer_gst_no']) == 1 and 'A' in obj['crm_no__customer_gst_no']):
                obj['is_cgst'] = True
            else:
                obj['is_cgst'] = False
        else:
            obj['is_cgst'] = False

    if request.method == 'POST' and 'submit' in request.POST and Bill.objects.filter(purchase_id__id=sales_id).count() == 0:
        bill_file = request.POST.get('bill_file')

        item = Bill()
        item.user_id = SiteUser.objects.get(id=request.user.id)
        item.log_entered_by = request.user.name
        item.company_type = bill_company_type
        try:
            update_bill_no = Bill.objects.filter(company_type=bill_company_type).latest('id').update_bill_no
        except:
            update_bill_no = ''
        if (update_bill_no != '' and update_bill_no != None ) and Bill.objects.filter(bill_no=update_bill_no, company_type=bill_company_type).count() == 0 :
            item.bill_no = str(update_bill_no)
            print('session called')
        else:
            try:
                item.bill_no = str((int(Bill.objects.filter(company_type=bill_company_type).latest('id').bill_no) + 1)).zfill(10)
                print('bill no increased')
            except:
                item.bill_no = '0000000001'
        item.purchase_id = Purchase_Details.objects.get(id=sales_id)

        context22 = {
            'invoice_details': purchase_details[0],
            'products_details': products_details,
            'sales_id': sales_id,
            'todays_date': todays_date,
            'latest_bill_no': latest_bill_no,
            'csrf_token': "busuicbig_uivgbiegbviuegviygu",
            'hide_buttons': True,
            'is_download': True,
        }
        if bill_company_type == "Sales":
            template = get_template('bills/sales_bill.html')
        else:
            template = get_template('bills/scales_bill.html')
        html = template.render(context22)
        file_pdf = ContentFile(html)
        # file =  file_pdf.save('AutoFollowup.pdf', file_pdf, save=False)
        item.bill_file.save('Bill_'+str(bill_company_type)+'_'+str(sales_id)+'.html', file_pdf, save=False)


        # item.bill_file = bill_file
        item.save()
        Purchase_Details.objects.filter(id=sales_id).update(bill_no=item.bill_no)
        try:
            del request.session['new_bill_no']
            del request.session['bill_no_company_type']
        except:
            pass
        messages.success(request,'Bill saved successfully !')
        return redirect('/update_customer_details/'+str(sales_id))                                                                   
    elif request.method == 'POST' and 'submit' in request.POST:
        item = Bill.objects.get(purchase_id__id=sales_id)
        if item.company_type == "Sales":
            template = get_template('bills/sales_bill.html')
        else:
            template = get_template('bills/scales_bill.html')
        context22 = {
            'invoice_details': purchase_details[0],
            'products_details': products_details,
            'sales_id': sales_id,
            'todays_date': todays_date,
            'latest_bill_no': latest_bill_no,
            'csrf_token': "busuicbig_uivgbiegbviuegviygu",
            'hide_buttons': True,
            'is_download': True,
        }
        html = template.render(context22)
        
        file_pdf = ContentFile(html)
        # file =  file_pdf.save('AutoFollowup.pdf', file_pdf, save=False)
        item.bill_file.save('Bill_'+str(bill_company_type)+'_'+str(sales_id)+'.html', file_pdf, save=False)
        item.save(update_fields=['bill_file',])
        messages.success(request,'Bill updated successfully !')
        return redirect('/update_customer_details/'+str(sales_id))


    
    context={
        'invoice_details':purchase_details[0],
        'products_details':products_details,
        'sales_id':sales_id,
        'todays_date':todays_date,
        'latest_bill_no':latest_bill_no,
        'hide_buttons': False,
        'is_download': False,

    }
    if bill_company_type == 'Sales':
        return render(request,"bills/sales_bill.html", context)
    elif bill_company_type == 'Scale':
        return render(request,"bills/scales_bill.html", context)
    else:
        print('fdskjfdskj')
        messages.error(request,'Please select company type - Sales or Scales to generate a bill !')
        return redirect('/update_customer_details/'+str(sales_id))
    return redirect('/update_customer_details/'+str(sales_id))
        

def showBillModule(request):
    if check_admin_roles(request):  # For ADMIN
        bills_list = Bill.objects.filter(Q(user_id__name=request.user.name)|Q(user_id__group__icontains=request.user.name),
                        user_id__is_deleted=False, entry_date__month=today_month).order_by('-id')
        
            
    else:  # For EMPLOYEE
        bills_list = Bill.objects.filter(user_id=request.user.pk, entry_date__month=today_month).order_by('-id')

    #filter by company type (sales or scales)
    if request.method == 'GET' and 'company_type' in request.GET:
        company_type = request.GET.get('company_type')
        
        if check_admin_roles(request):  # For ADMIN
            bills_list = Bill.objects.filter(Q(user_id__name=request.user.name)|Q(user_id__group__icontains=request.user.name),
                                                        user_id__is_deleted=False,company_type__icontains=company_type).order_by('-id')

        else:  # For EMPLOYEE
            bills_list = Bill.objects.filter(user_id=request.user.pk,company_type__icontains=company_type).order_by('-id')
        
        context = {
            'bills_list':bills_list,
        }
        return render(request,"bills/load_bills_company_type.html", context)

    # search by options
    if request.method == 'POST':
        if 'submit1' in request.POST:
            start_date = request.POST.get('date1')
            end_date = request.POST.get('date2')
            bills_list = Bill.objects.filter( entry_date__range=[start_date, end_date]).order_by('-id')
            context = {
                'bills_list': bills_list,
                'search_msg': 'Search result for date range: ' + start_date + ' TO ' + end_date,
            }
            return render(request,'bills/billsModuleDashboard.html',context)
        elif 'submit2' in request.POST:
            contact = request.POST.get('contact')
            bills_list = Bill.objects.filter(purchase_id__crm_no__contact_no__icontains=contact).order_by('-id')

            context = {
                'bills_list': bills_list,
                'search_msg': 'Search result for Customer Contact No: ' + contact,
            }
            return render(request,'bills/billsModuleDashboard.html',context)

        elif 'submit3' in request.POST:
            email = request.POST.get('email')

            bills_list = Bill.objects.filter(purchase_id__crm_no__customer_email_id__icontains=email).order_by('-id')

            context = {
                'bills_list': bills_list,
                'search_msg': 'Search result for Customer Email ID: ' + email,
            }
            return render(request,'bills/billsModuleDashboard.html',context)
        elif 'submit4' in request.POST:
            name = request.POST.get('name')

            bills_list = Bill.objects.filter(purchase_id__crm_no__customer_name__icontains=name).order_by('-id')


            context = {
                'bills_list': bills_list,
                'search_msg': 'Search result for Customer Name: ' + name,
            }
            return render(request,'bills/billsModuleDashboard.html',context)

        elif 'submit5' in request.POST:
            company = request.POST.get('company')

            bills_list = Bill.objects.filter(purchase_id__crm_no__company_name__icontains=company).order_by('-id')

            context = {
                'bills_list': bills_list,
                'search_msg': 'Search result for Company Name: ' + company,
            }
            return render(request,'bills/billsModuleDashboard.html',context)
        elif request.method == 'POST' and 'submit6' in request.POST:
            bill_id = request.POST.get('id')
            bills_list = Bill.objects.filter(purchase_id__purchase_no__icontains=bill_id).order_by('-id')

            context = {
                'bills_list': bills_list,
                'search_msg': 'Search result for Sales ID : ' + str(id),
            }
            return render(request, 'bills/billsModuleDashboard.html', context)
        elif request.method == 'POST' and 'delete_bill' in request.POST:
            bill_id = request.POST.get('bill_id')
            
            bills_list = Bill.objects.filter(id=bill_id).delete()
            messages.success(request,"Bill Deleted Successfully!")
            return redirect('/showBillModule/')
            return render(request, 'bills/billsModuleDashboard.html', context) 
        elif 'increase_bill_no' in request.POST:
            new_bill_no = request.POST.get('new_bill_no')
            company_type = request.POST.get('company_type')
            new_bill_no = str(new_bill_no).zfill(10)
            print('new_bill_no')
            print(new_bill_no)
            print(Bill.objects.filter(company_type=company_type).latest('id').bill_no)
            if new_bill_no < Bill.objects.filter(company_type=company_type).latest('id').bill_no :
                messages.error(request,"Bill no cannot be decreased  !")
            elif new_bill_no == Bill.objects.filter(bill_no = new_bill_no, company_type=company_type):
                messages.error(request,"Bill no already exists for company type "+company_type +"!")    
            else:
                bill = Bill.objects.filter(company_type=company_type).update(update_bill_no=new_bill_no)
                
                try:
                    del request.session['new_bill_no']
                    del request.session['bill_no_company_type']
                except:
                    pass
                try:
                    request.session['new_bill_no'] = new_bill_no
                    request.session['bill_no_company_type'] = company_type
                except:
                    pass
                # bill_no = request.session.get('new_bill_no')
                print(request.session.get('bill_no_company_type'))
                messages.success(request,"Bills will be now created from bill id "+str(new_bill_no)+" for company type - "+str(company_type))
            print('session bill no')
            return redirect('/showBillModule/')
    context={
        "bills_list":bills_list,
    }
    return render(request,'bills/billsModuleDashboard.html',context)


def report_bill_form(request):
    bill_list = Bill.objects.all()
    for bill in bill_list:
        try:
            if  bill.purchase_id.crm_no.customer_gst_no == 'None' or bill.purchase_id.crm_no.customer_gst_no == None or bill.purchase_id.crm_no.customer_gst_no == '' or bill.purchase_id.crm_no.customer_gst_no[:2] == '27'  :
                Purchase_Details.objects.filter(id=bill.purchase_id.id).update(cgst=F("tax_amount")/2 )
                Purchase_Details.objects.filter(id=bill.purchase_id.id).update(sgst=F("tax_amount")/2 )
            else :
                Purchase_Details.objects.filter(id=bill.purchase_id.id).update(igst=F("tax_amount") )
        except:
            pass
    if request.method =='POST':
        selected_purchase_list = request.POST.getlist('checks[]')
        selected_product_list = request.POST.getlist('products[]')
        selected_customer_list = request.POST.getlist('customer[]')
        payment_details = request.POST.get('payment_details')

        start_date = request.POST.get('date1')
        end_date = request.POST.get('date2')
        string = ','.join(selected_purchase_list)
        string_product = ','.join(selected_product_list)


        request.session['start_date'] = start_date
        request.session['end_date'] = end_date
        request.session['string'] = selected_purchase_list
        request.session['string_product'] = selected_product_list
        request.session['selected_list'] = selected_purchase_list
        request.session['selected_product_list'] = selected_product_list
        request.session['selected_customer_list'] = selected_customer_list
        request.session['payment_details'] = payment_details
        return redirect('/final_bill_report/')
    return render(request,"report/report_bill_form.html",)

def final_bill_report(request):
    start_date = request.session.get('start_date')
    end_date = request.session.get('end_date')
    string_purchase = ['purchase_id']  + request.session.get('string')  
    string_product = request.session.get('string_product')  + ['id'] + ['purchase_id']

    selected_customer_list = request.session.get('selected_customer_list')
    selected_list = request.session.get('selected_list') + ['crm_no_id']
    selected_product_list = request.session.get('selected_product_list') + ['Purchase ID']
    payment_details = request.session.get('payment_details')

    final_row_product = []
    final_row = []

    
  
    bill_query = Bill.objects.filter(entry_date__range=(start_date, end_date)).values(*string_purchase).order_by('-id')
    # for n, i in enumerate(product_query):
    #     if i == 'purchase_id__tax_amount':
    #         selected_list[n] = 'Purchase ID'
    #     if i == 'customer_app_customer_details.id':
    #         selected_list[n] = 'Customer No'
    #     if i == 'today_date':
    #         selected_list[n] = 'Entry Date'
    #     if i == 'second_person':
    #         selected_list[n] = 'Customer Name'
    bill_query_list = list(bill_query)
    if 'product_details' in selected_product_list:
        for single_bill in bill_query:
            # purchase_product  = Product_Details.objects.filter(purchase_id=single_bill['purchase_id'])
            single_bill['product details'] = list(Product_Details.objects.filter(purchase_id=single_bill['purchase_id']).values('type_of_scale','model_of_purchase','sub_model','sub_sub_model','quantity','amount')) 

        # try:
        #     if (purchase_product__sub_sub_model == None or purchase_product__sub_sub_model == ""):
        #         product_database = Product.objects.get(scale_type_=purchase_product__type_of_scale, main_category=purchase_product__model_of_purchase,
        #                                         sub_category=purchase_product__sub_model, sub_sub_category=None)
                
        #     elif (purchase_product__sub_sub_model != None or purchase_product__sub_sub_model != ""):
        #         product_database = Product.objects.get(cale_type_=purchase_product__type_of_scale, main_category=purchase_product__model_of_purchase,
        #                                         sub_category=purchase_product__sub_model, sub_sub_category__id=purchase_product__sub_sub_model)
        # lead.update(list(Product_Details.objects.filter(purchase_id=single_bill['purchase_id']).values('quantity','amount')))
       

    try:
        del request.session['start_date']
        del request.session['end_date']
        del request.session['string']
        del request.session['selected_list']
        del request.session['string_product']
        del request.session['selected_product_list']
    except:
        pass

    context={
        'final_row':final_row,
        'final_row_product':final_row_product,
        'selected_list':selected_list,
        'selected_product_list':selected_product_list+selected_list,
        'sales_query':bill_query,
    }
    return render(request,"report/final_bill_report.html",context)


def add_sales(request):
    return render(request,'bills/add_sales.html')

