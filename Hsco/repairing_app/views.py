from django.db import connection
from django.db.models import Min, Sum, Q, F
from django.http import HttpResponse
from django.shortcuts import render, redirect
from customer_app.models import Customer_Details
from django.utils import timezone
from user_app.models import SiteUser

from customer_app.models import Customer_Details

from purchase_app.views import check_admin_roles
from .forms import Repairing_Feedback_Form
from .models import Repairing_after_sales_service, Repairing_Product, Repairing_Feedback
from django.core.mail import send_mail
from Hsco import settings
import datetime
import requests
import json
from datetime import datetime
from ess_app.models import Employee_Analysis_month, Employee_Analysis_date


def add_repairing_details(request):
    cust_sugg=Customer_Details.objects.all()
    prev_rep_sugg=Repairing_after_sales_service.objects.all()
    if request.user.role == 'Super Admin' or request.user.role == 'Admin' or request.user.role == 'Manager':
        user_list=SiteUser.objects.filter(group__icontains=request.user.name,modules_assigned__icontains='Repairing Module', is_deleted=False)
    else: #display colleague
        list_group = SiteUser.objects.get(id=request.user.id).group
        import ast

        x = "[" + list_group + "]"
        x = ast.literal_eval(x)
        manager_list = []
        for item in x:
            name = SiteUser.objects.get(name=item)
            if name.role == 'Manager':
                if item not in manager_list:
                    manager_list.append(item)

        user_list = SiteUser.objects.filter(group__icontains=manager_list,
                                            modules_assigned__icontains='Repairing Module', is_deleted=False)





    if request.method == 'POST' or request.method == 'FILES':
        customer_name = request.POST.get('customer_name')
        company_name = request.POST.get('company_name')
        address = request.POST.get('customer_address')
        contact_no = request.POST.get('contact_no')
        customer_email_id = request.POST.get('customer_email_id')




        # repairingnumber = request.POST.get('repairingnumber')
        previous_repairing_number = request.POST.get('previous_repairing_number')
        in_warranty = request.POST.get('in_warranty')
        today_date = request.POST.get('today_date')
        location = request.POST.get('location')
        # products_to_be_repaired = request.POST.get('products_to_be_repaired')

        total_cost = 0.0

        informed_on = request.POST.get('informed_on')


        informed_by = request.POST.get('informed_by')
        confirmed_estimate = request.POST.get('confirmed_estimate')
        repaired = request.POST.get('repaired')
        delivery_by = request.POST.get('delivery_by')
        feedback_given = request.POST.get('feedback_given')
        current_stage = request.POST.get('current_stage')
        repaired_by = request.POST.get('repaired_by')

        item2 = Repairing_after_sales_service()

        item = Customer_Details()
        if Customer_Details.objects.filter(customer_name=customer_name,contact_no=contact_no).count() > 0:

            item2.crm_no = Customer_Details.objects.filter(customer_name=customer_name,contact_no=contact_no).first()
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
            if company_name != '':
                item.company_name = company_name
            if address != '':
                item.address = address
            item.contact_no = contact_no
            if customer_email_id != '':
                item.customer_email_id = customer_email_id
            # item.user_id = SiteUser.objects.get(id=request.user.pk)
            # item.manager_id = SiteUser.objects.get(id=request.user.pk).group
            try:
                item.save()
                item2.crm_no = Customer_Details.objects.get(id=item.pk)
            except:
                pass

        item2.previous_repairing_number = previous_repairing_number
        item2.in_warranty = in_warranty
        item2.today_date = today_date

        item2.location = location
        # item2.products_to_be_repaired = products_to_be_repaired

        item2.total_cost = 0.0
        if informed_on != '':
            item2.informed_on = informed_on

        item2.informed_by = informed_by
        item2.confirmed_estimate = confirmed_estimate
        item2.repaired = repaired
        item2.delivery_by = delivery_by
        item2.repaired_by = repaired_by
        item2.feedback_given = False
        item2.user_id = SiteUser.objects.get(id=request.user.pk)
        item2.manager_id = SiteUser.objects.get(id=request.user.pk).group
        item2.current_stage = current_stage


        item2.save()

        if Employee_Analysis_date.objects.filter(Q(entry_date=datetime.now().date()),
                                                 Q(user_id=SiteUser.objects.get(id=request.user.pk))).count() > 0:
            Employee_Analysis_date.objects.filter(user_id=request.user.pk, entry_date__month=datetime.now().month,
                                                  year=datetime.now().year).update(
                total_reparing_done_today=F("total_reparing_done_today") + total_cost)
            # ead.total_sales_done_today=.filter(category_id_id=id).update(total_views=F("total_views") + value_of_goods)

            # ead.save(update_fields=['total_sales_done_today'])

        else:
            ead = Employee_Analysis_date()
            ead.user_id = SiteUser.objects.get(id=request.user.pk)
            ead.total_reparing_done_today = total_cost
            ead.manager_id = SiteUser.objects.get(id=request.user.pk).group

            ead.month = datetime.now().month
            ead.year = datetime.now().year
            ead.save()

        if Employee_Analysis_month.objects.filter(Q(entry_date__month=datetime.now().month),
                                                  Q(user_id=SiteUser.objects.get(id=request.user.pk))).count() > 0:
            Employee_Analysis_month.objects.filter(user_id=request.user.pk, entry_date__month=datetime.now().month,
                                                   year=datetime.now().year).update(
                total_reparing_done=F("total_reparing_done") + total_cost)
            # ead.total_sales_done_today=.filter(category_id_id=id).update(total_views=F("total_views") + value_of_goods)

            # ead.save(update_fields=['total_sales_done_today'])

        else:
            ead = Employee_Analysis_month()
            ead.user_id = SiteUser.objects.get(id=request.user.pk)
            ead.total_reparing_done = total_cost
            ead.manager_id = SiteUser.objects.get(id=request.user.pk).group

            ead.month = datetime.now().month
            ead.year = datetime.now().year
            ead.save()


        if Customer_Details.objects.filter(Q(customer_name=customer_name),Q(contact_no=contact_no)).count() > 0:
            crm_no = Customer_Details.objects.filter(Q(customer_name=customer_name),Q(contact_no=contact_no)).first()
            try:
                send_mail('Feedback Form',
                      'Click on the link to give feedback http://vikka.pythonanywhere.com/feedback_repairing/' + str(
                          request.user.pk) + '/' + str(crm_no.pk) + '/' + str(item2.id), settings.EMAIL_HOST_USER,
                      [crm_no.customer_email_id])
            except:
                pass

            message = 'Click on the link to give feedback http://vikka.pythonanywhere.com/feedback_repairing/' + str(
                request.user.pk) + '/' + str(crm_no.pk) + '/' + str(item2.id)

            url = "http://smshorizon.co.in/api/sendsms.php?user=" + settings.user + "&apikey=" + settings.api + "&mobile=" + crm_no.contact_no + "&message=" + message + "&senderid=" + settings.senderid + "&type=txt"
            payload = ""
            headers = {'content-type': 'application/x-www-form-urlencoded'}

            response = requests.request("GET", url, data=json.dumps(payload), headers=headers)
            x = response.text
        else:
            try:

                send_mail('Feedback Form',
                      'Click on the link to give feedback http://vikka.pythonanywhere.com/feedback_repairing/' + str(
                          request.user.pk) + '/' + str(item.pk) + '/' + str(item2.id), settings.EMAIL_HOST_USER,
                      [item.customer_email_id])
            except:
                pass

            message = 'Click on the link to give feedback http://vikka.pythonanywhere.com/feedback_repairing/' + str(
                request.user.pk) + '/' + str(item.pk) + '/' + str(item2.id)

            url = "http://smshorizon.co.in/api/sendsms.php?user=" + settings.user + "&apikey=" + settings.api + "&mobile=" + item.contact_no + "&message=" + message + "&senderid=" + settings.senderid + "&type=txt"
            payload = ""
            headers = {'content-type': 'application/x-www-form-urlencoded'}

            response = requests.request("GET", url, data=json.dumps(payload), headers=headers)
            x = response.text



        return redirect('/repair_product/'+str(item2.id))


    context={
        'cust_sugg':cust_sugg,
        'user_list':user_list,
        'prev_rep_sugg':prev_rep_sugg,
    }

    return render(request,'forms/rep_mod_form.html',context)

def repair_product(request,id):
    repair_id = Repairing_after_sales_service.objects.get(id=id).id

    if request.method=='POST':
        type_of_machine = request.POST.get('type_of_machine')
        model = request.POST.get('model')
        sub_model = request.POST.get('sub_model')
        problem_in_scale = request.POST.get('problem_in_scale')
        components_replaced_in_warranty = request.POST.get('components_replaced_in_warranty')
        components_replaced = request.POST.get('components_replaced')
        replaced_scale_given = request.POST.get('replaced_scale_given')
        Replaced_scale_serial_no = request.POST.get('Replaced_scale_serial_no')
        deposite_taken_for_replaced_scale = request.POST.get('deposite_taken_for_replaced_scale')
        cost = request.POST.get('cost')
        in_warranty = request.POST.get('in_warranty')

        item=Repairing_Product()
        item.user_id = SiteUser.objects.get(id=request.user.pk)
        item.manager_id = SiteUser.objects.get(id=request.user.pk).group

        item.type_of_machine = type_of_machine
        item.model = model
        item.sub_model = sub_model
        item.problem_in_scale = problem_in_scale
        item.components_replaced_in_warranty = components_replaced_in_warranty
        item.components_replaced = components_replaced
        item.replaced_scale_given = replaced_scale_given
        item.Replaced_scale_serial_no = Replaced_scale_serial_no
        item.deposite_taken_for_replaced_scale = deposite_taken_for_replaced_scale
        item.repairing_id_id = repair_id
        item.in_warranty = in_warranty

        item.cost = cost

        item.save()

        Repairing_after_sales_service.objects.filter(id=id).update(total_cost=F("total_cost") + cost)
        Employee_Analysis_month.objects.filter(user_id=request.user.pk, entry_date__month=datetime.now().month,
                                               year=datetime.now().year).update(
            total_reparing_done=F("total_reparing_done") + cost)

        Employee_Analysis_date.objects.filter(user_id=request.user.pk, entry_date__month=datetime.now().month,
                                              year=datetime.now().year).update(
            total_reparing_done_today=F("total_reparing_done_today") + cost)

        return redirect('/update_repairing_details/'+str(id))
    context = {
        'repair_id': repair_id,
    }
    return render(request,'dashboardnew/repair_product.html',context)

def update_repairing_details(request,id):
    repair_id = Repairing_after_sales_service.objects.get(id=id)
    # customer_id = Repairing_after_sales_service.objects.get(id=id).crm_no
    customer_id = Customer_Details.objects.get(id=repair_id.crm_no)
    repair_list = Repairing_Product.objects.filter(repairing_id=id)
    if request.method=='POST':
        customer_name = request.POST.get('customer_name')
        company_name = request.POST.get('company_name')
        address = request.POST.get('customer_address')
        contact_no = request.POST.get('contact_no')
        customer_email_id = request.POST.get('customer_email_id')

        item = customer_id

        item.customer_name = customer_name
        item.contact_no = contact_no

        if company_name != '':
            item.company_name = company_name
            item.save(update_fields=['company_name'])
        if address != '':
            item.address = address
            item.save(update_fields=['address'])

        if customer_email_id != '':
            item.customer_email_id = customer_email_id
            item.save(update_fields=['customer_email_id'])



        # repairingnumber = request.POST.get('repairingnumber')
        # previous_repairing_number = request.POST.get('previous_repairing_number')
        # today_date = request.POST.get('today_date')
        # location = request.POST.get('location')
        # products_to_be_repaired = request.POST.get('products_to_be_repaired')
        total_cost = request.POST.get('total_cost')
        informed_on = request.POST.get('informed_on')
        informed_by = request.POST.get('informed_by')
        confirmed_estimate = request.POST.get('confirmed_estimate')
        repaired = request.POST.get('repaired')
        repaired_date = request.POST.get('repaired_date')
        delivery_date = request.POST.get('delivery_date')
        delivery_by = request.POST.get('delivery_by')
        repaired_by = request.POST.get('repaired_by')
        # feedback_given = request.POST.get('feedback_given')
        current_stage = request.POST.get('current_stage')

        item2 = repair_id

        # item2.repairingnumber = repairingnumber
        item2.crm_no = Customer_Details.objects.get(id=item.pk)

        # item2.previous_repairing_number = previous_repairing_number
        # item2.today_date = today_date

        # item2.location = location
        # item2.products_to_be_repaired = products_to_be_repaired

        # item2.total_cost = total_cost
        if informed_on != '':

            item2.informed_on = informed_on
            item2.save(update_fields=['informed_on', ]),
        item2.informed_by = informed_by
        item2.confirmed_estimate = confirmed_estimate
        item2.repaired = repaired
        item2.repaired_date = repaired_date
        item2.delivery_date = delivery_date
        item2.delivery_by = delivery_by
        item2.repaired_by = repaired_by
        # item2.feedback_given = feedback_given
        item2.current_stage = current_stage
        item2.stage_update_timedate = timezone.now()

        # item2.save()

        # item2.save(update_fields=['repairingnumber', ]),
        # item2.save(update_fields=['previous_repairing_number', ]),
        # item2.save(update_fields=['today_date', ]),
        # item2.save(update_fields=['products_to_be_repaired', ]),
        # item2.save(update_fields=['total_cost', ]),

        item2.save(update_fields=['informed_by', ]),
        item2.save(update_fields=['confirmed_estimate', ]),
        item2.save(update_fields=['repaired', ]),
        item2.save(update_fields=['repaired_date', ]),
        item2.save(update_fields=['delivery_date', ]),
        item2.save(update_fields=['delivery_by', ]),
        item2.save(update_fields=['repaired_by', ]),
        # item2.save(update_fields=['feedback_given', ])
        item2.save(update_fields=['current_stage', ])
        item2.save(update_fields=['stage_update_timedate', ])
        repair_id = Repairing_after_sales_service.objects.get(id=id)
        customer_id = Repairing_after_sales_service.objects.get(id=id).crm_no
        customer_id = Customer_Details.objects.get(id=customer_id)
        repair_list = Repairing_Product.objects.filter(repairing_id=id)
        context = {
            'repair_list': repair_list,
            'repair_id': repair_id,
            'customer_id': customer_id,
        }
        return render(request, 'update_forms/update_rep_mod_form.html', context)

    print(repair_list)
    context={
        'repair_list': repair_list,
        'repair_id': repair_id,
        'customer_id':customer_id,

    }
    return render(request,'update_forms/update_rep_mod_form.html',context)

def repairing_module_home(request):
    from django.db.models import Count
    from django.db.models import Q



    if request.method == 'POST':
        if'submit1' in request.POST:
            start_date = request.POST.get('date1')
            end_date = request.POST.get('date2')
            if check_admin_roles(request):  # For ADMIN
                repair_list = Repairing_after_sales_service.objects.filter(user_id__group__icontains=request.user.group,
                                                                           user_id__is_deleted=False,entry_timedate__range=[start_date, end_date]).order_by('-id')
            else:  # For EMPLOYEE
                repair_list = Repairing_after_sales_service.objects.filter(user_id=request.user.pk,entry_timedate__range=[start_date, end_date]).order_by('-id')
            # repair_list = Repairing_after_sales_service.objects.filter(entry_timedate__range=[start_date, end_date])
            context = {
                'repair_list': repair_list,
            }
            return render(request, 'dashboardnew/repairing_module_home.html', context)
        elif 'submit2' in request.POST:
            contact = request.POST.get('contact')
            if check_admin_roles(request):  # For ADMIN
                repair_list = Repairing_after_sales_service.objects.filter(user_id__group__icontains=request.user.group,
                                                                           user_id__is_deleted=False,crm_no__contact_no=contact).order_by('-id')
            else:  # For EMPLOYEE
                repair_list = Repairing_after_sales_service.objects.filter(user_id=request.user.pk,crm_no__contact_no=contact).order_by('-id')
            # repair_list = Repairing_after_sales_service.objects.filter(phone_no=contact)
            context = {
                'repair_list': repair_list,
            }
            return render(request, 'dashboardnew/repairing_module_home.html', context)

        elif 'submit3' in request.POST:
            email = request.POST.get('email')
            if check_admin_roles(request):  # For ADMIN
                repair_list = Repairing_after_sales_service.objects.filter(user_id__group__icontains=request.user.group,
                                                                           user_id__is_deleted=False,crm_no__customer_email_id=email).order_by('-id')
            else:  # For EMPLOYEE
                repair_list = Repairing_after_sales_service.objects.filter(user_id=request.user.pk,crm_no__customer_email_id=email).order_by('-id')
            # repair_list = Repairing_after_sales_service.objects.filter(customer_email_id=email)
            context = {
                'repair_list': repair_list,
            }
            return render(request, 'dashboardnew/repairing_module_home.html', context)
        elif 'submit4' in request.POST:
            customer = request.POST.get('customer')
            if check_admin_roles(request):  # For ADMIN
                repair_list = Repairing_after_sales_service.objects.filter(user_id__group__icontains=request.user.group,
                                                                           user_id__is_deleted=False,crm_no__customer_name=customer).order_by('-id')
            else:  # For EMPLOYEE
                repair_list = Repairing_after_sales_service.objects.filter(user_id=request.user.pk,crm_no__customer_name=customer).order_by('-id')
            # repair_list = Repairing_after_sales_service.objects.filter(name=customer)
            context = {
                'repair_list': repair_list,
            }
            return render(request, 'dashboardnew/repairing_module_home.html', context)

        elif  'submit5' in request.POST:
            company = request.POST.get('company')
            if check_admin_roles(request):  # For ADMIN
                repair_list = Repairing_after_sales_service.objects.filter(user_id__group__icontains=request.user.group,
                                                                           user_id__is_deleted=False,crm_no__company_name=company).order_by('-id')
            else:  # For EMPLOYEE
                repair_list = Repairing_after_sales_service.objects.filter(user_id=request.user.pk,crm_no__company_name=company).order_by('-id')
            # repair_list = Repairing_after_sales_service.objects.filter(company_name=company)
            context = {
                'repair_list': repair_list,
            }
            return render(request, 'dashboardnew/repairing_module_home.html', context)
        elif request.method=='POST' and 'submit6' in request.POST:
            crm = request.POST.get('crm')
            if check_admin_roles(request):  # For ADMIN
                repair_list = Repairing_after_sales_service.objects.filter(user_id__group__icontains=request.user.group,
                                                                           user_id__is_deleted=False,crm_no__pk=crm).order_by('-id')
            else:  # For EMPLOYEE
                repair_list = Repairing_after_sales_service.objects.filter(user_id=request.user.pk,crm_no__pk=crm).order_by('-id')
            # repair_list = Repairing_after_sales_service.objects.filter(crn_number=crm)
            context = {
                'repair_list': repair_list,
            }
            return render(request, 'dashboardnew/repairing_module_home.html', context)
    else:
        if check_admin_roles(request):     #For ADMIN
            repair_list = Repairing_after_sales_service.objects.filter(user_id__group__icontains=request.user.group,user_id__is_deleted=False).order_by('-id')
        else:  #For EMPLOYEE
            repair_list = Repairing_after_sales_service.objects.filter(user_id=request.user.pk).order_by('-id')
        # repair_list = Repairing_after_sales_service.objects.all()
        res = Repairing_after_sales_service.objects.filter(~Q(delivery_by=None)).values('current_stage').annotate(
            dcount=Count('current_stage'))
        context = {
            'repair_list': repair_list,

        }
        from datetime import datetime, timedelta

        # Using current time
        ini_time_for_now = datetime.now()

        new_final_time = ini_time_for_now - timedelta(days=4)
        res_4d = Repairing_after_sales_service.objects.filter(Q(stage_update_timedate=new_final_time)).values('current_stage').annotate(
            dcount=Count('current_stage'))
        try:
            x = res_4d
            # if x['current_stage'] == 'Scale is collected but estimate is not given':
            rep4_4d = x['dcount']
            context4d = {
                'rep4_4d': rep4_4d,
            }
            context.update(context4d)
        except:
            pass

        new_final_time = ini_time_for_now - timedelta(days=10)
        res_10d = Repairing_after_sales_service.objects.filter(Q(stage_update_timedate=new_final_time)).values('current_stage').annotate(dcount=Count('current_stage'))
        x = res_10d
        # if x['current_stage'] == 'Scale is collected but estimate is not given':
        try:
            rep4_10d = x['dcount']
            context10d = {
                'rep4_10d': rep4_10d,
            }
            context.update(context10d)
        except:
            pass
        print(res)

        for i in res:
            x = i
            if x['current_stage'] == 'Scale is collected but estimate is not given':
                rep1 = x['dcount']
                context1 = {
                    'rep1': rep1,
                }
                context.update(context1)

            if x['current_stage'] == 'Estimate is given but Estimate is not confirmed':
                rep2 = x['dcount']
                context2 = {

                  'rep2': rep2,

                }
                context.update(context2)
            if x['current_stage'] == 'Estimate is confirmed but not repaired':
                rep3 = x['dcount']
                context3 = {

                    'rep3': rep3,

                }
                context.update(context3)
            if x['current_stage'] == 'Repaired but not collected':
                rep4 = x['dcount']
                context4 = {

                    'rep4': rep4,

                }
                context.update(context4)
            if x['current_stage'] == 'Finally Collected':
                rep5 = x['dcount']
                context5 = {

                    'rep5': rep5,
                }
                context.update(context5)



        print(context)
        print(context)
        return render(request, 'dashboardnew/repairing_module_home.html', context)

def manager_repairing_module_home(request):
    repair_employee_list = SiteUser.objects.all()
    context={
        'repair_employee_list':repair_employee_list,
    }
    return render(request,'dashboardnew/manager_repairing_module_home.html',context)


def repairing_analytics(request):
    mon = datetime.now().month
    this_month = Employee_Analysis_month.objects.all().values('entry_date').annotate(data_sum=Sum('total_reparing_done'))
    this_lis_date = []
    this_lis_sum = []
    for i in this_month:
        x = i
        this_lis_date.append(x['entry_date'].strftime("%B-%Y"))
        this_lis_sum.append(x['data_sum'])

    from django.db.models import Max
    # Generates a "SELECT MAX..." query
    value = Employee_Analysis_month.objects.aggregate(Max('total_reparing_done'))
    print(value['total_reparing_done__max'])
    try:
        value = Employee_Analysis_month.objects.get(total_sales_done=value['total_reparing_done__max'])
    except:
        pass

    value_low = Employee_Analysis_month.objects.aggregate(Min('total_reparing_done'))
    print(value_low['total_reparing_done__min'])
    try:
        value_low = Employee_Analysis_month.objects.filter(total_sales_done=value_low['total_reparing_done__min']).order_by('id').first()
    except:
        pass
    context = {

        'this_lis_date': this_lis_date,
        'this_lis_sum': this_lis_sum,
        'value': value,
        'value_low': value_low,

    }
    return render(request,'analytics/repairing_analytics.html',context)

def repairing_report_module(request):
    if request.method == 'POST' or None:
        selected_list = request.POST.getlist('checks[]')
        repair_start_date = request.POST.get('date1')
        repair_end_date = request.POST.get('date2')
        repair_string = ','.join(selected_list)
        request.session['start_date'] = repair_start_date
        request.session['repair_end_date'] = repair_end_date
        request.session['repair_string'] = repair_string
        request.session['selected_list'] = selected_list
        return redirect('/final_repairing_report_module/')
    return render(request,'report/report_rep_mod_form.html',)

def final_repairing_report_module(request):
    repair_start_date = str(request.session.get('repair_start_date'))
    repair_end_date = str(request.session.get('repair_end_date'))
    repair_string = request.session.get('repair_string')
    selected_list = request.session.get('selected_list')

    with connection.cursor() as cursor:
        cursor.execute("SELECT  " + repair_string + " from repairing_app_repairing_after_sales_service , customer_app_customer_details"
                                             "  where repairing_app_repairing_after_sales_service.crm_no_id = customer_app_customer_details.id and entry_timedate between '" + repair_start_date + "' and '" + repair_end_date + "';")
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
    return render(request,'report/final_report_rep_mod_form.html',context)

def feedback_repairing(request,user_id,customer_id,repairing_id):
    feedback_form = Repairing_Feedback_Form(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        satisfied_with_communication = request.POST.get('satisfied_with_communication')
        speed_of_performance = request.POST.get('speed_of_performance')
        price_of_reparing = request.POST.get('price_of_reparing')
        overall_interaction = request.POST.get('overall_interaction')
        about_hsco = request.POST.get('about_hsco')
        any_suggestion = request.POST.get('any_suggestion')

        item = Repairing_Feedback()
        item.satisfied_with_communication = satisfied_with_communication
        item.speed_of_performance = speed_of_performance
        item.price_of_reparing = price_of_reparing
        item.overall_interaction = overall_interaction
        item.about_hsco = about_hsco
        item.any_suggestion = any_suggestion
        item.user_id = SiteUser.objects.get(id=user_id)
        item.customer_id = Customer_Details.objects.get(id=customer_id)
        item.repairing_id = Repairing_after_sales_service.objects.get(id=repairing_id)
        try:
            item.save()

            repairing = Repairing_after_sales_service.objects.get(id=repairing_id)
            repairing .avg_feedback = (float(satisfied_with_communication) + float(speed_of_performance) + float(price_of_reparing) + float(overall_interaction)) / float(4.0)
            repairing.feedback_given = True
            repairing.save(update_fields=['avg_feedback', 'feedback_given'])
        except:
            pass
        return HttpResponse('Feedback Submitted!!!')
    context = {
        'feedback_form': feedback_form,
    }
    return render(request,'feedback/feedback_repairing.html',context)

def edit_product(request,id):
    product_id = Repairing_Product.objects.get(id=id)
    if request.method == 'POST':
        type_of_machine = request.POST.get('type_of_machine')
        model = request.POST.get('model')
        sub_model = request.POST.get('sub_model')
        problem_in_scale = request.POST.get('problem_in_scale')
        components_replaced = request.POST.get('components_replaced')
        components_replaced_in_warranty = request.POST.get('components_replaced_in_warranty')
        replaced_scale_given = request.POST.get('replaced_scale_given')
        Replaced_scale_serial_no = request.POST.get('Replaced_scale_serial_no')
        deposite_taken_for_replaced_scale = request.POST.get('deposite_taken_for_replaced_scale')
        in_warranty = request.POST.get('in_warranty')

        cost = request.POST.get('cost')

        product_id = Repairing_Product.objects.get(id=id)
        reparing_id = Repairing_after_sales_service.objects.get(
            id=Repairing_Product.objects.get(id=id).repairing_id.pk).pk
        cost2 = product_id.cost

        Repairing_after_sales_service.objects.filter(id=reparing_id).update(total_cost=F("total_cost") - cost2)

        Employee_Analysis_month.objects.filter(user_id=request.user.pk,
                                               entry_date__month=product_id.entry_timedate.month,
                                               year=product_id.entry_timedate.year).update(
            total_reparing_done=F("total_reparing_done") - cost2)

        Employee_Analysis_date.objects.filter(user_id=request.user.pk,
                                              entry_date__month=product_id.entry_timedate.month,
                                              year=product_id.entry_timedate.year).update(
            total_reparing_done_today=F("total_reparing_done_today") - cost2)



        item = product_id
        item.type_of_machine = type_of_machine
        item.model = model
        item.sub_model = sub_model
        item.problem_in_scale = problem_in_scale
        item.components_replaced = components_replaced
        item.components_replaced_in_warranty = components_replaced_in_warranty
        item.replaced_scale_given = replaced_scale_given
        item.Replaced_scale_serial_no = Replaced_scale_serial_no
        item.deposite_taken_for_replaced_scale = deposite_taken_for_replaced_scale
        item.in_warranty = in_warranty

        item.cost = cost





        item.save(update_fields=['type_of_machine', ]),
        item.save(update_fields=['model', ]),
        item.save(update_fields=['sub_model', ]),
        item.save(update_fields=['problem_in_scale', ]),
        item.save(update_fields=['components_replaced', ]),
        item.save(update_fields=['components_replaced_in_warranty', ]),
        item.save(update_fields=['replaced_scale_given', ]),
        item.save(update_fields=['Replaced_scale_serial_no', ]),
        item.save(update_fields=['deposite_taken_for_replaced_scale', ]),
        item.save(update_fields=['cost', ]),
        item.save(update_fields=['in_warranty', ]),


        Repairing_after_sales_service.objects.filter(id=reparing_id).update(total_cost=F("total_cost") + cost)
        # Repairing_after_sales_service.objects.filter(id=reparing_id).update(total_cost=F("total_cost") + float(cost))
        # Repairing_after_sales_service.objects.filter(id=reparing_id).update(total_cost=F("total_cost") + 100.0)



        Employee_Analysis_month.objects.filter(user_id=request.user.pk,
                                               entry_date__month=product_id.entry_timedate.month,
                                               year=product_id.entry_timedate.year).update(
            total_reparing_done=F("total_reparing_done") + cost)

        Employee_Analysis_date.objects.filter(user_id=request.user.pk,
                                              entry_date__month=product_id.entry_timedate.month,
                                              year=product_id.entry_timedate.year).update(
            total_reparing_done_today=F("total_reparing_done_today") + cost)

        context = {
        'product_id': product_id,
        }

        return render(request, 'edit_product/edit_product_repair.html', context)

    context = {
            'product_id': product_id,
    }


    return render(request,'edit_product/edit_product_repair.html',context)

def repairing_employee_graph(request,user_id):
    # user_id=user_id
    currentMonth = datetime.now().month
    currentYear = datetime.now().year
    # list_sales=Employee_Analysis_month.objects.filter(year=currentYear,user_id=user_id).values_list('month')
    # list_sales_month=Employee_Analysis_month.objects.filter(year=currentYear,user_id=user_id).values_list('total_reparing_done')
    # # list_sales=Employee_Analysis.objects.filter(year=currentYear,user_id=user_id).values_list('total_sales_done')
    # print(list(list_sales_month))
    # print(list(list_sales))
    # list_avg = Employee_Analysis_month.objects.filter(year=currentYear,user_id=user_id).values_list('avg_time_to_repair_single_scale')
    # list_total_restamp =Employee_Analysis_month.objects.filter(year=currentYear,user_id=user_id).values_list('avg_time_to_give_estimate')
    # final_list=[]
    # final_list2=[]
    # final_list3=[]
    # final_list4=[]
    # for item in list_sales:
    #     final_list.append(item[0])
    #
    # for item in list_sales_month:
    #     final_list2.append(item[0])
    #
    # for item in list_sales_month:
    #     final_list3.append(item[0])
    #
    # for item in list_sales_month:
    #     final_list4.append(item[0])
    # print(final_list)
    # print(final_list2)

    from django.db.models import Sum
    rep_feedback = Repairing_Feedback.objects.all()

    print(user_id)
    mon = datetime.now().month

    obj = Employee_Analysis_month.objects.get(user_id=user_id,entry_date__month=mon)
    obj.reparing_target_achived_till_now = (obj.total_reparing_done/obj.reparing_target_given)*100
    obj.save(update_fields=['reparing_target_achived_till_now'])
    #current month
    target_achieved =  obj.reparing_target_achived_till_now
    this_month = Employee_Analysis_date.objects.filter(user_id=user_id,entry_date__month=mon).values('entry_date',
                                                                                                     'total_reparing_done_today')

    this_lis_date = []
    this_lis_sum = []
    for i in this_month:
        x = i
        this_lis_date.append(x['entry_date'].strftime('%Y-%m-%d'))
        this_lis_sum.append(x['total_reparing_done_today'])

    # previous month sales

    mon = (datetime.now().month) - 1
    previous_month = Employee_Analysis_date.objects.filter(user_id=user_id,entry_date__month=mon).values('entry_date',
                                                                                                     'total_reparing_done_today')
    previous_lis_date = []
    previous_lis_sum = []
    for i in previous_month:
        x = i
        previous_lis_date.append(x['entry_date'].strftime('%Y-%m-%d'))
        previous_lis_sum.append(x['total_reparing_done_today'])

    if request.method == 'POST':
        start_date = request.POST.get('date1')
        end_date = request.POST.get('date2')
        qs = Employee_Analysis_date.objects.filter(user_id=user_id,entry_date__range=(start_date, end_date)).values('entry_date',
                                                                                                     'total_reparing_done_today')
        lis_date = []
        lis_sum = []
        for i in qs:
            x = i
            lis_date.append(x['entry_date'].strftime('%Y-%m-%d'))
            lis_sum.append(x['total_reparing_done_today'])


        context = {
            'final_list': lis_date,
            'final_list2': lis_sum,
            'previous_lis_date': previous_lis_date,
            'previous_lis_sum': previous_lis_sum,
            'this_lis_date': this_lis_date,
            'this_lis_sum': this_lis_sum,
            'rep_feedback': rep_feedback,
        }
        return render(request, "graphs/repairing_employee_graph.html", context)
    else:

        qs = Employee_Analysis_date.objects.filter(user_id=user_id,entry_date__month=datetime.now().month).values('entry_date',
                                                                                                     'total_reparing_done_today')
        lis_date = []
        lis_sum = []
        for i in qs:
            x=i
            lis_date.append(x['entry_date'].strftime('%Y-%m-%d'))
            lis_sum.append(x['total_reparing_done_today'])
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
        context={
            'final_list':lis_date,
            'final_list2':lis_sum,
            'previous_lis_date': previous_lis_date,
            'previous_lis_sum': previous_lis_sum,
            'this_lis_date': this_lis_date,
            'this_lis_sum': this_lis_sum,
            'target_achieved': target_achieved,
            'rep_feedback': rep_feedback,
            # 'feeback': feeback,
        }
        return render(request,"graphs/repairing_employee_graph.html",context)

def load_reparing_stages_list(request,):

    selected = request.GET.get('loc_id')
    locc_id = request.GET.get('strUser')
    print(selected)
    print(locc_id)
    print(locc_id)
    if selected == 'All':
        repair_list = Repairing_after_sales_service.objects.filter(current_stage=locc_id)
        print("True")
        print(repair_list)
    else:
        date= datetime.date.today()-datetime.timedelta(int(selected))
        repair_list = Repairing_after_sales_service.objects.filter(entry_timedate__range=[date,datetime.date.today()],current_stage=locc_id)
        print("False")
        print(date)
        print(datetime.date.today())
        print(repair_list)

    context = {
        'repair_list': repair_list,
    }
    context.update(context)
    return render(request, 'AJAX/load_reparing_stage.html', context)

def load_reparing_manager(request):
    selected = request.GET.get('loc_id')

    if selected=='true':
        user_list = Employee_Analysis_month.objects.filter(manager_id=request.user.name)
        # dispatch_list = Employee_Analysis_month.objects.filter(user_id__group=str(request.user.name))

        context = {
            'user_list': user_list,
            'manager': True,
        }

        return render(request, 'AJAX/load_reparing_manager.html', context)
    else:
        repair_list = Repairing_after_sales_service.objects.all()

        context = {
            'repair_list': repair_list,
            'manager': False,
        }

        return render(request, 'AJAX/load_reparing_manager.html', context)

def load_customer(request):
    cust_id = request.GET.get('item_id')

    cust_list = Customer_Details.objects.get(id=cust_id)

    context = {
        'cust_list': cust_list,

    }

    return render(request, 'AJAX/load_customer.html', context)

def load_prev_rep(request):
    rep_id = request.GET.get('item_id')

    rep_list = Repairing_after_sales_service.objects.get(id=rep_id)

    # cust_list = Customer_Details.objects.get(id=rep_list.crm_no)

    context = {
        'cust_list': rep_list,

    }

    return render(request, 'AJAX/load_prev_rep.html', context)








