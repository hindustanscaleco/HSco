from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render, redirect
from customer_app.models import Customer_Details
from user_app.models import SiteUser
from dispatch_app.models import Dispatch
from dispatch_app.models import Product_Details_Dispatch
from ess_app.models import Employee_Analysis_month, Employee_Analysis_date
from purchase_app.forms import Purchase_Details_Form, Feedback_Form
from ess_app.models import Employee_Leave
from django.db.models import Q,F
from ess_app.models import Employee_Analysis_date
from .models import  Purchase_Details, Feedback, Product_Details
from purchase_app.forms import Product_Details_Form
from _datetime import datetime
from django.core.mail import send_mail
from Hsco import settings
import requests
import json
from django.db.models.functions import TruncMonth
from django.db.models import Count

def add_purchase_details(request):
    form = Purchase_Details_Form(request.POST or None, request.FILES or None)

    if request.method == 'POST' or request.method == 'FILES':
        customer_name = request.POST.get('customer_name')
        company_name = request.POST.get('company_name')
        address = request.POST.get('address')
        contact_no = request.POST.get('contact_no')
        customer_email_id = request.POST.get('customer_email_id')

        item = Customer_Details()

        item.customer_name = customer_name
        item.company_name = company_name
        item.address = address
        item.contact_no = contact_no
        item.customer_email_id = customer_email_id

        item.save()

        date_of_purchase = request.POST.get('date_of_purchase')
        new_repeat_purchase = request.POST.get('new_repeat_purchase')
        sales_person = request.POST.get('product_purchase_date')
        product_purchase_date = request.POST.get('sales_person')
        bill_no = request.POST.get('bill_no')
        upload_op_file = request.POST.get('upload_op_file')
        po_number = request.POST.get('po_number')
        photo_lr_no = request.POST.get('photo_lr_no')
        channel_of_sales = request.POST.get('channel_of_sales')
        industry = request.POST.get('industry')
        value_of_goods = request.POST.get('value_of_goods')
        channel_of_dispatch = request.POST.get('channel_of_dispatch')
        notes = request.POST.get('notes')
        feedback_form_filled = request.POST.get('feedback_form_filled')

        item2 = Purchase_Details()

        item2.crm_no = Customer_Details.objects.get(id=item.pk)
        item2.new_repeat_purchase = new_repeat_purchase
        item2.date_of_purchase = date_of_purchase
        item2.product_purchase_date = product_purchase_date
        item2.sales_person = sales_person
        item2.bill_no = bill_no
        item2.upload_op_file = upload_op_file
        item2.photo_lr_no = photo_lr_no
        item2.po_number = po_number
        item2.channel_of_sales = channel_of_sales
        item2.industry = industry
        item2.value_of_goods = value_of_goods
        item2.channel_of_dispatch = channel_of_dispatch
        item2.notes = notes
        item2.feedback_form_filled = feedback_form_filled
        item2.user_id = SiteUser.objects.get(id=request.user.pk)
        item2.manager_id = SiteUser.objects.get(id=request.user.pk).group
        item2.save()

        dispatch = Dispatch()


        dispatch.crm_no = Customer_Details.objects.get(id=item.pk)
        dispatch.user_id = SiteUser.objects.get(id=request.user.pk)
        dispatch.manager_id = SiteUser.objects.get(id=request.user.pk).group
        dispatch.customer_email = customer_email_id
        dispatch.customer_name = customer_name
        dispatch.company_name = company_name
        dispatch.customer_address = address

        dispatch.save()


        dispatch2 = Dispatch.objects.get(id=dispatch.pk)
        dispatch2.dispatch_id = str(dispatch.pk + 00000)
        dispatch2.save(update_fields=['dispatch_id'])
        customer_id = Purchase_Details.objects.get(id=item2.pk)
        customer_id.dispatch_id_assigned = Dispatch.objects.get(id=dispatch.pk) #str(dispatch.pk + 00000)
        customer_id.save(update_fields=['dispatch_id_assigned'])
        send_mail('Feedback Form','Click on the link to give feedback http://vikka.pythonanywhere.com/'+str(request.user.pk)+'/'+str(item.id)+'/'+str(item2.id) , settings.EMAIL_HOST_USER, [customer_email_id])

        # if Employee_Analysis_date.objects.filter(Q(entry_date=datetime.date.today),Q(user_id=SiteUser.objects.get(id=request.user.pk))).count() > 0:
        #     Employee_Analysis_date.objects.get(user_id=request.user.pk,entry_date=datetime.date.today,month = datetime.now().month,year = datetime.now().year).update(total_sales_done_today=F("total_sales_done_today") + value_of_goods)
        #     # ead.total_sales_done_today=.filter(category_id_id=id).update(total_views=F("total_views") + value_of_goods)
        #
        #     # ead.save(update_fields=['total_sales_done_today'])
        #
        # else:
        #     ead = Employee_Analysis_date()
        #     ead.user_id = SiteUser.objects.get(id=request.user.pk)
        #     ead.total_sales_done_today = value_of_goods
        #     ead.month = datetime.now().month
        #     ead.year = datetime.now().year
        #     ead.save()

        mobile = '+91 7757860524'  # 9766323877'
        user_hsco = 'HSCo'
        user = 'vikka'
        api_hsco = 'PF8MzCBOGTopfpYFlSZT'
        api = 'puU087yJ0uAQdhggM3T0'
        message = 'txt'
        senderid = 'MYTEXT'

        url = "http://smshorizon.co.in/api/sendsms.php?user="+user+"&apikey="+api+"&mobile="+contact_no+"&message="+message+"&senderid="+senderid+"&type=txt"
        payload = ""
        headers = {'content-type': 'application/x-www-form-urlencoded'}

        response = requests.request("GET", url, data=json.dumps(payload), headers=headers)
        x = response.text
        print(x)
        return redirect('/add_product_details/'+str(item2.id))

    context = {
        'form': form,
    }
    return render(request,'forms/cust_mod_form.html',context)


def view_customer_details(request):
    date_today= datetime.now().strftime('%Y-%m-%d')
    message_list = Employee_Leave.objects.filter(entry_date=str(date_today))



    if request.method == 'POST' and 'deleted' not in request.POST:
        if'submit1' in request.POST:
            start_date = request.POST.get('date1')
            end_date = request.POST.get('date2')
            if check_admin_roles(request):  # For ADMIN
                cust_list = Purchase_Details.objects.filter(user_id__group__icontains=request.user.group,
                                                            user_id__is_deleted=False,entry_timedate__range=[start_date, end_date]).order_by('-id')
            else:  # For EMPLOYEE
                cust_list = Purchase_Details.objects.filter(user_id=request.user.pk,entry_timedate__range=[start_date, end_date]).order_by('-id')
            # cust_list = Customer_Details.objects.filter()
            context = {
                'customer_list': cust_list,
            }
            return render(request, 'dashboardnew/cm.html', context)
        elif 'submit2' in request.POST:
            contact = request.POST.get('contact')
            if check_admin_roles(request):  # For ADMIN
                cust_list = Purchase_Details.objects.filter(user_id__group__icontains=request.user.group,
                                                            user_id__is_deleted=False,crm_no__contact_no=contact).order_by('-id')
            else:  # For EMPLOYEE
                cust_list = Purchase_Details.objects.filter(user_id=request.user.pk,crm_no__contact_no=contact).order_by('-id')
            # cust_list = Customer_Details.objects.filter(contact_no=contact)
            context = {
                'customer_list': cust_list,
            }
            return render(request, 'dashboardnew/cm.html', context)

        elif 'submit3' in request.POST:
            email = request.POST.get('email')
            if check_admin_roles(request):  # For ADMIN
                cust_list = Purchase_Details.objects.filter(user_id__group__icontains=request.user.group,
                                                            user_id__is_deleted=False,crm_no__customer_email_id=email).order_by('-id')
            else:  # For EMPLOYEE
                cust_list = Purchase_Details.objects.filter(user_id=request.user.pk,crm_no__customer_email_id=email).order_by('-id')
            # cust_list = Customer_Details.objects.filter(customer_email_id=email)
            context = {
                'customer_list': cust_list,
            }
            return render(request, 'dashboardnew/cm.html', context)
        elif 'submit4' in request.POST:
            customer = request.POST.get('customer')
            if check_admin_roles(request):  # For ADMIN
                cust_list = Purchase_Details.objects.filter(user_id__group__icontains=request.user.group,
                                                            user_id__is_deleted=False,crm_no__customer_name=customer).order_by('-id')
            else:  # For EMPLOYEE
                cust_list = Purchase_Details.objects.filter(user_id=request.user.pk,crm_no__customer_name=customer).order_by('-id')
            # cust_list = Customer_Details.objects.filter(customer_name=customer)
            context = {
                'customer_list': cust_list,
            }
            return render(request, 'dashboardnew/cm.html', context)

        elif  'submit5' in request.POST:
            company = request.POST.get('company')
            if check_admin_roles(request):  # For ADMIN
                cust_list = Purchase_Details.objects.filter(user_id__group__icontains=request.user.group,
                                                            user_id__is_deleted=False,crm_no__company_name=company).order_by('-id')
            else:  # For EMPLOYEE
                cust_list = Purchase_Details.objects.filter(user_id=request.user.pk,crm_no__company_name=company).order_by('-id')
            # cust_list = Customer_Details.objects.filter(company_name=company)
            context = {
                'customer_list': cust_list,
            }
            return render(request, 'dashboardnew/cm.html', context)
        elif request.method=='POST' and 'submit6' in request.POST:
            crm = request.POST.get('crm')
            if check_admin_roles(request):  # For ADMIN
                cust_list = Purchase_Details.objects.filter(user_id__group__icontains=request.user.group,
                                                            user_id__is_deleted=False,crm_no__pk=crm).order_by('-id')
            else:  # For EMPLOYEE
                cust_list = Purchase_Details.objects.filter(user_id=request.user.pk,crm_no__pk=crm).order_by('-id')
            # cust_list = Customer_Details.objects.filter(crn_number=crm)
            context = {
                'customer_list': cust_list,
            }
            return render(request, 'dashboardnew/cm.html', context)
    elif 'deleted' in request.POST:
        if check_admin_roles(request):  # For ADMIN
            cust_list = Purchase_Details.objects.filter(user_id__group__icontains=request.user.group,user_id__is_deleted=True).order_by('-id')
        else:  # For EMPLOYEE
            cust_list = Purchase_Details.objects.filter(user_id=request.user.pk).order_by('-id')

        context = {
            'customer_list': cust_list,
            'message': message_list,
            'deleted': True,
        }
        return render(request, 'dashboardnew/cm.html', context)
    else:
        if check_admin_roles(request):  # For ADMIN
            cust_list = Purchase_Details.objects.filter(user_id__group__icontains=request.user.group,user_id__is_deleted=False).order_by('-id')
        else:  # For EMPLOYEE
            cust_list = Purchase_Details.objects.filter(user_id=request.user.pk).order_by('-id')

        # with connection.cursor() as cursor:
        #     cursor.execute(000000000000000
        #     p_customer_details  ;")
        #     row = cursor.fetchall()
        #     customer_list = [list(x) for x in row]
        #     print(customer_list)
        #     list2 = []
        #     list3 = []
        #     for item in customer_list:
        #         list2.append(item[0])
        #         list3.append(item[1])
        #        #     final_list = zip(list2,list3)

        context = {
            'customer_list': cust_list,
            'message': message_list,
        }
        return render(request,'dashboardnew/cm.html',context )


def update_customer_details(request,id):
    purchase_id_id = Purchase_Details.objects.get(id=id)
    # customer_id = Purchase_Details.objects.get(id=id).crm_no
    customer_id = Customer_Details.objects.get(id=purchase_id_id)
    product_id = Product_Details.objects.filter(purchase_id=id)
    if request.method=='POST':
        customer_name = request.POST.get('customer_name')
        company_name = request.POST.get('company_name')
        address = request.POST.get('address')
        contact_no = request.POST.get('phone_no')
        customer_email_id = request.POST.get('customer_email_id')

        item=customer_id

        item.customer_name = customer_name
        item.company_name = company_name
        item.address = address
        item.contact_no = contact_no
        item.customer_email_id = customer_email_id

        item.save(update_fields=['customer_name','company_name','address','contact_no','customer_email_id',])

        date_of_purchase = request.POST.get('date_of_purchase')
        product_purchase_date = request.POST.get('product_purchase_date')
        bill_no = request.POST.get('bill_no')
        new_repeat_purchase = request.POST.get('new_repeat_purchase')
        upload_op_file = request.POST.get('upload_op_file')
        po_number = request.POST.get('po_number')
        photo_lr_no = request.POST.get('photo_lr_no')
        channel_of_sales = request.POST.get('channel_of_sales')
        industry = request.POST.get('industry')
        value_of_goods = request.POST.get('value_of_goods')
        channel_of_dispatch = request.POST.get('channel_of_dispatch')
        notes = request.POST.get('notes')
        feedback_form_filled = request.POST.get('feedback_form_filled')

        item2 = purchase_id_id

        item2.crm_no = Customer_Details.objects.get(id=item.pk)
        item2.date_of_purchase = date_of_purchase
        item2.new_repeat_purchase = new_repeat_purchase
        item2.product_purchase_date = product_purchase_date
        item2.bill_no = bill_no
        item2.upload_op_file = upload_op_file
        item2.photo_lr_no = photo_lr_no
        item2.po_number = po_number
        item2.channel_of_sales = channel_of_sales
        item2.industry = industry
        item2.value_of_goods = value_of_goods
        item2.channel_of_dispatch = channel_of_dispatch
        item2.notes = notes
        item2.feedback_form_filled = feedback_form_filled
        item2.user_id = SiteUser.objects.get(id=request.user.pk)
        item2.manager_id = SiteUser.objects.get(id=request.user.pk).group
        item2.save(update_fields=['date_of_purchase','product_purchase_date','bill_no','upload_op_file','photo_lr_no','manager_id',
                                  'po_number','channel_of_sales','industry','channel_of_dispatch','notes','feedback_form_filled','user_id'])

    context={
        'product_id':product_id,
        'customer_id': customer_id,
        'purchase_id_id': purchase_id_id,
    }

    return render(request,'update_forms/update_cust_mod_form.html',context)


def add_product_details(request,id):
    purchase = Purchase_Details.objects.get(id=id)
    purchase_id = purchase.id
    dispatch_id_assigned = str(purchase.dispatch_id_assigned)
    form = Product_Details_Form(request.POST or None)
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        quantity = request.POST.get('quantity')
        model_of_purchase = request.POST.get('model_of_purchase')
        type_of_scale = request.POST.get('type_of_scale')
        sub_model = request.POST.get('sub_model')
        sub_sub_model = request.POST.get('sub_sub_model')
        serial_no_scale = request.POST.get('serial_no_scale')
        brand = request.POST.get('brand')
        capacity = request.POST.get('capacity')
        unit = request.POST.get('unit')
        sales_person = request.POST.get('sales_person')
        purchase_type = request.POST.get('purchase_type')

        item = Product_Details()

        item.product_name = product_name
        item.quantity = quantity
        item.type_of_scale = type_of_scale
        item.model_of_purchase = model_of_purchase
        item.sub_model = sub_model
        item.sub_sub_model = sub_sub_model
        item.serial_no_scale = serial_no_scale
        item.brand = brand
        item.capacity = capacity
        item.unit = unit
        item.purchase_id_id = purchase_id
        item.sales_person = sales_person
        item.purchase_type = purchase_type
        item.user_id = SiteUser.objects.get(id=request.user.pk)
        item.manager_id = SiteUser.objects.get(id=request.user.pk).group
        item.save()

        dispatch_id=Dispatch.objects.get(id=dispatch_id_assigned)
        dispatch_pro = Product_Details_Dispatch()
        dispatch_pro.user_id = SiteUser.objects.get(id=request.user.pk)
        dispatch_pro.manager_id = SiteUser.objects.get(id=request.user.pk).group
        dispatch_pro.product_name = product_name
        dispatch_pro.quantity = quantity
        dispatch_pro.type_of_scale = type_of_scale
        dispatch_pro.model_of_purchase = model_of_purchase
        dispatch_pro.sub_model = sub_model
        dispatch_pro.sub_sub_model = sub_sub_model
        dispatch_pro.serial_no_scale = serial_no_scale
        dispatch_pro.brand = brand
        dispatch_pro.capacity = capacity
        dispatch_pro.unit = unit
        dispatch_pro.dispatch_id = dispatch_id
        dispatch_pro.sales_person = sales_person
        dispatch_pro.purchase_type = purchase_type
        dispatch_pro.save()



        return redirect('/update_customer_details/'+str(item.id))


    context = {
        'form': form,
        'purchase_id': purchase_id,
    }
    return render(request,'dashboardnew/add_product.html',context)


def report(request):
    if request.method =='POST':
        selected_list = request.POST.getlist('checks[]')
        start_date = request.POST.get('date1')
        end_date = request.POST.get('date2')
        string = ','.join(selected_list)
        print(selected_list)
        request.session['start_date'] = start_date
        request.session['end_date'] = end_date
        request.session['string'] = string
        request.session['selected_list'] = selected_list
        return redirect('/final_report/')
    return render(request,"report/report_cust_mod_form.html",)


def final_report(request):
    start_date = request.session.get('start_date')
    end_date = request.session.get('end_date')
    string = request.session.get('string')
    selected_list = request.session.get('selected_list')
    with connection.cursor() as cursor:
        cursor.execute("SELECT  "+string+" from customer_app_customer_details where date_of_purchase between '"+start_date+"' and '"+end_date+"';")
        row = cursor.fetchall()


        final_row= [list(x) for x in row]
        list3=[]
        for i in row:
            list3.append(list(i))


    context={
        'final_row':final_row,
        'selected_list':selected_list,
    }
    return render(request,"dashboardnew/final_report.html",context)


def manager_report(request):
    employee_list = SiteUser.objects.all()
    context={
        'employee_list':employee_list,
    }
    return render(request, 'dashboardnew/manager_report.html',context)

def feedbacka(request):
    return render(request, 'feedback/feedbacka.html')

def purchase_analytics(request):
    return render(request, 'analytics/purchase_analytics.html')

def customer_employee_sales_graph(request,user_id):
    #x=Employee_Analysis_date.objects.annotate(date=TruncMonth('entry_timedate')).values('date').annotate(c=Count('id')).values('date', 'c')
    #print(x)
    from django.db.models import Sum
    feeback = Feedback.objects.filter(user_id=user_id)
    #this month sales

    mon = datetime.now().month
    this_month = Employee_Analysis_date.objects.filter(user_id=user_id,entry_date__month=mon).values('entry_date').annotate(
        data_sum=Sum('total_sales_done_today'))
    this_lis_date = []
    this_lis_sum = []
    for i in this_month:
        x = i
        this_lis_date.append(x['entry_date'].strftime('%Y-%m-%d'))
        this_lis_sum.append(x['data_sum'])

    #previous month sales
    mon = (datetime.now().month)-1
    previous_month = Employee_Analysis_date.objects.filter(user_id=user_id,entry_date__month=mon).values('entry_date').annotate(
        data_sum=Sum('total_sales_done_today'))
    previous_lis_date = []
    previous_lis_sum = []
    for i in previous_month:
        x = i
        previous_lis_date.append(x['entry_date'].strftime('%Y-%m-%d'))
        previous_lis_sum.append(x['data_sum'])

    if request.method=='POST':
        start_date = request.POST.get('date1')
        end_date = request.POST.get('date2')
        qs = Employee_Analysis_date.objects.filter(user_id=user_id,entry_date__range=(start_date, end_date)).values(
            'entry_date').annotate(data_sum=Sum('total_sales_done_today'))
        lis_date = []
        lis_sum = []
        for i in qs:
            x = i
            lis_date.append(x['entry_date'].strftime('%Y-%m-%d'))
            lis_sum.append(x['data_sum'])
        context = {
            'final_list': lis_date,
            'final_list2': lis_sum,

            'previous_lis_date': previous_lis_date,
            'previous_lis_sum': previous_lis_sum,
            'this_lis_date': this_lis_date,
            'this_lis_sum': this_lis_sum,
            'feeback': feeback,
        }
        return render(request, "graphs/sales_graph.html", context)
    else:

        qs = Employee_Analysis_date.objects.filter(user_id=user_id,entry_date__month=datetime.now().month).values('entry_date').annotate(data_sum=Sum('total_sales_done_today'))
        lis_date = []
        lis_sum = []
        for i in qs:
            x=i
            lis_date.append(x['entry_date'].strftime('%Y-%m-%d'))
            lis_sum.append(x['data_sum'])
        print(lis_date)
        print(lis_sum)

        context={
            'final_list':lis_date,
            'final_list2':lis_sum,
            'previous_lis_date': previous_lis_date,
            'previous_lis_sum': previous_lis_sum,
            'this_lis_date': this_lis_date,
            'this_lis_sum': this_lis_sum,
            'feeback': feeback,
        }
        return render(request,"graphs/sales_graph.html",context)

def feedback_purchase(request,user_id,customer_id,purchase_id):
    feedback_form = Feedback_Form(request.POST or None, request.FILES or None)
    if request.method == 'POST' :
        knowledge_of_person = request.POST.get('knowledge_of_person')
        timeliness_of_person = request.POST.get('timeliness_of_person')
        price_of_product = request.POST.get('price_of_product')
        overall_interaction = request.POST.get('overall_interaction')
        about_hsco = request.POST.get('about_hsco')
        any_suggestion = request.POST.get('any_suggestion')

        item = Feedback()
        item.knowledge_of_person = knowledge_of_person
        item.timeliness_of_person = timeliness_of_person
        item.price_of_product = price_of_product
        item.overall_interaction = overall_interaction
        item.about_hsco = about_hsco
        item.user_id = SiteUser.objects.get(id=user_id)
        item.customer_id = Customer_Details.objects.get(id=customer_id)
        item.purchase_id = Purchase_Details.objects.get(id=purchase_id)
        item.save()

        purchase=Purchase_Details.objects.get(id=purchase_id)
        purchase.feedback_stars= (knowledge_of_person+timeliness_of_person+price_of_product+overall_interaction)/4.0
        purchase.feedback_form_filled= 'YES'
        purchase.save(update_fields=['feedback_stars','feedback_form_filled'])



        return HttpResponse('Feedback Submitted!!!')
    context={
        'feedback_form': feedback_form,
    }
    return render(request,"feedback/feedback_customer.html",context)

def edit_product_customer(request,id):
    product_id = Product_Details.objects.get(id=id)
    print(product_id)
    context = {
        'product_id': product_id,
    }

    return render(request,'edit_product/edit_product_customer.html',context)

def load_users(request):
    selected = request.GET.get('loc_id')

    if selected=='true':
        user_list = Employee_Analysis_month.objects.filter(manager_id=request.user.name)
        # dispatch_list = Employee_Analysis_month.objects.filter(user_id__group=str(request.user.name))

        context = {
            'user_list': user_list,
            'manager': True,
        }

        return render(request, 'AJAX/load_users.html', context)
    else:
        if check_admin_roles(request):     #For ADMIN
            cust_list = Purchase_Details.objects.filter(user_id__group__icontains=request.user.group,user_id__is_deleted=False).order_by('-id')
        else:  #For EMPLOYEE
            cust_list = Purchase_Details.objects.filter(user_id=request.user.pk).order_by('-id')

        context = {
            'customer_list': cust_list,
            'manager': False,
        }

        return render(request, 'AJAX/load_users.html', context)

def check_admin_roles(request):
    if request.user.role == 'Super Admin' or request.user.role == 'Admin' or request.user.role == 'Manager':
        return True
    else:
        return False








