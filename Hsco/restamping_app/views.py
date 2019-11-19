from datetime import datetime

from django.db import connection
from django.db.models import Min, Sum, Q, F, Count
from django.shortcuts import render, redirect

from django.core.mail import send_mail
from Hsco import settings
from customer_app.models import Customer_Details

from ess_app.models import Employee_Analysis_date

from purchase_app.views import check_admin_roles
from user_app.models import SiteUser
from .models import Restamping_after_sales_service, Restamping_Product
import requests
import json
from ess_app.models import Employee_Analysis_month

def restamping_manager(request):

    if request.method == 'POST' and 'deleted' not in request.POST:
        if 'submit1' in request.POST:
            start_date = request.POST.get('date1')
            end_date = request.POST.get('date2')
            if check_admin_roles(request):  # For ADMIN
                restamp_list = Restamping_after_sales_service.objects.filter(
                    user_id__group__icontains=request.user.group, user_id__is_deleted=False,entry_timedate__range=[start_date, end_date]).order_by('-id')
            else:  # For EMPLOYEE
                restamp_list = Restamping_after_sales_service.objects.filter(user_id=request.user.pk,entry_timedate__range=[start_date, end_date]).order_by('-id')

            # restamp_list = Restamping_after_sales_service.objects.filter(entry_timedate__range=[start_date, end_date])
            context = {
                'restamp_list': restamp_list,
            }
            return render(request, "manager/restamping_manager.html", context)
        elif 'submit2' in request.POST:
            contact = request.POST.get('contact')
            if check_admin_roles(request):  # For ADMIN
                restamp_list = Restamping_after_sales_service.objects.filter(
                    user_id__group__icontains=request.user.group, user_id__is_deleted=False,crm_no__contact_no=contact).order_by('-id')
            else:  # For EMPLOYEE
                restamp_list = Restamping_after_sales_service.objects.filter(user_id=request.user.pk,crm_no__contact_no=contact).order_by('-id')

            # restamp_list = Restamping_after_sales_service.objects.filter(mobile_no=contact)
            context = {
                'restamp_list': restamp_list,
            }
            return render(request, "manager/restamping_manager.html", context)

        elif 'submit3' in request.POST:
            email = request.POST.get('email')
            if check_admin_roles(request):  # For ADMIN
                restamp_list = Restamping_after_sales_service.objects.filter(
                    user_id__group__icontains=request.user.group, user_id__is_deleted=False,crm_no__customer_email_id=email).order_by('-id')
            else:  # For EMPLOYEE
                restamp_list = Restamping_after_sales_service.objects.filter(user_id=request.user.pk,crm_no__customer_email_id=email).order_by('-id')
            # restamp_list = Restamping_after_sales_service.objects.filter(customer_email_id=email)
            context = {
                'restamp_list': restamp_list,
            }
            return render(request, "manager/restamping_manager.html", context)
        elif 'submit4' in request.POST:
            customer = request.POST.get('customer')
            restamp_list = Restamping_after_sales_service.objects.filter(name=customer)
            if check_admin_roles(request):  # For ADMIN
                restamp_list = Restamping_after_sales_service.objects.filter(
                    user_id__group__icontains=request.user.group, user_id__is_deleted=False,crm_no__customer_name=customer).order_by('-id')
            else:  # For EMPLOYEE
                restamp_list = Restamping_after_sales_service.objects.filter(user_id=request.user.pk,crm_no__customer_name=customer).order_by('-id')
            context = {
                'restamp_list': restamp_list,
            }
            return render(request, "manager/restamping_manager.html", context)

        elif 'submit5' in request.POST:
            company = request.POST.get('company')
            restamp_list = Restamping_after_sales_service.objects.filter(company_name=company)
            if check_admin_roles(request):  # For ADMIN
                restamp_list = Restamping_after_sales_service.objects.filter(
                    user_id__group__icontains=request.user.group, user_id__is_deleted=False,crm_no__company_name=company).order_by('-id')
            else:  # For EMPLOYEE
                restamp_list = Restamping_after_sales_service.objects.filter(user_id=request.user.pk,crm_no__company_name=company).order_by('-id')
            context = {
                'restamp_list': restamp_list,
            }
            return render(request, "manager/restamping_manager.html", context)
        elif request.method == 'POST' and 'submit6' in request.POST:
            crm = request.POST.get('crm')
            if check_admin_roles(request):  # For ADMIN
                restamp_list = Restamping_after_sales_service.objects.filter(
                    user_id__group__icontains=request.user.group, user_id__is_deleted=False,crm_no__pk=crm).order_by('-id')
            else:  # For EMPLOYEE
                restamp_list = Restamping_after_sales_service.objects.filter(user_id=request.user.pk,crm_no__pk=crm).order_by('-id')
            restamp_list = Restamping_after_sales_service.objects.filter(crn_number=crm)

            context = {
                'restamp_list': restamp_list,
            }
            return render(request, "manager/restamping_manager.html", context)
    elif 'deleted' in request.POST:
        if check_admin_roles(request):  # For ADMIN
            restamp_list = Restamping_after_sales_service.objects.filter(user_id__group__icontains=request.user.group, user_id__is_deleted=True,user_id__modules_assigned__icontains='Restamping Module').order_by('-id')
        else:  # For EMPLOYEE
            restamp_list = Restamping_after_sales_service.objects.filter(user_id=request.user.pk).order_by('-id')
        # restamp_list = Restamping_after_sales_service.objects.all()

        context = {
            'restamp_list': restamp_list,
            'deleted': True,
        }
        return render(request, "manager/restamping_manager.html", context)
    else:
        context = {
            'none':None,
        }
        if check_admin_roles(request):     #For ADMIN
            restamp_list = Restamping_after_sales_service.objects.filter(user_id__group__icontains=request.user.name,user_id__is_deleted=False,user_id__modules_assigned__icontains="'Restamping Module'").order_by('-id')
        else:  #For EMPLOYEE
            restamp_list = Restamping_after_sales_service.objects.filter(user_id=request.user.pk).order_by('-id')
        # restamp_list = Restamping_after_sales_service.objects.all()

        stage1 = Restamping_after_sales_service.objects.filter(Q(current_stage='Scales in Restamping Queue')).values('current_stage').annotate(dcount=Count('current_stage'))
        x = stage1
        if not x:
            x = None
        # if x['current_stage'] == 'Scale is collected but estimate is not given':
        try:
            for item in x:
                stage1 = item['dcount']
            context10d = {
                'stage1': stage1,
            }
            context.update(context10d)

        except:

            pass

        stage2 = Restamping_after_sales_service.objects.filter(Q(current_stage='Restamping is done but scale is not collected')).values(
            'current_stage').annotate(dcount=Count('current_stage'))
        x = stage2
        # if x['current_stage'] == 'Scale is collected but estimate is not given':
        if not x:
            x = None
        try:

            for item in x:
                if item['dcount'] in x:
                # stage1 = item['dcount']
                    stage2 = item['dcount']
            contextd = {
                'stage2': stage2,
            }
            context.update(contextd)
        except:
            pass

        stage3 = Restamping_after_sales_service.objects.filter(Q(current_stage='Restamping done and scale also collected')).values(
            'current_stage').annotate(dcount=Count('current_stage'))
        x = stage3
        if not x:
            x = None
        # if x['current_stage'] == 'Scale is collected but estimate is not given':
        try:
            for item in x:
                # stage1 = item['dcount']
                stage3 = item['dcount']
            context10d = {
                'stage3': stage3,
            }
            context.update(context10d)
        except:
            pass


        context2 = {
            'restamp_list': restamp_list,
        }
        context.update(context2)
        print(context)
        print(context)

        return render(request, "manager/restamping_manager.html", context)


def restamping_after_sales_service(request):
    # form = Customer_Details_Form(request.POST or None, request.FILES or None)
    cust_sugg=Customer_Details.objects.all()

    if request.method == 'POST' or request.method=='FILES':
        customer_name = request.POST.get('customer_name')
        company_name = request.POST.get('company_name')
        address = request.POST.get('customer_address')
        contact_no = request.POST.get('contact_no')
        customer_email_id = request.POST.get('customer_email_id')

        # item = Customer_Details()
        #
        # item.customer_name = customer_name
        # item.company_name = company_name
        # item.address = address
        # item.contact_no = contact_no
        # item.customer_email_id = customer_email_id
        #
        # item.save()

        # restampingno = request.POST.get('restampingno')
        # customer_no = request.POST.get('customer_no')
        today_date = request.POST.get('today_date')
        # second_person = request.POST.get('second_person')
        # third_person = request.POST.get('third_person')
        # second_contact_no = request.POST.get('second_contact_no')
        # third_contact_no = request.POST.get('third_contact_no')
        # new_serial_no = request.POST.get('new_serial_no')
        # brand = request.POST.get('brand')
        # scale_delivery_date = request.POST.get('scale_delivery_date')

        item = Customer_Details()
        item2 = Restamping_after_sales_service()

        if Customer_Details.objects.filter(customer_name=customer_name,
                                           contact_no=contact_no).count() > 0:

            item2.crm_no = Customer_Details.objects.filter(customer_name=customer_name,
                                                           contact_no=contact_no).first()
            item3 = Customer_Details.objects.filter(customer_name=customer_name, contact_no=contact_no).first()
            if company_name != '':
                item3.company_name = company_name
                item3.save(update_fields=['company_name'])
            if address != '':
                item3.address = address
                item3.save(update_fields=['address'])
            if customer_email_id != '':
                item3.customer_email_id = customer_email_id
                item3.save(update_fields=['customer_email_id'])

        else:

            item.customer_name = customer_name


            item.contact_no = contact_no

            item.customer_name = customer_name
            if company_name != '':
                item.company_name = company_name
            if address != '':
                item.address = address
            if customer_email_id != '':
                item.customer_email_id = customer_email_id
            # item.user_id = SiteUser.objects.get(id=request.user.pk)
            # item.manager_id = SiteUser.objects.get(id=request.user.pk).group
            try:
                item.save()
                item2.crm_no = Customer_Details.objects.get(id=item.pk)
            except:
                pass




        item2.user_id = SiteUser.objects.get(id=request.user.pk)
        item2.manager_id = SiteUser.objects.get(id=request.user.pk).group
        # item2.crm_no_id = item.pk
        # item2.restampingno = restampingno
        # item2.customer_no = customer_no
        item2.second_person = customer_name  # new1
        item2.second_contact_no = contact_no  # new2
        # item2.second_person=second_person
        # item2.third_person=third_person
        # item2.second_contact_no=second_contact_no
        # item2.third_contact_no=third_contact_no
        item2.today_date = today_date
        # item2.new_serial_no = new_serial_no
        # item2.brand = brand
        item2.total_amount = 0.0
        # item2.scale_delivery_date = scale_delivery_date


        item2.save()





        return redirect('/restamping_product/'+str(item2.pk))
    context={
        'cust_sugg':cust_sugg
    }
    return render(request, 'forms/restamping_form.html',context)

def restamping_product(request,id):
    restamping_id = Restamping_after_sales_service.objects.get(id=id).id

    if request.method=='POST':
        # product_to_stampped = request.POST.get('product_to_stampped')
        scale_type = request.POST.get('scale_type')
        sub_model = request.POST.get('sub_model')
        capacity = request.POST.get('capacity')
        old_serial_no = request.POST.get('old_serial_no')
        # old_brand = request.POST.get('brand')
        amount = request.POST.get('amount')
        new_sr_no = request.POST.get('new_sr_no')
        brand = request.POST.get('brand')

        item=Restamping_Product()

        # item.product_to_stampped = product_to_stampped
        item.scale_type = scale_type
        item.sub_model = sub_model
        item.capacity = capacity
        item.old_serial_no = old_serial_no
        item.brand = brand
        item.amount = amount
        item.new_sr_no = new_sr_no
        # item.old_brand = old_brand
        item.restamping_id_id = restamping_id
        item.user_id = SiteUser.objects.get(id=request.user.pk)
        item.manager_id = SiteUser.objects.get(id=request.user.pk).group

        item.save()

        Restamping_after_sales_service.objects.filter(id=id).update(total_amount=F("total_amount") + amount)

        current_stage_in_db = Restamping_after_sales_service.objects.get(
            id=id).current_stage  # updatestage2
        if (current_stage_in_db == '' or current_stage_in_db == None) and (sub_model != '' or sub_model != None):
            Restamping_after_sales_service.objects.filter(id=id).update(
                current_stage='Scales in Restamping Queue')
        if (current_stage_in_db == 'Scales in Restamping Queue') and (new_sr_no != '' or new_sr_no != None):
            Restamping_after_sales_service.objects.filter(id=id).update(
                current_stage='Restamping is done but scale is not collected')

        if Employee_Analysis_date.objects.filter(user_id=request.user.pk,entry_date__month=datetime.now().month,year = datetime.now().year).count() > 0:
            # print(Employee_Analysis_date.objects.filter(user_id=request.user.pk,entry_date__month=datetime.now().month,year = datetime.now().year))
            # print(Employee_Analysis_date.objects.filter(user_id=request.user.pk,entry_date__month=datetime.now().month,year = datetime.now().year))
            # print(Employee_Analysis_date.objects.filter(user_id=request.user.pk,entry_date__month=datetime.now().month,year = datetime.now().year))
            Employee_Analysis_date.objects.filter(user_id=request.user.pk,entry_date__month=datetime.now().month,year = datetime.now().year).update(total_restamping_done_today=F("total_restamping_done_today") + amount)
            # ead.total_sales_done_today=.filter(category_id_id=id).update(total_views=F("total_views") + value_of_goods)

            # ead.save(update_fields=['total_sales_done_today'])

        else:
            ead = Employee_Analysis_date()
            ead.user_id = SiteUser.objects.get(id=request.user.pk)
            ead.total_restamping_done_today = amount
            # ead.total_dispatch_done_today = value_of_goods
            ead.manager_id = SiteUser.objects.get(id=request.user.pk).group
            ead.month = datetime.now().month
            ead.year = datetime.now().year
            ead.save()

        if Employee_Analysis_month.objects.filter(user_id=request.user.pk,entry_date__month=datetime.now().month,year = datetime.now().year).count() > 0:
            Employee_Analysis_month.objects.filter(user_id=request.user.pk,entry_date__month=datetime.now().month,year = datetime.now().year).update(total_restamping_done=F("total_restamping_done") + amount)
            # ead.total_sales_done_today=.filter(category_id_id=id).update(total_views=F("total_views") + value_of_goods)

            # ead.save(update_fields=['total_sales_done_today'])

        else:
            ead = Employee_Analysis_month()
            ead.user_id = SiteUser.objects.get(id=request.user.pk)
            ead.total_restamping_done = amount
            # ead.total_dispatch_done = value_of_goods
            ead.manager_id = SiteUser.objects.get(id=request.user.pk).group
            ead.month = datetime.now().month
            ead.year = datetime.now().year
            ead.save()



        return redirect('/update_restamping_details/'+str(id))
    context = {
        'restamping_id': restamping_id,
    }
    return render(request,'dashboardnew/restamping_product.html',context)



def restamping_analytics(request):
    mon = datetime.now().month
    this_month = Employee_Analysis_month.objects.all().values('entry_date').annotate(
        data_sum=Sum('total_restamping_done'))
    this_lis_date = []
    this_lis_sum = []
    for i in this_month:
        x = i
        this_lis_date.append(x['entry_date'].strftime("%B-%Y"))
        this_lis_sum.append(x['data_sum'])

    from django.db.models import Max
    # Generates a "SELECT MAX..." query
    value = Employee_Analysis_month.objects.aggregate(Max('total_restamping_done'))
    print(value['total_restamping_done__max'])
    try:
        value = Employee_Analysis_month.objects.get(total_restamping_done=value['total_restamping_done__max'])
    except:
        pass

    value_low = Employee_Analysis_month.objects.aggregate(Min('total_restamping_done'))
    print(value_low['total_restamping_done__min'])
    try:
        value_low = Employee_Analysis_month.objects.filter(
            total_restamping_done=value_low['total_restamping_done__min']).order_by('id').first()
    except:
        pass
    context = {

        'this_lis_date': this_lis_date,
        'this_lis_sum': this_lis_sum,
        'value': value,
        'value_low': value_low,

    }
    # print("value['total_restamping_done__max']")
    # print("value['total_restamping_done__max']")
    # print(value)
    # print(value_low)
    return render(request,'analytics/restamping_analytics.html',context)

def update_restamping_details(request,id):
    personal_id = Restamping_after_sales_service.objects.get(id=id)
    restamp_product_list = Restamping_Product.objects.filter(restamping_id=id)
    # customer_id = Restamping_after_sales_service.objects.get(id=id).crm_no
    customer_id = Customer_Details.objects.get(id=personal_id.crm_no)

    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        company_name = request.POST.get('company_name')
        address = request.POST.get('customer_address')
        contact_no = request.POST.get('contact_no')
        customer_email_id = request.POST.get('customer_email_id')

        item2 = customer_id

        item2.contact_no = contact_no
        item2.customer_name = customer_name
        item2.save(update_fields=['customer_name', 'contact_no']) #new3


        if company_name != '':
            item2.company_name = company_name
            item2.save(update_fields=['company_name'])
        if address != '':
            item2.address = address
            item2.save(update_fields=['address'])

        if customer_email_id != '':
            item2.customer_email_id = customer_email_id
            item2.save(update_fields=['customer_email_id'])

        total_amount = request.POST.get('total_amount')
        # second_person=request.POST.get('second_person')
        # third_person=request.POST.get('third_person')
        # second_contact_no=request.POST.get('second_contact_no')
        # third_contact_no=request.POST.get('third_contact_no')
        # address = request.POST.get('address')
        # today_date = request.POST.get('today_date')
        # mobile_no = request.POST.get('mobile_no')
        # new_serial_no = request.POST.get('new_serial_no')
        # brand = request.POST.get('brand')
        scale_delivery_date = request.POST.get('scale_delivery_date')








        item = personal_id

        # item.restampingno = restampingno
        # item.address = address
        # item.total_amount = total_amount
        # item.mobile_no = mobile_no
        # item.new_serial_no = new_serial_no
        # item.brand = brand
        # item.second_person=second_person
        # item.third_person=third_person
        # item.second_contact_no=second_contact_no
        # item.third_contact_no=third_contact_no
        item.second_person=customer_name   #new4
        item.second_contact_no=contact_no   #new5

        item.scale_delivery_date = scale_delivery_date

        current_stage_in_db = Restamping_after_sales_service.objects.get(
            id=id).current_stage  # updatestage2

        if (current_stage_in_db == 'Restamping is done but scale is not collected') and (
                scale_delivery_date != '' or scale_delivery_date != None):
            Restamping_after_sales_service.objects.filter(id=id).update(
                current_stage='Restamping done and scale also collected')


        # item.save(update_fields=['total_amount', ]),
        # item.save(update_fields=['new_serial_no', ]),
        # item.save(update_fields=['brand', ]),
        item.save(update_fields=['scale_delivery_date','second_person','second_contact_no', ]),

        personal_id = Restamping_after_sales_service.objects.get(id=id)
        restamp_product_list = Restamping_Product.objects.filter(restamping_id=id)

        context = {
            'personal_id': personal_id,
            'restamp_product_list': restamp_product_list,

        }

        return render(request, 'update_forms/update_restamping_form.html', context)

    context = {
        'personal_id': personal_id,
        'restamp_product_list': restamp_product_list,
    }

    return render(request,'update_forms/update_restamping_form.html',context)

def report_restamping(request):
    if request.method == 'POST' or None:
        selected_list = request.POST.getlist('checks[]')
        repair_start_date = request.POST.get('date1')
        repair_end_date = request.POST.get('date2')
        repair_string = ','.join(selected_list)

        request.session['start_date'] = repair_start_date
        request.session['repair_end_date'] = repair_end_date
        request.session['repair_string'] = repair_string
        request.session['selected_list'] = selected_list
        return redirect('/final_report_restamping/')
    return render(request, "report/report_restamping_form.html",)

def final_report_restamping(request):
    restamp_start_date = str(request.session.get('repair_start_date'))
    restamp_end_date = str(request.session.get('repair_end_date'))
    restamp_string = request.session.get('repair_string')
    selected_list = request.session.get('selected_list')

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT  " + restamp_string + " from restamping_app_restamping_after_sales_service , customer_app_customer_details"
                                         "  where restamping_app_restamping_after_sales_service.crm_no_id = customer_app_customer_details.id and entry_timedate between '" + restamp_start_date + "' and '" + restamp_end_date + "';")
        row = cursor.fetchall()
        final_row = [list(x) for x in row]
        repairing_data = []
        for i in row:
            repairing_data.append(list(i))

    try:
        del request.session['repair_start_date']
        del request.session['repair_end_date']
        del request.session['repair_string']
        del request.session['selected_list']
    except:
        pass

    context = {
        'final_row': final_row,
        'selected_list': selected_list,
    }
    return render(request,"report/final_report_restamp_mod_form.html",context)

def restamping_employee_graph(request,user_id):
    from django.db.models import Sum


    #current month
    mon = datetime.now().month
    this_month = Employee_Analysis_date.objects.filter(user_id=user_id,entry_date__month=mon).values('entry_date',
                                                                                                         'total_restamping_done_today')
    this_lis_date = []
    this_lis_sum = []
    for i in this_month:
        x = i
        this_lis_date.append(x['entry_date'].strftime('%Y-%m-%d'))
        this_lis_sum.append(x['total_restamping_done_today'])

    # previous month sales
    mon = (datetime.now().month) - 1
    previous_month = Employee_Analysis_date.objects.filter(user_id=user_id,entry_date__month=mon).values('entry_date',
                                                                                                         'total_restamping_done_today')
    previous_lis_date = []
    previous_lis_sum = []
    for i in previous_month:
        x = i
        previous_lis_date.append(x['entry_date'].strftime('%Y-%m-%d'))
        previous_lis_sum.append(x['total_restamping_done_today'])

    if request.method == 'POST':
        start_date = request.POST.get('date1')
        end_date = request.POST.get('date2')
        qs = Employee_Analysis_date.objects.filter(user_id=user_id,entry_date__range=(start_date, end_date)).values('entry_date',
                                                                                                         'total_restamping_done_today')
        lis_date = []
        lis_sum = []
        for i in qs:
            x = i
            lis_date.append(x['entry_date'].strftime('%Y-%m-%d'))
            lis_sum.append(x['total_restamping_done_today'])

        context = {
            'final_list': lis_date,
            'final_list2': lis_sum,
            'previous_lis_date': previous_lis_date,
            'previous_lis_sum': previous_lis_sum,
            'this_lis_date': this_lis_date,
            'this_lis_sum': this_lis_sum,
            # 'rep_feedback': rep_feedback,
            # 'feeback': feeback,
        }
        return render(request, "graphs/restamping_employee_graph.html", context)
    else:

        qs = Employee_Analysis_date.objects.filter(user_id=user_id,entry_date__month=datetime.now().month).values(
            'entry_date', 'total_restamping_done_today')
        lis_date = []
        lis_sum = []
        for i in qs:
            x = i
            lis_date.append(x['entry_date'].strftime('%Y-%m-%d'))
            lis_sum.append(x['total_restamping_done_today'])
        print(lis_date)
        print(lis_sum)

        # user_id=request.user.pk
        # currentMonth = datetime.now().month
        # currentYear = datetime.now().year
        # list_sales=Employee_Analysis_month.objects.filter(year=currentYear,user_id=user_id).values_list('month')
        # list_sales_month=Employee_Analysis_month.objects.filter(year=currentYear,user_id=user_id).values_list('total_sales_done')
        # # list_sales=Employee_Analysis.objects.filter(year=currentYear,user_id=user_id).values_list('total_sales_done')
        # print(list(list_sales_month))
        # print(list(list_sales))
        # final_list=[]
        # final_list2=[]
        # for item in list_sales:
        #     final_list.append(item[0])
        #
        # for item in list_sales_month:
        #     final_list2.append(item[0])
        #
        # print(final_list)
        # print(final_list2)
        context = {
            'final_list': lis_date,
            'final_list2': lis_sum,
            'previous_lis_date': previous_lis_date,
            'previous_lis_sum': previous_lis_sum,
            'this_lis_date': this_lis_date,
            'this_lis_sum': this_lis_sum,
            # 'target_achieved': target_achieved,
            # 'feeback': feeback,
        }
    return render(request, "graphs/restamping_employee_graph.html", context)


def update_restamping_product(request,id):
    restamping_product = Restamping_Product.objects.get(id=id)
    restamping_id = Restamping_Product.objects.get(id=id).restamping_id

    if request.method == 'POST':
        # customer_email_id = request.POST.get('customer_email_id')
        # product_to_stampped = request.POST.get('product_to_stampped')
        scale_type = request.POST.get('scale_type')
        sub_model = request.POST.get('sub_model')
        capacity = request.POST.get('capacity')
        old_serial_no = request.POST.get('old_serial_no')
        brand = request.POST.get('brand')
        amount = request.POST.get('amount')
        new_sr_no = request.POST.get('new_sr_no')


        # product_id = Restamping_Product.objects.get(id=id)
        restamping_id = Restamping_after_sales_service.objects.get(id=restamping_id.pk).pk
        cost2 = restamping_product.amount


        Restamping_after_sales_service.objects.filter(id=restamping_id).update(total_amount=F("total_amount") - cost2)
        Employee_Analysis_month.objects.filter(user_id=request.user.pk, entry_date__month=datetime.now().month,
                                               year=datetime.now().year).update(
            total_restamping_done=F("total_restamping_done") - cost2)

        Employee_Analysis_date.objects.filter(user_id=request.user.pk, entry_date__month=datetime.now().month,
                                              year=datetime.now().year).update(
            total_restamping_done_today=F("total_restamping_done_today") - cost2)

        current_stage_in_db = Restamping_after_sales_service.objects.get(
            id=restamping_id).current_stage  # updatestage2
        if (current_stage_in_db == '' or current_stage_in_db == None) and (sub_model != '' or sub_model != None):
            Restamping_after_sales_service.objects.filter(id=restamping_id).update(
                current_stage='Scales in Restamping Queue')
        if (current_stage_in_db == 'Scales in Restamping Queue') and (new_sr_no != '' or new_sr_no != None):
            Restamping_after_sales_service.objects.filter(id=restamping_id).update(
                current_stage='Restamping is done but scale is not collected')
        if (current_stage_in_db == 'Restamping is done but scale is not collected') and (new_sr_no != '' or new_sr_no != None):
            Restamping_after_sales_service.objects.filter(id=restamping_id).update(
                current_stage='Restamping is done but scale is not collected')

        item = restamping_product
        item.new_sr_no = new_sr_no

        # item.restamping_id_id = restamping_id
        # item.customer_email_id = customer_email_id
        # item.product_to_stampped = product_to_stampped
        item.scale_type = scale_type
        item.sub_model = sub_model
        item.capacity = capacity
        item.old_serial_no = old_serial_no
        item.brand = brand
        item.amount = amount
        # item.user_id = SiteUser.objects.get(id=request.user.pk)
        # item.manager_id = SiteUser.objects.get(id=request.user.pk).group



        item.save(update_fields=['scale_type','sub_model','capacity','old_serial_no','brand',
                                 'amount','new_sr_no', ])




        Restamping_after_sales_service.objects.filter(id=restamping_id).update(total_amount=F("total_amount") + amount)
        Employee_Analysis_month.objects.filter(user_id=request.user.pk, entry_date__month=datetime.now().month,
                                               year=datetime.now().year).update(
            total_restamping_done=F("total_restamping_done") + amount)

        Employee_Analysis_date.objects.filter(user_id=request.user.pk, entry_date__month=datetime.now().month,
                                              year=datetime.now().year).update(
            total_restamping_done_today=F("total_restamping_done_today") + amount)
        print(cost2)
        print(cost2)
        print(amount)


        return redirect('/update_restamping_details/'+str(restamping_id))
    context = {
        'restamping_product_id': restamping_product,
    }

    return render(request,'update_forms/update_restamping_product.html',context)



def load_restamping_manager(request):
    selected = request.GET.get('loc_id')

    if selected=='true':
        user_list = Employee_Analysis_month.objects.filter(manager_id__icontains=request.user.name,user_id__is_deleted=False,user_id__modules_assigned__icontains='Restamping Module')
        # dispatch_list = Employee_Analysis_month.objects.filter(user_id__group=str(request.user.name))

        context = {
            'user_list': user_list,
            'manager': True,
        }

        return render(request, 'AJAX/load_restamping_manager.html', context)
    else:
        if check_admin_roles(request):     #For ADMIN
            restamp_list = Restamping_after_sales_service.objects.filter(user_id__group__icontains=request.user.group,user_id__is_deleted=False,user_id__modules_assigned__icontains='Restamping Module').order_by('-id')
        else:  #For EMPLOYEE
            restamp_list = Restamping_after_sales_service.objects.filter(user_id=request.user.pk).order_by('-id')
        # restamp_list = Restamping_after_sales_service.objects.all()

        context = {
            'restamp_list': restamp_list,
            'manager': False,

        }


        return render(request, 'AJAX/load_restamping_manager.html', context)

def load_restamping_stages_list(request,):

    selected_stage = request.GET.get('selected_stage')

    restamp_list = Restamping_after_sales_service.objects.filter(Q(user_id=request.user.pk)|Q(user_id__manager=request.user.name)|Q(user_id__admin=request.user.name)|Q(user_id__super_admin=request.user.name),current_stage=selected_stage)

    context = {
        'restamp_list': restamp_list,
    }
    context.update(context)
    return render(request, 'AJAX/load_restamping_stage.html', context)














