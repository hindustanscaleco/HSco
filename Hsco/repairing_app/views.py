from django.db import connection
from django.db.models import Min, Sum, Q, F, Avg
from django.http import HttpResponse
from django.shortcuts import render, redirect
from customer_app.models import Customer_Details
from django.utils import timezone
from user_app.models import SiteUser
from django.contrib.auth.decorators import login_required

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
from .serializers import CustomerSerializer


@login_required(login_url='/')
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
        notes = request.POST.get('notes')
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


        # item = Customer_Details()
        # item2  = Repairing_after_sales_service()
        try:
            del request.session['company_name']
            del request.session['address']
            del request.session['customer_email_id']
            del request.session['repairing_no']
            del request.session['previous_repairing_number']
            del request.session['in_warranty']
            del request.session['today_date']
            del request.session['location']
            del request.session['taken_by']
            del request.session['notes']
            del request.session['second_person']
            del request.session['second_contact_no']
            del request.session['entered_by']
            del request.session['total_cost']
            del request.session['informed_on']
            del request.session['informed_by']
            del request.session['repaired_date']
            del request.session['repaired_by']
            del request.session['confirmed_estimate']
            del request.session['repaired']
            del request.session['delivery_by']
            del request.session['feedback_given']
        except:
            pass
        request.session['company_name'] = company_name
        request.session['address'] = address
        request.session['customer_email_id'] = customer_email_id

        request.session['repairing_no'] = Repairing_after_sales_service.objects.latest('repairing_no').repairing_no + 1
        request.session['previous_repairing_number'] = previous_repairing_number
        request.session['in_warranty'] = in_warranty
        request.session['today_date'] = today_date
        request.session['location'] = location
        request.session['taken_by'] = taken_by
        request.session['notes'] = notes
        request.session['second_person'] = customer_name
        request.session['second_contact_no'] = contact_no
        request.session['entered_by'] = request.user.name
        request.session['total_cost'] = 0.0

        request.session['informed_on'] = datetime.today().strftime('%Y-%m-%d')
        request.session['informed_by'] = informed_by

        request.session['repaired_date'] = datetime.today().strftime('%Y-%m-%d')
        request.session['repaired_by'] = repaired_by
        # request.session['repairing_done_timedate'] = timezone.now().strftime("%Y-%m-%d %H:%M:%S")

        request.session['confirmed_estimate'] = confirmed_estimate
        request.session['repaired'] = repaired
        request.session['delivery_by'] = delivery_by
        request.session['feedback_given'] = False
        # request.session['user_id'] = SiteUser.objects.get(id=request.user.pk)
        # request.session['manager_id'] = SiteUser.objects.get(id=request.user.pk).group


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
        # f = Repairing_after_sales_service()
        # item2 =f.save(force_insert=True)
        # request.session['item2'] = item2
        latest_restamp_id = Repairing_after_sales_service.objects.latest('id').id + 1

        return redirect('/repair_product/'+str(latest_restamp_id))


    context={
        'cust_sugg':cust_sugg,
        'user_list':user_list,
        'prev_rep_sugg':prev_rep_sugg,
    }

    return render(request,'forms/rep_mod_form.html',context)


@login_required(login_url='/')
def repair_product(request,id):
    # repair_id = Repairing_after_sales_service.objects.latest('id').id + 1
    type_of_purchase_list =type_purchase.objects.all() #1
    components_replaced_popup = []

    if request.method=='POST':
        type_of_machine = request.POST.get('type_of_scale')
        model = request.POST.get('model_of_purchase')
        sub_model = request.POST.get('sub_model')


        problem_in_scale = request.POST.get('problem_in_scale')
        components_replaced_in_warranty = request.POST.getlist('components_replaced_in_warranty')
        components_replaced = request.POST.getlist('components_replaced')
        replaced_scale_given = request.POST.get('replaced_scale_given')
        Replaced_scale_serial_no = request.POST.get('Replaced_scale_serial_no')
        deposite_taken_for_replaced_scale = request.POST.get('deposite_taken_for_replaced_scale')
        cost = request.POST.get('cost')
        in_warranty = request.POST.get('in_warranty')
        is_last_product_yes = request.POST.get('is_last_product_yes')
        # is_last_product_no = request.POST.get('is_last_product_no')
        if cost == '' or cost == None:
            cost=0.0
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
        item.repairing_id_id = id
        if in_warranty != '' or in_warranty != None:
            item.in_warranty = in_warranty
        # print(is_last_product_no)
        # if is_last_product_yes == None:
        #     item.is_last_product = False
        # else:
        #     item.is_last_product = True

        # if in_warranty.lower() == 'yes':
        #     item.cost = 0.0
        # else:
        item.cost = cost


        if Repairing_after_sales_service.objects.filter(id=id).count() == 0 :
            item2 = Repairing_after_sales_service()

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

            item2.repairing_no = request.session.get('repairing_no')
            item2.previous_repairing_number = request.session.get('previous_repairing_number')
            item2.in_warranty = request.session.get('in_warranty')
            item2.today_date = request.session.get('today_date')

            item2.location = request.session.get('location')
            item2.taken_by = request.session.get('taken_by')
            item2.notes = request.session.get('notes')
            item2.second_person = request.session.get('second_person')  # new1
            item2.second_contact_no = request.session.get('second_contact_no')  # new2
            item2.entered_by = request.session.get('entered_by') # new2

            total_cost = 0.0
            if request.session.get('informed_by') != '' and request.session.get('informed_by') != None:
                item2.informed_on = request.session.get('informed_on')
                item2.informed_by = request.session.get('informed_by')

            if request.session.get('repaired_by') != '' and request.session.get('repaired_by') != None:
                item2.repaired_date = request.session.get('repaired_date')
                item2.repaired_by = request.session.get('repaired_by')
                item2.repairing_done_timedate = request.session.get('repairing_done_timedate')
            if request.session.get('second_company_name') != '' and request.session.get('second_company_name') != None:
                item2.second_company_name = request.session.get('second_company_name')

            if request.session.get('company_address') != '' and request.session.get('company_address') != None:
                item2.company_address = request.session.get('company_address')

            if request.session.get('company_email_id') != '' and request.session.get('company_email_id') != None:
                item2.company_email_id = request.session.get('company_email_id')

            item2.confirmed_estimate = request.session.get('confirmed_estimate')
            item2.repaired = request.session.get('repaired')
            item2.delivery_by = request.session.get('delivery_by')
            # item2.repaired_by = repaired_by
            item2.feedback_given = request.session.get('feedback_given')
            item2.notes = request.session.get('notes')
            item2.repairing_start_timedate = timezone.now()
            item2.user_id = SiteUser.objects.get(id=request.user.pk)
            item2.manager_id = SiteUser.objects.get(id=request.user.pk).group
            item2.save()
        else:
            pass
        item.save()
        Repairing_after_sales_service.objects.filter(id=id).update(total_cost=F("total_cost") + cost)

        if request.session.get('repaired_by') != '' and request.session.get('repaired_by') != None:
            new_repair_id = Repairing_after_sales_service.objects.get(id=id)
            if new_repair_id.ess_calculated == False:
                repaired_by_user_id = SiteUser.objects.get(profile_name=request.session.get('repaired_by'))
                if Employee_Analysis_date.objects.filter(Q(entry_date=datetime.now().date()),
                                                         Q(user_id=repaired_by_user_id)).count() > 0:
                    Employee_Analysis_date.objects.filter(user_id=repaired_by_user_id, entry_date=datetime.now().date(),
                                                          year=datetime.now().year).update(
                        total_reparing_done_today=F("total_reparing_done_today") + cost)
                    # ead.total_sales_done_today=.filter(category_id_id=id).update(total_views=F("total_views") + value_of_goods)

                    # ead.save(update_fields=['total_sales_done_today'])

                else:
                    ead = Employee_Analysis_date()
                    ead.user_id = repaired_by_user_id
                    ead.total_reparing_done_today = cost
                    ead.manager_id = repaired_by_user_id.group

                    ead.month = datetime.now().month
                    ead.year = datetime.now().year
                    ead.save()

                if Employee_Analysis_month.objects.filter(Q(entry_date__month=datetime.now().month),
                                                      Q(user_id=repaired_by_user_id)).count() > 0:
                    Employee_Analysis_month.objects.filter(user_id=repaired_by_user_id, entry_date__month=datetime.now().month,
                                                           year=datetime.now().year).update(
                        total_reparing_done=F("total_reparing_done") + cost)
                    # ead.total_sales_done_today=.filter(category_id_id=id).update(total_views=F("total_views") + value_of_goods)

                    # ead.save(update_fields=['total_sales_done_today'])

                else:
                    ead = Employee_Analysis_month()
                    ead.user_id = repaired_by_user_id
                    ead.total_reparing_done = cost
                    ead.manager_id = repaired_by_user_id.group

                    ead.month = datetime.now().month
                    ead.year = datetime.now().year
                    ead.save()
                new_repair_id.ess_calculated = True
                new_repair_id.save(update_fields=['ess_calculated', ])

        user_id = Repairing_after_sales_service.objects.get(id=id).user_id

        current_stage_in_db=Repairing_after_sales_service.objects.get(id=id).current_stage #updatestage1
        if (current_stage_in_db == '' or current_stage_in_db == None ) and (sub_model !='' or sub_model != None):
            Repairing_after_sales_service.objects.filter(id=id).update(current_stage='Scale is collected but estimate is not given',stage_update_timedate = timezone.now())
            # item2.save(update_fields=['stage_update_timedate', ])

        rep = Repairing_after_sales_service.objects.get(id=id)

        if is_last_product_yes == 'yes':
            cust = Customer_Details.objects.get(id=rep.crm_no)
            # ret = send_sms(request, rep.second_person, rep.second_contact_no, rep.crm_no.customer_email_id, id, '1')
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

                # msg_old= 'Click on the link to give feedback http://139.59.76.87/feedback_repairing/' + str(
            #               request.user.pk) + '/' + str(rep.crm_no.pk) + '/' + str(rep.pk) +'\nHere is a list of Products:\n'+product_list
            # msg='Dear '+rep.second_person+',Thank you for selecting HSCo. Your Scales have been successfully ' \
            #     'received at our Repairing Center. Your Repairing No is '+str(rep.repairing_no)+'. Please use this Unique ID for further communication. For any ' \
            #     'further details please contact our customer service team on 7045922251 \n Product Details:\n'+product_list

            # msg = 'Dear ' + rep.second_person + ', Your Scales has been ' \
            #                            'received at our Repairing Center. Your Repairing No is ' + str(rep.repairing_no) + '.' \
            #                           ' For any further details please contact our customer service team on 7045922251 \n Product Details:\n'+product_list
            # if Customer_Details.objects.filter(Q(customer_name=customer_name),Q(contact_no=contact_no)).count() > 0:
            # crm_no = Customer_Details.objects.filter(Q(customer_name=customer_name),Q(contact_no=contact_no)).first()
            try:
                send_mail('HSCo',
                          ' Dear ' + item.customer_name + ',Thank you for selecting HSCo. Your Scales have been successfully received at our repairing center.'
                                                         'Your Repairing No is' + str(
                              rep.repairing_no) + '.Please ' \
                                                  'use this Unique ID for further communication.\n' \
                                                  'For any further details please contact our customer service team on 7045922251:\n ' \
                                                  ' Product Details: \n' + product_list,
                          settings.EMAIL_HOST_USER,
                          [item.company_email, ])
            except:
                pass



            # message_old = 'Click on the link to give feedback http://139.59.76.87/feedback_repairing/' + str(
            #     request.user.pk) + '/' + str(rep.crm_no.pk) + '/' + str(rep.pk)
            repair_id = Repairing_after_sales_service.objects.get(id=id)
            if repair_id.first_message_send == False:
                message = 'Dear ' + rep.second_person + ', Your Scales has been ' \
                                                    'received at our Repairing Center. Your Repairing No is ' + str(
                    rep.repairing_no) + '.' \
                                        ' For any further details please contact our customer service team on 7045922251'

                url = "http://smshorizon.co.in/api/sendsms.php?user=" + settings.user + "&apikey=" + settings.api + "&mobile=" + rep.second_contact_no + "&message=" + message + "&senderid=" + settings.senderid + "&type=txt"
                payload = ""
                headers = {'content-type': 'application/x-www-form-urlencoded'}

                response = requests.request("GET", url, data=json.dumps(payload), headers=headers)
                x = response.text
                repair_id.first_message_send = True
                repair_id.save(update_fields=['first_message_send', ])


        # current_stage_in_db = Repairing_after_sales_service.objects.get(id=id).current_stage  #updatestage2

        # if current_stage_in_db == 'Scale is collected but estimate is not given' :
        #     Repairing_after_sales_service.objects.filter(id=id).update(
        #         current_stage='Estimate is given but Estimate is not confirmed',stage_update_timedate = timezone.now())



        Component_Replaced.objects.filter(pk__in=components_replaced_popup).update(product_id=item.pk)

        if is_last_product_yes == 'yes':
            return redirect('/update_repairing_details/'+str(id))
        elif is_last_product_yes == 'no':
            return redirect('/repair_product/'+str(id))

    context = {
        'repair_id': id,
        'type_purchase': type_of_purchase_list,  # 2
    }
    return render(request,'dashboardnew/repair_product.html',context)


@login_required(login_url='/')
def update_repairing_details(request,id):
    # time = datetime(float(20:00:00.640187+00:00))
    from datetime import datetime
    repair_id = Repairing_after_sales_service.objects.get(id=id)


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
        if customer_id.contact_no != item.contact_no or customer_id.customer_name != item.customer_name :
            item.save(update_fields=['customer_name', 'contact_no'])  # new3

        informed_on = request.POST.get('informed_on')
        informed_by = request.POST.get('informed_by')
        confirmed_estimate = request.POST.get('confirmed_estimate')
        repaired = request.POST.get('repaired')
        taken_by = request.POST.get('taken_by')
        repaired_date = request.POST.get('repaired_date')
        delivery_date = request.POST.get('delivery_date')
        delivery_by = request.POST.get('delivery_by')
        repaired_by = request.POST.get('repaired_by')
        notes = request.POST.get('notes')

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
        if current_stage_in_db == 'Scale is collected but estimate is not given'  and (informed_by != None and informed_by!="" and informed_by!="None") and informed_by !=repair_id.informed_by:
            Repairing_after_sales_service.objects.filter(id=id).update(
                current_stage='Estimate is given but Estimate is not confirmed', stage_update_timedate=timezone.now())
            item2.stage_update_timedate = timezone.now()
            item2.save(update_fields=['stage_update_timedate',])

        if current_stage_in_db == 'Estimate is given but Estimate is not confirmed' and confirmed_estimate == 'Yes' and confirmed_estimate !=repair_id.confirmed_estimate:
            Repairing_after_sales_service.objects.filter(id=id).update(current_stage='Estimate is confirmed but not repaired')
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

                msg='Dear '+customer_name+',Thank you for selecting HSCo. The Estimate for Your ' \
                    'Repairing No '+str(repair_id.repairing_no)+' is  '+str(repair_id.total_cost)+'.\n For any further details please contact our customer ' \
                    'service team on 7045922251. \n Estimate Details:'+product_list
                send_mail('Feedback Form',msg
                          , settings.EMAIL_HOST_USER,
                          [item.customer_email_id,])
            except:
                pass

            # message = 'Click on the link to give feedback http://139.59.76.87/feedback_repairing/' + str(
            #     request.user.pk) + '/' + str(item.pk) + '/' + str(item2.id)

            message='Dear '+customer_name+', The Estimate for Your ' \
                    'Repairing No '+str(repair_id.repairing_no)+' is  '+str(repair_id.total_cost)+'/- For any further details please contact our customer ' \
                    'service team on 7045922251'

            url = "http://smshorizon.co.in/api/sendsms.php?user=" + settings.user + "&apikey=" + settings.api + "&mobile=" + item.contact_no + "&message=" + message + "&senderid=" + settings.senderid + "&type=txt"
            payload = ""
            headers = {'content-type': 'application/x-www-form-urlencoded'}

            response = requests.request("GET", url, data=json.dumps(payload), headers=headers)
            x = response.text

            Repairing_after_sales_service.objects.filter(id=id).update(
                estimate_informed_sms_count=F("estimate_informed_sms_count") + 1)







        current_stage_in_db = Repairing_after_sales_service.objects.get(id=id).current_stage  # updatestage4
        # if current_stage_in_db == 'Estimate is confirmed but not repaired' and (repaired_by != None or repaired_by!=""):
        if (repaired_by != None and repaired_by!="" and repaired_by != 'None') and repaired_by !=repair_id.repaired_by:
            Repairing_after_sales_service.objects.filter(id=id).update(
                current_stage='Repaired but not collected')
            item2.stage_update_timedate = timezone.now()

            item2.repaired = repaired
            item2.save(update_fields=['stage_update_timedate', ])
            item2.save(update_fields=['repaired'])

            try:
                send_mail('Repairing Done - HSCo',
                          ' Dear '+customer_name+',Thank you for selecting HSCo. Your Repairing Complaint No '+str(repair_id.repairing_no)+' is resolved.'
                          ' Please collect your Scales within the next 3 days.For any further details please contact '
                          'our customer service team on 7045922251', settings.EMAIL_HOST_USER,
                          [item.customer_email_id,])
            except:
                pass

            # message = 'Click on the link to give feedback http://139.59.76.87/feedback_repairing/' + str(
            #     request.user.pk) + '/' + str(item.pk) + '/' + str(item2.id)

            message=' Dear '+customer_name+', Your Repairing Complaint No '+str(repair_id.repairing_no)+' is resolved. ' \
                    'Please collect your Scales within the next 3 days.For any further details please contact our ' \
                    'customer service team on 7045922251'

            url = "http://smshorizon.co.in/api/sendsms.php?user=" + settings.user + "&apikey=" + settings.api + "&mobile=" + item.contact_no + "&message=" + message + "&senderid=" + settings.senderid + "&type=txt"
            payload = ""
            headers = {'content-type': 'application/x-www-form-urlencoded'}

            response = requests.request("GET", url, data=json.dumps(payload), headers=headers)
            x = response.text
            Repairing_after_sales_service.objects.filter(id=id).update(
                reparing_done_sms_count=F("reparing_done_sms_count") + 1)


        if delivery_by != None and delivery_by !='' and delivery_by != 'None' and delivery_by !=repair_id.delivery_by :
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
                                  repair_id.repairing_no) + ' has been ' \
                          'Successfully Collected. We hope that your Repairing Complaint was resolved to your satisfaction. WE\'d love ' \
                          'to hear your feedback to help us improve our customer experience,just click on the link below:\n ' \
                                                  ' http://139.59.76.87/feedback_repairing/'+ str(request.user.pk) + '/' + str(repair_id.crm_no.pk) + '/' + str(repair_id.id)+'\n If you ' \
                          'feel that your complaint has not been resolved please contact our customer service team on 7045922251', settings.EMAIL_HOST_USER,
                              [item.customer_email_id,])
                except:
                    pass
                #
                # message = 'Click on the link to give feedback http://139.59.76.87/feedback_repairing/' + str(
                #     request.user.pk) + '/' + str(item.pk) + '/' + str(item2.id)

                message = ' Dear ' + customer_name + ',Thank you for selecting HSCo. Your Scale with Repairing No ' + str(
                                  repair_id.repairing_no) + ' has been ' \
                          'Successfully Resolved and Collected. We will love ' \
                          'to hear your feedback to help us improve our customer experience. Please click on the link below:\n ' \
                                                  ' http://139.59.76.87/feedback_repairing/'+str(request.user.pk)+'/'+str(repair_id.crm_no.pk)+'/'+str(repair_id.id)+'\n ' \
                          'Contact our customer service team on 7045922251'

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
        if informed_by != '' and informed_by!= None and informed_by != 'None' and informed_by !=repair_id.informed_by:
            item2.informed_on = datetime.today().strftime('%Y-%m-%d')

            item2.informed_by = informed_by
            item2.save(update_fields=['informed_on'])
            item2.save(update_fields=['informed_by', ])
        if repaired_by != '' and repaired_by!= None and repaired_by != 'None':
            item2.repaired_by = repaired_by
            item2.repaired_date = datetime.today().strftime('%Y-%m-%d')
            item2.repairing_done_timedate = timezone.now()

            item2.save(update_fields=['repaired_by'])
            item2.save(update_fields=['repaired_date',])
            item2.save(update_fields=['repairing_done_timedate',])
            if repair_id.ess_calculated == False:
                repaired_by_user_id = SiteUser.objects.get(profile_name=repaired_by)
                if Employee_Analysis_date.objects.filter(Q(entry_date=datetime.now().date()),
                                                         Q(user_id=repaired_by_user_id)).count() > 0:
                    Employee_Analysis_date.objects.filter(user_id=repaired_by_user_id, entry_date=datetime.now().date(),
                                                          year=datetime.now().year).update(
                        total_reparing_done_today=F("total_reparing_done_today") + repair_id.total_cost)
                    # ead.total_sales_done_today=.filter(category_id_id=id).update(total_views=F("total_views") + value_of_goods)

                    # ead.save(update_fields=['total_sales_done_today'])

                else:
                    ead = Employee_Analysis_date()
                    ead.user_id = repaired_by_user_id
                    ead.total_reparing_done_today = repair_id.total_cost
                    ead.manager_id = repaired_by_user_id.group

                    ead.month = datetime.now().month
                    ead.year = datetime.now().year
                    ead.save()

                if Employee_Analysis_month.objects.filter(Q(entry_date__month=datetime.now().month),
                                                          Q(user_id=repaired_by_user_id)).count() > 0:
                    Employee_Analysis_month.objects.filter(user_id=repaired_by_user_id,
                                                           entry_date__month=datetime.now().month,
                                                           year=datetime.now().year).update(
                        total_reparing_done=F("total_reparing_done") + repair_id.total_cost)
                    # ead.total_sales_done_today=.filter(category_id_id=id).update(total_views=F("total_views") + value_of_goods)

                    # ead.save(update_fields=['total_sales_done_today'])

                else:
                    ead = Employee_Analysis_month()
                    ead.user_id = repaired_by_user_id
                    ead.total_reparing_done = repair_id.total_cost
                    ead.manager_id = repaired_by_user_id.group

                    ead.month = datetime.now().month
                    ead.year = datetime.now().year
                    ead.save()

                repair_id.ess_calculated = True
                item2.save(update_fields=['ess_calculated', ])

        if repair_id.repairing_time_calculated == False and repair_id.repairing_start_timedate != None and repair_id.repairing_done_timedate != None:
            if item2.repaired_date != None and item2.repaired_by != None :
                date_format = "%Y-%m-%d %H:%M:%S"

                if repair_id.repaired_date == repair_id.entry_timedate:
                    total_time_taken = repair_id.repairing_done_timedate - repair_id.repairing_start_timedate
                    time = total_time_taken.total_seconds() / 3600
                    item2.total_repairing_time = time
                    item2.save(update_fields=['total_repairing_time'])
                else:
                    time1_format = repair_id.repairing_start_timedate.strftime("%Y-%m-%d")
                    start_day_time1 = datetime.strptime(str(time1_format) + ' 20:00:00', date_format)

                    start_day_time2 = datetime.strptime(str(repair_id.repairing_start_timedate)[:19], date_format)
                    a = start_day_time1 - start_day_time2
                    first_day_time = a.total_seconds() / 3600

                    time2_format = repair_id.repairing_done_timedate.strftime("%Y-%m-%d")

                    end_day_time1 = datetime.strptime(str(time2_format) + ' 10:00:00', date_format)
                    end_day_time2 = datetime.strptime(str(repair_id.repairing_done_timedate)[:19], date_format)
                    b = end_day_time2 - end_day_time1
                    last_day_time = b.total_seconds() / 3600

                    total_days = (repair_id.repairing_done_timedate - repair_id.repairing_start_timedate).days - 1
                    total_days_time = total_days * 10
                    total_time_taken = total_days_time + last_day_time + first_day_time

                    item2.total_repairing_time = total_time_taken
                    item2.save(update_fields=['total_repairing_time'])

                # total_time = repair_id.repairing_done_timedate - repair_id.repairing_start_timedate
                # total_hours = total_time.total_seconds() // 3600        #for 24 hours (total hours for a single repair)

                # total_days = (total_time.total_seconds() // 3600) / 24          #total days for a single repair
                # final_time_hours = total_hours - (total_days*14)
                user_name = SiteUser.objects.get(profile_name=repair_id.repaired_by)

                avg_daily = Repairing_after_sales_service.objects.filter(repaired_by=user_name.profile_name,entry_timedate=repair_id.entry_timedate).aggregate(Avg('total_repairing_time'))

                Employee_Analysis_date.objects.filter(user_id=user_name.id,
                                                      entry_date=repair_id.entry_timedate,
                                                  year=repair_id.entry_timedate.year).update(
                    avg_time_to_repair_single_scale_today=avg_daily['total_repairing_time__avg'])

                avg_monthly = Repairing_after_sales_service.objects.filter(repaired_by=user_name.profile_name,entry_timedate__month=repair_id.entry_timedate.month).aggregate(Avg('total_repairing_time'))

                Employee_Analysis_month.objects.filter(user_id=user_name.id,
                                                       entry_date__month=repair_id.entry_timedate.month,
                                                       year=repair_id.entry_timedate.year).update(
                    avg_time_to_repair_single_scale=avg_monthly['total_repairing_time__avg'])


                item2.repairing_time_calculated = True
                item2.save(update_fields=['repairing_time_calculated',])

        item2.second_person=customer_name
        # item2.third_person=third_person
        item2.second_contact_no=contact_no
        # item2.third_contact_no=third_contact_no
        item2.confirmed_estimate = confirmed_estimate
        item2.repaired = repaired
        item2.notes = notes
        if taken_by != '' and taken_by != None and taken_by != 'None':

            item2.repairing_start_timedate = timezone.now()

            item2.taken_by = taken_by
            item2.user_id = SiteUser.objects.get(profile_name=taken_by)
            item2.save(update_fields=['taken_by',])
            item2.save(update_fields=['user_id', ])
            item2.save(update_fields=['notes', ])
            item2.save(update_fields=['repairing_start_timedate', ])


        # item2.feedback_given = feedback_given
        # item2.current_stage = current_stage


        # item2.save()

        # item2.save(update_fields=['repairingnumber', ]),
        # item2.save(update_fields=['previous_repairing_number', ]),
        # item2.save(update_fields=['today_date', ]),
        # item2.save(update_fields=['products_to_be_repaired', ]),


        # item2.save(update_fields=['informed_by', ]),
        item2.save(update_fields=['confirmed_estimate',])
        item2.save(update_fields=['second_company_name',])
        item2.save(update_fields=['company_address',])
        item2.save(update_fields=['repaired',])
        item2.save(update_fields=['company_email',])
        item2.save(update_fields=['repaired_by','taken_by',])
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


@login_required(login_url='/')
def repairing_module_home(request):

    if request.method == 'POST':
        if'submit1' in request.POST:
            start_date = request.POST.get('date1')
            end_date = request.POST.get('date2')
            if check_admin_roles(request):  # For ADMIN
                repair_list = Repairing_after_sales_service.objects.filter(user_id__group__icontains=request.user.name,
                                                                           user_id__is_deleted=False,entry_timedate__range=[start_date, end_date]).order_by('-repairing_no')
            else:  # For EMPLOYEE
                repair_list = Repairing_after_sales_service.objects.filter(user_id=request.user.pk,entry_timedate__range=[start_date, end_date]).order_by('-repairing_no')
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
                                                                           user_id__is_deleted=False,second_contact_no__icontains=contact).order_by('-repairing_no')
            else:  # For EMPLOYEE
                repair_list = Repairing_after_sales_service.objects.filter(user_id=request.user.pk,second_contact_no__icontains=contact).order_by('-repairing_no')
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
                                                                           user_id__is_deleted=False,company_email__icontains=email).order_by('-repairing_no')
            else:  # For EMPLOYEE
                repair_list = Repairing_after_sales_service.objects.filter(user_id=request.user.pk,company_email__icontains=email).order_by('-repairing_no')
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
                                                                           user_id__is_deleted=False,second_person__icontains=customer).order_by('-repairing_no')
            else:  # For EMPLOYEE
                repair_list = Repairing_after_sales_service.objects.filter(user_id=request.user.pk,second_person__icontains=customer).order_by('-repairing_no')
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
                                                                           user_id__is_deleted=False,second_company_name__icontains=company).order_by('-repairing_no')
            else:  # For EMPLOYEE
                repair_list = Repairing_after_sales_service.objects.filter(user_id=request.user.pk,second_company_name__icontains=company).order_by('-repairing_no')
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
                                                                           user_id__is_deleted=False,crm_no__pk=crm).order_by('-repairing_no')
            else:  # For EMPLOYEE
                repair_list = Repairing_after_sales_service.objects.filter(user_id=request.user.pk,crm_no__pk=crm).order_by('-repairing_no')
            # repair_list = Repairing_after_sales_service.objects.filter(crn_number=crm)
            context = {
                'repair_list': repair_list,
                'search_msg': 'Search result for CRM No. : ' + crm,
            }
            return render(request, 'dashboardnew/repairing_module_home.html', context)
    else:
        if request.user.role =='Super Admin':     #For ADMIN
            repair_list = Repairing_after_sales_service.objects.filter((Q(taken_by=None) | Q(taken_by='') |Q(user_id__name=request.user.name)|Q(taken_by=request.user.name)| Q(user_id__group__icontains=request.user.name))&Q(user_id__is_deleted=False)&Q(user_id__modules_assigned__icontains="'Repairing Module'")).order_by('-repairing_no')

            res = Repairing_after_sales_service.objects.filter(Q(taken_by=None) | Q(taken_by='') |Q(user_id__name=request.user.name)|Q(taken_by=request.user.name) | Q(user_id__group__icontains=request.user.name)).values(
                'current_stage').annotate(
                dcount=Count('current_stage'))
        elif request.user.role =='Admin':
            repair_list = Repairing_after_sales_service.objects.filter((Q(taken_by=request.user.name)| Q(user_id__group__icontains=request.user.name)|Q(user_id__name=request.user.name))).order_by(
                '-repairing_no')

            res = Repairing_after_sales_service.objects.filter(
                (Q(taken_by=request.user.name) | Q(taken_by=None) | Q(taken_by='')|Q(user_id__name=request.user.name)) ).values(
                'current_stage').annotate(
                dcount=Count('current_stage'))
        elif request.user.role =='Manager':
            admin = SiteUser.objects.get(id=request.user.pk).admin
            repair_list = Repairing_after_sales_service.objects.filter(
                (Q(taken_by=request.user.name) | Q(taken_by=None) | Q(taken_by='')|Q(user_id__name=request.user.name)) & Q(user_id__admin=admin)).order_by(
                '-repairing_no')

            res = Repairing_after_sales_service.objects.filter(
                (Q(taken_by=request.user.name) | Q(taken_by=None) | Q(taken_by='')|Q(user_id__name=request.user.name)) & Q(user_id__admin=admin)).values(
                'current_stage').annotate(
                dcount=Count('current_stage'))

        else:  #For EMPLOYEE
            admin = SiteUser.objects.get(id=request.user.pk).admin
            repair_list = Repairing_after_sales_service.objects.filter((Q(taken_by=request.user.name)|Q(taken_by=None) | Q(taken_by=''))&Q(user_id__admin=admin)).order_by('-repairing_no')

            res = Repairing_after_sales_service.objects.filter((Q(taken_by=request.user.name)|Q(taken_by=None) | Q(taken_by=''))&Q(user_id__admin=admin)).values('current_stage').annotate(
                dcount=Count('current_stage'))
            # repair_list2 = Repairing_after_sales_service.objects.filter(Q(taken_by='')).order_by('-repairing_no')
            # repair_list = Repairing_after_sales_service.objects.filter(taken_by=request.user.name,).order_by('-repairing_no')
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


@login_required(login_url='/')
def manager_repairing_module_home(request):
    repair_employee_list = SiteUser.objects.all()
    context={
        'repair_employee_list':repair_employee_list,
    }
    return render(request,'dashboardnew/manager_repairing_module_home.html',context)


@login_required(login_url='/')
def repairing_analytics(request):
    mon = datetime.now().month
    this_month = Employee_Analysis_month.objects.all().values('entry_date').annotate(data_sum=Sum('total_reparing_done'))
    this_lis_date = []
    this_lis_sum = []
    for i in this_month:
        x = i
        this_lis_date.append(x['entry_date'].strftime("%B-%Y"))
        this_lis_sum.append(x['data_sum'])

    # Generates a "SELECT MAX..." query
    value = Employee_Analysis_month.objects.aggregate(Max('total_reparing_done'))
    print(value['total_reparing_done__max'])
    try:
        value = Employee_Analysis_month.objects.get(total_reparing_done=value['total_reparing_done__max'])
    except:
        pass

    value_low = Employee_Analysis_month.objects.aggregate(Min('total_reparing_done'))
    print(value_low['total_reparing_done__min'])
    try:
        value_low = Employee_Analysis_month.objects.filter(total_reparing_done=value_low['total_reparing_done__min']).order_by('id').first()
    except:
        pass
    context = {

        'this_lis_date': this_lis_date,
        'this_lis_sum': this_lis_sum,
        'value': value,
        'value_low': value_low,

    }
    return render(request,'analytics/repairing_analytics.html',context)


@login_required(login_url='/')
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


@login_required(login_url='/')
def final_repairing_report_module(request):
    repair_start_date = str(request.session.get('repair_start_date'))
    repair_end_date = str(request.session.get('repair_end_date'))
    repair_string = request.session.get('repair_string')
    repair_product_string = request.session.get('repair_product_string')
    selected_product_list = request.session.get('selected_product_list')
    final_row = []
    final_row_product = []

    selected_list = request.session.get('selected_list')
    for n, i in enumerate(selected_list):
        if i == 'repairing_app_repairing_after_sales_service.id':
            selected_list[n] = 'Reparing ID'
        if i == 'crm_no_id':
            selected_list[n] = 'Customer No'
        if i == 'today_date':
            selected_list[n] = 'Entry Date'


    with connection.cursor() as cursor:

        if repair_product_string != '' and repair_string != '':

            cursor.execute("SELECT " + (repair_product_string +","+ repair_string) + " from repairing_app_repairing_product  PRODUCT , repairing_app_repairing_after_sales_service "
            "REP , customer_app_customer_details CRM where PRODUCT.repairing_id_id = REP.id and REP.crm_no_id = CRM.id and "
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
        'repair_start_date': repair_start_date,
        'repair_end_date': repair_end_date,
        'final_row': final_row,
        'final_row_product': final_row_product,
        # 'selected_list': selected_list,
        'selected_product_list': selected_product_list+selected_list,
    }
    return render(request,'report/final_report_rep_mod_form.html',context)


# @login_required(login_url='/')
def feedback_repairing(request,user_id,customer_id,repairing_id):
    feedback_form = Repairing_Feedback_Form(request.POST or None, request.FILES or None)
    if Repairing_after_sales_service.objects.get(id=repairing_id).feedback_given:
        return HttpResponse('Feedback Already Submitted.')
    else:
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


@login_required(login_url='/')
def edit_product(request,id):
    product_id = Repairing_Product.objects.get(id=id)
    repairing_id = Repairing_Product.objects.get(id=id).repairing_id
    user_id=Repairing_after_sales_service.objects.get(id=repairing_id).user_id
    if request.method == 'POST':
        type_of_machine = request.POST.get('type_of_machine')
        model = request.POST.get('model')
        sub_model = request.POST.get('sub_model')
        problem_in_scale = request.POST.get('problem_in_scale')
        components_replaced_in_warranty = request.POST.getlist('components_replaced_in_warranty')
        components_replaced = request.POST.getlist('components_replaced')

        replaced_scale_given = request.POST.get('replaced_scale_given')
        Replaced_scale_serial_no = request.POST.get('Replaced_scale_serial_no')
        deposite_taken_for_replaced_scale = request.POST.get('deposite_taken_for_replaced_scale')
        in_warranty = request.POST.get('in_warranty')

        cost = request.POST.get('cost')

        product_id = Repairing_Product.objects.get(id=id)
        reparing_id = Repairing_after_sales_service.objects.get(
            id=Repairing_Product.objects.get(id=id).repairing_id.pk).pk
        cost2 = product_id.cost

        if cost != None or '':
            Repairing_after_sales_service.objects.filter(id=reparing_id).update(total_cost=F("total_cost") - cost2)
            Repairing_after_sales_service.objects.filter(id=reparing_id).update(total_cost=F("total_cost") + cost)
            if Repairing_after_sales_service.objects.get(id=repairing_id).repaired_by != None or '':
                repaired_by =  Repairing_after_sales_service.objects.get(id=repairing_id).repaired_by
                repaired_by_user_id = SiteUser.objects.get(profile_name=repaired_by)

                Employee_Analysis_month.objects.filter(user_id=repaired_by_user_id,
                                                       entry_date__month=product_id.entry_timedate.month,
                                                       year=product_id.entry_timedate.year).update(
                    total_reparing_done=F("total_reparing_done") - cost2)

                Employee_Analysis_date.objects.filter(user_id=repaired_by_user_id,
                                                      entry_date=product_id.entry_timedate,
                                                      year=product_id.entry_timedate.year).update(
                    total_reparing_done_today=F("total_reparing_done_today") - cost2)

                Employee_Analysis_month.objects.filter(user_id=repaired_by_user_id,
                                                       entry_date__month=product_id.entry_timedate.month,
                                                       year=product_id.entry_timedate.year).update(
                    total_reparing_done=F("total_reparing_done") + cost)
                Employee_Analysis_date.objects.filter(user_id=repaired_by_user_id,
                                                      entry_date=product_id.entry_timedate,
                                                      year=product_id.entry_timedate.year).update(
                    total_reparing_done_today=F("total_reparing_done_today") + cost)

        current_stage_in_db = Repairing_after_sales_service.objects.get(id=repairing_id.pk).current_stage  # updatestage2



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

        # if in_warranty.lower() == 'yes':
        #     # Repairing_after_sales_service.objects.filter(id=reparing_id).update(total_cost=F("total_cost") - item.cost)
        #     item.cost = 0.0
        # else:
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


        # Repairing_after_sales_service.objects.filter(id=reparing_id).update(total_cost=F("total_cost") + float(cost))
        # Repairing_after_sales_service.objects.filter(id=reparing_id).update(total_cost=F("total_cost") + 100.0)



        context = {
        'product_id': product_id,
        }

        return render(request, 'edit_product/edit_product_repair.html', context)

    context = {
            'product_id': product_id,
    }


    return render(request,'edit_product/edit_product_repair.html',context)


@login_required(login_url='/')
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

    mon = datetime.now().month

    target_achieved = 0.0
    avg_time = 0.0
    try:
        obj = Employee_Analysis_month.objects.get(user_id=user_id, entry_date__month=mon)
        obj.reparing_target_achived_till_now = (obj.total_reparing_done / obj.reparing_target_given) * 100
        obj.save(update_fields=['reparing_target_achived_till_now'])
        target_achieved = obj.reparing_target_achived_till_now
        avg_time = obj.avg_time_to_repair_single_scale
    except:
        pass

    this_month = Repairing_after_sales_service.objects.filter(repaired_by=SiteUser.objects.get(id=user_id).profile_name,entry_timedate__month=mon)\
        .values('entry_timedate').annotate(data_sum=Sum('total_cost'))

    this_lis_date = []
    this_lis_sum = []
    for i in this_month:
        x = i
        this_lis_date.append(x['entry_timedate'].strftime('%Y-%m-%d'))
        this_lis_sum.append(x['data_sum'])
        print(this_lis_sum)
        print(this_lis_sum)

    # previous month sales
    mon = (datetime.now().month)
    if mon == 1 :
        previous_mon = 12
    else:
        previous_mon = (datetime.now().month) - 1

    previous_month = Repairing_after_sales_service.objects.filter(repaired_by=SiteUser.objects.get(id=user_id).profile_name,entry_timedate__month=previous_mon)\
        .values('entry_timedate').annotate(data_sum=Sum('total_cost'))
    print(previous_month)
    previous_lis_date = []
    previous_lis_sum = []
    for i in previous_month:
        x = i
        previous_lis_date.append(x['entry_timedate'].strftime('%Y-%m-%d'))
        previous_lis_sum.append(x['data_sum'])

    if request.method == 'POST':
        start_date = request.POST.get('date1')
        end_date = request.POST.get('date2')

        qs=Repairing_after_sales_service.objects.filter(repaired_by=SiteUser.objects.get(id=user_id).profile_name,entry_timedate__range=(start_date, end_date))\
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
            'rep_feedback': rep_feedback,
            'avg_time': avg_time,
        }
        return render(request, "graphs/repairing_employee_graph.html", context)
    else:

        qs = Repairing_after_sales_service.objects.filter(repaired_by=SiteUser.objects.get(id=user_id).profile_name,entry_timedate__month=datetime.now().month)\
        .values('entry_timedate').annotate(data_sum=Sum('total_cost'))
        lis_date = []
        lis_sum = []
        for i in qs:
            x=i
            lis_date.append(x['entry_timedate'].strftime('%Y-%m-%d'))
            lis_sum.append(x['data_sum'])

        context={
            'final_list':lis_date,
            'final_list2':lis_sum,
            'previous_lis_date': previous_lis_date,
            'previous_lis_sum': previous_lis_sum,
            'this_lis_date': this_lis_date,
            'this_lis_sum': this_lis_sum,
            'target_achieved': target_achieved,
            'rep_feedback': rep_feedback,
            'avg_time': avg_time,
            # 'feeback': feeback,
        }
        return render(request,"graphs/repairing_employee_graph.html",context)


@login_required(login_url='/')
def load_reparing_stages_list(request,):

    selected_stage = request.GET.get('selected_stage')
    ini_time_for_now = datetime.now()
    if selected_stage == '4days':


        new_final_time = ini_time_for_now - timedelta(days=4)

        if check_admin_roles(request):  # For ADMIN


            repair_list = Repairing_after_sales_service.objects.filter(Q(stage_update_timedate=new_final_time)&(Q(taken_by=None) | Q(taken_by='')| Q(taken_by=request.user.name)| Q(
                user_id__group__icontains=request.user.name)) & Q(current_stage='Repaired but not collected')).order_by('repairing_no')
        else:  # For EMPLOYEE

            repair_list = Repairing_after_sales_service.objects.filter(Q(stage_update_timedate=new_final_time)&(Q(taken_by=None) | Q(taken_by='')| Q(taken_by=request.user.name)) & Q(current_stage='Repaired but not collected')).order_by('repairing_no')
        # repair_list = Repairing_after_sales_service.objects.filter(current_stage=selected_stage)
    elif selected_stage == '10days':
        new_final_time = ini_time_for_now - timedelta(days=10)
        if check_admin_roles(request):  # For ADMIN


            repair_list = Repairing_after_sales_service.objects.filter(Q(stage_update_timedate=new_final_time)&(Q(taken_by=None) | Q(taken_by='')| Q(taken_by=request.user.name)| Q(
                user_id__group__icontains=request.user.name)) & Q(current_stage='Repaired but not collected')).order_by('repairing_no')
        else:  # For EMPLOYEE

            repair_list = Repairing_after_sales_service.objects.filter(Q(stage_update_timedate=new_final_time)&(Q(taken_by=None) | Q(taken_by='')| Q(taken_by=request.user.name)) & Q(current_stage='Repaired but not collected')).order_by('repairing_no')
    else:
        if check_admin_roles(request):  # For ADMIN


            repair_list = Repairing_after_sales_service.objects.filter((Q(taken_by=None) | Q(taken_by='')| Q(taken_by=request.user.name)| Q(
                user_id__group__icontains=request.user.name)) & Q(current_stage=selected_stage)).order_by(
                '-repairing_no')
        else:  # For EMPLOYEE
            admin = SiteUser.objects.get(id=request.user.pk).admin
            repair_list = Repairing_after_sales_service.objects.filter((
                (Q(taken_by=request.user.name) | Q(taken_by=None) | Q(taken_by='')) & Q(user_id__admin=admin)) & Q(current_stage=selected_stage)).order_by(
                '-repairing_no')

    # else:
    #     repair_list = Repairing_after_sales_service.objects.filter(Q(user_id=request.user.pk)|Q(user_id__manager=request.user.name)|Q(user_id__admin=request.user.name)|Q(user_id__super_admin=request.user.name),current_stage=selected_stage)

    context = {
        'repair_list': repair_list,
    }
    context.update(context)
    return render(request, 'AJAX/load_reparing_stage.html', context)


@login_required(login_url='/')
def load_reparing_manager(request):
    selected = request.GET.get('loc_id')
    current_month = datetime.now().month
    current_year = datetime.now().year
    if selected=='true':
        user_list = Employee_Analysis_month.objects.filter(entry_date__month=current_month,entry_date__year=current_year,manager_id__icontains=request.user.name,user_id__is_deleted=False,user_id__modules_assigned__icontains="'Repairing Module'")
        # dispatch_list = Employee_Analysis_month.objects.filter(user_id__group=str(request.user.name))

        context = {
            'user_list': user_list,
            'manager': True,
        }

        return render(request, 'AJAX/load_reparing_manager.html', context)
    else:
        if request.user.role =='Super Admin':     #For ADMIN
            repair_list = Repairing_after_sales_service.objects.filter((Q(taken_by=None) | Q(taken_by='') |Q(user_id__name=request.user.name)|Q(taken_by=request.user.name)| Q(user_id__group__icontains=request.user.name))
                                                                       &Q(user_id__is_deleted=False)&Q(user_id__modules_assigned__icontains="'Repairing Module'")).order_by('-repairing_no')

        elif request.user.role =='Admin':
            repair_list = Repairing_after_sales_service.objects.filter((Q(taken_by=request.user.name) | Q(
                user_id__group__icontains=request.user.name) | Q(user_id__name=request.user.name))).order_by('-repairing_no')

        elif request.user.role =='Manager':
            admin = SiteUser.objects.get(id=request.user.pk).admin
            repair_list = Repairing_after_sales_service.objects.filter(
                (Q(taken_by=request.user.name) | Q(taken_by=None) | Q(taken_by='')) & Q(user_id__admin=admin)).order_by('-repairing_no')


        else:  #For EMPLOYEE
            admin = SiteUser.objects.get(id=request.user.pk).admin
            repair_list = Repairing_after_sales_service.objects.filter((Q(taken_by=request.user.name)|Q(taken_by=None) | Q(taken_by=''))&Q(user_id__admin=admin)).order_by('-repairing_no')




        context = {
            'repair_list': repair_list,
            'manager': False,
        }

        return render(request, 'AJAX/load_reparing_manager.html', context)


@login_required(login_url='/')
def load_customer(request):
    cust_id = request.GET.get('item_id')

    cust_list = Customer_Details.objects.get(id=cust_id)
    # serialize_cust_list = CustomerSerializer(cust_list)
    # cust_list = CustomerSerializer.objects.get(id=cust_id)
    context = {
        'cust_list': cust_list,

    }

    return render(request, 'AJAX/load_customer.html', context)


@login_required(login_url='/')
def load_prev_rep(request):
    rep_id = request.GET.get('item_id')

    rep_list = Repairing_after_sales_service.objects.get(id=rep_id)

    context = {
        'cust_list': rep_list,

    }

    return render(request, 'AJAX/load_prev_rep.html', context)
from django.http import JsonResponse

@login_required(login_url='/')
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
    repair_id = Repairing_after_sales_service.objects.get(id=id).repairing_no
    api = 'PF8MzCBOGTopfpYFlSZT'
    if msg_id == '1':
        message = 'Dear '+name+', Your Scales has been ' \
                  'received at our Repairing Center. Your Repairing No is '+str(repair_id)+'.' \
                  ' For any further details please contact our customer service team on 7045922251'
        Repairing_after_sales_service.objects.filter(id=id).update(scale_sub_sms_count=F("scale_sub_sms_count")+1)
        try:
            send_mail('Scale Submit - HSCo', message, settings.EMAIL_HOST_USER,[email,])
        except:
            pass
    elif msg_id == '2':
        rep_id = Repairing_after_sales_service.objects.get(id=id)
        message = 'Dear '+name+', The Estimate for Your' \
                  ' Repairing No '+str(repair_id)+' is  '+str(rep_id.total_cost)+'/- For any further details please contact our ' \
                  'customer service team on 7045922251'
        Repairing_after_sales_service.objects.filter(id=id).update(estimate_informed_sms_count=F("estimate_informed_sms_count") + 1)
        try:
            send_mail('Reparing Estimate - HSCo',  message, settings.EMAIL_HOST_USER, [email,])

        except:
            pass
    elif msg_id == '3':
        message = 'Dear '+name+', Your Repairing Complaint No '+str(repair_id)+' is resolved.' \
                  ' Please collect your Scales within the next 3 days.For any further details please contact our customer service team on 7045922251'
        Repairing_after_sales_service.objects.filter(id=id).update(reparing_done_sms_count=F("reparing_done_sms_count") + 1)
        try:
            send_mail('Reparing done - HSCo', message, settings.EMAIL_HOST_USER, [email,])
        except:
            pass
    elif msg_id == '4':
        print('late mark sms')
        message = 'Dear '+name+', Your Repairing No '+str(repair_id)+' has been Overdue ' \
                  'with us for more than 3 days. Please Collect it without fail today before 8 pm else we will scrap it.' \
                  ' We will not be liable for any claims thereafter. For more information ' \
                  'contact our customer service team on 7045922251'
        Repairing_after_sales_service.objects.filter(id=id).update(late_mark_sms_count=F("late_mark_sms_count") + 1)
        try:
            send_mail('Late Mark - HSCo', message, settings.EMAIL_HOST_USER, [email,])
        except:
            pass
    elif msg_id == '5':
        rep_id=Repairing_after_sales_service.objects.get(id=id)
        message = 'Dear ' + name + ',Your Repairing Complaint No ' + str(repair_id) +' is resolved. Plz collect your Scales within the next 3 days.' \
                                                                                      'Contact our service team on 7045922251 \n click on the link below for feedback:\n ' \
                            ' http://139.59.76.87/feedback_repairing/'+ str(request.user.pk) + '/' + str(rep_id.crm_no.pk) + '/' + str(rep_id.pk) + '\n'
        Repairing_after_sales_service.objects.filter(id=id).update(final_del_sms_count=F("final_del_sms_count") + 1)
        try:
            send_mail('Scale Collected - HSCo', message, settings.EMAIL_HOST_USER, [email,])
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
#
# @login_required(login_url='/')
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



@login_required(login_url='/')
def repairing_form(request,id):
    data=Repairing_after_sales_service.objects.get(id=id)
    product_list=Repairing_Product.objects.filter(repairing_id=id)
    context={
        'data':data,
        'product_list':product_list,
    }
    return render(request,'repairing_format/reparingform.html',context)

#
#
# @login_required(login_url='/')
# def repairing_form_back(request):
#     return render(request,'repairing_form/reparingformback.html')
