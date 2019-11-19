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
from django.db.models import Q, F, Min
from django.db.models import Sum
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
    if 'purchase_id' in request.session:
        if request.session.get('product_saved'):
            pass

            # request.session['product_saved'] = True

        else:
            prod_list=Product_Details.objects.all().values_list('purchase_id', flat=True)
            if request.session.get('purchase_id') not in prod_list:
                Purchase_Details.objects.filter(id=request.session.get('purchase_id')).delete()

        try:
            del request.session['purchase_id']
            del request.session['user_id']
            del request.session['product_saved']
        except:
            pass
    cust_sugg = Customer_Details.objects.all()
    # sales_person_sugg = SiteUser.objects.filter(group__icontains=request.user.name)
    # if request.user.role == 'Super Admin' or request.user.role == 'Admin' or request.user.role == 'Manager':
    #     sales_person_sugg = SiteUser.objects.filter(group__icontains=request.user.name,
    #                                         modules_assigned__icontains='Customer Module', is_deleted=False)
    #
    #
    # else:  # display colleague
    #     list_group = SiteUser.objects.get(id=request.user.id).group
    #     import ast
    #
    #     x = "[" + list_group + "]"
    #     x = ast.literal_eval(x)
    #     manager_list = []
    #     for item in x:
    #         name = SiteUser.objects.filter(name=item)
    #         for i in name:
    #             if i.role == 'Manager':
    #                 if item not in manager_list:
    #                     manager_list.append(item)
    #
    #     sales_person_sugg = SiteUser.objects.filter(group__icontains=manager_list,
    #                                         modules_assigned__icontains='Customer Module', is_deleted=False)

    if request.user.role == 'Super Admin':
        sales_person_sugg=SiteUser.objects.filter(Q(id=request.user.id) | Q(group__icontains=request.user.name),modules_assigned__icontains='Customer Module', is_deleted=False)

    elif request.user.role == 'Admin':
        sales_person_sugg = SiteUser.objects.filter(admin=request.user.name,
                                            modules_assigned__icontains='Customer Module', is_deleted=False)
    elif request.user.role == 'Manager':
        sales_person_sugg = SiteUser.objects.filter(Q(id=request.user.id) | Q(manager=request.user.name),modules_assigned__icontains='Customer Module', is_deleted=False)
    else: #display colleague

        list_group = SiteUser.objects.get(id=request.user.id).manager
        sales_person_sugg = SiteUser.objects.filter(Q(id=request.user.id) | Q(manager=list_group),
                                            modules_assigned__icontains='Customer Module', is_deleted=False )




    form = Purchase_Details_Form(request.POST or None, request.FILES or None)
    if request.method == 'POST' or request.method == 'FILES':
        customer_name = request.POST.get('customer_name')
        company_name = request.POST.get('company_name')
        address = request.POST.get('customer_address')
        contact_no = request.POST.get('contact_no')
        customer_email_id = request.POST.get('customer_email_id')
        date_of_purchase = request.POST.get('date_of_purchase')
        new_repeat_purchase = request.POST.get('new_repeat_purchase')
        sales_person = request.POST.get('sales_person')
        product_purchase_date = request.POST.get('product_purchase_date')
        bill_no = request.POST.get('bill_no')
        upload_op_file = request.FILES.get('upload_op_file')
        # second_person = request.POST.get('second_person')
        # third_person = request.POST.get('third_person')
        # second_contact_no = request.POST.get('second_contact_no')
        # third_contact_no = request.POST.get('third_contact_no')
        po_number = request.POST.get('po_number')
        channel_of_sales = request.POST.get('channel_of_sales')
        industry = request.POST.get('industry')
        # value_of_goods = request.POST.get('value_of_goods')
        channel_of_dispatch = request.POST.get('channel_of_dispatch')
        notes = request.POST.get('notes')
        # feedback_form_filled = request.POST.get('feedback_form_filled')

        item2 = Purchase_Details()
        item = Customer_Details()
        if Customer_Details.objects.filter(customer_name=customer_name,contact_no=contact_no).count() > 0:

            item2.crm_no = Customer_Details.objects.filter(customer_name=customer_name,contact_no=contact_no).first()
            item3 = Customer_Details.objects.filter(customer_name=customer_name,contact_no=contact_no).first()
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
            import sys
            try:
                item.save()
                item2.crm_no = Customer_Details.objects.get(id=item.pk)


            except:
                print("Unexpected error:", sys.exc_info()[0])
                pass
        site_user_id=SiteUser.objects.get(name=sales_person).pk
        # item2.crm_no = Customer_Details.objects.get(id=item.pk)
        item2.new_repeat_purchase = new_repeat_purchase
        item2.second_person=customer_name  #new1
        # item2.third_person=third_person
        item2.second_contact_no=contact_no  #new2
        # item2.third_contact_no=third_contact_no
        item2.date_of_purchase = date_of_purchase
        item2.product_purchase_date = product_purchase_date
        item2.sales_person = sales_person
        item2.user_id=SiteUser.objects.get(id=site_user_id)
        item2.bill_no = bill_no
        item2.upload_op_file = upload_op_file
        item2.po_number = po_number
        item2.channel_of_sales = channel_of_sales
        item2.industry = industry
        item2.value_of_goods = 0.0
        item2.channel_of_dispatch = channel_of_dispatch
        item2.notes = notes
        item2.feedback_form_filled = False
        # item2.user_id = SiteUser.objects.get(id=request.user.pk)
        item2.manager_id = SiteUser.objects.get(id=request.user.pk).group
        item2.save()

        try:
            del request.session['purchase_id']
            del request.session['user_id']
        except:
            pass

        request.session['purchase_id'] = item2.pk
        request.session['user_id'] = request.user.pk

        if not (channel_of_dispatch == 'Franchisee Store'):
            dispatch = Dispatch()

            if Customer_Details.objects.filter(customer_name=customer_name,
                                               contact_no=contact_no).count() > 0:


                dispatch.crm_no = Customer_Details.objects.filter(customer_name=customer_name,
                                                               contact_no=contact_no).first()

            else:
                dispatch.crm_no = Customer_Details.objects.get(id=item.pk)

            dispatch.second_person = customer_name  # new1
            dispatch.second_contact_no = contact_no  # new2
            dispatch.user_id = SiteUser.objects.get(id=request.user.pk)
            dispatch.manager_id = SiteUser.objects.get(id=request.user.pk).group
            # dispatch.customer_email = customer_email_id
            # dispatch.customer_name = customer_name
            # dispatch.company_name = company_name
            # dispatch.customer_address = address

            dispatch.save()


            # dispatch2 = Dispatch.objects.get(id=dispatch.pk)
            # dispatch2.dispatch_id = dispatch.pk
            # dispatch2.save(update_fields=['dispatch_id'])
            customer_id = Purchase_Details.objects.get(id=item2.pk)
            customer_id.dispatch_id_assigned = Dispatch.objects.get(id=dispatch.pk) #str(dispatch.pk + 00000)
            customer_id.save(update_fields=['dispatch_id_assigned'])

        # customer_id = Purchase_Details.objects.get(id=item2.pk)
        # customer_id.dispatch_id_assigned = Dispatch.objects.get(id=dispatch.pk)  # str(dispatch.pk + 00000)
        # customer_id.save(update_fields=['dispatch_id_assigned'])




        # send_mail('Feedback Form','Click on the link to give feedback http://vikka.pythonanywhere.com/feedback_purchase/'+str(request.user.pk)+'/'+str(item.id)+'/'+str(item2.id) , settings.EMAIL_HOST_USER, [customer_email_id])

        if Employee_Analysis_date.objects.filter(Q(entry_date=datetime.now().date()),Q(user_id=site_user_id)).count() > 0:
            Employee_Analysis_date.objects.filter(user_id=site_user_id,entry_date__month=datetime.now().month,year = datetime.now().year).update(total_sales_done_today=F("total_sales_done_today") + 0.0)
            # ead.total_sales_done_today=.filter(category_id_id=id).update(total_views=F("total_views") + value_of_goods)

            # ead.save(update_fields=['total_sales_done_today'])

        else:
            ead = Employee_Analysis_date()
            ead.user_id = SiteUser.objects.get(id=site_user_id)
            ead.total_sales_done_today = 0.0
            # ead.total_dispatch_done_today = value_of_goods
            ead.manager_id = SiteUser.objects.get(id=site_user_id).group
            ead.month = datetime.now().month
            ead.year = datetime.now().year
            ead.save()

        if Employee_Analysis_month.objects.filter(Q(entry_date__month=datetime.now().month),Q(user_id=site_user_id)).count() > 0:
            Employee_Analysis_month.objects.filter(user_id=site_user_id,entry_date__month=datetime.now().month,year = datetime.now().year).update(total_sales_done=F("total_sales_done") + 0.0)
            # ead.total_sales_done_today=.filter(category_id_id=id).update(total_views=F("total_views") + value_of_goods)

            # ead.save(update_fields=['total_sales_done_today'])

        else:
            ead = Employee_Analysis_month()
            ead.user_id = SiteUser.objects.get(id=site_user_id)
            ead.total_sales_done = 0.0
            # ead.total_dispatch_done = value_of_goods
            ead.manager_id = SiteUser.objects.get(id=site_user_id).group
            ead.month = datetime.now().month
            ead.year = datetime.now().year
            ead.save()



        if Customer_Details.objects.filter(Q(customer_name=customer_name),
                                           Q(contact_no=contact_no)).count() > 0:
            crm_no = Customer_Details.objects.filter(Q(customer_name=customer_name),
                                                     Q(contact_no=contact_no)).first()


            try:
                message = 'Dear ' + str(crm_no.customer_name) + '. Thanks for purchasing your scale from HSCo. ' \
                                                           'Your Purchase ID is ' + str(item2.pk) + '. Please quote this Purchase number for all future references. Please fill the feedback form to' \
                                                                                               ' avail exciting offers in the future Click on the link to give feedback http://vikka.pythonanywhere.com/feedback_purchase/' \
                          + str(request.user.pk) + '/' + str(crm_no.pk) + '/' + str(item2.id)
                send_mail('Feedback Form',
                          message, settings.EMAIL_HOST_USER,
                          [crm_no.customer_email_id])
                print("send mail!!")
            except:
                print("exception occured!!")
                pass

            message = 'Dear '+str(crm_no.customer_name)+'. Thanks for purchasing your scale from HSCo. ' \
                      'Your Purchase ID is '+str(item2.pk)+'. Please quote this Purchase number for all future references. Please fill the feedback form to' \
                      ' avail exciting offers in the future Click on the link to give feedback http://vikka.pythonanywhere.com/feedback_purchase/'+ str(request.user.pk) + '/' + str(crm_no.pk) + '/' + str(item2.id)

            url = "http://smshorizon.co.in/api/sendsms.php?user=" + settings.user + "&apikey=" + settings.api + "&mobile=" + crm_no.contact_no + "&message=" + message + "&senderid=" + settings.senderid + "&type=txt"
            payload = ""
            headers = {'content-type': 'application/x-www-form-urlencoded'}

            response = requests.request("GET", url, data=json.dumps(payload), headers=headers)
            x = response.text
            print(x)

        else:
            try:
                message = 'Dear '+item.customer_name+'. Thanks for purchasing your scale from HSCo. ' \
                      'Your Purchase ID is '+str(item2.pk)+'. Please quote this Purchase number for all future references. Please fill the feedback form to' \
                      ' avail exciting offers in the future Click on the link to give feedback http://vikka.pythonanywhere.com/feedback_purchase/' \
                      + str(request.user.pk) + '/' + str(item.pk) + '/' + str(item2.id)

                send_mail('Feedback Form',
                          message, settings.EMAIL_HOST_USER,
                          [item.customer_email_id])

            except:
                pass

            message = 'Dear '+item.customer_name+'. Thanks for purchasing your scale from HSCo. ' \
                      'Your Purchase ID is '+item2.pk+'. Please quote this Purchase number for all future references. Please fill the feedback form to' \
                      ' avail exciting offers in the future Click on the link to give feedback http://vikka.pythonanywhere.com/feedback_purchase/' \
                      + str(request.user.pk) + '/' + str(item.pk) + '/' + str(item2.id)


            url = "http://smshorizon.co.in/api/sendsms.php?user=" + settings.user + "&apikey=" + settings.api + "&mobile=" + item.contact_no + "&message=" + message + "&senderid=" + settings.senderid + "&type=txt"
            payload = ""
            headers = {'content-type': 'application/x-www-form-urlencoded'}

            response = requests.request("GET", url, data=json.dumps(payload), headers=headers)
            x = response.text
            print("else wala x")
            print(x)



        return redirect('/add_product_details/'+str(item2.pk))



    context = {
        'form': form,
        'cust_sugg': cust_sugg,
        'sales_person_sugg': sales_person_sugg,
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
                'search_msg': 'Search result for date range: '+start_date+' TO '+end_date,
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
                'search_msg': 'Search result for Customer Contact No: ' + contact,
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
                'search_msg': 'Search result for Customer Email ID: ' + email,
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
                'search_msg': 'Search result for Customer Name: ' +customer,
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
                'search_msg': 'Search result for Company Name: ' + company,
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
                'search_msg': 'Search result for CRM No. : ' + crm,
            }
            return render(request, 'dashboardnew/cm.html', context)
    elif 'deleted' in request.POST:
        if check_admin_roles(request):  # For ADMIN
            cust_list = Purchase_Details.objects.filter(user_id__group__icontains=request.user.group,user_id__is_deleted=True,user_id__modules_assigned__icontains='Customer Module').order_by('-id')
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
            cust_list = Purchase_Details.objects.filter(user_id__group__icontains=request.user.group,user_id__is_deleted=False,user_id__modules_assigned__icontains='Customer Module').order_by('-id')
        else:  # For EMPLOYEE
            cust_list = Purchase_Details.objects.filter(user_id=request.user.pk).order_by('-id')


        context = {
            'customer_list': cust_list,
            'message': message_list,
        }
        return render(request,'dashboardnew/cm.html',context )


def update_customer_details(request,id):
    purchase_id_id = Purchase_Details.objects.get(id=id)
    customer_id = Purchase_Details.objects.get(id=id).crm_no
    customer_id = Customer_Details.objects.get(id=customer_id)
    product_id = Product_Details.objects.filter(purchase_id=id)

    if 'product_saved' in request.session:
        if request.session.get('product_saved'):
            pass

            # request.session['product_saved'] = True

        else:
            prod_list=Product_Details.objects.all().values_list('purchase_id', flat=True)
            if request.session.get('purchase_id') not in prod_list:
                Purchase_Details.objects.filter(id=request.session.get('purchase_id')).delete()

        try:
            del request.session['purchase_id']
            del request.session['user_id']
            del request.session['product_saved']
        except:
            pass


    try:
        feedback = Feedback.objects.get(customer_id=customer_id.pk,purchase_id=id)
        print(feedback)
        print(id)
        print(customer_id.pk)
    except:
        feedback = None

    if request.method=='POST':
        customer_name = request.POST.get('customer_name')
        company_name = request.POST.get('company_name')
        address = request.POST.get('customer_address')
        contact_no = request.POST.get('contact_no')
        customer_email_id = request.POST.get('customer_email_id')

        item=customer_id

        item.customer_name = customer_name
        item.contact_no = contact_no
        item.save(update_fields=['customer_name','contact_no'])  #new3

        if company_name != '':
            item.company_name = company_name
            item.save(update_fields=['company_name'])
        if address != '':
            item.address = address
            item.save(update_fields=['address'])

        if customer_email_id != '':
            item.customer_email_id = customer_email_id
            item.save(update_fields=['customer_email_id'])






        date_of_purchase = request.POST.get('date_of_purchase')
        # second_person=request.POST.get('second_person')
        # third_person=request.POST.get('third_person')
        # second_contact_no=request.POST.get('second_contact_no')
        # third_contact_no=request.POST.get('third_contact_no')
        sales_person = request.POST.get('sales_person')
        bill_no = request.POST.get('bill_no')
        new_repeat_purchase = request.POST.get('new_repeat_purchase')
        upload_op_file = request.FILES.get('upload_op_file')
        po_number = request.POST.get('po_number')
        channel_of_sales = request.POST.get('channel_of_sales')
        industry = request.POST.get('industry')
        # value_of_goods = request.POST.get('value_of_goods')
        channel_of_dispatch = request.POST.get('channel_of_dispatch')
        notes = request.POST.get('notes')
        # feedback_form_filled = request.POST.get('feedback_form_filled')


        item2 = purchase_id_id

        item2.crm_no = Customer_Details.objects.get(id=item.pk)



        item2.date_of_purchase = date_of_purchase
        item2.second_person=customer_name   #new4
        # item2.third_person=third_person
        item2.second_contact_no=contact_no   #new5
        # item2.third_contact_no=third_contact_no
        item2.sales_person = sales_person
        item2.new_repeat_purchase = new_repeat_purchase
        item2.bill_no = bill_no
        item2.upload_op_file = upload_op_file
        item2.po_number = po_number
        item2.channel_of_sales = channel_of_sales
        item2.industry = industry
        # item2.value_of_goods = value_of_goods
        item2.channel_of_dispatch = channel_of_dispatch
        item2.notes = notes
        # item2.feedback_form_filled = feedback_form_filled
        # item2.user_id = SiteUser.objects.get(id=request.user.pk)
        # item2.manager_id = SiteUser.objects.get(id=request.user.pk).group
        item2.save(update_fields=['date_of_purchase','sales_person','bill_no','upload_op_file','po_number','new_repeat_purchase',
                                  'channel_of_sales','industry','channel_of_dispatch','notes','second_person','second_contact_no',
                                  ])  #new6


        # purchase_id_id = Purchase_Details.objects.get(id=id)
        # customer_id = Purchase_Details.objects.get(id=id).crm_no
        # customer_id = Customer_Details.objects.get(id=customer_id)
        # product_id = Product_Details.objects.filter(purchase_id=id)
        # context = {
        #     'product_id': product_id,
        #     'customer_id': customer_id,
        #     'purchase_id_id': purchase_id_id,
        #     'feedback': feedback,
        # }

        return redirect('/view_customer_details/')

    context = {
        'product_id':product_id,
        'customer_id': customer_id,
        'purchase_id_id': purchase_id_id,
        'feedback': feedback,
    }


    return render(request,'update_forms/update_cust_mod_form.html',context)


def add_product_details(request,id):
    purchase = Purchase_Details.objects.get(id=id)
    purchase_id = purchase.id
    if 'purchase_id' in request.session:
        request.session['product_saved'] = False

    try:
        dispatch_id_assigned = str(purchase.dispatch_id_assigned)
    except:
        dispatch_id_assigned=None
    form = Product_Details_Form(request.POST or None)
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        model_of_purchase = request.POST.get('model_of_purchase')
        type_of_scale = request.POST.get('type_of_scale')
        sub_model = request.POST.get('sub_model')
        sub_sub_model = request.POST.get('sub_sub_model')
        serial_no_scale = request.POST.get('serial_no_scale')
        brand = request.POST.get('brand')
        capacity = request.POST.get('capacity')
        unit = request.POST.get('unit')
        value_of_goods = request.POST.get('value_of_goods')
        # sales_person = request.POST.get('sales_person')
        # purchase_type = request.POST.get('purchase_type')
        if value_of_goods == '' or value_of_goods == None:
            value_of_goods=0.0



        item = Product_Details()

        item.quantity = quantity
        item.type_of_scale = type_of_scale
        item.model_of_purchase = model_of_purchase
        item.sub_model = sub_model
        item.sub_sub_model = sub_sub_model
        item.serial_no_scale = serial_no_scale
        item.brand = brand
        item.capacity = capacity
        item.unit = unit
        # item.unit = unit
        item.value_of_goods = value_of_goods
        item.purchase_id_id = purchase_id

        # item.sales_person = sales_person
        # item.purchase_type = purchase_type
        item.user_id = SiteUser.objects.get(id=request.user.pk)
        item.manager_id = SiteUser.objects.get(id=request.user.pk).group
        item.save()



        Purchase_Details.objects.filter(id=purchase_id).update(value_of_goods=F("value_of_goods") + value_of_goods)


        Employee_Analysis_month.objects.filter(user_id=purchase.user_id,
                                               entry_date__month=datetime.now().month,
                                               year=datetime.now().year).update(
            total_sales_done=F("total_sales_done") + value_of_goods)

        Employee_Analysis_date.objects.filter(user_id=purchase.user_id,
                                              entry_date__month=datetime.now().month,
                                              year=datetime.now().year).update(
            total_sales_done_today=F("total_sales_done_today") + value_of_goods)


        try:
            dispatch_id=Dispatch.objects.get(id=dispatch_id_assigned)
            dispatch_pro = Product_Details_Dispatch()
            dispatch_pro.user_id = SiteUser.objects.get(id=request.user.pk)
            dispatch_pro.manager_id = SiteUser.objects.get(id=request.user.pk).group
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
            # dispatch_pro.sales_person = sales_person
            # dispatch_pro.purchase_type = purchase_type
            dispatch_pro.save()

            Product_Details.objects.filter(id=item.pk).update(product_dispatch_id=dispatch_pro.pk)
            # item.product_dispatch_id = dispatch_pro.pk
            # item.save(update_fields=['product_dispatch_id'])
        except:
            print("Franchisee Store selected")


        if 'purchase_id' in request.session:


            request.session['product_saved'] = True



        return redirect('/update_customer_details/'+str(purchase_id))


    context = {
        'form': form,
        'purchase_id': purchase_id,
    }
    return render(request,'dashboardnew/add_product.html',context)


def report(request):
    if request.method =='POST':
        selected_list = request.POST.getlist('checks[]')
        selected_product_list = request.POST.getlist('products[]')
        start_date = request.POST.get('date1')
        end_date = request.POST.get('date2')
        string = ','.join(selected_list)
        string_product = ','.join(selected_product_list)
        print(selected_list)
        request.session['start_date'] = start_date
        request.session['end_date'] = end_date
        request.session['string'] = string
        request.session['string_product'] = string_product
        request.session['selected_list'] = selected_list
        request.session['selected_product_list'] = selected_product_list
        return redirect('/final_report/')
    return render(request,"report/report_cust_mod_form.html",)


def final_report(request):
    start_date = request.session.get('start_date')
    end_date = request.session.get('end_date')
    string = request.session.get('string')
    string_product = request.session.get('string_product')
    selected_list = request.session.get('selected_list')
    selected_product_list = request.session.get('selected_product_list')


    for n, i in enumerate(selected_list):
        if i == 'purchase_app_purchase_details.id':
            selected_list[n] = 'Purchase ID'
        if i == 'customer_app_customer_details.id':
            selected_list[n] = 'Customer No'
        if i == 'today_date':
            selected_list[n] = 'Entry Date'
        if i == 'second_person':
            selected_list[n] = 'Customer Name'

    with connection.cursor() as cursor:
        cursor.execute("SELECT  "+string+" from purchase_app_purchase_details , customer_app_customer_details"
                                "  where purchase_app_purchase_details.crm_no_id = customer_app_customer_details.id and entry_timedate between '"+start_date+"' and '"+end_date+"';")
        row = cursor.fetchall()


        final_row= [list(x) for x in row]
        list3=[]
        for i in row:
            list3.append(list(i))

        cursor.execute("SELECT  " + string_product + " from purchase_app_product_details , purchase_app_purchase_details"
                                             "  where purchase_app_product_details.purchase_id_id = purchase_app_purchase_details.id and purchase_app_product_details.entry_timedate between '" + start_date + "' and '" + end_date + "';")
        row = cursor.fetchall()

        final_row_product = [list(x) for x in row]
        list3 = []
        for i in row:
            list3.append(list(i))



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
        'selected_product_list':selected_product_list,
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
    mon = datetime.now().month
    this_month = Employee_Analysis_month.objects.all().values('entry_date').annotate(data_sum=Sum('total_sales_done'))
    this_lis_date = []
    this_lis_sum = []
    for i in this_month:
        x = i
        this_lis_date.append(x['entry_date'].strftime("%B-%Y"))
        this_lis_sum.append(x['data_sum'])



    from django.db.models import Max
    # Generates a "SELECT MAX..." query
    value=Employee_Analysis_month.objects.aggregate(Max('total_sales_done'))
    print(value['total_sales_done__max'])
    try:

        value = Employee_Analysis_month.objects.get(total_sales_done=value['total_sales_done__max'])
    except:
        value = None
    value_low = Employee_Analysis_month.objects.aggregate(Min('total_sales_done'))
    print(value_low['total_sales_done__min'])
    value_low = Employee_Analysis_month.objects.filter(total_sales_done=value_low['total_sales_done__min']).order_by('total_sales_done')[0]
    context = {

        'this_lis_date': this_lis_date,
        'this_lis_sum': this_lis_sum,
        'value': value,
        'value_low': value_low,

    }
    print(value_low)
    return render(request, 'analytics/purchase_analytics_new.html',context)

def customer_employee_sales_graph(request,user_id):
    #x=Employee_Analysis_date.objects.annotate(date=TruncMonth('entry_timedate')).values('date').annotate(c=Count('id')).values('date', 'c')
    #print(x)

    feeback = Feedback.objects.filter(user_id=user_id)
    #this month sales

    mon = datetime.now().month
    this_month = Employee_Analysis_date.objects.filter(user_id=user_id,entry_date__month=mon).values('entry_date',
                                                                                                         'total_sales_done_today')
    this_lis_date = []
    this_lis_sum = []
    for i in this_month:
        x = i
        this_lis_date.append(x['entry_date'].strftime('%Y-%m-%d'))
        this_lis_sum.append(x['total_sales_done_today'])

    #previous month sales
    mon = (datetime.now().month)-1
    previous_month = Employee_Analysis_date.objects.filter(user_id=user_id,entry_date__month=mon).values('entry_date',
                                                                                                         'total_sales_done_today')
    previous_lis_date = []
    previous_lis_sum = []
    for i in previous_month:
        x = i
        previous_lis_date.append(x['entry_date'].strftime('%Y-%m-%d'))
        previous_lis_sum.append(x['total_sales_done_today'])

    if request.method=='POST':
        start_date = request.POST.get('date1')
        end_date = request.POST.get('date2')
        qs = Employee_Analysis_date.objects.filter(user_id=user_id,entry_date__range=(start_date, end_date)).values(
            'entry_date','total_sales_done_today')
        lis_date = []
        lis_sum = []
        for i in qs:
            x = i
            lis_date.append(x['entry_date'].strftime('%Y-%m-%d'))
            lis_sum.append(x['total_sales_done_today'])
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

        qs = Employee_Analysis_date.objects.filter(user_id=user_id,entry_date__month=datetime.now().month).values('entry_date',
                                                                                                         'total_sales_done_today')
        lis_date = []
        lis_sum = []
        for i in qs:
            x=i
            lis_date.append(x['entry_date'].strftime('%Y-%m-%d'))
            lis_sum.append(x['total_sales_done_today'])


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
        item.any_suggestion = any_suggestion
        item.user_id = SiteUser.objects.get(id=user_id)
        item.customer_id = Customer_Details.objects.get(id=customer_id)
        item.purchase_id = Purchase_Details.objects.get(id=purchase_id)
        try:
            item.save()

            purchase=Purchase_Details.objects.get(id=purchase_id)
            purchase.feedback_stars= (float(knowledge_of_person)+float(timeliness_of_person)+float(price_of_product)+float(overall_interaction))/float(4.0)
            purchase.feedback_form_filled= True
            purchase.save(update_fields=['feedback_stars','feedback_form_filled'])

            if Employee_Analysis_month.objects.filter(Q(entry_date__month=datetime.now().month),
                                                      Q(user_id=SiteUser.objects.get(id=user_id))).count() > 0:
                Employee_Analysis_month.objects.filter(user_id=user_id, entry_date__month=datetime.now().month,
                                                       year=datetime.now().year).update(
                    start_rating_feedback_sales=(F("start_rating_feedback_sales") + Purchase_Details.objects.get(id=purchase_id).feedback_stars) / 2.0)
                # ead.total_sales_done_today=.filter(category_id_id=id).update(total_views=F("total_views") + value_of_goods)

                # ead.save(update_fields=['total_sales_done_today'])

            else:
                ead = Employee_Analysis_month()
                ead.user_id = SiteUser.objects.get(id=user_id)
                ead.start_rating_feedback_sales = Purchase_Details.objects.get(id=purchase_id).feedback_stars
                # ead.total_dispatch_done = value_of_goods
                ead.manager_id = SiteUser.objects.get(id=user_id).group
                ead.month = datetime.now().month
                ead.year = datetime.now().year
                ead.save()

        except:
            pass



        return HttpResponse('Feedback Submitted!!! Thankyou For Your Response.')
    context={
        'feedback_form': feedback_form,
    }
    return render(request,"feedback/feedback_customer.html",context)

def edit_product_customer(request,product_id_rec):
    purchase = Product_Details.objects.get(id=product_id_rec)
    purchase_id = Purchase_Details.objects.get(id=purchase.purchase_id)
    # dispatch_id_assigned = str(purchase_id.dispatch_id_assigned)
    try:
        dispatch_id_assigned = str(purchase.dispatch_id_assigned)
    except:
        dispatch_id_assigned=None
    product_id = Product_Details.objects.get(id=product_id_rec)
    if request.method == 'POST':
        quantity = request.POST.get('quantity')
        model_of_purchase = request.POST.get('model_of_purchase')
        type_of_scale = request.POST.get('type_of_scale')
        sub_model = request.POST.get('sub_model')
        sub_sub_model = request.POST.get('sub_sub_model')
        serial_no_scale = request.POST.get('serial_no_scale')
        brand = request.POST.get('brand')
        capacity = request.POST.get('capacity')
        unit = request.POST.get('unit')
        # sales_person = request.POST.get('sales_person')
        value_of_goods = request.POST.get('value_of_goods')
        # purchase_type = request.POST.get('purchase_type')

        cost2 = purchase.value_of_goods

        Purchase_Details.objects.filter(id=purchase_id.pk).update(value_of_goods=F("value_of_goods") - cost2)
        # Repairing_after_sales_service.objects.filter(id=reparing_id).update(total_cost=F("total_cost") + float(cost))
        # Repairing_after_sales_service.objects.filter(id=reparing_id).update(total_cost=F("total_cost") + 100.0)
        # if cost2 > 0.0:
        Employee_Analysis_month.objects.filter(user_id=purchase_id.user_id,
                                               entry_date__month=product_id.entry_timedate.month,
                                               year=product_id.entry_timedate.year).update(
            total_sales_done=F("total_sales_done") - cost2)

        Employee_Analysis_date.objects.filter(user_id=purchase_id.user_id,
                                              entry_date__month=product_id.entry_timedate.month,
                                              year=product_id.entry_timedate.year).update(
            total_sales_done_today=F("total_sales_done_today") - cost2)





        item = product_id

        item.quantity = quantity
        item.type_of_scale = type_of_scale
        item.model_of_purchase = model_of_purchase
        item.sub_model = sub_model
        item.sub_sub_model = sub_sub_model
        item.serial_no_scale = serial_no_scale
        item.brand = brand
        item.capacity = capacity
        item.unit = unit
        item.value_of_goods = value_of_goods
        # item.purchase_id_id = purchase_id
        # item.sales_person = sales_person
        # item.purchase_type = purchase_type
        # item.user_id = SiteUser.objects.get(id=request.user.pk)
        # item.manager_id = SiteUser.objects.get(id=request.user.pk).group
        item.save(update_fields=['quantity', 'type_of_scale', 'model_of_purchase', 'sub_model','sub_sub_model',
                                 'serial_no_scale', 'brand', 'capacity', 'unit','value_of_goods',
                                 ])

        Purchase_Details.objects.filter(id=purchase_id.pk).update(
            value_of_goods=F("value_of_goods") + value_of_goods)
        # Repairing_after_sales_service.objects.filter(id=reparing_id).update(total_cost=F("total_cost") + float(cost))
        # Repairing_after_sales_service.objects.filter(id=reparing_id).update(total_cost=F("total_cost") + 100.0)

        Employee_Analysis_month.objects.filter(user_id=request.user.pk,
                                               entry_date__month=purchase_id.entry_timedate.month,
                                               year=purchase_id.entry_timedate.year).update(
            total_sales_done=F("total_sales_done") + value_of_goods)

        Employee_Analysis_date.objects.filter(user_id=request.user.pk,
                                              entry_date__month=purchase_id.entry_timedate.month,
                                              year=purchase_id.entry_timedate.year).update(
            total_sales_done_today=F("total_sales_done_today") + value_of_goods)


        if dispatch_id_assigned != '' or dispatch_id_assigned != None:
            if product_id.product_dispatch_id != '' or product_id.product_dispatch_id != None:
                dispatch_pro = Product_Details_Dispatch.objects.get(id=product_id.product_dispatch_id.pk)

                # dispatch_pro.user_id = SiteUser.objects.get(id=request.user.pk)
                # dispatch_pro.manager_id = SiteUser.objects.get(id=request.user.pk).group
                # dispatch_pro.product_name = product_name
                dispatch_pro.quantity = quantity
                dispatch_pro.type_of_scale = type_of_scale
                dispatch_pro.model_of_purchase = model_of_purchase
                dispatch_pro.sub_model = sub_model
                dispatch_pro.sub_sub_model = sub_sub_model
                dispatch_pro.serial_no_scale = serial_no_scale
                dispatch_pro.brand = brand
                dispatch_pro.capacity = capacity
                dispatch_pro.unit = unit
                # dispatch_pro.dispatch_id = dispatch_id
                # dispatch_pro.sales_person = sales_person
                # dispatch_pro.purchase_type = purchase_type
                dispatch_pro.save(
                    update_fields=['quantity', 'type_of_scale', 'model_of_purchase', 'sub_model',
                                   'sub_sub_model',
                                   'serial_no_scale', 'brand', 'capacity', 'unit',
                                   ])

        # try:
        #     # dispatch_id = Dispatch.objects.get(id=dispatch_id_assigned)
        #
        # except:
        #     pass

        return redirect('/update_customer_details/' + str(purchase_id.id))

    context = {
        'product_id': product_id,
    }

    return render(request,'edit_product/edit_product_customer.html',context)

def load_users(request):
    selected = request.GET.get('loc_id')

    if selected=='true':
        user_list = Employee_Analysis_month.objects.filter(manager_id__icontains=request.user.name,user_id__is_deleted=False,user_id__modules_assigned__icontains='Customer Module')
        # dispatch_list = Employee_Analysis_month.objects.filter(user_id__group=str(request.user.name))

        context = {
            'user_list': user_list,
            'manager': True,
        }

        return render(request, 'AJAX/load_users.html', context)
    else:
        if check_admin_roles(request):     #For ADMIN
            cust_list = Purchase_Details.objects.filter(user_id__group__icontains=request.user.group,user_id__is_deleted=False,user_id__modules_assigned__icontains='Customer Module').order_by('-id')
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








