from django.db import connection
from django.db.models import Sum, Min, Q, F, Count, Avg
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.http import HttpResponse
from django.shortcuts import render, redirect
from _datetime import datetime
from django.contrib.auth.decorators import login_required

from customer_app.models import Customer_Details, Log
from customer_app.models import type_purchase

from ess_app.models import Employee_Analysis_month

from user_app.models import SiteUser

from purchase_app.views import check_admin_roles

from ess_app.models import Defects_Warning
from .forms import add_Onsite_aftersales_service_form

from .forms import Onsite_Repairing_Feedback_Form
from .models import Onsite_aftersales_service, Onsite_Products, Onsite_Feedback
from django.core.mail import send_mail
from Hsco import settings
from ess_app.models import Employee_Analysis_month
from ess_app.models import Employee_Analysis_date
import requests
import json
from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from customer_app.models import Log

@receiver(pre_save, sender=Onsite_aftersales_service)
def dispatch_handler(sender, instance, update_fields=None, **kwargs):
    try:
        if instance.id == None or instance.id == '' or instance.id == 'None':
            #########for insert action##########
            new_instance = instance
            log = Log()
            print('somethibng')

            log.entered_by = instance.entered_by
            # log.entered_by = SiteUser.objects.get(id=new_instance.user_id_id).profile_name
            log.module_name = 'Onsite Repairing Module'
            log.action_type = 'Insert'
            log.table_name = 'Onsite_aftersales_service'

            log.reference = 'Onsite No: ' + str(new_instance.onsite_no)

            # log.action = old_list
            log.save()
        elif instance.id != None or instance.id !='' or instance.id !='None':
            print('somethibng')
            #########for update action##########
            old_instance = instance
            new_instance = Onsite_aftersales_service.objects.get(id=instance.id)
            print('somethibng')
            track = instance.tracker.changed()
            # string = ''
            # new_list = []
            # for key in track:
            #     new_list.append(key)
            #     string = string+str(key)+','
            #     print('New value:'+str(key) + old_instance.key)


            # with connection.cursor() as cursor:
                # if new_string != '' :
                #     print('something 1')
                #     new = Repairing_after_sales_service.objects.filter(id=instance.id).values(new_list)
                #     cursor.execute("SELECT " + (
                #                 new_string ) + " from  repairing_app_repairing_after_sales_service "
                #                                                                " where repairing_app_repairing_after_sales_service.repairing_no = '"+new_instance.repairing_no+"' ;")
            if  track:
                old_list = []
                for key, value in track.items():
                    old_list.append('Old value: ' + key )
                print('something')
                log = Log()

                log.entered_by = new_instance.entered_by
                log.module_name = 'Onsite Repairing Module'
                log.action_type = 'Update'
                log.table_name = 'Onsite_aftersales_service'

                log.reference = 'Onsite No: '+str(new_instance.onsite_no)

                log.action = old_list
                log.save()


    except:
        pass

@receiver(pre_save, sender=Onsite_Products)
def dispatch_handler(sender, instance, update_fields=None, **kwargs):
    try:
        if instance.id == None or instance.id == '' or instance.id == 'None' :
            #########for insert action##########
            new_instance = instance
            log = Log()
            dispatch = Onsite_Products.objects.get(id=new_instance.purchase_id_id)

            log.entered_by = dispatch.entered_by
            # log.entered_by = SiteUser.objects.get(id=new_instance.user_id_id).profile_name
            log.module_name = 'Onsite Repairing Module'
            log.action_type = 'Insert'
            log.table_name = 'Onsite_Products'

            log.reference = 'Onsite No: ' + str(dispatch.onsite_no)+ ', Product id:' +str(new_instance.id)

            # log.action = old_list
            log.save()
        elif instance.id != None or instance.id !='' or instance.id !='None':

            #########for update action##########
            old_instance = instance
            new_instance = Onsite_Products.objects.get(id=instance.id)

            track = instance.tracker.changed()
            # string = ''
            # new_list = []
            # for key in track:
            #     new_list.append(key)
            #     string = string+str(key)+','
            #     print('New value:'+str(key) + old_instance.key)


            # with connection.cursor() as cursor:
                # if new_string != '' :
                #     print('something 1')
                #     new = Repairing_after_sales_service.objects.filter(id=instance.id).values(new_list)
                #     cursor.execute("SELECT " + (
                #                 new_string ) + " from  repairing_app_repairing_after_sales_service "
                #                                                                " where repairing_app_repairing_after_sales_service.repairing_no = '"+new_instance.repairing_no+"' ;")
            if  track:
                old_list = []
                for key, value in track.items():
                    old_list.append('Old value: ' + key )
                log = Log()
                onsite = Onsite_aftersales_service.objects.get(id=new_instance.purchase_id_id)
                log.entered_by = onsite.entered_by
                log.module_name = 'Onsite Repairing Module'
                log.action_type = 'Update'
                log.table_name = 'Onsite_Products'
                log.reference = 'Onsite No: '+str(onsite.onsite_no) + ', Product id:' +str(new_instance.id)
                log.action = old_list
                log.save()


    except:
        pass

@receiver(pre_save, sender = Onsite_aftersales_service)
def onsite_handler(sender, instance, update_fields=None, **kwargs):
    try:
        new_instance = Onsite_aftersales_service.objects.get(id=instance.id)
        track = instance.tracker.changed()
        print(new_instance.key)
        print(instance.key)
        if track:
            old_list = []
            for key,value in track.items():
                print(new_instance.key)
                print(instance.key)
                if new_instance.key != instance.key:
                    print(value)
                    old_list.append('Old Value: ' + value)
            print(old_list)
            log = Log()

            log.entered_by = SiteUser.objects.get(id=new_instance.user_id_id).profile_name
            log.module_name = 'Onsite Repairing Module'
            log.action_type = 'Update'
            log.table_name = 'Onsite_aftersales_service'
            log.reference = 'Onsite No: '+str(new_instance.onsite_no)
            log.action = old_list
            log.save()
        # else:
        #     new_instance = Onsite_aftersales_service.objects.get(id=instance.id)
        #     log = Log()
        #     log.entered_by = SiteUser.objects.get(id=new_instance.user_id_id).profile_name
        #     log.module_name = 'Onsite Repairing Module'
        #     log.action_type = 'Insert'
        #     log.table_name = 'Onsite_aftersales_service'
        #     log.reference = 'Onsite No: ' + str(new_instance.onsite_no)
        #     log.action = ''
        #     log.save()
    except:
        pass

@login_required(login_url='/')
def onsite_views(request):

    if request.method=='POST' and 'deleted' not in request.POST:
        if'submit1' in request.POST:
            start_date = request.POST.get('date1')
            end_date = request.POST.get('date2')
            if check_admin_roles(request):  # For ADMIN
                onsite_list = Onsite_aftersales_service.objects.filter(user_id__group__icontains=request.user.name,
                                                                       user_id__is_deleted=False,entry_timedate__range=[start_date, end_date]).order_by('-onsite_no')
            else:  # For EMPLOYEE
                onsite_list = Onsite_aftersales_service.objects.filter(user_id=request.user.pk,entry_timedate__range=[start_date, end_date]).order_by('-onsite_no')

            # onsite_list = Onsite_aftersales_service.objects.filter(entry_timedate__range=[start_date, end_date])
            context = {
                'onsite_list': onsite_list,
                'search_msg': 'Search result for date range: ' + start_date + ' TO ' + end_date,
            }
            return render(request, "manager/onsite_reparing.html", context)
        elif 'submit2' in request.POST:
            contact = request.POST.get('contact')
            if check_admin_roles(request):  # For ADMIN
                onsite_list = Onsite_aftersales_service.objects.filter(user_id__group__icontains=request.user.name,
                                                                       user_id__is_deleted=False,second_contact_no__icontains=contact).order_by('-onsite_no')
            else:  # For EMPLOYEE
                onsite_list = Onsite_aftersales_service.objects.filter(user_id=request.user.pk,second_contact_no__icontains=contact).order_by('-onsite_no')
            # onsite_list = Onsite_aftersales_service.objects.filter(phone_no=contact)
            context = {
                'onsite_list': onsite_list,
                'search_msg': 'Search result for Customer Contact No: ' + contact,
            }
            return render(request, "manager/onsite_reparing.html", context)

        elif 'submit3' in request.POST:
            email = request.POST.get('email')
            if check_admin_roles(request):  # For ADMIN
                onsite_list = Onsite_aftersales_service.objects.filter(user_id__group__icontains=request.user.name,
                                                                       user_id__is_deleted=False,company_email=email).order_by('-onsite_no')
            else:  # For EMPLOYEE
                onsite_list = Onsite_aftersales_service.objects.filter(user_id=request.user.pk,company_email=email).order_by('-onsite_no')
            # onsite_list = Onsite_aftersales_service.objects.filter(customer_email_id=email)
            context = {
                'onsite_list': onsite_list,
                'search_msg': 'Search result for Customer Email ID: ' + email,
            }
            return render(request, "manager/onsite_reparing.html", context)
        elif 'submit4' in request.POST:
            customer = request.POST.get('customer')
            if check_admin_roles(request):  # For ADMIN
                onsite_list = Onsite_aftersales_service.objects.filter(user_id__group__icontains=request.user.name,
                                                                       user_id__is_deleted=False,second_person=customer).order_by('-onsite_no')
            else:  # For EMPLOYEE
                onsite_list = Onsite_aftersales_service.objects.filter(user_id=request.user.pk,second_person=customer).order_by('-onsite_no')
            # onsite_list = Onsite_aftersales_service.objects.filter(customer_name=customer)
            context = {
                'onsite_list': onsite_list,
                'search_msg': 'Search result for Customer Name: ' + customer,
            }
            return render(request, "manager/onsite_reparing.html", context)

        elif  'submit5' in request.POST:
            company = request.POST.get('company')
            if check_admin_roles(request):  # For ADMIN
                onsite_list = Onsite_aftersales_service.objects.filter(user_id__group__icontains=request.user.name,
                                                                       user_id__is_deleted=False,second_company_name=company).order_by('-onsite_no')
            else:  # For EMPLOYEE
                onsite_list = Onsite_aftersales_service.objects.filter(user_id=request.user.pk,second_company_name=company).order_by('-onsite_no')
            # onsite_list = Onsite_aftersales_service.objects.filter(company_name=company)
            context = {
                'onsite_list': onsite_list,
                'search_msg': 'Search result for Company Name: ' + company,
            }
            return render(request, "manager/onsite_reparing.html", context)
        elif request.method=='POST' and 'submit6' in request.POST:
            crm = request.POST.get('crm')
            if check_admin_roles(request):  # For ADMIN
                onsite_list = Onsite_aftersales_service.objects.filter(user_id__group__icontains=request.user.name,
                                                                       user_id__is_deleted=False,crm_no__pk=crm).order_by('-onsite_no')
            else:  # For EMPLOYEE
                onsite_list = Onsite_aftersales_service.objects.filter(user_id=request.user.pk,crm_no__pk=crm).order_by('-onsite_no')
            # onsite_list = Onsite_aftersales_service.objects.filter(crn_number=crm)
            context = {
                'onsite_list': onsite_list,
                'search_msg': 'Search result for CRM No. : ' + crm,
            }
            return render(request, "manager/onsite_reparing.html", context)
    elif 'deleted' in request.POST:
        if check_admin_roles(request):  # For ADMIN
            onsite_list = Onsite_aftersales_service.objects.filter(user_id__group__icontains=request.user.name,user_id__is_deleted=True,user_id__modules_assigned__icontains='Onsite Repairing Module').order_by('-onsite_no')
        else:  # For EMPLOYEE
            onsite_list = Onsite_aftersales_service.objects.filter(user_id=request.user.pk).order_by('-onsite_no')
        # onsite_list = Onsite_aftersales_service.objects.all()

        context = {
            'onsite_list': onsite_list,
            'deleted': True,

        }
        return render(request, "manager/onsite_reparing.html", context)
    else:
        context={}
        if check_admin_roles(request):     #For ADMIN

            onsite_list = Onsite_aftersales_service.objects.filter(Q(user_id=request.user.pk)|Q(user_id__group__icontains=request.user.name,user_id__is_deleted=False,user_id__modules_assigned__icontains='Onsite Repairing Module')).order_by('-onsite_no')
            stage1 = Onsite_aftersales_service.objects.filter((Q(user_id=request.user.pk)|Q(user_id__group__icontains=request.user.name))&Q(user_id__is_deleted=False, current_stage='Onsite repairing request is raised')).values(
                'current_stage').annotate(dcount=Count('current_stage'))
            stage2 = Onsite_aftersales_service.objects.filter((Q(user_id=request.user.pk)|Q(user_id__group__icontains=request.user.name))&Q(user_id__is_deleted=False,
                current_stage='Onsite repairing request is assigned')).values(
                'current_stage').annotate(dcount=Count('current_stage'))

            stage3 = Onsite_aftersales_service.objects.filter((Q(user_id=request.user.pk)|Q(user_id__group__icontains=request.user.name))&Q(user_id__is_deleted=False,
                current_stage='Onsite repairing request is completed')).values(
                'current_stage').annotate(dcount=Count('current_stage'))
        else:  #For EMPLOYEE
            onsite_list = Onsite_aftersales_service.objects.filter(Q(user_id=request.user.pk)|Q(complaint_assigned_to=request.user.name)).order_by('-onsite_no')
            stage1 = Onsite_aftersales_service.objects.filter((Q(user_id=request.user.pk)|Q(complaint_assigned_to=request.user.name))& Q(current_stage='Onsite repairing request is raised')).values(
                'current_stage').annotate(dcount=Count('current_stage'))
            stage2 = Onsite_aftersales_service.objects.filter((Q(user_id=request.user.pk)|Q(complaint_assigned_to=request.user.name))& Q(
                current_stage='Onsite repairing request is assigned')).values(
                'current_stage').annotate(dcount=Count('current_stage'))

            stage3 = Onsite_aftersales_service.objects.filter((Q(user_id=request.user.pk)|Q(complaint_assigned_to=request.user.name))& Q(
                current_stage='Onsite repairing request is completed')).values(
                'current_stage').annotate(dcount=Count('current_stage'))
        # onsite_list = Onsite_aftersales_service.objects.all()



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


        x = stage2
        # if x['current_stage'] == 'Scale is collected but estimate is not given':
        if not x:
            x = None
        try:

            for item in x:
                # if item['dcount'] in x:
                    # stage1 = item['dcount']
                stage2 = item['dcount']
            contextd = {
                'stage2': stage2,
            }
            context.update(contextd)
        except:
            pass


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
            'onsite_list': onsite_list,
        }
        context.update(context2)
        return render(request, "manager/onsite_reparing.html", context)


@login_required(login_url='/')
def add_onsite_aftersales_service(request):
    cust_sugg = Customer_Details.objects.all()

    if request.user.role == 'Super Admin':
        user_list=SiteUser.objects.filter(Q(id=request.user.id) | Q(group__icontains=request.user.name),modules_assigned__icontains='Onsite Repairing Module', is_deleted=False)

    elif request.user.role == 'Admin':
        user_list = SiteUser.objects.filter(Q(id=request.user.id) | Q(admin=request.user.name),
                                            modules_assigned__icontains='Onsite Repairing Module', is_deleted=False)
    elif request.user.role == 'Manager':
        user_list = SiteUser.objects.filter(Q(id=request.user.id) | Q(manager=request.user.name),
                                            modules_assigned__icontains='Onsite Repairing Module', is_deleted=False)
    else: #display colleague

        list_group = SiteUser.objects.get(id=request.user.id).manager
        user_list = SiteUser.objects.filter(Q(id=request.user.id) | Q(manager=list_group),
                                            modules_assigned__icontains='Onsite Repairing Module', is_deleted=False)

    # user_list=SiteUser.objects.filter(group__icontains=request.user.name,modules_assigned__icontains='Onsite Repairing Module')

    # form = add_Onsite_aftersales_service_form(request.POST or None, request.FILES or None)
    if request.method == 'POST' or request.method == 'FILES':
        customer_name = request.POST.get('customer_name')
        company_name = request.POST.get('company_name')
        address = request.POST.get('customer_address')
        contact_no = request.POST.get('contact_no')
        customer_email_id = request.POST.get('customer_email_id')

        # second_person = request.POST.get('second_person')
        # third_person = request.POST.get('third_person')
        # second_contact_no = request.POST.get('second_contact_no')
        # third_contact_no = request.POST.get('third_contact_no')
        previous_repairing_number = request.POST.get('previous_repairing_number')
        date_of_complaint_received = request.POST.get('date_of_complaint_received')
        complaint_received_by = request.POST.get('complaint_received_by')
        nearest_railwaystation = request.POST.get('nearest_railwaystation')
        train_line = request.POST.get('train_line')
        products_to_be_repaired = request.POST.get('products_to_be_repaired')

        visiting_charges_told_customer = request.POST.get('visiting_charges_told_customer')
        total_cost = 0.0
        complaint_assigned_to = request.POST.get('complaint_assigned_to')
        time_taken_destination_return_office_min = request.POST.get('time_taken_destination_return_office_min')
        notes = request.POST.get('notes')
        # feedback_given = request.POST.get('feedback_given')

        try:
            del request.session['company_name']
            del request.session['address']
            del request.session['customer_email_id']
            del request.session['second_person']
            del request.session['previous_repairing_number']
            del request.session['second_contact_no']
            del request.session['total_cost']
            del request.session['feedback_given']
            del request.session['date_of_complaint_received']
            del request.session['complaint_received_by']
            del request.session['nearest_railwaystation']
            del request.session['train_line']
            del request.session['products_to_be_repaired']
            del request.session['visiting_charges_told_customer']
            del request.session['notes']
            del request.session['feedback_given']
            del request.session['complaint_assigned_to']
            del request.session['complaint_assigned_on']
            del request.session['onsite_no']

        except:
            pass
        request.session['company_name'] = company_name
        request.session['address'] = address
        request.session['customer_email_id'] = customer_email_id

        request.session['previous_repairing_number'] = previous_repairing_number

        request.session['second_person'] = customer_name
        request.session['second_contact_no'] = contact_no
        request.session['total_cost'] = 0.0

        # request.session['repairing_done_timedate'] = timezone.now().strftime("%Y-%m-%d %H:%M:%S")
        request.session['feedback_given'] = False
        if date_of_complaint_received != None and date_of_complaint_received != '':
            request.session['date_of_complaint_received'] = date_of_complaint_received
        request.session['complaint_received_by'] = complaint_received_by
        request.session['nearest_railwaystation'] = nearest_railwaystation
        request.session['train_line'] = train_line
        request.session['products_to_be_repaired'] = products_to_be_repaired
        request.session['visiting_charges_told_customer'] = float(visiting_charges_told_customer)
        request.session['time_taken_destination_return_office_min'] = time_taken_destination_return_office_min
        request.session['notes'] = notes
        request.session['feedback_given'] = False
        if complaint_assigned_to != None and complaint_assigned_to != '':
            request.session['complaint_assigned_to'] = complaint_assigned_to
            request.session['complaint_assigned_on'] = datetime.today().strftime('%Y-%m-%d')
        request.session['onsite_no'] = Onsite_aftersales_service.objects.latest('onsite_no').onsite_no + 1


        # if Customer_Details.objects.filter(Q(customer_name=customer_name),Q(contact_no=contact_no)).count() > 0:
        #     crm_no = Customer_Details.objects.filter(Q(customer_name=customer_name),Q(contact_no=contact_no)).first()
        #     try:
        #         send_mail('Feedback Form',
        #               'Click on the link to give feedback http://139.59.76.87/feedback_onrepairing/' + str(
        #                   request.user.pk) + '/' + str(crm_no.pk) + '/' + str(item2.id), settings.EMAIL_HOST_USER,
        #               [crm_no.customer_email_id])
        #     except:
        #         pass
        #
        #     message = 'Click on the link to give feedback http://139.59.76.87/feedback_onrepairing/' + str(
        #         request.user.pk) + '/' + str(crm_no.pk) + '/' + str(item2.id)
        #
        #     url = "http://smshorizon.co.in/api/sendsms.php?user=" + settings.user + "&apikey=" + settings.api + "&mobile=" + crm_no.contact_no + "&message=" + message + "&senderid=" + settings.senderid + "&type=txt"
        #     payload = ""
        #     headers = {'content-type': 'application/x-www-form-urlencoded'}
        #
        #     response = requests.request("GET", url, data=json.dumps(payload), headers=headers)
        #     x = response.text
        # else:
        #
        #     try:
        #         send_mail('Feedback Form',
        #               'Click on the link to give feedback http://139.59.76.87/feedback_onrepairing/' + str(
        #                   request.user.pk) + '/' + str(item.pk) + '/' + str(item2.id), settings.EMAIL_HOST_USER,
        #               [item.customer_email_id])
        #     except:
        #         pass
        #
        #     message = 'Click on the link to give feedback http://139.59.76.87/feedback_onrepairing/' + str(
        #         request.user.pk) + '/' + str(item.pk) + '/' + str(item2.id)
        #
        #     url = "http://smshorizon.co.in/api/sendsms.php?user=" + settings.user + "&apikey=" + settings.api + "&mobile=" + item.contact_no + "&message=" + message + "&senderid=" + settings.senderid + "&type=txt"
        #     payload = ""
        #     headers = {'content-type': 'application/x-www-form-urlencoded'}
        #
        #     response = requests.request("GET", url, data=json.dumps(payload), headers=headers)
        #     x = response.text
        latest_onsite_no = Onsite_aftersales_service.objects.latest('id').id + 1


        return redirect('/add_onsite_product/'+str(latest_onsite_no))
    context={
        'cust_sugg':cust_sugg,
        'user_list':user_list,

    }

    return render(request, 'forms/onsite_rep_form.html',context)

@login_required(login_url='/')
def add_onsite_product(request,id):
    # onsite_id = Onsite_aftersales_service.objects.latest('id').id + 1
    # crm_id = Onsite_aftersales_service.objects.get(id=id).crm_no
    type_of_purchase_list =type_purchase.objects.all() #1

    if request.method == 'POST':
        type_of_machine = request.POST.get('type_of_scale')
        model = request.POST.get('model_of_purchase')
        sub_model = request.POST.get('sub_model')

        capacity = request.POST.get('capacity')
        problem_in_scale = request.POST.get('problem_in_scale')
        components_replaced_in_warranty = request.POST.get('components_replaced_in_warranty')
        components_replaced = request.POST.get('components_replaced')
        cost = request.POST.get('cost')
        in_warranty = request.POST.get('in_warranty')



        item = Onsite_Products()

        item.onsite_repairing_id_id = id
        item.type_of_machine = type_of_machine
        # item.type_of_machine = type_of_machine
        item.model = model

        item.sub_model = sub_model

        item.capacity = capacity
        item.problem_in_scale = problem_in_scale
        item.components_replaced_in_warranty = components_replaced_in_warranty
        item.components_replaced = components_replaced
        item.cost = cost
        item.user_id = SiteUser.objects.get(id=request.user.pk)
        item.manager_id = SiteUser.objects.get(id=request.user.pk).group
        # item.crm_no = Customer_Details.objects.get(id=crm_id)
        item.in_warranty = in_warranty
        if cost == '' or cost == None:
            cost=0.0
        if Onsite_aftersales_service.objects.filter(id=id).count() == 0 :

            item2 = Onsite_aftersales_service()
            if Customer_Details.objects.filter(customer_name=request.session.get('second_person'),contact_no=request.session.get('second_contact_no')).count() > 0:

                item2.crm_no= Customer_Details.objects.filter(contact_no=request.session.get('second_contact_no')).first()

                item3 = Customer_Details.objects.filter(customer_name=request.session.get('second_person'), contact_no=request.session.get('second_contact_no')).first()
                if request.session.get('company_name') != '' and request.session.get('company_name') != None:
                    # request.session.get('second_company_name') = company_name  # new2
                    item2.second_company_name = request.session.get('company_name')
                    item3.company_name = request.session.get('company_name')
                    item3.save(update_fields=['company_name'])
                if request.session.get('address')  != '' and request.session.get('address')  != None:
                    item3.address = request.session.get('address')
                    # request.session['company_address'] = address        # new2
                    item2.company_address = request.session.get('address')
                    item3.save(update_fields=['address'])
                if request.session.get('customer_email_id') != '' and request.session.get('customer_email_id') != None:
                    # request.session['company_email'] = customer_email_id        # new2
                    item2.company_email = request.session.get('customer_email_id')   # new2
                    item3.customer_email_id = request.session.get('customer_email_id')
                    item3.save(update_fields=['customer_email_id'])

            else:
                new_cust = Customer_Details()

                new_cust.customer_name = request.session.get('second_person')
                if request.session.get('company_name') != '':
                    # request.session['second_company_name'] = company_name  # new2
                    new_cust.company_name = request.session.get('company_name')
                if request.session.get('address') != '':
                    # request.session['company_address'] = address  # new2
                    new_cust.address = request.session.get('address')
                new_cust.contact_no = request.session.get('second_contact_no')
                if request.session.get('customer_email_id') != '':
                    # request.session['customer_email_id'] = customer_email_id  # new2
                    new_cust.customer_email_id = request.session.get('customer_email_id')
                # item.user_id = SiteUser.objects.get(id=request.user.pk)
                # item.manager_id = SiteUser.objects.get(id=request.user.pk).group
                try:
                    new_cust.save()
                    item2.crm_no = Customer_Details.objects.get(id=new_cust.pk)
                except:
                    pass


            if request.session.get('complaint_assigned_to') != None and request.session.get('complaint_assigned_to') != '':
                item2.complaint_assigned_to = request.session.get('complaint_assigned_to')
                item2.complaint_assigned_on = datetime.today().strftime('%Y-%m-%d')

            item2.onsite_no = request.session.get('onsite_no')

            item2.second_person = request.session.get('second_person')
            # customer_name  # new1
            item2.second_contact_no = request.session.get('second_contact_no')  # new2
            item2.previous_repairing_number =  request.session.get('previous_repairing_number')
            if request.session.get('date_of_complaint_received') != None and request.session.get('date_of_complaint_received') != '':
                item2.date_of_complaint_received =  request.session.get('date_of_complaint_received')

            item2.complaint_received_by =  request.session.get('complaint_received_by')
            item2.nearest_railwaystation =  request.session.get('nearest_railwaystation')
            item2.train_line =  request.session.get('train_line')
            item2.products_to_be_repaired = request.session.get('products_to_be_repaired')

            item2.visiting_charges_told_customer = request.session.get('visiting_charges_told_customer')
            item2.total_cost = 0.0
            # item2.complaint_assigned_to = complaint_assigned_to
            item2.time_taken_destination_return_office_min = request.session.get('time_taken_destination_return_office_min')
            item2.notes = request.session.get('notes')
            item2.feedback_given = request.session.get('feedback_given')
            item2.user_id = SiteUser.objects.get(id=request.user.pk)
            item2.manager_id = SiteUser.objects.get(id=request.user.pk).group

            item2.save()
        else:
            pass
        item.save()
        current_stage_in_db = Onsite_aftersales_service.objects.get(id=id).current_stage  # updatestage2

        if (current_stage_in_db == '' or current_stage_in_db == None) and (
                problem_in_scale != '' and problem_in_scale != None and problem_in_scale != 'None'):
            Onsite_aftersales_service.objects.filter(id=id).update(
                current_stage='Onsite repairing request is raised')

        if (current_stage_in_db == 'Onsite repairing request is raised') and (
                request.session.get('complaint_assigned_to')  != '' or request.session.get('complaint_assigned_to')  != None):
            Onsite_aftersales_service.objects.filter(id=id).update(
                current_stage='Onsite repairing request is assigned')

        if (current_stage_in_db == 'Onsite repairing request is assigned') and (
                request.session.get('time_taken_destination_return_office_min')  != '' or request.session.get('time_taken_destination_return_office_min') != None):
            Onsite_aftersales_service.objects.filter(id=id).update(
                current_stage='Onsite repairing request is completed')



        if request.session.get('complaint_assigned_to') != None and request.session.get('complaint_assigned_to') != '':
            new_onsite_id = Onsite_aftersales_service.objects.get(id=id)
            if new_onsite_id.ess_calculated == False:
                compliant_assign_user_id = SiteUser.objects.get(profile_name=request.session.get('complaint_assigned_to'))

                if Employee_Analysis_date.objects.filter(Q(entry_date=datetime.now().date()),
                                                         Q(user_id=compliant_assign_user_id)).count() > 0:
                    Employee_Analysis_date.objects.filter(user_id=compliant_assign_user_id, entry_date=datetime.now().date(),
                                                          year=datetime.now().year).update(
                        total_reparing_done_onsite_today=F("total_reparing_done_onsite_today") + cost)
                    # ead.total_sales_done_today=.filter(category_id_id=id).update(total_views=F("total_views") + value_of_goods)

                    # ead.save(update_fields=['total_sales_done_today'])

                else:
                    ead = Employee_Analysis_date()
                    ead.user_id = compliant_assign_user_id
                    ead.total_reparing_done_onsite_today = cost
                    ead.manager_id = compliant_assign_user_id.group

                    ead.month = datetime.now().month
                    ead.year = datetime.now().year

                    ead.save()

                if Employee_Analysis_month.objects.filter(Q(entry_date__month=datetime.now().month),
                                                          Q(user_id=compliant_assign_user_id)).count() > 0:
                    Employee_Analysis_month.objects.filter(user_id=compliant_assign_user_id, entry_date__month=datetime.now().month,
                                                           year=datetime.now().year).update(
                        total_reparing_done_onsite=F("total_reparing_done_onsite") + cost)
                    # ead.total_sales_done_today=.filter(category_id_id=id).update(total_views=F("total_views") + value_of_goods)

                    # ead.save(update_fields=['total_sales_done_today'])

                else:
                    ead = Employee_Analysis_month()
                    ead.user_id = compliant_assign_user_id
                    ead.total_reparing_done_onsite = cost
                    ead.manager_id = compliant_assign_user_id.group

                    ead.month = datetime.now().month
                    ead.year = datetime.now().year
                    ead.save()

                new_onsite_id.ess_calculated = True
                new_onsite_id.save(update_fields=['ess_calculated', ]),
        # if (current_stage_in_db == 'Scales in Restamping Queue') and (new_sr_no != '' or new_sr_no != None):
        #     Onsite_aftersales_service.objects.filter(id=id).update(
        #         current_stage='Restamping is done but scale is not collected')



        return redirect('/update_onsite_details/'+str(id))
    context = {
        'onsite_id': id,
        'type_purchase': type_of_purchase_list,  # 2

    }
    return render(request,"forms/onsite_product.html",context)

@login_required(login_url='/')
def update_onsite_product(request,id):
    onsite_id = Onsite_Products.objects.get(id=id)
    onsite = Onsite_aftersales_service.objects.get(id=onsite_id.onsite_repairing_id.pk).pk
    # crm_id = Onsite_aftersales_service.objects.get(id=onsite).crm_no
    if request.method == 'POST' or request.method == 'FILES':
        type_of_machine = request.POST.get('type_of_machine')
        model = request.POST.get('model')
        sub_model = request.POST.get('sub_model')
        capacity = request.POST.get('capacity')
        problem_in_scale = request.POST.get('problem_in_scale')
        components_replaced_in_warranty = request.POST.get('components_replaced_in_warranty')
        components_replaced = request.POST.get('components_replaced')
        cost = request.POST.get('cost')
        in_warranty = request.POST.get('in_warranty')

        cost2 = onsite_id.cost
        if cost != None or '':
            Onsite_aftersales_service.objects.filter(id=onsite).update(total_cost=F("total_cost") - cost2)
            Onsite_aftersales_service.objects.filter(id=onsite).update(total_cost=F("total_cost") + cost)
            if Onsite_aftersales_service.objects.get(id=onsite).complaint_assigned_to != None or '':
                complaint_assigned_user = Onsite_aftersales_service.objects.get(id=onsite).complaint_assigned_to
                compliant_assign_user_id = SiteUser.objects.get(profile_name=complaint_assigned_user)

                Employee_Analysis_month.objects.filter(user_id=compliant_assign_user_id,
                                                       entry_date__month=onsite_id.entry_timedate.month,
                                                       year=onsite_id.entry_timedate.year).update(
                    total_reparing_done_onsite=F("total_reparing_done_onsite") - cost2)

                Employee_Analysis_date.objects.filter(user_id=compliant_assign_user_id,
                                                      entry_date=onsite_id.entry_timedate,
                                                      year=onsite_id.entry_timedate.year).update(
                    total_reparing_done_onsite_today=F("total_reparing_done_onsite_today") - cost2)


                Employee_Analysis_month.objects.filter(user_id=compliant_assign_user_id,
                                                       entry_date__month=onsite_id.entry_timedate.month,
                                                       year=onsite_id.entry_timedate.year).update(
                    total_reparing_done_onsite=F("total_reparing_done_onsite") + cost)

                Employee_Analysis_date.objects.filter(user_id=compliant_assign_user_id,
                                                      entry_date=onsite_id.entry_timedate,
                                                      year=onsite_id.entry_timedate.year).update(
                    total_reparing_done_onsite_today=F("total_reparing_done_onsite_today") + cost)

        item = Onsite_Products.objects.get(id=id)

        # item.onsite_repairing_id_id = onsite_id
        item.type_of_machine = type_of_machine
        item.model = model
        item.sub_model = sub_model
        item.capacity = capacity
        item.problem_in_scale = problem_in_scale
        item.components_replaced_in_warranty = components_replaced_in_warranty
        item.components_replaced = components_replaced
        item.cost = cost
        item.in_warranty = in_warranty

        # item.user_id = SiteUser.objects.get(id=request.user.pk)
        # item.manager_id = SiteUser.objects.get(id=request.user.pk).group
        # item.crm_no = Customer_Details.objects.get(id=crm_id)
        item.save(update_fields=['type_of_machine', ]),
        item.save(update_fields=['model', ]),
        item.save(update_fields=['sub_model', ]),
        item.save(update_fields=['capacity', ]),
        item.save(update_fields=['problem_in_scale', ]),
        item.save(update_fields=['components_replaced', ]),
        item.save(update_fields=['components_replaced_in_warranty', ]),
        item.save(update_fields=['cost', ]),
        item.save(update_fields=['in_warranty', ]),

        current_stage_in_db = Onsite_aftersales_service.objects.get(
            id=onsite).current_stage  # updatestage2
        if (current_stage_in_db == '' or current_stage_in_db == None) and (
                problem_in_scale != '' or problem_in_scale != None):
            Onsite_aftersales_service.objects.filter(id=onsite).update(
                current_stage='Onsite repairing request is raised')






        return redirect('/update_onsite_details/'+str(onsite))
    context = {
        'onsite_id': onsite_id,
    }
    return render(request,"edit_product/edit_onsite_product.html",context)

@login_required(login_url='/')
def update_onsite_details(request,id):
    onsite_id = Onsite_aftersales_service.objects.get(id=id)
    onsite_product_list = Onsite_Products.objects.filter(onsite_repairing_id=id)
    employee_list = SiteUser.objects.filter(role='Employee',group__icontains=request.user.name)
    customer_id = Onsite_aftersales_service.objects.get(id=id).crm_no

    customer_id = Customer_Details.objects.get(id=customer_id)
    if request.user.role == 'Super Admin':
        user_list=SiteUser.objects.filter(Q(id=request.user.id) | Q(group__icontains=request.user.name),modules_assigned__icontains='Onsite Repairing Module', is_deleted=False)

    elif request.user.role == 'Admin':
        user_list = SiteUser.objects.filter(Q(id=request.user.id) | Q(admin=request.user.name),
                                            modules_assigned__icontains='Onsite Repairing Module', is_deleted=False)
    elif request.user.role == 'Manager':
        user_list = SiteUser.objects.filter(Q(id=request.user.id) | Q(manager=request.user.name),
                                            modules_assigned__icontains='Onsite Repairing Module', is_deleted=False)
    else: #display colleague

        list_group = SiteUser.objects.get(id=request.user.id).manager
        user_list = SiteUser.objects.filter(Q(id=request.user.id) | Q(manager=list_group),
                                            modules_assigned__icontains='Onsite Repairing Module', is_deleted=False)
    try:
        feedback = Onsite_Feedback.objects.get(onsite_repairing_id=onsite_id.pk, customer_id=customer_id)

    except:
        feedback = None
    if request.method == 'POST' or request.method == 'FILES':
        customer_name = request.POST.get('customer_name')
        company_name = request.POST.get('company_name')
        address = request.POST.get('customer_address')
        contact_no = request.POST.get('contact_no')
        customer_email_id = request.POST.get('customer_email_id')

        item2 = customer_id
        item2.customer_name = customer_name
        if company_name != '':
            item2.company_name = company_name
            item2.save(update_fields=['company_name'])
        if address != '':
            item2.address = address
            item2.save(update_fields=['address'])

        if customer_email_id != '':
            item2.customer_email_id = customer_email_id
            item2.save(update_fields=['customer_email_id'])
        item2.contact_no = contact_no
        if customer_id.contact_no != item2.contact_no or customer_id.customer_name != item2.customer_name :
            item2.save(update_fields=['customer_name','contact_no'])  #new3

        # repairingno = request.POST.get('repairingno')
        # customer_no = request.POST.get('customer_no')
        # second_person=request.POST.get('second_person')
        # third_person=request.POST.get('third_person')
        # second_contact_no=request.POST.get('second_contact_no')
        # third_contact_no=request.POST.get('third_contact_no')
        previous_repairing_number = request.POST.get('previous_repairing_number')
        # customer_email_id = request.POST.get('customer_email_id')
        # date_of_complaint_received = request.POST.get('date_of_complaint_received')
        # customer_address = request.POST.get('customer_address')
        complaint_received_by = request.POST.get('complaint_received_by')
        nearest_railwaystation = request.POST.get('nearest_railwaystation')
        train_line = request.POST.get('train_line')
        # products_to_be_repaired = request.POST.get('products_to_be_repaired')

        visiting_charges_told_customer = request.POST.get('visiting_charges_told_customer')
        total_cost = request.POST.get('components_replaced_in_warranty')
        complaint_assigned_to = request.POST.get('complaint_assigned_to')
        complaint_assigned_on = request.POST.get('complaint_assigned_on')
        time_taken_destination_return_office_min = request.POST.get('time_taken_destination_return_office_min')
        notes = request.POST.get('notes')
        # feedback_given = request.POST.get('feedback_given')
        assigned_to = request.POST.get('assigned_to')

        current_stage_in_db = Onsite_aftersales_service.objects.get(id=id).current_stage  # updatestage2


        if (current_stage_in_db == 'Onsite repairing request is raised' and complaint_assigned_to != '' and complaint_assigned_to != None and  complaint_assigned_to != 'None'):
            Onsite_aftersales_service.objects.filter(id=id).update(
                current_stage='Onsite repairing request is assigned')


        if (current_stage_in_db == 'Onsite repairing request is assigned') and (
                time_taken_destination_return_office_min != '' or time_taken_destination_return_office_min != None):
            Onsite_aftersales_service.objects.filter(id=id).update(
                current_stage='Onsite repairing request is completed')

            msg='Dear '+customer_name+',Thank you for selecting HSCo. Your Onsite Repairing No '+str(onsite_id.onsite_no)+' has been successfully' \
                ' resolved. We hope that your Repairing Complaint was resolved to your satisfaction. WE\'d love to hear your' \
                ' feedback to help us improve our customer experience, just click on the link below:\n http://139.59.76.87/feedback_onrepairing/'\
                + str(request.user.pk) + '/' + str(item2.pk) + '/' + str(onsite_id.pk)+' If you feel ' \
                'that your complaint has not been resolved please contact our customer service team on 7045922251'

            try:
                send_mail('Onsite-Reparing Feedback - HSCo',msg,
                          settings.EMAIL_HOST_USER,
                          [customer_email_id,])
            except:
                pass

            message = 'Dear ' + customer_name + ',Thank you for selecting HSCo. Your Onsite Repairing No ' + str(
                onsite_id.onsite_no) + ' has been successfully' \
                            ' resolved. We hope that your Repairing Complaint was resolved to your satisfaction. WE\'d love to hear your' \
                            ' feedback to help us improve our customer experience, just click on the link below:\n http://139.59.76.87/feedback_onrepairing/' \
                  + str(request.user.pk) + '/' + str(item2.pk) + '/' + str(onsite_id.pk) + ' If you feel ' \
                                                                                              'that your complaint has not been resolved please contact our customer service team on 7045922251'

            url = "http://smshorizon.co.in/api/sendsms.php?user=" + settings.user + "&apikey=" + settings.api + "&mobile=" + contact_no + "&message=" + message + "&senderid=" + settings.senderid + "&type=txt"
            payload = ""
            headers = {'content-type': 'application/x-www-form-urlencoded'}

            response = requests.request("GET", url, data=json.dumps(payload), headers=headers)
            x = response.text



        item = onsite_id
        if company_name != '':
            item.second_company_name = company_name  # new2


            item2.company_name = company_name
            item2.save(update_fields=['company_name'])
            item.save(update_fields=['second_company_name', ]),

        if address != '':
            item2.address = address

            item.company_address = address  # new2
            item2.save(update_fields=['address'])
            item.save(update_fields=['company_address', ]),
        if customer_email_id != '':
            item2.customer_email_id = customer_email_id
            item.company_email = customer_email_id  # new2
            item.save(update_fields=['company_email'])
            item2.save(update_fields=['customer_email_id', ]),
        # item.repairingno = repairingno
        # item.second_person=second_person
        # item.third_person=third_person
        # item.second_contact_no=second_contact_no
        # item.third_contact_no=third_contact_no
        item.second_person=customer_name   #new4
        item.second_contact_no=contact_no   #new5
        item.customer_name = customer_name
        item.company_name = company_name
        # item.customer_no = customer_no
        item.previous_repairing_number = previous_repairing_number
        # item.customer_email_id = customer_email_id
        # item.date_of_complaint_received = date_of_complaint_received
        item.customer_address = address
        item.complaint_received_by = complaint_received_by
        item.nearest_railwaystation = nearest_railwaystation
        item.train_line = train_line
        # item.products_to_be_repaired = products_to_be_repaired
        item.visiting_charges_told_customer = visiting_charges_told_customer
        # item.total_cost = total_cost
        # item.complaint_assigned_to = complaint_assigned_to
        item.complaint_assigned_on = complaint_assigned_on
        item.time_taken_destination_return_office_min = time_taken_destination_return_office_min
        item.notes = notes
        # item.feedback_given = feedback_given
        item.assigned_to = assigned_to

        if complaint_assigned_to != None and complaint_assigned_to != '' and complaint_assigned_to != 'None' :
            item.complaint_assigned_to = complaint_assigned_to
            item.complaint_assigned_on = datetime.today().strftime('%Y-%m-%d')
            item.save(update_fields=['complaint_assigned_to'])
            item.save(update_fields=['complaint_assigned_on', ]),
            if item.ess_calculated == False:
                product_list_total = Onsite_Products.objects.filter(onsite_repairing_id=id).values('cost').annotate(data_sum=Sum('cost'))
                for i in product_list_total:
                    x = i
                    total = x['data_sum']
                # compliant_assign = Onsite_aftersales_service.objects.get(id=complaint_assigned_to).assigned_to
                compliant_assign_user_id = SiteUser.objects.get(profile_name=complaint_assigned_to)
                if Employee_Analysis_date.objects.filter(Q(entry_date=datetime.now().date()),
                                                         Q(user_id=compliant_assign_user_id)).count() > 0:
                    Employee_Analysis_date.objects.filter(user_id=request.user.pk, entry_date=datetime.now().date(),
                                                          year=datetime.now().year).update(
                        total_reparing_done_onsite_today=F("total_reparing_done_onsite_today") + total)
                    # ead.total_sales_done_today=.filter(category_id_id=id).update(total_views=F("total_views") + value_of_goods)

                    # ead.save(update_fields=['total_sales_done_today'])

                else:
                    ead = Employee_Analysis_date()
                    ead.user_id = compliant_assign_user_id
                    ead.total_reparing_done_onsite_today = total
                    ead.manager_id = compliant_assign_user_id.group

                    ead.month = datetime.now().month
                    ead.year = datetime.now().year
                    ead.save()

                if Employee_Analysis_month.objects.filter(Q(entry_date__month=datetime.now().month),
                                                          Q(user_id=compliant_assign_user_id)).count() > 0:
                    Employee_Analysis_month.objects.filter(user_id=request.user.pk, entry_date__month=datetime.now().month,
                                                           year=datetime.now().year).update(
                        total_reparing_done_onsite=F("total_reparing_done_onsite") + total)
                    # ead.total_sales_done_today=.filter(category_id_id=id).update(total_views=F("total_views") + value_of_goods)

                    # ead.save(update_fields=['total_sales_done_today'])

                else:
                    ead = Employee_Analysis_month()
                    ead.user_id = compliant_assign_user_id
                    ead.total_reparing_done_onsite = total
                    ead.manager_id = compliant_assign_user_id.group

                    ead.month = datetime.now().month
                    ead.year = datetime.now().year
                    ead.save()
                item.ess_calculated = True
                item.save(update_fields=['ess_calculated', ]),

        #item.save(update_fields=['onsite_repairing_id_id', ]),
        # item.save(update_fields=['assigned_to', ]),
        # item.save(update_fields=['repairingno', ]),
        # item.save(update_fields=['customer_name', ]),
        # item.save(update_fields=['company_name', ]),
        # item.save(update_fields=['customer_no', ]),
        item.save(update_fields=['previous_repairing_number', ]),
        # item.save(update_fields=['phone_no', ]),
        # item.save(update_fields=['customer_email_id', ]),
        # item.save(update_fields=['date_of_complaint_received', ]),
        # item.save(update_fields=['customer_address', ]),
        item.save(update_fields=['complaint_received_by', ]),
        item.save(update_fields=['nearest_railwaystation', ]),
        item.save(update_fields=['train_line', ]),
        # item.save(update_fields=['products_to_be_repaired', ]),
        item.save(update_fields=['visiting_charges_told_customer', ]),
        # item.save(update_fields=['total_cost', ]),
        # item.save(update_fields=['complaint_assigned_to', ]),
        # item.save(update_fields=['complaint_assigned_on', ]),
        item.save(update_fields=['time_taken_destination_return_office_min', ]),
        item.save(update_fields=['notes','second_person','second_contact_no',]),

        # item.save(update_fields=['feedback_given', ]),
        onsite_id = Onsite_aftersales_service.objects.get(id=id)

        context = {
            'onsite_id': onsite_id,
            'onsite_product_list': onsite_product_list,
            'employee_list': employee_list,
            'feedback': feedback,
        }

        return render(request, 'update_forms/update_onsite_rep_form.html', context)


    context={
        'onsite_id':onsite_id,
        'onsite_product_list':onsite_product_list,
        'employee_list':employee_list,
        'feedback': feedback,
        'user_list': user_list,
    }

    return render(request,'update_forms/update_onsite_rep_form.html',context)

@login_required(login_url='/')
def report_onsite(request):
    if request.method == 'POST' or None:
        selected_list = request.POST.getlist('checks[]')
        selected_product_list = request.POST.getlist('products[]')
        onsite_start_date = request.POST.get('date1')
        onsite_end_date = request.POST.get('date2')
        onsite_string = ','.join(selected_list)
        onsite_repair_product_string = ','.join(selected_product_list)


        request.session['start_date'] = onsite_start_date
        request.session['repair_end_date'] = onsite_end_date
        request.session['repair_string'] = onsite_string
        request.session['onsite_repair_product_string'] = onsite_repair_product_string
        request.session['selected_product_list'] = selected_product_list
        request.session['selected_list'] = selected_list
        return redirect('/final_report_onsite/')
    return render(request,"report/report_onsite_rep_form.html",)

@login_required(login_url='/')
def final_report_onsite(request):
    repair_start_date = str(request.session.get('repair_start_date'))
    repair_end_date = str(request.session.get('repair_end_date'))
    repair_string = request.session.get('repair_string')
    onsite_repair_product_string = request.session.get('onsite_repair_product_string')
    selected_product_list = request.session.get('selected_product_list')
    final_row=[]
    final_row_product=[]


    selected_list = request.session.get('selected_list')
    for n, i in enumerate(selected_list):
        if i == 'onsitevisit_app_onsite_aftersales_service.id':
            selected_list[n] = 'Onsite Rep ID'
        if i == 'customer_app_customer_details.id':
            selected_list[n] = 'CRM No.'
        if i == 'today_date':
            selected_list[n] = 'Entry Date'

    with connection.cursor() as cursor:

        if onsite_repair_product_string != '' and repair_string != '':

            cursor.execute("SELECT " + (onsite_repair_product_string +","+ repair_string) + " from onsitevisit_app_onsite_products  PRODUCT , onsitevisit_app_onsite_aftersales_service "
            "REP , customer_app_customer_details CRM where PRODUCT.onsite_repairing_id_id = REP.id and REP.crm_no_id = CRM.id and "
            " PRODUCT.entry_timedate between'" + repair_start_date + "' and '" + repair_end_date + "';")
            row = cursor.fetchall()
            final_row_product = [list(x) for x in row]
            repairing_data = []
            for i in row:
                repairing_data.append(list(i))

            final_row = [list(x) for x in row]
            repairing_data = []
            for i in row:
                repairing_data.append(list(i))

    # with connection.cursor() as cursor:
    #     if repair_string!= '':
    #         cursor.execute("SELECT  " + repair_string + " from onsitevisit_app_onsite_aftersales_service , customer_app_customer_details where onsitevisit_app_onsite_aftersales_service.crm_no_id = customer_app_customer_details.id and entry_timedate between '" + repair_start_date + "' and '" + repair_end_date + "';")
    #         row = cursor.fetchall()
    #
    #         print(row)
    #         final_row = [list(x) for x in row]
    #         repairing_data = []
    #         for i in row:
    #             repairing_data.append(list(i))
    #
    #     if onsite_repair_product_string != '':
    #         cursor.execute("SELECT  " + (onsite_repair_product_string) + " from onsitevisit_app_onsite_products PRODUCT, onsitevisit_app_onsite_aftersales_service ONSITE"
    #                                              "  where PRODUCT.onsite_repairing_id_id = ONSITE.id and PRODUCT.entry_timedate between '" + repair_start_date + "' and '" + repair_end_date + "';")
    #         row = cursor.fetchall()
    #
    #         print(row)
    #         final_row_product = [list(x) for x in row]
    #         repairing_data = []
    #         for i in row:
    #             repairing_data.append(list(i))
    try:
        del request.session['repair_start_date']
        del request.session['repair_end_date']
        del request.session['repair_string']
        del request.session['selected_list']
        del request.session['selected_product_list']
        del request.session['onsite_repair_product_string']
    except:
        pass

    context = {
        'final_row': final_row,
        'selected_list': selected_list,
        'selected_product_list': selected_product_list+selected_list,
        'final_row_product': final_row_product,
    }
    return render(request,'report/final_onsite_report.html',context)

@login_required(login_url='/')
def feedback_onrepairing(request,user_id,customer_id,onsiterepairing_id):
    feedback_form = Onsite_Repairing_Feedback_Form(request.POST or None, request.FILES or None)
    if Onsite_aftersales_service.objects.get(id=onsiterepairing_id).feedback_given:
        return HttpResponse('Feedback Already Submitted.')
    else:

        if request.method == 'POST':
            backend_team = request.POST.get('backend_team')
            onsite_worker = request.POST.get('onsite_worker')
            speed_of_performance = request.POST.get('speed_of_performance')
            price_of_reparing = request.POST.get('price_of_reparing')
            overall_interaction = request.POST.get('overall_interaction')
            about_hsco = request.POST.get('about_hsco')
            any_suggestion = request.POST.get('any_suggestion')

            item = Onsite_Feedback()
            item.backend_team = backend_team
            item.onsite_worker = onsite_worker
            item.speed_of_performance = speed_of_performance
            item.price_of_reparing = price_of_reparing
            item.overall_interaction = overall_interaction
            item.about_hsco = about_hsco
            item.any_suggestion = any_suggestion
            item.user_id = SiteUser.objects.get(id=user_id)
            item.customer_id = Customer_Details.objects.get(id=customer_id)
            item.onsiterepairing_id = Onsite_aftersales_service.objects.get(id=onsiterepairing_id)
            try:
                item.save()

                onsiterepairing = Onsite_aftersales_service.objects.get(id=onsiterepairing_id)
                onsiterepairing.avg_feedback = (float(backend_team) + float(onsite_worker) + float(speed_of_performance) + float(price_of_reparing) + float(overall_interaction)) / float(5.0)
                onsiterepairing.feedback_given = True
                onsiterepairing.save(update_fields=['avg_feedback', 'feedback_given'])

                if Employee_Analysis_month.objects.filter(Q(entry_date__month=datetime.now().month),
                                                          Q(user_id=SiteUser.objects.get(id=user_id))).count() > 0:
                    Employee_Analysis_month.objects.filter(user_id=user_id, entry_date__month=datetime.now().month,
                                                           year=datetime.now().year).update(
                        start_rating_feedback_onsite_reparing=(F(
                            "start_rating_feedback_onsite_reparing") + Onsite_aftersales_service.objects.get(id=onsiterepairing_id).avg_feedback) / 2.0)
                    # ead.total_sales_done_today=.filter(category_id_id=id).update(total_views=F("total_views") + value_of_goods)

                    # ead.save(update_fields=['total_sales_done_today'])

                else:
                    ead = Employee_Analysis_month()
                    ead.user_id = SiteUser.objects.get(id=user_id)
                    ead.start_rating_feedback_onsite_reparing = Onsite_aftersales_service.objects.get(id=onsiterepairing_id).avg_feedback
                    # ead.total_dispatch_done = value_of_goods
                    ead.manager_id = SiteUser.objects.get(id=user_id).group
                    ead.month = datetime.now().month
                    ead.year = datetime.now().year
                    ead.save()



            except:
                pass
            # mon = datetime.now().month

            # ess_id = Employee_Analysis_month.objects.get(user_id=user_id,entry_date__month=mon )
            #
            #
            # ess_id.start_rating_feedback_onsite_reparing = onsiterepairing.avg_feedback
            return HttpResponse('Feedback Submitted!!!')
        context = {
            'feedback_form': feedback_form,
        }
        return render(request,"feedback/feedback_onrepairing.html",context)


@login_required(login_url='/')
def load_onsite_reparing_stages_list(request,):
    selected = request.GET.get('loc_id')
    if check_admin_roles(request):  # For ADMIN

        onsite_list = Onsite_aftersales_service.objects.filter(
            (Q(user_id=request.user.pk) | Q(user_id__group__icontains=request.user.name)) & Q(user_id__is_deleted=False,
                                                                                              current_stage=selected))

    else:  # For EMPLOYEE

        onsite_list = Onsite_aftersales_service.objects.filter(
            (Q(user_id=request.user.pk) | Q(complaint_assigned_to=request.user.name)) & Q(
                current_stage=selected))

    context = {
        'onsite_list': onsite_list,
    }

    return render(request, 'AJAX/load_onsite_reparing_stage.html', context)

@login_required(login_url='/')
def onsite_analytics(request,):
    mon = datetime.now().month
    this_month = Employee_Analysis_month.objects.all().values('entry_date').annotate(
        data_sum=Sum('total_reparing_done_onsite'))
    this_lis_date = []
    this_lis_sum = []
    for i in this_month:
        x = i
        this_lis_date.append(x['entry_date'].strftime("%B-%Y"))
        this_lis_sum.append(x['data_sum'])

    from django.db.models import Max
    # Generates a "SELECT MAX..." query
    value = Employee_Analysis_month.objects.aggregate(Max('total_reparing_done_onsite'))
    print(value['total_reparing_done_onsite__max'])
    try:
        value = Employee_Analysis_month.objects.get(total_reparing_done_onsite=value['total_reparing_done_onsite__max'])
    except:
        pass

    value_low = Employee_Analysis_month.objects.aggregate(Min('total_reparing_done_onsite'))
    print(value_low['total_reparing_done_onsite__min'])
    try:
        value_low = Employee_Analysis_month.objects.filter(
            total_reparing_done_onsite=value_low['total_reparing_done_onsite__min']).order_by('id').first()
    except:
        pass
    context = {

        'this_lis_date': this_lis_date,
        'this_lis_sum': this_lis_sum,
        'value': value,
        'value_low': value_low,

    }
    return render(request, 'analytics/onsite_analytics.html',context)

@login_required(login_url='/')
def load_onsite_reparing_manager(request,):
    selected = request.GET.get('loc_id')
    current_month = datetime.now().month
    current_year = datetime.now().year
    if selected=='true':
        user_list = Employee_Analysis_month.objects.filter(entry_date__month=current_month,entry_date__year=current_year,manager_id__icontains=request.user.name,user_id__is_deleted=False,user_id__modules_assigned__icontains='Onsite Repairing Module')
        # dispatch_list = Employee_Analysis_month.objects.filter(user_id__group=str(request.user.name))

        context = {
            'user_list': user_list,
            'manager': True,
        }

        return render(request, 'AJAX/load_onsite_reparing_manager.html', context)
    else:
        if check_admin_roles(request):  # For ADMIN

            onsite_list = Onsite_aftersales_service.objects.filter(
                Q(user_id=request.user.pk) | Q(user_id__group__icontains=request.user.name, user_id__is_deleted=False,
                                               user_id__modules_assigned__icontains='Onsite Repairing Module')).order_by(
                '-id')

        else:  # For EMPLOYEE
            onsite_list = Onsite_aftersales_service.objects.filter(
                Q(user_id=request.user.pk) | Q(complaint_assigned_to=request.user.name)).order_by('-onsite_no')


        context = {
            'onsite_list': onsite_list,
            'manager': False,

        }

        return render(request, 'AJAX/load_onsite_reparing_manager.html', context)

# @login_required(login_url='/')
def onsitevisit_app_graph(request,user_id):
    from django.db.models import Sum
    # user_id = request.user.pk
    rep_feedback = Onsite_Feedback.objects.filter(user_id=user_id)
    backend_team = Onsite_Feedback.objects.filter(user_id=user_id).aggregate(Avg('backend_team'))
    onsite_worker = Onsite_Feedback.objects.filter(user_id=user_id).aggregate(Avg('onsite_worker'))
    price_of_reparing = Onsite_Feedback.objects.filter(user_id=user_id).aggregate(Avg('price_of_reparing'))
    overall_interaction = Onsite_Feedback.objects.filter(user_id=user_id).aggregate(Avg('overall_interaction'))
    speed_of_performance = Onsite_Feedback.objects.filter(user_id=user_id).aggregate(Avg('speed_of_performance'))

    try:
        backend_team_avg = round(backend_team['backend_team__avg'])
        price_of_reparing_avg = round(price_of_reparing['price_of_reparing__avg'])
        overall_interaction_avg = round(overall_interaction['overall_interaction__avg'])
        onsite_worker_avg = round(onsite_worker['onsite_worker__avg'])
        speed_of_performance_avg = round(speed_of_performance['speed_of_performance__avg'])
        context={
            'backend_team_avg': backend_team_avg,
            'onsite_worker_avg': onsite_worker_avg,
            'price_of_reparing_avg': price_of_reparing_avg,
            'overall_interaction_avg': overall_interaction_avg,
            'speed_of_performance_avg': speed_of_performance_avg,
        }
        context.update(context)
    except:
        pass
    mon = datetime.now().month

    print(user_id)
    obj = Employee_Analysis_month.objects.get(user_id=user_id,entry_date__month=mon)
    try:
        obj.onsitereparing_target_achived_till_now = (obj.total_reparing_done_onsite / obj.onsitereparing_target_given) * 100
    except:
        pass
    obj.save(update_fields=['onsitereparing_target_achived_till_now'])
    # current month
    target_achieved = obj.onsitereparing_target_achived_till_now
    avg_time =  obj.avg_time_to_repair_single_scale

    # current month
    this_month = Onsite_aftersales_service.objects.filter(complaint_assigned_to=SiteUser.objects.get(id=user_id).profile_name,entry_timedate__month=datetime.now().month)\
        .values('entry_timedate').annotate(data_sum=Sum('total_cost'))
    this_lis_date = []
    this_lis_sum = []
    for i in this_month:
        x = i
        this_lis_date.append(x['entry_timedate'].strftime('%Y-%m-%d'))
        this_lis_sum.append(x['data_sum'])

    # previous month sales
    mon = (datetime.now().month)
    if mon == 1:
        previous_mon = 12
    else:
        previous_mon = (datetime.now().month) - 1
    previous_month = Onsite_aftersales_service.objects.filter(complaint_assigned_to=SiteUser.objects.get(id=user_id).profile_name,entry_timedate__month=previous_mon)\
        .values('entry_timedate').annotate(data_sum=Sum('total_cost'))
    previous_lis_date = []
    previous_lis_sum = []
    for i in previous_month:
        x = i
        previous_lis_date.append(x['entry_timedate'].strftime('%Y-%m-%d'))
        previous_lis_sum.append(x['data_sum'])

    if request.method == 'POST' and 'date1' in request.POST:
        start_date = request.POST.get('date1')
        end_date = request.POST.get('date2')
        qs = Onsite_aftersales_service.objects.filter(complaint_assigned_to=SiteUser.objects.get(id=user_id).profile_name,entry_date__range=(start_date, end_date)) \
            .values('entry_timedate').annotate(data_sum=Sum('total_cost'))

        lis_date = []
        lis_sum = []
        for i in qs:
            x = i
            lis_date.append(x['entry_timedate'].strftime('%Y-%m-%d'))
            lis_sum.append(x['data_sum'])

        context = {
            'final_list': lis_date,
            'final_list2': lis_sum,
            'previous_lis_date': previous_lis_date,
            'previous_lis_sum': previous_lis_sum,
            'this_lis_date': this_lis_date,
            'this_lis_sum': this_lis_sum,
            'target_achieved': target_achieved,
            'rep_feedback': rep_feedback,

        }
        return render(request, "graphs/onsitevisit_app_graph2.html", context)
    elif request.method=='POST' and 'defect_submit' in request.POST:
        defect = request.POST.get('defect')

        def_obj = Defects_Warning()


        if defect != None or defect != '' or defect != 'None':
            def_obj.content = defect
            def_obj.type = 'defect'

        def_obj.user_id = SiteUser.objects.get(id=user_id)
        def_obj.given_by = SiteUser.objects.get(id=request.user.id).profile_name
        def_obj.save()
        return HttpResponse('Defect Submitted!!!')
    elif request.method=='POST' and 'warning_submit' in request.POST:
        warning = request.POST.get('warning')

        def_obj = Defects_Warning()

        if warning != None or warning != '' or warning != 'None':
            def_obj.content = warning
            def_obj.type = 'warning'
        def_obj.user_id = SiteUser.objects.get(id=user_id)
        def_obj.given_by = SiteUser.objects.get(id=request.user.id).profile_name
        def_obj.save()
        return HttpResponse('Warning Submitted!!!')
    else:

        qs = Onsite_aftersales_service.objects.filter(complaint_assigned_to=SiteUser.objects.get(id=user_id).profile_name,entry_timedate__month=datetime.now().month)\
        .values('entry_timedate').annotate(data_sum=Sum('total_cost'))
        lis_date = []
        lis_sum = []
        for i in qs:
            x = i
            lis_date.append(x['entry_timedate'].strftime('%Y-%m-%d'))
            lis_sum.append(x['data_sum'])
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
            'target_achieved': target_achieved,
            'rep_feedback': rep_feedback,
        }
        try:
            backend_team_avg = round(backend_team['backend_team__avg'])
            price_of_reparing_avg = round(price_of_reparing['price_of_reparing__avg'])
            overall_interaction_avg = round(overall_interaction['overall_interaction__avg'])
            onsite_worker_avg = round(onsite_worker['onsite_worker__avg'])
            speed_of_performance_avg = round(speed_of_performance['speed_of_performance__avg'])
            context = {
                'backend_team_avg': backend_team_avg,
                'onsite_worker_avg': onsite_worker_avg,
                'price_of_reparing_avg': price_of_reparing_avg,
                'overall_interaction_avg': overall_interaction_avg,
                'speed_of_performance_avg': speed_of_performance_avg,
            }
            context.update(context)
        except:
            pass
        return render(request,"graphs/onsitevisit_app_graph2.html",context)

@login_required(login_url='/')
def onsite_repairing_logs(request):
    return render(request,"logs/onsite_reparing_logs.html",)

