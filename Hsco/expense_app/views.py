from django.shortcuts import render
from .models import Expense_Type_Sub_Master, Expense_Type_Sub_Sub_Master, Vendor, Expense, Expense_Product
from django.shortcuts import render, redirect
from user_app.models import SiteUser
from django.http import HttpResponse, JsonResponse
from customer_app.models import type_purchase,main_model,sub_model,sub_sub_model
from stock_management_system_app.models import Godown
from purchase_app.views import check_admin_roles
from django.db.models import Q, F, Min, Avg
from django.contrib import messages


# Create your views here.

def expense_dashboard(request):
    expense_list = Expense.objects.all()

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
    vendors_list = Vendor.objects.all()
    expense_masters = Expense_Type_Sub_Sub_Master.objects.all()
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
        item.po_issued   = po_issued  
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

        if credit_pending_amount != '':
            item.credit_pending_amount = float(credit_pending_amount)
        item.credit_authorised_by = credit_authorised_by

        item.save()
        return redirect('/expense_product/'+str(item.pk))  

    context={
        'expense_masters' : expense_masters,
        'vendors_list' : vendors_list,
    }
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
        item.po_issued   = po_issued  
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

    selected_expense_list = request.session.get('selected_expense_list')    
    selected_product_list = request.session.get('selected_product_list')    
    string_expense = request.session.get('string_expense')    
    string_product = request.session.get('string_product')    

    product_query = Expense_Product.objects.filter(entry_date__range=(start_date, end_date)).values(*string_product)
    for product in product_query:
        expense_query = Expense.objects.filter(id=product['id']).values(*string_expense)
        
        print(sales_query)
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
        'selected_list':selected_list,
        'selected_product_list':selected_product_list+selected_list,
        'sales_query':product_query,
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
        return redirect('/expense_master/')  

    return render(request,'expense_app/expense_type_sub_master.html')

def update_expense_type_sub_master(request, sub_master_id):
    sub_master =  Expense_Type_Sub_Master.objects.get(id=sub_master_id)
    if request.method == 'POST' or request.method == 'FILES' :
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
        item.log_entered_by = request.user.name
        item.expense_type_sub_master_id = Expense_Type_Sub_Master.objects.get(id=expense_type_sub_master)
        item.expense_type_sub_sub_master = expense_type_sub_sub_master
        item.notes = notes
        item.save()
        return redirect('/expense_master/')  
    return render(request,'expense_app/expense_type_sub_sub_master.html', context)

def update_expense_type_sub_sub_master(request, sub_sub_master_id):
    sub_master = Expense_Type_Sub_Master.objects.all()
    sub_sub_master =  Expense_Type_Sub_Master.objects.get(id=sub_sub_master_id)
    context = {
        'sub_master': sub_master,
        'sub_sub_master': sub_sub_master,
    }
    if request.method == 'POST' or request.method == 'FILES' :
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
    return render(request,'expense_app/expense_type_sub_sub_master.html', context)


def load_expense_sub_master(request):
    expense_type_master = request.GET.get('expense_type_master')

    expense_type_sub_masters = Expense_Type_Sub_Master.objects.filter(expense_type_master=expense_type_master)
    return render(request, 'AJAX_dropdowns/expense_sub_master_dropdown.html', {'expense_type_sub_masters': expense_type_sub_masters})

def load_expense_sub_sub_master(request):
    expense_type_sub_master = request.GET.get('expense_type_sub_master')

    expense_type_sub_sub_masters = Expense_Type_Sub_Sub_Master.objects.filter(expense_type_sub_master_id__id=expense_type_sub_master)
    print('expense type')
    print(expense_type_sub_master)
    print(expense_type_sub_sub_masters)
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

def showBill(request):
    return render(request,'bills/billsNew.html')

def showBillModule(request):
    return render(request,'bills/billsModuleDashboard.html')

def add_sales(request):
    return render(request,'bills/add_sales.html')

