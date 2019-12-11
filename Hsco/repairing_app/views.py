from django.db import connection
from django.db.models import Min, Sum, Q, F
from django.http import HttpResponse
from django.shortcuts import render, redirect
from customer_app.models import Customer_Details
from django.utils import timezone
from user_app.models import SiteUser

from customer_app.models import Customer_Details

from purchase_app.views import check_admin_roles

from customer_app.models import type_purchase
from .forms import Repairing_Feedback_Form
from .models import Repairing_after_sales_service, Repairing_Product, Repairing_Feedback,Component_Replaced
from django.core.mail import send_mail
from Hsco import settings
import datetime
import requests
import json
from ess_app.models import Employee_Analysis_month, Employee_Analysis_date
from django.db.models import Count
from django.db.models import Q
from datetime import date,datetime, timedelta

def add_repairing_details(request):
    cust_sugg=Customer_Details.objects.all()
    prev_rep_sugg=Repairing_after_sales_service.objects.all()
    if request.user.role == 'Super Admin':
        user_list=SiteUser.objects.filter(Q(id=request.user.id) | Q(group__icontains=request.user.name),modules_assigned__icontains="'Repairing Module'", is_deleted=False)

    elif request.user.role == 'Admin':
        user_list = SiteUser.objects.filter(Q(id=request.user.id) | Q(admin=request.user.name),
                                            modules_assigned__icontains="'Repairing Module'", is_deleted=False)
    elif request.user.role == 'Manager':
        user_list = SiteUser.objects.filter(Q(id=request.user.id) | Q(manager=request.user.name),
                                            modules_assigned__icontains="'Repairing Module'", is_deleted=False)
    else: #display colleague

        list_group = SiteUser.objects.get(id=request.user.id).manager
        user_list = SiteUser.objects.filter(Q(id=request.user.id) | Q(manager=list_group),
                                            modules_assigned__icontains="'Repairing Module'", is_deleted=False)

        # import ast
        #
        # x = "[" + list_group + "]"
        # x = ast.literal_eval(x)
        # manager_list = []
        # for item in x:
        #     name = SiteUser.objects.filter(name__icontains=item)
        #     for it in name:
        #         if it.role == 'Manager':
        #             if item not in manager_list:
        #                 manager_list.append(item)
        #
        # user_list = SiteUser.objects.filter(group__icontains=manager_list,
        #                                     modules_assigned__icontains='Repairing Module', is_deleted=False)

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
        taken_by = request.POST.get('taken_by')
        # second_person = request.POST.get('second_person')
        # third_person = request.POST.get('third_person')
        # second_contact_no = request.POST.get('second_contact_no')
        # third_contact_no = request.POST.get('third_contact_no')
        # products_to_be_repaired = request.POST.get('products_to_be_repaired')

        total_cost = 0.0

        informed_on = request.POST.get('informed_on')


        informed_by = request.POST.get('informed_by')
        confirmed_estimate = request.POST.get('confirmed_estimate')
        repaired = request.POST.get('repaired')
        delivery_by = request.POST.get('delivery_by')
        feedback_given = request.POST.get('feedback_given')
        # current_stage = request.POST.get('current_stage')
        repaired_by = request.POST.get('repaired_by')

        item2 = Repairing_after_sales_service()

        item = Customer_Details()
        if Customer_Details.objects.filter(customer_name=customer_name,contact_no=contact_no).count() > 0:

            item2.crm_no = Customer_Details.objects.filter(customer_name=customer_name,contact_no=contact_no).first()
            item3 = Customer_Details.objects.filter(customer_name=customer_name, contact_no=contact_no).first()
            if company_name != '':
                item2.second_company_name = company_name  # new2

                item3.company_name = company_name
                item3.save(update_fields=['company_name'])
            if address != '':
                item3.address = address

                item2.company_address = address  # new2
                item3.save(update_fields=['address'])
            if customer_email_id != '':
                item3.customer_email_id = customer_email_id
                item2.company_email = customer_email_id  # new2
                item3.save(update_fields=['customer_email_id'])

        else:



            item.customer_name = customer_name
            if company_name != '':
                item2.second_company_name = company_name  # new2
                item.company_name = company_name
            if address != '':
                item.address = address
                item2.company_address = address  # new2
            item.contact_no = contact_no
            if customer_email_id != '':
                item2.company_email = customer_email_id  # new2
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
        item2.taken_by = taken_by
        item2.second_person = customer_name  # new1
        item2.second_contact_no = contact_no  # new2
        item2.entered_by = request.user.name  # new2
        # item2.second_person=second_person
        # item2.third_person=third_person
        # item2.second_contact_no=second_contact_no
        # item2.third_contact_no=third_contact_no
        # item2.products_to_be_repaired = products_to_be_repaired

        item2.total_cost = 0.0
        if informed_by != '' and informed_by!= None:
            item2.informed_on = datetime.today().strftime('%Y-%m-%d')

            item2.informed_by = informed_by
        if repaired_by != '' and repaired_by!= None:
            item2.repaired_date = datetime.today().strftime('%Y-%m-%d')

            item2.repaired_by = repaired_by
        item2.confirmed_estimate = confirmed_estimate
        item2.repaired = repaired
        item2.delivery_by = delivery_by
        # item2.repaired_by = repaired_by
        item2.feedback_given = False
        item2.user_id = SiteUser.objects.get(id=request.user.pk)
        item2.manager_id = SiteUser.objects.get(id=request.user.pk).group
        # item2.current_stage = current_stage


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


        # if Customer_Details.objects.filter(Q(customer_name=customer_name),Q(contact_no=contact_no)).count() > 0:
        #     crm_no = Customer_Details.objects.filter(Q(customer_name=customer_name),Q(contact_no=contact_no)).first()
        #     try:
        #         send_mail('Feedback Form',
        #               'Click on the link to give feedback http://139.59.76.87/feedback_repairing/' + str(
        #                   request.user.pk) + '/' + str(crm_no.pk) + '/' + str(item2.id), settings.EMAIL_HOST_USER,
        #               [crm_no.customer_email_id])
        #     except:
        #         pass
        #
        #     message = 'Click on the link to give feedback http://139.59.76.87/feedback_repairing/' + str(
        #         request.user.pk) + '/' + str(crm_no.pk) + '/' + str(item2.id)
        #
        #     url = "http://smshorizon.co.in/api/sendsms.php?user=" + settings.user + "&apikey=" + settings.api + "&mobile=" + crm_no.contact_no + "&message=" + message + "&senderid=" + settings.senderid + "&type=txt"
        #     payload = ""
        #     headers = {'content-type': 'application/x-www-form-urlencoded'}
        #
        #     response = requests.request("GET", url, data=json.dumps(payload), headers=headers)
        #     x = response.text
        # else:
        #     try:
        #
        #         send_mail('Feedback Form',
        #               'Click on the link to give feedback http://139.59.76.87/feedback_repairing/' + str(
        #                   request.user.pk) + '/' + str(item.pk) + '/' + str(item2.id), settings.EMAIL_HOST_USER,
        #               [item.customer_email_id])
        #     except:
        #         pass
        #
        #     message = 'Click on the link to give feedback http://139.59.76.87/feedback_repairing/' + str(
        #         request.user.pk) + '/' + str(item.pk) + '/' + str(item2.id)
        #
        #     url = "http://smshorizon.co.in/api/sendsms.php?user=" + settings.user + "&apikey=" + settings.api + "&mobile=" + item.contact_no + "&message=" + message + "&senderid=" + settings.senderid + "&type=txt"
        #     payload = ""
        #     headers = {'content-type': 'application/x-www-form-urlencoded'}
        #
        #     response = requests.request("GET", url, data=json.dumps(payload), headers=headers)
        #     x = response.text



        return redirect('/repair_product/'+str(item2.pk))


    context={
        'cust_sugg':cust_sugg,
        'user_list':user_list,
        'prev_rep_sugg':prev_rep_sugg,
    }

    return render(request,'forms/rep_mod_form.html',context)

def repair_product(request,id):
    repair_id = Repairing_after_sales_service.objects.get(id=id).id
    user_id = Repairing_after_sales_service.objects.get(id=id).user_id
    type_of_purchase_list =type_purchase.objects.all() #1
    components_replaced_popup = []

    if request.method=='POST' and 'components_replaced_popup_iw' not in request.POST and 'components_replaced_popup' not in request.POST:
        type_of_machine = request.POST.get('type_of_scale')
        model = request.POST.get('model_of_purchase')
        sub_model = request.POST.get('sub_model')


        problem_in_scale = request.POST.get('problem_in_scale')
        components_replaced_in_warranty = request.POST.get('components_replaced_in_warranty')
        components_replaced = request.POST.get('components_replaced')
        replaced_scale_given = request.POST.get('replaced_scale_given')
        Replaced_scale_serial_no = request.POST.get('Replaced_scale_serial_no')
        deposite_taken_for_replaced_scale = request.POST.get('deposite_taken_for_replaced_scale')
        cost = request.POST.get('cost')
        in_warranty = request.POST.get('in_warranty')
        is_last_product_yes = request.POST.get('is_last_product_yes')
        # is_last_product_no = request.POST.get('is_last_product_no')

        item=Repairing_Product()
        item.user_id = SiteUser.objects.get(id=request.user.pk)
        item.manager_id = SiteUser.objects.get(id=request.user.pk).group

        item.type_of_machine = type_of_machine
        # if model != None and model != '':
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
        print("is_last_product_yes")
        print(is_last_product_yes)
        print("is_last_product_no")
        # print(is_last_product_no)
        # if is_last_product_yes == None:
        #     item.is_last_product = False
        # else:
        #     item.is_last_product = True

        if in_warranty.lower() == 'yes':
            item.cost = 0.0
        else:
            item.cost = cost

        item.save()

        current_stage_in_db=Repairing_after_sales_service.objects.get(id=id).current_stage #updatestage1
        if (current_stage_in_db == '' or current_stage_in_db == None ) and (sub_model !='' or sub_model != None):
            Repairing_after_sales_service.objects.filter(id=id).update(current_stage='Scale is collected but estimate is not given',stage_update_timedate = timezone.now())
            # item2.save(update_fields=['stage_update_timedate', ])

        rep = Repairing_after_sales_service.objects.get(id=id)

        if is_last_product_yes == 'yes':
            ret = send_sms(request, rep.second_person, rep.second_contact_no, rep.crm_no.customer_email_id, id, '1')
            Repairing_after_sales_service.objects.filter(id=id).update(is_last_product_added=True)
            product_list = ''' '''
            pro_lis = Repairing_Product.objects.filter(repairing_id_id=rep.pk)

            for idx, item in enumerate(pro_lis):
                # for it in item:

                email_body_text = (
                    u"\nSr. No.: {},"
                    "\tModel: {},"
                    "\tSub Model: {}"
                    "\tproblem in scale: {}"
                    "\tReplaced scale serial no.: {}"
                    "\tCost: {}"

                ).format(
                    idx + 1,
                    item.type_of_machine,
                    item.sub_model,
                    item.problem_in_scale,
                    item.Replaced_scale_serial_no,
                    item.cost,
                )
                product_list = product_list + '' + str(email_body_text)

                msg_old= 'Click on the link to give feedback http://139.59.76.87/feedback_repairing/' + str(
                              request.user.pk) + '/' + str(rep.crm_no.pk) + '/' + str(rep.id) +'\nHere is a list of Products:\n'+product_list
                msg='Dear '+rep.second_person+',Thank you for selecting HSCo. Your Scales have been successfully ' \
                    'received at our Repairing Center. Your Repairing No is '+str(rep.pk)+'. Please use this Unique ID for further communication. For any ' \
                    'further details please contact our customer service team on 7045922251 \n Product Details:\n'+product_list
                # if Customer_Details.objects.filter(Q(customer_name=customer_name),Q(contact_no=contact_no)).count() > 0:
                # crm_no = Customer_Details.objects.filter(Q(customer_name=customer_name),Q(contact_no=contact_no)).first()
                try:
                    send_mail('Feedback Form',msg

                              ,settings.EMAIL_HOST_USER,
                          [rep.company_email])
                except:
                    pass

                message_old = 'Click on the link to give feedback http://139.59.76.87/feedback_repairing/' + str(
                    request.user.pk) + '/' + str(rep.crm_no.pk) + '/' + str(rep.id)

                message = 'Dear '+rep.second_person+', Thank you for selecting HSCo. Your Scales have been successfully ' \
                          'received at our Repairing Center. Your Repairing No is '+str(rep.pk)+'. Please use this Unique ID for ' \
                          'further communication. For any further details please contact our customer service team on 7045922251'

                url = "http://smshorizon.co.in/api/sendsms.php?user=" + settings.user + "&apikey=" + settings.api + "&mobile=" + rep.second_contact_no + "&message=" + message + "&senderid=" + settings.senderid + "&type=txt"
                payload = ""
                headers = {'content-type': 'application/x-www-form-urlencoded'}

                response = requests.request("GET", url, data=json.dumps(payload), headers=headers)
                x = response.text



                # pass
                # item.is_last_product = False
            # else:
            #     ret=send_sms(request, rep.second_person, rep.second_contact_no, rep.crm_no.customer_email_id, id, '1')


        # current_stage_in_db = Repairing_after_sales_service.objects.get(id=id).current_stage  #updatestage2

        if current_stage_in_db == 'Scale is collected but estimate is not given' and float(cost) > 0.0:
            Repairing_after_sales_service.objects.filter(id=id).update(
                current_stage='Estimate is given but Estimate is not confirmed',stage_update_timedate = timezone.now())



        Component_Replaced.objects.filter(pk__in=components_replaced_popup).update(product_id=item.pk)

        Repairing_after_sales_service.objects.filter(id=id).update(total_cost=F("total_cost") + cost)
        Employee_Analysis_month.objects.filter(user_id=user_id, entry_date__month=datetime.now().month,
                                               year=datetime.now().year).update(
            total_reparing_done=F("total_reparing_done") + cost)

        Employee_Analysis_date.objects.filter(user_id=user_id, entry_date__month=datetime.now().month,
                                              year=datetime.now().year).update(
            total_reparing_done_today=F("total_reparing_done_today") + cost)


        if is_last_product_yes == 'yes':
            return redirect('/update_repairing_details/'+str(id))
        elif is_last_product_yes == 'no':
            return redirect('/repair_product/'+str(id))
    # if request.method == 'POST' and 'components_replaced_popup' in request.POST and 'components_replaced_popup_iw' not in request.POST:
    #     replaced_name=request.POST.get('components_replaced_popup')
    #     in_waranty= False
    #     item = Component_Replaced()
    #     item.user_id=SiteUser.objects.get(id=request.user.pk)
    #     #item.product_id=
    #     item.replaced_name=replaced_name
    #     item.in_waranty=in_waranty
    #     item.save()
    #     components_replaced_popup.append(item.pk)
    #     components_replaced_popup_name.append(replaced_name)
    #     context3 = {
    #         'components_replaced_popup_name': components_replaced_popup_name,
    #     }
    #     context.update(context3)
    #
    # if request.method == 'POST' and 'components_replaced_popup_iw' in request.POST and 'components_replaced_popup' not in request.POST:
    #     replaced_name=request.POST.get('components_replaced_popup_iw')
    #     in_waranty=True
    #     item = Component_Replaced()
    #     item.user_id=SiteUser.objects.get(id=request.user.pk)
    #     #item.product_id=
    #     item.replaced_name=replaced_name
    #     item.in_waranty=in_waranty
    #     item.save()
    #     components_replaced_popup.append(item.pk)
    #     components_replaced_popup_iw_name.append(replaced_name)
    #     context2={
    #         'components_replaced_popup_iw': components_replaced_popup_iw_name,
    #     }
    #     context.update(context2)
    #



    context = {
        'repair_id': repair_id,
        'type_purchase': type_of_purchase_list,  # 2
    }
    return render(request,'dashboardnew/repair_product.html',context)

def update_repairing_details(request,id):
    repair_id = Repairing_after_sales_service.objects.get(id=id)
    # customer_id = Repairing_after_sales_service.objects.get(id=id).crm_no
    customer_id = Customer_Details.objects.get(id=repair_id.crm_no)
    repair_list = Repairing_Product.objects.filter(repairing_id=id)

    if request.user.role == 'Super Admin':
        user_list=SiteUser.objects.filter(Q(id=request.user.id) | Q(group__icontains=request.user.name),modules_assigned__icontains="'Repairing Module'", is_deleted=False)

    elif request.user.role == 'Admin':
        user_list = SiteUser.objects.filter(Q(id=request.user.id) | Q(admin=request.user.name),
                                            modules_assigned__icontains="'Repairing Module'", is_deleted=False)
    elif request.user.role == 'Manager':
        user_list = SiteUser.objects.filter(Q(id=request.user.id) | Q(manager=request.user.name),
                                            modules_assigned__icontains="'Repairing Module'", is_deleted=False)
    else: #display colleague

        list_group = SiteUser.objects.get(id=request.user.id).manager
        user_list = SiteUser.objects.filter(Q(id=request.user.id) | Q(manager=list_group),
                                            modules_assigned__icontains="'Repairing Module'", is_deleted=False)

    if request.method=='POST':
        customer_name = request.POST.get('customer_name')
        company_name = request.POST.get('company_name')
        address = request.POST.get('customer_address')
        contact_no = request.POST.get('contact_no')
        customer_email_id = request.POST.get('customer_email_id')

        item = customer_id

        item.customer_name = customer_name
        item.contact_no = contact_no
        item.save(update_fields=['customer_name', 'contact_no'])  # new3



        # repairingnumber = request.POST.get('repairingnumber')
        # previous_repairing_number = request.POST.get('previous_repairing_number')
        # today_date = request.POST.get('today_date')
        # location = request.POST.get('location')
        # products_to_be_repaired = request.POST.get('products_to_be_repaired')
        # second_person=request.POST.get('second_person')
        # third_person=request.POST.get('third_person')
        # second_contact_no=request.POST.get('second_contact_no')
        # third_contact_no=request.POST.get('third_contact_no')
        total_cost = request.POST.get('total_cost')
        informed_on = request.POST.get('informed_on')
        informed_by = request.POST.get('informed_by')
        confirmed_estimate = request.POST.get('confirmed_estimate')
        repaired = request.POST.get('repaired')
        taken_by = request.POST.get('taken_by')
        repaired_date = request.POST.get('repaired_date')
        delivery_date = request.POST.get('delivery_date')
        delivery_by = request.POST.get('delivery_by')
        repaired_by = request.POST.get('repaired_by')
        # feedback_given = request.POST.get('feedback_given')
        # current_stage = request.POST.get('current_stage')



        item2 = repair_id

        # item2.repairingnumber = repairingnumber
        item2.crm_no = Customer_Details.objects.get(id=item.pk)
        if company_name != '':
            item2.second_company_name = company_name  # new2

            item.company_name = company_name
            item.save(update_fields=['company_name'])
        if address != '':
            item.address = address

            item2.company_address = address  # new2
            item.save(update_fields=['address'])
        if customer_email_id != '':
            item.customer_email_id = customer_email_id
            item2.company_email = customer_email_id  # new2
            item.save(update_fields=['customer_email_id'])


        current_stage_in_db = Repairing_after_sales_service.objects.get(id=id).current_stage  # updatestage3
        if current_stage_in_db == 'Estimate is given but Estimate is not confirmed' and confirmed_estimate == 'Yes':
            Repairing_after_sales_service.objects.filter(id=id).update(
                current_stage='Estimate is confirmed but not repaired')
            item2.stage_update_timedate = timezone.now()
            item2.save(update_fields=['stage_update_timedate',])

            product_list = ''' '''
            pro_lis = Repairing_Product.objects.filter(repairing_id_id=id)

            for idx, item2 in enumerate(pro_lis):
                # for it in item:

                email_body_text = (
                    u"\nSr. No.: {},"
                    "\tModel: {},"
                    "\tSub Model: {}"
                    "\tComponents replaced: {}"
                    "\tComponents Replaced In Warranty: {}"


                ).format(
                    idx + 1,
                    item2.type_of_machine,
                    item2.sub_model,
                    item2.components_replaced,
                    item2.components_replaced_in_warranty,

                )
                product_list = product_list + '' + str(email_body_text)

            try:
                # msg='Click on the link to give feedback http://139.59.76.87/feedback_repairing/' + str(
                #               request.user.pk) + '/' + str(item.pk) + '/' + str(item2.id)
                msg='Dear '+customer_name+',Thank you for selecting HSCo. The Estimate for Your ' \
                    'Repairing No '+str(repair_id.pk)+' is  '+str(repair_id.total_cost)+' For any further details please contact our customer ' \
                    'service team on 7045922251 Estimate Details:\n'+product_list
                send_mail('Feedback Form',msg
                          , settings.EMAIL_HOST_USER,
                          [item.customer_email_id])
            except:
                pass

            # message = 'Click on the link to give feedback http://139.59.76.87/feedback_repairing/' + str(
            #     request.user.pk) + '/' + str(item.pk) + '/' + str(item2.id)

            message='Dear '+customer_name+',Thank you for selecting HSCo. The Estimate for Your ' \
                    'Repairing No '+str(repair_id.pk)+' is  '+str(repair_id.total_cost)+'/- For any further details please contact our customer ' \
                    'service team on 7045922251'

            url = "http://smshorizon.co.in/api/sendsms.php?user=" + settings.user + "&apikey=" + settings.api + "&mobile=" + item.contact_no + "&message=" + message + "&senderid=" + settings.senderid + "&type=txt"
            payload = ""
            headers = {'content-type': 'application/x-www-form-urlencoded'}

            response = requests.request("GET", url, data=json.dumps(payload), headers=headers)
            x = response.text

            Repairing_after_sales_service.objects.filter(id=id).update(
                estimate_informed_sms_count=F("estimate_informed_sms_count") + 1)







        current_stage_in_db = Repairing_after_sales_service.objects.get(id=id).current_stage  # updatestage4
        if current_stage_in_db == 'Estimate is confirmed but not repaired' and repaired == 'Yes':
            Repairing_after_sales_service.objects.filter(id=id).update(
                current_stage='Repaired but not collected')
            item2.stage_update_timedate = timezone.now()

            item2.repaired = repaired
            item2.save(update_fields=['stage_update_timedate', ])
            item2.save(update_fields=['repaired'])

            try:
                send_mail('Your Repairing Done - HSCo',
                          ' Dear '+customer_name+',Thank you for selecting HSCo. Your Repairing Complaint No '+str(repair_id.pk)+' is resolved.'
                          ' Please collect your Scales within the next 3 days.For any further details please contact '
                          'our customer service team on 7045922251', settings.EMAIL_HOST_USER,
                          [item.customer_email_id])
            except:
                pass

            # message = 'Click on the link to give feedback http://139.59.76.87/feedback_repairing/' + str(
            #     request.user.pk) + '/' + str(item.pk) + '/' + str(item2.id)

            message=' Dear '+customer_name+',Thank you for selecting HSCo. Your Repairing Complaint No '+str(repair_id.pk)+' is resolved. ' \
                    'Please collect your Scales within the next 3 days.For any further details please contact our ' \
                    'customer service team on 7045922251'

            url = "http://smshorizon.co.in/api/sendsms.php?user=" + settings.user + "&apikey=" + settings.api + "&mobile=" + item.contact_no + "&message=" + message + "&senderid=" + settings.senderid + "&type=txt"
            payload = ""
            headers = {'content-type': 'application/x-www-form-urlencoded'}

            response = requests.request("GET", url, data=json.dumps(payload), headers=headers)
            x = response.text
            Repairing_after_sales_service.objects.filter(id=id).update(
                reparing_done_sms_count=F("reparing_done_sms_count") + 1)


        if delivery_by != None and delivery_by !='' and delivery_by != 'None':
            item2.delivery_by = delivery_by
            item2.delivery_date = datetime.today().strftime('%Y-%m-%d')
            item2.save(update_fields=['delivery_by'])
            item2.save(update_fields=['delivery_date', ])

            current_stage_in_db = Repairing_after_sales_service.objects.get(id=id).current_stage  # updatestage4
            if current_stage_in_db == 'Repaired but not collected' and item2.delivery_date != '' and item2.delivery_date != None:
                Repairing_after_sales_service.objects.filter(id=id).update(
                    current_stage='Finally Collected')


                item2.stage_update_timedate = timezone.now()
                item2.save(update_fields=['stage_update_timedate', ])

                try:
                    send_mail('Scale Collected - HSCo',
                              ' Dear ' + customer_name + ',Thank you for selecting HSCo. Your Scale with Repairing No ' + str(
                                  repair_id.pk) + ' has been ' \
                          'Successfully Collected. We hope that your Repairing Complaint was resolved to your satisfaction. WE\'d love ' \
                          'to hear your feedback to help us improve our customer experience,just click on the link below:\n ' \
                                                  ' http://139.59.76.87/feedback_repairing/'+ str(request.user.pk) + '/' + str(repair_id.crm_no.pk) + '/' + str(repair_id.id)+'\n If you ' \
                          'feel that your complaint has not been resolved please contact our customer service team on 7045922251', settings.EMAIL_HOST_USER,
                              [item.customer_email_id])
                except:
                    pass
                #
                # message = 'Click on the link to give feedback http://139.59.76.87/feedback_repairing/' + str(
                #     request.user.pk) + '/' + str(item.pk) + '/' + str(item2.id)

                message = ' Dear ' + customer_name + ',Thank you for selecting HSCo. Your Scale with Repairing No ' + str(
                                  repair_id.pk) + ' has been ' \
                          'Successfully Collected. We hope that your Repairing Complaint was resolved to your satisfaction. WE\'d love ' \
                          'to hear your feedback to help us improve our customer experience,just click on the link below:\n ' \
                                                  ' http://139.59.76.87/feedback_repairing/'+str(request.user.pk) + '/' + str(repair_id.crm_no.pk) + '/' + str(repair_id.id)+'\n If you ' \
                          'feel that your complaint has not been resolved please contact our customer service team on 7045922251'

                url = "http://smshorizon.co.in/api/sendsms.php?user=" + settings.user + "&apikey=" + settings.api + "&mobile=" + item.contact_no + "&message=" + message + "&senderid=" + settings.senderid + "&type=txt"
                payload = ""
                headers = {'content-type': 'application/x-www-form-urlencoded'}

                response = requests.request("GET", url, data=json.dumps(payload), headers=headers)
                x = response.text




        # item2.total_cost = total_cost
        # if informed_on != '':
        #
        #     item2.informed_on = informed_on
        #     item2.save(update_fields=['informed_on', ]),
        #
        if informed_by != '' and informed_by!= None and informed_by != 'None':
            item2.informed_on = datetime.today().strftime('%Y-%m-%d')

            item2.informed_by = informed_by
            item2.save(update_fields=['informed_on'])
            item2.save(update_fields=['informed_by', ])
        if repaired_by != '' and repaired_by!= None and repaired_by != 'None':
            item2.repaired_by = repaired_by
            item2.repaired_date = datetime.today().strftime('%Y-%m-%d')
            item2.save(update_fields=['repaired_by'])
            item2.save(update_fields=['repaired_date', ])

        if item2.repaired == 'Yes'and item2.repaired_date != 'No' and type(item2.repaired_date) != str:
            Employee_Analysis_date.objects.filter(user_id=repair_id.user_id,
                                                  entry_date__month=repair_id.entry_timedate.month,
                                                  year=repair_id.entry_timedate.year).update(
                avg_time_to_repair_single_scale_today= (repair_id.repaired_date - repair_id.entry_timedate ).days)

        item2.second_person=customer_name
        # item2.third_person=third_person
        item2.second_contact_no=contact_no
        # item2.third_contact_no=third_contact_no
        item2.confirmed_estimate = confirmed_estimate
        item2.repaired = repaired
        # if item2.taken_by == None or item2.taken_by==''and item2.taken_by != 'None':
        if taken_by != '' or taken_by != None and taken_by != 'None':
            item2.taken_by = taken_by
            item2.user_id = SiteUser.objects.get(name=taken_by)
            item2.save(update_fields=['taken_by',])
            item2.save(update_fields=['user_id', ])





        # item2.feedback_given = feedback_given
        # item2.current_stage = current_stage


        # item2.save()

        # item2.save(update_fields=['repairingnumber', ]),
        # item2.save(update_fields=['previous_repairing_number', ]),
        # item2.save(update_fields=['today_date', ]),
        # item2.save(update_fields=['products_to_be_repaired', ]),


        # item2.save(update_fields=['informed_by', ]),
        item2.save(update_fields=['confirmed_estimate', ])
        item2.save(update_fields=['second_company_name', ])
        item2.save(update_fields=['company_address', ])
        item2.save(update_fields=['repaired', ])
        item2.save(update_fields=['company_email', ])
        item2.save(update_fields=['repaired_by','taken_by', ])
        # item2.save(update_fields=['feedback_given', ])
        # item2.save(update_fields=['current_stage', ])
        item2.save(update_fields=['second_person','second_contact_no', ])
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

    context={
        'repair_list': repair_list,
        'repair_id': repair_id,
        'user_list': user_list,
        'customer_id':customer_id,

    }
    return render(request,'update_forms/update_rep_mod_form.html',context)

def repairing_module_home(request):

    if request.method == 'POST':
        if'submit1' in request.POST:
            start_date = request.POST.get('date1')
            end_date = request.POST.get('date2')
            if check_admin_roles(request):  # For ADMIN
                repair_list = Repairing_after_sales_service.objects.filter(user_id__group__icontains=request.user.name,
                                                                           user_id__is_deleted=False,entry_timedate__range=[start_date, end_date]).order_by('-id')
            else:  # For EMPLOYEE
                repair_list = Repairing_after_sales_service.objects.filter(user_id=request.user.pk,entry_timedate__range=[start_date, end_date]).order_by('-id')
            # repair_list = Repairing_after_sales_service.objects.filter(entry_timedate__range=[start_date, end_date])
            context = {
                'repair_list': repair_list,
                'search_msg': 'Search result for date range: ' + start_date + ' TO ' + end_date,
            }
            return render(request, 'dashboardnew/repairing_module_home.html', context)
        elif 'submit2' in request.POST:
            contact = request.POST.get('contact')
            if check_admin_roles(request):  # For ADMIN
                repair_list = Repairing_after_sales_service.objects.filter(user_id__group__icontains=request.user.name,
                                                                           user_id__is_deleted=False,second_contact_no__icontains=contact).order_by('-id')
            else:  # For EMPLOYEE
                repair_list = Repairing_after_sales_service.objects.filter(user_id=request.user.pk,second_contact_no__icontains=contact).order_by('-id')
            # repair_list = Repairing_after_sales_service.objects.filter(phone_no=contact)
            context = {
                'repair_list': repair_list,
                'search_msg': 'Search result for Customer Contact No: ' + contact,
            }
            return render(request, 'dashboardnew/repairing_module_home.html', context)

        elif 'submit3' in request.POST:
            email = request.POST.get('email')
            if check_admin_roles(request):  # For ADMIN
                repair_list = Repairing_after_sales_service.objects.filter(user_id__group__icontains=request.user.name,
                                                                           user_id__is_deleted=False,company_email__icontains=email).order_by('-id')
            else:  # For EMPLOYEE
                repair_list = Repairing_after_sales_service.objects.filter(user_id=request.user.pk,company_email__icontains=email).order_by('-id')
            # repair_list = Repairing_after_sales_service.objects.filter(customer_email_id=email)
            context = {
                'repair_list': repair_list,
                'search_msg': 'Search result for Customer Email ID: ' + email,
            }
            return render(request, 'dashboardnew/repairing_module_home.html', context)
        elif 'submit4' in request.POST:
            customer = request.POST.get('customer')
            if check_admin_roles(request):  # For ADMIN
                repair_list = Repairing_after_sales_service.objects.filter(user_id__group__icontains=request.user.name,
                                                                           user_id__is_deleted=False,second_person__icontains=customer).order_by('-id')
            else:  # For EMPLOYEE
                repair_list = Repairing_after_sales_service.objects.filter(user_id=request.user.pk,second_person__icontains=customer).order_by('-id')
            # repair_list = Repairing_after_sales_service.objects.filter(name=customer)
            context = {
                'repair_list': repair_list,
                'search_msg': 'Search result for Customer Name: ' + customer,
            }
            return render(request, 'dashboardnew/repairing_module_home.html', context)

        elif  'submit5' in request.POST:
            company = request.POST.get('company')
            if check_admin_roles(request):  # For ADMIN
                repair_list = Repairing_after_sales_service.objects.filter(user_id__group__icontains=request.user.name,
                                                                           user_id__is_deleted=False,second_company_name__icontains=company).order_by('-id')
            else:  # For EMPLOYEE
                repair_list = Repairing_after_sales_service.objects.filter(user_id=request.user.pk,second_company_name__icontains=company).order_by('-id')
            # repair_list = Repairing_after_sales_service.objects.filter(company_name=company)
            context = {
                'repair_list': repair_list,
                'search_msg': 'Search result for Company Name: ' + company,
            }
            return render(request, 'dashboardnew/repairing_module_home.html', context)
        elif request.method=='POST' and 'submit6' in request.POST:
            crm = request.POST.get('crm')
            if check_admin_roles(request):  # For ADMIN
                repair_list = Repairing_after_sales_service.objects.filter(user_id__group__icontains=request.user.name,
                                                                           user_id__is_deleted=False,crm_no__pk=crm).order_by('-id')
            else:  # For EMPLOYEE
                repair_list = Repairing_after_sales_service.objects.filter(user_id=request.user.pk,crm_no__pk=crm).order_by('-id')
            # repair_list = Repairing_after_sales_service.objects.filter(crn_number=crm)
            context = {
                'repair_list': repair_list,
                'search_msg': 'Search result for CRM No. : ' + crm,
            }
            return render(request, 'dashboardnew/repairing_module_home.html', context)
    else:
        if request.user.role =='Super Admin':     #For ADMIN
            repair_list = Repairing_after_sales_service.objects.filter((Q(taken_by=None) | Q(taken_by='') |Q(user_id__name=request.user.name)|Q(taken_by=request.user.name)| Q(user_id__group__icontains=request.user.name))&Q(user_id__is_deleted=False)&Q(user_id__modules_assigned__icontains="'Repairing Module'")).order_by('-id')

            res = Repairing_after_sales_service.objects.filter(Q(taken_by=None) | Q(taken_by='') |Q(user_id__name=request.user.name)|Q(taken_by=request.user.name) | Q(user_id__group__icontains=request.user.name)).values(
                'current_stage').annotate(
                dcount=Count('current_stage'))
        elif request.user.role =='Admin':
            repair_list = Repairing_after_sales_service.objects.filter((Q(taken_by=request.user.name) | Q(taken_by=None) | Q(taken_by='')|Q(user_id__name=request.user.name))).order_by(
                '-id')

            res = Repairing_after_sales_service.objects.filter(
                (Q(taken_by=request.user.name) | Q(taken_by=None) | Q(taken_by='')|Q(user_id__name=request.user.name)) ).values(
                'current_stage').annotate(
                dcount=Count('current_stage'))
        elif request.user.role =='Manager':
            admin = SiteUser.objects.get(id=request.user.pk).admin
            repair_list = Repairing_after_sales_service.objects.filter(
                (Q(taken_by=request.user.name) | Q(taken_by=None) | Q(taken_by='')|Q(user_id__name=request.user.name)) & Q(user_id__admin=admin)).order_by(
                '-id')

            res = Repairing_after_sales_service.objects.filter(
                (Q(taken_by=request.user.name) | Q(taken_by=None) | Q(taken_by='')|Q(user_id__name=request.user.name)) & Q(user_id__admin=admin)).values(
                'current_stage').annotate(
                dcount=Count('current_stage'))

        else:  #For EMPLOYEE
            admin = SiteUser.objects.get(id=request.user.pk).admin
            repair_list = Repairing_after_sales_service.objects.filter((Q(taken_by=request.user.name)|Q(taken_by=None) | Q(taken_by=''))&Q(user_id__admin=admin)).order_by('-id')

            res = Repairing_after_sales_service.objects.filter((Q(taken_by=request.user.name)|Q(taken_by=None) | Q(taken_by=''))&Q(user_id__admin=admin)).values('current_stage').annotate(
                dcount=Count('current_stage'))
            # repair_list2 = Repairing_after_sales_service.objects.filter(Q(taken_by='')).order_by('-id')
            # repair_list = Repairing_after_sales_service.objects.filter(taken_by=request.user.name,).order_by('-id')
        # repair_list = Repairing_after_sales_service.objects.all()

        context = {
            'repair_list': repair_list,
        }
        # Using current time
        ini_time_for_now = datetime.now()

        new_final_time = ini_time_for_now - timedelta(days=4)

        res_4d = Repairing_after_sales_service.objects.filter(Q(user_id=request.user.pk)|Q(user_id__manager=request.user.name)|Q(user_id__admin=request.user.name)|Q(user_id__super_admin=request.user.name),Q(stage_update_timedate=new_final_time),Q(current_stage='Repaired but not collected')).values('current_stage').annotate(dcount=Count('current_stage'))
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
        res_10d = Repairing_after_sales_service.objects.filter(Q(user_id=request.user.pk)|Q(user_id__manager=request.user.name)|Q(user_id__admin=request.user.name)|Q(user_id__super_admin=request.user.name),Q(stage_update_timedate=new_final_time),Q(current_stage='Repaired but not collected')).values('current_stage').annotate(dcount=Count('current_stage'))
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
        selected_product_list = request.POST.getlist('products[]')
        repair_start_date = request.POST.get('date1')
        repair_end_date = request.POST.get('date2')
        repair_string = ','.join(selected_list)
        repair_product_string = ','.join(selected_product_list)
        request.session['start_date'] = repair_start_date
        request.session['repair_end_date'] = repair_end_date
        request.session['repair_string'] = repair_string
        request.session['selected_product_list'] = selected_product_list
        request.session['repair_product_string'] = repair_product_string
        request.session['selected_list'] = selected_list
        return redirect('/final_repairing_report_module/')
    return render(request,'report/report_rep_mod_form.html',)

def final_repairing_report_module(request):
    repair_start_date = str(request.session.get('repair_start_date'))
    repair_end_date = str(request.session.get('repair_end_date'))
    repair_string = request.session.get('repair_string')
    repair_product_string = request.session.get('repair_product_string')
    selected_product_list = request.session.get('selected_product_list')


    selected_list = request.session.get('selected_list')
    for n, i in enumerate(selected_list):
        if i == 'repairing_app_repairing_after_sales_service.id':
            selected_list[n] = 'Reparing ID'
        if i == 'crm_no_id':
            selected_list[n] = 'Customer No'
        if i == 'today_date':
            selected_list[n] = 'Entry Date'


    with connection.cursor() as cursor:

        cursor.execute("SELECT "+repair_string+" from repairing_app_repairing_after_sales_service , customer_app_customer_details where repairing_app_repairing_after_sales_service.crm_no_id = customer_app_customer_details.id and entry_timedate between '" + repair_start_date + "' and '" + repair_end_date + "';")
        row = cursor.fetchall()
        final_row = [list(x) for x in row]
        repairing_data = []
        for i in row:
            repairing_data.append(list(i))

        cursor.execute(
            "SELECT " + (repair_product_string) + " from repairing_app_repairing_product  PRODUCT , repairing_app_repairing_after_sales_service  REP where PRODUCT.repairing_id_id = REP.id and PRODUCT.entry_timedate between'" + repair_start_date + "' and '" + repair_end_date + "';")
        row = cursor.fetchall()
        final_row_product = [list(x) for x in row]
        repairing_data = []
        for i in row:
            repairing_data.append(list(i))

    try:
        del request.session['repair_start_date']
        del request.session['repair_end_date']
        del request.session['repair_string']
        del request.session['selected_list']
        del request.session['repair_product_string']
        del request.session['selected_product_list']
    except:
        pass

    context = {
        'final_row': final_row,
        'final_row_product': final_row_product,
        'selected_list': selected_list,
        'selected_product_list': selected_product_list,
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


            if Employee_Analysis_month.objects.filter(Q(entry_date__month=datetime.now().month),
                                                      Q(user_id=SiteUser.objects.get(id=user_id))).count() > 0:
                Employee_Analysis_month.objects.filter(user_id=user_id, entry_date__month=datetime.now().month,
                                                       year=datetime.now().year).update(
                    start_rating_feedback_reparing=(F("start_rating_feedback_reparing") + Repairing_after_sales_service.objects.get(id=repairing_id).avg_feedback) / 2.0)
                # ead.total_sales_done_today=.filter(category_id_id=id).update(total_views=F("total_views") + value_of_goods)

                # ead.save(update_fields=['total_sales_done_today'])

            else:
                ead = Employee_Analysis_month()
                ead.user_id = SiteUser.objects.get(id=user_id)
                ead.start_rating_feedback_reparing = Repairing_after_sales_service.objects.get(id=repairing_id).avg_feedback
                # ead.total_dispatch_done = value_of_goods
                ead.manager_id = SiteUser.objects.get(id=user_id).group
                ead.month = datetime.now().month
                ead.year = datetime.now().year
                ead.save()
        except:
            pass
        return HttpResponse('Feedback Submitted!!!')
    context = {
        'feedback_form': feedback_form,
    }
    return render(request,'feedback/feedback_repairing.html',context)

def edit_product(request,id):
    product_id = Repairing_Product.objects.get(id=id)
    repairing_id = Repairing_Product.objects.get(id=id).repairing_id
    user_id=Repairing_after_sales_service.objects.get(id=repairing_id).user_id
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

        Employee_Analysis_month.objects.filter(user_id=user_id,
                                               entry_date__month=product_id.entry_timedate.month,
                                               year=product_id.entry_timedate.year).update(
            total_reparing_done=F("total_reparing_done") - cost2)

        Employee_Analysis_date.objects.filter(user_id=user_id,
                                              entry_date__month=product_id.entry_timedate.month,
                                              year=product_id.entry_timedate.year).update(
            total_reparing_done_today=F("total_reparing_done_today") - cost2)

        current_stage_in_db = Repairing_after_sales_service.objects.get(id=repairing_id.pk).current_stage  # updatestage2


        if current_stage_in_db == 'Scale is collected but estimate is not given' and float(cost) > 0.0:
            Repairing_after_sales_service.objects.filter(id=repairing_id.pk).update(
                current_stage='Estimate is given but Estimate is not confirmed', stage_update_timedate=timezone.now())

        current_stage_in_db = Repairing_after_sales_service.objects.get(id=repairing_id.pk).current_stage  # updatestage1
        if (current_stage_in_db == '' or current_stage_in_db == None) and (sub_model != '' or sub_model != None):
            Repairing_after_sales_service.objects.filter(id=repairing_id.pk).update(
                current_stage='Scale is collected but estimate is not given', stage_update_timedate = timezone.now())
            # rep=Repairing_after_sales_service.objects.get(id=reparing_id)
            # send_sms(request, rep.second_person, rep.second_contact_no, rep.crm_no.customer_email_id, reparing_id, '1')

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


        if in_warranty.lower() == 'yes':
            # Repairing_after_sales_service.objects.filter(id=reparing_id).update(total_cost=F("total_cost") - item.cost)
            item.cost = 0.0
        else:
            item.cost = cost
            Repairing_after_sales_service.objects.filter(id=reparing_id).update(total_cost=F("total_cost") + cost)

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


        # Repairing_after_sales_service.objects.filter(id=reparing_id).update(total_cost=F("total_cost") + float(cost))
        # Repairing_after_sales_service.objects.filter(id=reparing_id).update(total_cost=F("total_cost") + 100.0)

        Employee_Analysis_month.objects.filter(user_id=user_id,
                                               entry_date__month=product_id.entry_timedate.month,
                                               year=product_id.entry_timedate.year).update(
            total_reparing_done=F("total_reparing_done") + cost)

        Employee_Analysis_date.objects.filter(user_id=user_id,
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
    rep_feedback = Repairing_Feedback.objects.filter(user_id=user_id)

    print(user_id)
    mon = datetime.now().month

    obj = Employee_Analysis_month.objects.get(user_id=user_id,entry_date__month=mon)
    try:
        obj.reparing_target_achived_till_now = (obj.total_reparing_done/obj.reparing_target_given)*100
    except:
        pass
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

    selected_stage = request.GET.get('selected_stage')
    ini_time_for_now = datetime.now()
    if selected_stage == '4days':


        new_final_time = ini_time_for_now - timedelta(days=4)

        if check_admin_roles(request):  # For ADMIN


            repair_list = Repairing_after_sales_service.objects.filter(Q(stage_update_timedate=new_final_time)&(Q(taken_by=None) | Q(taken_by='')| Q(taken_by=request.user.name)| Q(
                user_id__group__icontains=request.user.name)) & Q(current_stage='Repaired but not collected'))
        else:  # For EMPLOYEE

            repair_list = Repairing_after_sales_service.objects.filter(Q(stage_update_timedate=new_final_time)&(Q(taken_by=None) | Q(taken_by='')| Q(taken_by=request.user.name)) & Q(current_stage='Repaired but not collected'))
        # repair_list = Repairing_after_sales_service.objects.filter(current_stage=selected_stage)
    elif selected_stage == '10days':
        new_final_time = ini_time_for_now - timedelta(days=10)
        if check_admin_roles(request):  # For ADMIN


            repair_list = Repairing_after_sales_service.objects.filter(Q(stage_update_timedate=new_final_time)&(Q(taken_by=None) | Q(taken_by='')| Q(taken_by=request.user.name)| Q(
                user_id__group__icontains=request.user.name)) & Q(current_stage='Repaired but not collected'))
        else:  # For EMPLOYEE

            repair_list = Repairing_after_sales_service.objects.filter(Q(stage_update_timedate=new_final_time)&(Q(taken_by=None) | Q(taken_by='')| Q(taken_by=request.user.name)) & Q(current_stage='Repaired but not collected'))
    else:
        if check_admin_roles(request):  # For ADMIN


            repair_list = Repairing_after_sales_service.objects.filter((Q(taken_by=None) | Q(taken_by='')| Q(taken_by=request.user.name)| Q(
                user_id__group__icontains=request.user.name)) & Q(current_stage=selected_stage))
        else:  # For EMPLOYEE
            admin = SiteUser.objects.get(id=request.user.pk).admin
            repair_list = Repairing_after_sales_service.objects.filter((
                (Q(taken_by=request.user.name) | Q(taken_by=None) | Q(taken_by='')) & Q(user_id__admin=admin)) & Q(current_stage=selected_stage)).order_by(
                '-id')

    # else:
    #     repair_list = Repairing_after_sales_service.objects.filter(Q(user_id=request.user.pk)|Q(user_id__manager=request.user.name)|Q(user_id__admin=request.user.name)|Q(user_id__super_admin=request.user.name),current_stage=selected_stage)

    context = {
        'repair_list': repair_list,
    }
    context.update(context)
    return render(request, 'AJAX/load_reparing_stage.html', context)

def load_reparing_manager(request):
    selected = request.GET.get('loc_id')

    if selected=='true':
        user_list = Employee_Analysis_month.objects.filter(manager_id__icontains=request.user.name,user_id__is_deleted=False,user_id__modules_assigned__icontains="'Repairing Module'")
        # dispatch_list = Employee_Analysis_month.objects.filter(user_id__group=str(request.user.name))

        context = {
            'user_list': user_list,
            'manager': True,
        }

        return render(request, 'AJAX/load_reparing_manager.html', context)
    else:
        if request.user.role =='Super Admin':     #For ADMIN
            repair_list = Repairing_after_sales_service.objects.filter((Q(taken_by=None) | Q(taken_by='') |Q(user_id__name=request.user.name)|Q(taken_by=request.user.name)| Q(user_id__group__icontains=request.user.name))
                                                                       &Q(user_id__is_deleted=False)&Q(user_id__modules_assigned__icontains="'Repairing Module'")).order_by('-id')

        elif request.user.role =='Admin':
            admin = SiteUser.objects.get(id=request.user.pk).name
            repair_list = Repairing_after_sales_service.objects.filter((Q(taken_by=request.user.name) | Q(taken_by=None) | Q(taken_by=''))).order_by(
                '-id')

        elif request.user.role =='Manager':
            admin = SiteUser.objects.get(id=request.user.pk).admin
            repair_list = Repairing_after_sales_service.objects.filter(
                (Q(taken_by=request.user.name) | Q(taken_by=None) | Q(taken_by='')) & Q(user_id__admin=admin)).order_by(
                '-id')


        else:  #For EMPLOYEE
            admin = SiteUser.objects.get(id=request.user.pk).admin
            repair_list = Repairing_after_sales_service.objects.filter((Q(taken_by=request.user.name)|Q(taken_by=None) | Q(taken_by=''))&Q(user_id__admin=admin)).order_by('-id')




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

    context = {
        'cust_list': rep_list,

    }

    return render(request, 'AJAX/load_prev_rep.html', context)
from django.http import JsonResponse
def send_sms(request,name,phone,email,repair_id,item_id):
    msg_id = None
    msg_id =item_id
    name = name
    phone =phone
    email = email
    id = repair_id

    import requests
    import json

    mobile = '+91'+phone  # 9766323877'
    user = 'HSCo'
    senderid = 'HSCALE'

    api = 'PF8MzCBOGTopfpYFlSZT'
    if msg_id == '1':
        message = 'Dear '+name+',Thank you for selecting HSCo. Your Scales have been successfully ' \
                  'received at our Repairing Center. Your Repairing No is '+str(repair_id)+'. Please use this Unique ID for further communication.' \
                  'For any further details please contact our customer service team on 7045922251'
        Repairing_after_sales_service.objects.filter(id=id).update(scale_sub_sms_count=F("scale_sub_sms_count")+1)
        try:
            send_mail('Scale Submit - HSCo', message, settings.EMAIL_HOST_USER,[email])
        except:
            pass
    elif msg_id == '2':
        rep_id = Repairing_after_sales_service.objects.filter(id=id)
        message = 'Dear '+name+',Thank you for selecting HSCo. The Estimate for Your' \
                  ' Repairing No '+str(repair_id)+' is  '+str(rep_id.total_cost)+'/- For any further details please contact our ' \
                  'customer service team on 7045922251'
        Repairing_after_sales_service.objects.filter(id=id).update(estimate_informed_sms_count=F("estimate_informed_sms_count") + 1)
        try:
            send_mail('Reparing Estimate - HSCo',  message, settings.EMAIL_HOST_USER, [email])
        except:
            pass
    elif msg_id == '3':
        message = 'Dear '+name+', Thank you for selecting HSCo. Your Repairing Complaint No '+str(repair_id)+' is resolved.' \
                  ' Please collect your Scales within the next 3 days.For any further details please contact our customer service team on 7045922251'
        Repairing_after_sales_service.objects.filter(id=id).update(reparing_done_sms_count=F("reparing_done_sms_count") + 1)
        try:
            send_mail('Reparing done - HSCo', message, settings.EMAIL_HOST_USER, [email])
        except:
            pass
    elif msg_id == '4':
        message = 'Dear '+name+',Thank you for selecting HSCo. Your Repairing No '+str(repair_id)+' has been Overdue ' \
                  'with us for more than 3 days. Please Collect it without fail today before 8 pm else we will scrap it.' \
                  ' We will not be liable for any claims thereafter. Consider this as your final reminder.for more information ' \
                  'contact our customer service team on 7045922251'
        Repairing_after_sales_service.objects.filter(id=id).update(late_mark_sms_count=F("late_mark_sms_count") + 1)
        try:
            send_mail('Late Mark - HSCo', message, settings.EMAIL_HOST_USER, [email])
        except:
            pass
    elif msg_id == '5':
        rep_id=Repairing_after_sales_service.objects.filter(id=id)
        message = ' Dear ' + name + ',Thank you for selecting HSCo. Your Scale with Repairing No ' + str(
            repair_id) + ' has been ' \
                            'Successfully Collected. We hope that your Repairing Complaint was resolved to your satisfaction. WE\'d love ' \
                            'to hear your feedback to help us improve our customer experience,just click on the link below:\n ' \
                            ' http://139.59.76.87/feedback_repairing/'+ str(request.user.pk) + '/' + str(rep_id.crm_no.pk) + '/' + str(rep_id.pk) + '\n If you ' \
                                                                                            'feel that your complaint has not been resolved please contact our customer service team on 7045922251'
        Repairing_after_sales_service.objects.filter(id=id).update(final_del_sms_count=F("final_del_sms_count") + 1)
        try:
            send_mail('Final Delivery - HSCo', message, settings.EMAIL_HOST_USER, [email])
        except:
            pass


    url = "http://smshorizon.co.in/api/sendsms.php?user=" + user + "&apikey=" + api + "&mobile=" + mobile + "&message=" + message + "&senderid=" + senderid + "&type=txt"
    payload = ""
    headers = {'content-type': 'application/x-www-form-urlencoded'}

    response = requests.request("GET", url, data=json.dumps(payload), headers=headers)
    x = response.text
    print(x)
    repair_id = Repairing_after_sales_service.objects.get(id=id)
    data = {
        'repair_id': repair_id.scale_sub_sms_count
    }




    return JsonResponse(data)

#
# def add_component_replaced(request,component_id):
#     component_replaced_id = Repairing_Product.objects.get(id=component_id)
#     if request.method == 'POST':
#         replaced_name = request.POST.get('components_replaced_popup')
#         item = Repairing_Product()
#         item.component_replaced_id = Component_Replaced()
#         item.replaced_name = replaced_name
#         item.save()
#     context = {
#         'component_replaced_id':component_replaced_id,
#     }
#
#     return render(request,'dashboardnew/repair_product.html',context)



def repairing_form(request,id):
    data=Repairing_after_sales_service.objects.get(id=id)
    product_list=Repairing_Product.objects.filter(repairing_id=id)
    context={
        'data':data,
        'product_list':product_list,
    }
    return render(request,'repairing_format/reparingform.html',context)
#
# def repairing_form_back(request):
#     return render(request,'repairing_form/reparingformback.html')































