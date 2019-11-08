from django.db import connection
from django.db.models import Sum, Min, Q, F
from django.http import HttpResponse
from django.shortcuts import render, redirect
from _datetime import datetime

from customer_app.models import Customer_Details

from ess_app.models import Employee_Analysis_month

from user_app.models import SiteUser

from purchase_app.views import check_admin_roles
from .forms import add_Onsite_aftersales_service_form

from .forms import Onsite_Repairing_Feedback_Form
from .models import Onsite_aftersales_service, Onsite_Products, Onsite_Feedback
from django.core.mail import send_mail
from Hsco import settings
from ess_app.models import Employee_Analysis_month
from ess_app.models import Employee_Analysis_date
import requests
import json


def onsite_views(request):

    if request.method=='POST' and 'deleted' not in request.POST:
        if'submit1' in request.POST:
            start_date = request.POST.get('date1')
            end_date = request.POST.get('date2')
            if check_admin_roles(request):  # For ADMIN
                onsite_list = Onsite_aftersales_service.objects.filter(user_id__group__icontains=request.user.group,
                                                                       user_id__is_deleted=False,entry_timedate__range=[start_date, end_date]).order_by('-id')
            else:  # For EMPLOYEE
                onsite_list = Onsite_aftersales_service.objects.filter(user_id=request.user.pk,entry_timedate__range=[start_date, end_date]).order_by('-id')

            # onsite_list = Onsite_aftersales_service.objects.filter(entry_timedate__range=[start_date, end_date])
            context = {
                'onsite_list': onsite_list,
            }
            return render(request, "manager/onsite_reparing.html", context)
        elif 'submit2' in request.POST:
            contact = request.POST.get('contact')
            if check_admin_roles(request):  # For ADMIN
                onsite_list = Onsite_aftersales_service.objects.filter(user_id__group__icontains=request.user.group,
                                                                       user_id__is_deleted=False,crm_no__contact_no=contact).order_by('-id')
            else:  # For EMPLOYEE
                onsite_list = Onsite_aftersales_service.objects.filter(user_id=request.user.pk,crm_no__contact_no=contact).order_by('-id')
            # onsite_list = Onsite_aftersales_service.objects.filter(phone_no=contact)
            context = {
                'onsite_list': onsite_list,
            }
            return render(request, "manager/onsite_reparing.html", context)

        elif 'submit3' in request.POST:
            email = request.POST.get('email')
            if check_admin_roles(request):  # For ADMIN
                onsite_list = Onsite_aftersales_service.objects.filter(user_id__group__icontains=request.user.group,
                                                                       user_id__is_deleted=False,crm_no__customer_email_id=email).order_by('-id')
            else:  # For EMPLOYEE
                onsite_list = Onsite_aftersales_service.objects.filter(user_id=request.user.pk,crm_no__customer_email_id=email).order_by('-id')
            # onsite_list = Onsite_aftersales_service.objects.filter(customer_email_id=email)
            context = {
                'onsite_list': onsite_list,
            }
            return render(request, "manager/onsite_reparing.html", context)
        elif 'submit4' in request.POST:
            customer = request.POST.get('customer')
            if check_admin_roles(request):  # For ADMIN
                onsite_list = Onsite_aftersales_service.objects.filter(user_id__group__icontains=request.user.group,
                                                                       user_id__is_deleted=False,crm_no__customer_name=customer).order_by('-id')
            else:  # For EMPLOYEE
                onsite_list = Onsite_aftersales_service.objects.filter(user_id=request.user.pk,crm_no__customer_name=customer).order_by('-id')
            # onsite_list = Onsite_aftersales_service.objects.filter(customer_name=customer)
            context = {
                'onsite_list': onsite_list,
            }
            return render(request, "manager/onsite_reparing.html", context)

        elif  'submit5' in request.POST:
            company = request.POST.get('company')
            if check_admin_roles(request):  # For ADMIN
                onsite_list = Onsite_aftersales_service.objects.filter(user_id__group__icontains=request.user.group,
                                                                       user_id__is_deleted=False,crm_no__company_name=company).order_by('-id')
            else:  # For EMPLOYEE
                onsite_list = Onsite_aftersales_service.objects.filter(user_id=request.user.pk,crm_no__company_name=company).order_by('-id')
            # onsite_list = Onsite_aftersales_service.objects.filter(company_name=company)
            context = {
                'onsite_list': onsite_list,
            }
            return render(request, "manager/onsite_reparing.html", context)
        elif request.method=='POST' and 'submit6' in request.POST:
            crm = request.POST.get('crm')
            if check_admin_roles(request):  # For ADMIN
                onsite_list = Onsite_aftersales_service.objects.filter(user_id__group__icontains=request.user.group,
                                                                       user_id__is_deleted=False,crm_no__pk=crm).order_by('-id')
            else:  # For EMPLOYEE
                onsite_list = Onsite_aftersales_service.objects.filter(user_id=request.user.pk,crm_no__pk=crm).order_by('-id')
            # onsite_list = Onsite_aftersales_service.objects.filter(crn_number=crm)
            context = {
                'onsite_list': onsite_list,
            }
            return render(request, "manager/onsite_reparing.html", context)
    elif 'deleted' in request.POST:
        if check_admin_roles(request):  # For ADMIN
            onsite_list = Onsite_aftersales_service.objects.filter(user_id__group__icontains=request.user.group,user_id__is_deleted=True).order_by('-id')
        else:  # For EMPLOYEE
            onsite_list = Onsite_aftersales_service.objects.filter(user_id=request.user.pk).order_by('-id')
        # onsite_list = Onsite_aftersales_service.objects.all()

        context = {
            'onsite_list': onsite_list,
            'deleted': True,

        }
        return render(request, "manager/onsite_reparing.html", context)
    else:
        if check_admin_roles(request):     #For ADMIN
            onsite_list = Onsite_aftersales_service.objects.filter(user_id__group__icontains=request.user.group,user_id__is_deleted=False).order_by('-id')
        else:  #For EMPLOYEE
            onsite_list = Onsite_aftersales_service.objects.filter(user_id=request.user.pk).order_by('-id')
        # onsite_list = Onsite_aftersales_service.objects.all()

        context = {
            'onsite_list': onsite_list,
        }
        return render(request, "manager/onsite_reparing.html", context)


def add_onsite_aftersales_service(request):
    cust_sugg = Customer_Details.objects.all()
    if request.user.role == 'Super Admin' or request.user.role == 'Admin' or request.user.role == 'Manager':
        user_list = SiteUser.objects.filter(group__icontains=request.user.name,
                                            modules_assigned__icontains='Onsite Repairing Module' , is_deleted=False)


    else:  # display colleague
        list_group = SiteUser.objects.get(id=request.user.id).group
        import ast

        x = "[" + list_group + "]"
        x = ast.literal_eval(x)
        manager_list = []
        for item in x:
            name = SiteUser.objects.filter(name__icontains=item)
            for it in name:
                if it.role == 'Manager':
                    if item not in manager_list:
                        manager_list.append(item)

        user_list = SiteUser.objects.filter(group__icontains=manager_list,
                                            modules_assigned__icontains='Onsite Repairing Module',is_deleted=False)


    # user_list=SiteUser.objects.filter(group__icontains=request.user.name,modules_assigned__icontains='Onsite Repairing Module')

    # form = add_Onsite_aftersales_service_form(request.POST or None, request.FILES or None)
    if request.method == 'POST' or request.method == 'FILES':
        customer_name = request.POST.get('customer_name')
        company_name = request.POST.get('company_name')
        address = request.POST.get('customer_address')
        contact_no = request.POST.get('contact_no')
        customer_email_id = request.POST.get('customer_email_id')

        previous_repairing_number = request.POST.get('previous_repairing_number')
        in_warranty = request.POST.get('in_warranty')
        date_of_complaint_received = request.POST.get('date_of_complaint_received')
        complaint_received_by = request.POST.get('complaint_received_by')
        nearest_railwaystation = request.POST.get('nearest_railwaystation')
        train_line = request.POST.get('train_line')
        products_to_be_repaired = request.POST.get('products_to_be_repaired')

        visiting_charges_told_customer = request.POST.get('visiting_charges_told_customer')
        total_cost = 0.0
        complaint_assigned_to = request.POST.get('complaint_assigned_to')
        complaint_assigned_on = request.POST.get('complaint_assigned_on')
        time_taken_destination_return_office_min = request.POST.get('time_taken_destination_return_office_min')
        notes = request.POST.get('notes')
        # feedback_given = request.POST.get('feedback_given')


        item2 = Onsite_aftersales_service()


        item = Customer_Details()
        if Customer_Details.objects.filter(Q(customer_email_id=customer_email_id),
                                           Q(contact_no=contact_no)).count() > 0:

            item2.crm_no = Customer_Details.objects.filter(Q(customer_email_id=customer_email_id),
                                                           Q(contact_no=contact_no)).first()
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

            if company_name != '':
                item.company_name = company_name
            if address != '':
                item.address = address
            if customer_email_id != '':
                item.customer_email_id = customer_email_id
            # item.user_id = SiteUser.objects.get(id=request.user.pk)
            # item.manager_id = SiteUser.objects.get(id=request.user.pk).group
            item.save()
            item2.crm_no = Customer_Details.objects.get(id=item.pk)


        # item2.repairingno = repairingno
        item2.previous_repairing_number = previous_repairing_number
        item2.in_warranty = in_warranty
        item2.date_of_complaint_received = date_of_complaint_received
        item2.complaint_received_by = complaint_received_by
        item2.nearest_railwaystation = nearest_railwaystation
        item2.train_line = train_line
        item2.products_to_be_repaired = products_to_be_repaired

        item2.visiting_charges_told_customer = visiting_charges_told_customer
        item2.total_cost = 0.0
        item2.complaint_assigned_to = complaint_assigned_to
        item2.complaint_assigned_on = complaint_assigned_on
        item2.time_taken_destination_return_office_min = time_taken_destination_return_office_min
        item2.notes = notes
        item2.feedback_given = False
        item2.user_id = SiteUser.objects.get(id=request.user.pk)
        item2.manager_id = SiteUser.objects.get(id=request.user.pk).group

        item2.save()

        if Employee_Analysis_date.objects.filter(Q(entry_date=datetime.now().date()),
                                                 Q(user_id=SiteUser.objects.get(id=request.user.pk))).count() > 0:
            Employee_Analysis_date.objects.filter(user_id=request.user.pk, entry_date__month=datetime.now().month,
                                                  year=datetime.now().year).update(
                total_reparing_done_onsite_today=F("total_reparing_done_onsite_today") + total_cost)
            # ead.total_sales_done_today=.filter(category_id_id=id).update(total_views=F("total_views") + value_of_goods)


            # ead.save(update_fields=['total_sales_done_today'])

        else:
            ead = Employee_Analysis_date()
            ead.user_id = SiteUser.objects.get(id=request.user.pk)
            ead.total_reparing_done_onsite_today = total_cost
            ead.manager_id = SiteUser.objects.get(id=request.user.pk).group

            ead.month = datetime.now().month
            ead.year = datetime.now().year
            ead.save()

        if Employee_Analysis_month.objects.filter(Q(entry_date__month=datetime.now().month),
                                                  Q(user_id=SiteUser.objects.get(id=request.user.pk))).count() > 0:
            Employee_Analysis_month.objects.filter(user_id=request.user.pk, entry_date__month=datetime.now().month,
                                                   year=datetime.now().year).update(
                total_reparing_done=F("total_reparing_done_onsite") + total_cost)
            # ead.total_sales_done_today=.filter(category_id_id=id).update(total_views=F("total_views") + value_of_goods)

            # ead.save(update_fields=['total_sales_done_today'])

        else:
            ead = Employee_Analysis_month()
            ead.user_id = SiteUser.objects.get(id=request.user.pk)
            ead.total_reparing_done_onsite = total_cost
            ead.manager_id = SiteUser.objects.get(id=request.user.pk).group

            ead.month = datetime.now().month
            ead.year = datetime.now().year
            ead.save()


        if Customer_Details.objects.filter(Q(customer_name=customer_name),Q(contact_no=contact_no)).count() > 0:
            crm_no = Customer_Details.objects.filter(Q(customer_name=customer_name),Q(contact_no=contact_no)).first()
            try:
                send_mail('Feedback Form',
                      'Click on the link to give feedback http://vikka.pythonanywhere.com/feedback_onrepairing/' + str(
                          request.user.pk) + '/' + str(crm_no.pk) + '/' + str(item2.id), settings.EMAIL_HOST_USER,
                      [crm_no.customer_email_id])
            except:
                pass

            message = 'Click on the link to give feedback http://vikka.pythonanywhere.com/feedback_onrepairing/' + str(
                request.user.pk) + '/' + str(crm_no.pk) + '/' + str(item2.id)

            url = "http://smshorizon.co.in/api/sendsms.php?user=" + settings.user + "&apikey=" + settings.api + "&mobile=" + crm_no.contact_no + "&message=" + message + "&senderid=" + settings.senderid + "&type=txt"
            payload = ""
            headers = {'content-type': 'application/x-www-form-urlencoded'}

            response = requests.request("GET", url, data=json.dumps(payload), headers=headers)
            x = response.text
        else:

            try:
                send_mail('Feedback Form',
                      'Click on the link to give feedback http://vikka.pythonanywhere.com/feedback_onrepairing/' + str(
                          request.user.pk) + '/' + str(item.pk) + '/' + str(item2.id), settings.EMAIL_HOST_USER,
                      [item.customer_email_id])
            except:
                pass

            message = 'Click on the link to give feedback http://vikka.pythonanywhere.com/feedback_onrepairing/' + str(
                request.user.pk) + '/' + str(item.pk) + '/' + str(item2.id)

            url = "http://smshorizon.co.in/api/sendsms.php?user=" + settings.user + "&apikey=" + settings.api + "&mobile=" + item.contact_no + "&message=" + message + "&senderid=" + settings.senderid + "&type=txt"
            payload = ""
            headers = {'content-type': 'application/x-www-form-urlencoded'}

            response = requests.request("GET", url, data=json.dumps(payload), headers=headers)
            x = response.text


        return redirect('/add_onsite_product/'+str(item2.id))
    context={
        'cust_sugg':cust_sugg,
        'user_list':user_list,

    }

    return render(request, 'forms/onsite_rep_form.html',context)

def add_onsite_product(request,id):
    onsite_id = Onsite_aftersales_service.objects.get(id=id).id
    crm_id = Onsite_aftersales_service.objects.get(id=id).crm_no
    print(onsite_id)
    if request.method == 'POST' or request.method == 'FILES':
        type_of_machine = request.POST.get('type_of_machine')
        model = request.POST.get('model')
        sub_model = request.POST.get('sub_model')
        capacity = request.POST.get('capacity')
        problem_in_scale = request.POST.get('problem_in_scale')
        components_replaced_in_warranty = request.POST.get('components_replaced_in_warranty')
        components_replaced = request.POST.get('components_replaced')
        cost = request.POST.get('cost')

        item = Onsite_Products()

        item.onsite_repairing_id_id = onsite_id
        item.type_of_machine = type_of_machine
        item.model = model
        item.sub_model = sub_model
        item.capacity = capacity
        item.problem_in_scale = problem_in_scale
        item.components_replaced_in_warranty = components_replaced_in_warranty
        item.components_replaced = components_replaced
        item.cost = cost
        item.user_id = SiteUser.objects.get(id=request.user.pk)
        item.manager_id = SiteUser.objects.get(id=request.user.pk).group
        item.crm_no = Customer_Details.objects.get(id=crm_id)
        item.save()


        Onsite_aftersales_service.objects.filter(id=id).update(total_cost=F("total_cost") + cost)
        Employee_Analysis_month.objects.filter(user_id=request.user.pk, entry_date__month=datetime.now().month,
                                               year=datetime.now().year).update(
            total_reparing_done=F("total_reparing_done_onsite") + cost)

        Employee_Analysis_date.objects.filter(user_id=request.user.pk, entry_date__month=datetime.now().month,
                                              year=datetime.now().year).update(
            total_reparing_done_today=F("total_reparing_done_onsite_today") + cost)

        return redirect('/update_onsite_details/'+str(id))
    context = {
        'onsite_id': onsite_id,
    }
    return render(request,"forms/onsite_product.html",context)

def update_onsite_product(request,id):
    onsite_id = Onsite_Products.objects.get(id=id)
    onsite = Onsite_aftersales_service.objects.get(id=onsite_id.onsite_repairing_id.pk).pk
    # crm_id = Onsite_aftersales_service.objects.get(id=onsite).crm_no
    print(onsite_id)
    if request.method == 'POST' or request.method == 'FILES':
        type_of_machine = request.POST.get('type_of_machine')
        model = request.POST.get('model')
        sub_model = request.POST.get('sub_model')
        capacity = request.POST.get('capacity')
        problem_in_scale = request.POST.get('problem_in_scale')
        components_replaced_in_warranty = request.POST.get('components_replaced_in_warranty')
        components_replaced = request.POST.get('components_replaced')
        cost = request.POST.get('cost')

        cost2 = onsite_id.cost

        Onsite_aftersales_service.objects.filter(id=onsite).update(total_cost=F("total_cost") - cost2)

        Employee_Analysis_month.objects.filter(user_id=request.user.pk,
                                               entry_date__month=onsite_id.entry_timedate.month,
                                               year=onsite_id.entry_timedate.year).update(
            total_reparing_done=F("total_reparing_done_onsite") - cost2)

        Employee_Analysis_date.objects.filter(user_id=request.user.pk,
                                              entry_date__month=onsite_id.entry_timedate.month,
                                              year=onsite_id.entry_timedate.year).update(
            total_reparing_done_today=F("total_reparing_done_onsite_today") - cost2)

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


        Onsite_aftersales_service.objects.filter(id=onsite).update(total_cost=F("total_cost") + cost)

        Employee_Analysis_month.objects.filter(user_id=request.user.pk,
                                               entry_date__month=onsite_id.entry_timedate.month,
                                               year=onsite_id.entry_timedate.year).update(
            total_reparing_done=F("total_reparing_done_onsite") + cost)

        Employee_Analysis_date.objects.filter(user_id=request.user.pk,
                                              entry_date__month=onsite_id.entry_timedate.month,
                                              year=onsite_id.entry_timedate.year).update(
            total_reparing_done_today=F("total_reparing_done_onsite_today") + cost)



        return redirect('/update_onsite_details/'+str(id))
    context = {
        'onsite_id': onsite_id,
    }
    return render(request,"edit_product/edit_onsite_product.html",context)

def update_onsite_details(request,id):
    onsite_id = Onsite_aftersales_service.objects.get(id=id)
    onsite_product_list = Onsite_Products.objects.filter(onsite_repairing_id=id)
    employee_list = SiteUser.objects.filter(role='Employee',group__icontains=request.user.name)
    customer_id = Onsite_aftersales_service.objects.get(id=id).crm_no

    customer_id = Customer_Details.objects.get(id=customer_id)
    try:
        feedback = Onsite_Feedback.objects.get(onsite_repairing_id=onsite_id.pk, customer_id=customer_id)
        print(feedback)
        print(id)
        print(customer_id.pk)
    except:
        feedback = None
    print(onsite_product_list)
    if request.method == 'POST' or request.method == 'FILES':
        contact_no = request.POST.get('contact_no')
        customer_email = request.POST.get('customer_email_id')
        customer_name = request.POST.get('customer_name')
        company_name = request.POST.get('company_name')
        customer_address = request.POST.get('customer_address')

        item2 = customer_id

        item2.customer_name = customer_name
        # item2.company_name = company_name
        # item2.address = customer_address
        item2.contact_no = contact_no
        if company_name != '':
            item2.company_name = company_name
            item2.save(update_fields=['company_name'])
        if customer_address != '':
            item2.address = customer_address
            item2.save(update_fields=['address'])

        if customer_email != '':
            item2.customer_email_id = customer_email
            item2.save(update_fields=['customer_email_id'])

        # repairingno = request.POST.get('repairingno')
        # customer_no = request.POST.get('customer_no')
        previous_repairing_number = request.POST.get('previous_repairing_number')
        in_warranty = request.POST.get('in_warranty')
        # customer_email_id = request.POST.get('customer_email_id')
        date_of_complaint_received = request.POST.get('date_of_complaint_received')
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


        item = onsite_id

        # item.repairingno = repairingno
        item.customer_name = customer_name
        item.company_name = company_name
        # item.customer_no = customer_no
        item.previous_repairing_number = previous_repairing_number
        item.in_warranty = in_warranty
        # item.customer_email_id = customer_email_id
        item.date_of_complaint_received = date_of_complaint_received
        item.customer_address = customer_address
        item.complaint_received_by = complaint_received_by
        item.nearest_railwaystation = nearest_railwaystation
        item.train_line = train_line
        # item.products_to_be_repaired = products_to_be_repaired
        item.visiting_charges_told_customer = visiting_charges_told_customer
        # item.total_cost = total_cost
        item.complaint_assigned_to = complaint_assigned_to
        item.complaint_assigned_on = complaint_assigned_on
        item.time_taken_destination_return_office_min = time_taken_destination_return_office_min
        item.notes = notes
        # item.feedback_given = feedback_given
        item.assigned_to = assigned_to

        #item.save(update_fields=['onsite_repairing_id_id', ]),
        item.save(update_fields=['assigned_to', ]),
        # item.save(update_fields=['repairingno', ]),
        # item.save(update_fields=['customer_name', ]),
        # item.save(update_fields=['company_name', ]),
        # item.save(update_fields=['customer_no', ]),
        item.save(update_fields=['previous_repairing_number', ]),
        item.save(update_fields=['in_warranty', ]),
        # item.save(update_fields=['phone_no', ]),
        # item.save(update_fields=['customer_email_id', ]),
        item.save(update_fields=['date_of_complaint_received', ]),
        # item.save(update_fields=['customer_address', ]),
        item.save(update_fields=['complaint_received_by', ]),
        item.save(update_fields=['nearest_railwaystation', ]),
        item.save(update_fields=['train_line', ]),
        # item.save(update_fields=['products_to_be_repaired', ]),
        item.save(update_fields=['visiting_charges_told_customer', ]),
        # item.save(update_fields=['total_cost', ]),
        item.save(update_fields=['complaint_assigned_to', ]),
        item.save(update_fields=['complaint_assigned_on', ]),
        item.save(update_fields=['time_taken_destination_return_office_min', ]),
        item.save(update_fields=['notes', ]),
        # item.save(update_fields=['feedback_given', ]),
        onsite_id = Onsite_aftersales_service.objects.get(id=id)

        context = {
            'onsite_id': onsite_id,
            'onsite_product_list': onsite_product_list,
        }

        return render(request, 'update_forms/update_onsite_rep_form.html', context)


    context={
        'onsite_id':onsite_id,
        'onsite_product_list':onsite_product_list,
        'employee_list':employee_list,
        'feedback': feedback,
    }

    return render(request,'update_forms/update_onsite_rep_form.html',context)

def report_onsite(request):
    if request.method == 'POST' or None:
        selected_list = request.POST.getlist('checks[]')
        onsite_start_date = request.POST.get('date1')
        onsite_end_date = request.POST.get('date2')
        onsite_string = ','.join(selected_list)

        request.session['start_date'] = onsite_start_date
        request.session['repair_end_date'] = onsite_end_date
        request.session['repair_string'] = onsite_string
        request.session['selected_list'] = selected_list
        return redirect('/final_report_onsite/')
    return render(request,"report/report_onsite_rep_form.html",)

def final_report_onsite(request):
    repair_start_date = str(request.session.get('repair_start_date'))
    repair_end_date = str(request.session.get('repair_end_date'))
    repair_string = request.session.get('repair_string')
    selected_list = request.session.get('selected_list')
    with connection.cursor() as cursor:
        cursor.execute("SELECT  " + repair_string + " from onsitevisit_app_onsite_aftersales_service , customer_app_customer_details"
                                             "  where onsitevisit_app_onsite_aftersales_service.crm_no_id = customer_app_customer_details.id and entry_timedate between '" + repair_start_date + "' and '" + repair_end_date + "';")
        row = cursor.fetchall()

        print(row)
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
    return render(request,'report/final_onsite_report.html',context)

def feedback_onrepairing(request,user_id,customer_id,onsiterepairing_id):
    feedback_form = Onsite_Repairing_Feedback_Form(request.POST or None, request.FILES or None)
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


def load_onsite_reparing_stages_list(request,):
    selected = request.GET.get('loc_id')
    onsite_list = Onsite_aftersales_service.objects.filter(current_stage=selected)
    context = {
        'onsite_list': onsite_list,
    }

    return render(request, 'AJAX/load_onsite_reparing_stage.html', context)

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
        value = Employee_Analysis_month.objects.get(total_sales_done=value['total_reparing_done_onsite__max'])
    except:
        pass

    value_low = Employee_Analysis_month.objects.aggregate(Min('total_reparing_done_onsite'))
    print(value_low['total_reparing_done_onsite__min'])
    try:
        value_low = Employee_Analysis_month.objects.filter(
            total_sales_done=value_low['total_reparing_done_onsite__min']).order_by('id').first()
    except:
        pass
    context = {

        'this_lis_date': this_lis_date,
        'this_lis_sum': this_lis_sum,
        'value': value,
        'value_low': value_low,

    }
    return render(request, 'analytics/onsite_analytics.html',context)

def load_onsite_reparing_manager(request,):
    selected = request.GET.get('loc_id')

    if selected=='true':
        user_list = Employee_Analysis_month.objects.filter(manager_id=request.user.name)
        # dispatch_list = Employee_Analysis_month.objects.filter(user_id__group=str(request.user.name))

        context = {
            'user_list': user_list,
            'manager': True,
        }

        return render(request, 'AJAX/load_onsite_reparing_manager.html', context)
    else:
        onsite_list = Onsite_aftersales_service.objects.all()

        context = {
            'onsite_list': onsite_list,
            'manager': False,

        }

        return render(request, 'AJAX/load_onsite_reparing_manager.html', context)

def onsitevisit_app_graph(request,user_id):
    from django.db.models import Sum
    # user_id = request.user.pk
    rep_feedback = Onsite_Feedback.objects.all()
    mon = datetime.now().month

    print(user_id)
    obj = Employee_Analysis_month.objects.get(user_id=user_id,entry_date__month=mon)
    obj.onsitereparing_target_achived_till_now = (obj.total_reparing_done_onsite / obj.onsitereparing_target_given) * 100
    obj.save(update_fields=['onsitereparing_target_achived_till_now'])
    # current month
    target_achieved = obj.onsitereparing_target_achived_till_now
    # current month
    this_month = Employee_Analysis_date.objects.filter(user_id=user_id,entry_date__month=mon).values('entry_date',
                                                                                                     'total_reparing_done_onsite_today')
    this_lis_date = []
    this_lis_sum = []
    for i in this_month:
        x = i
        this_lis_date.append(x['entry_date'].strftime('%Y-%m-%d'))
        this_lis_sum.append(x['total_reparing_done_onsite_today'])

    # previous month sales
    mon = (datetime.now().month) - 1
    previous_month = Employee_Analysis_date.objects.filter(user_id=user_id,entry_date__month=mon).values('entry_date',
                                                                                                         'total_reparing_done_onsite_today')
    previous_lis_date = []
    previous_lis_sum = []
    for i in previous_month:
        x = i
        previous_lis_date.append(x['entry_date'].strftime('%Y-%m-%d'))
        previous_lis_sum.append(x['total_reparing_done_onsite_today'])

    if request.method == 'POST':
        start_date = request.POST.get('date1')
        end_date = request.POST.get('date2')
        qs = Employee_Analysis_date.objects.filter(user_id=user_id,entry_date__range=(start_date, end_date)).values(
            'entry_date','total_reparing_done_onsite_today')
        lis_date = []
        lis_sum = []
        for i in qs:
            x = i
            lis_date.append(x['entry_date'].strftime('%Y-%m-%d'))
            lis_sum.append(x['total_reparing_done_onsite_today'])

        context = {
            'final_list': lis_date,
            'final_list2': lis_sum,
            'previous_lis_date': previous_lis_date,
            'previous_lis_sum': previous_lis_sum,
            'this_lis_date': this_lis_date,
            'this_lis_sum': this_lis_sum,
            'target_achieved': target_achieved,
            # 'rep_feedback': rep_feedback,
        }
        return render(request, "graphs/onsitevisit_app_graph.html", context)
    else:

        qs = Employee_Analysis_date.objects.filter(user_id=user_id,entry_date__month=datetime.now().month).values('entry_date',
                                                                                                                  'total_reparing_done_onsite_today')
        lis_date = []
        lis_sum = []
        for i in qs:
            x = i
            lis_date.append(x['entry_date'].strftime('%Y-%m-%d'))
            lis_sum.append(x['total_reparing_done_onsite_today'])
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
            # 'feeback': feeback,
        }
        return render(request,"graphs/onsitevisit_app_graph.html",context)

