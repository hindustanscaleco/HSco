from datetime import datetime
from purchase_app.models import Product_Details
from django.db.models import Sum, Min, Q, Count, F
from django.shortcuts import render, redirect
from django.db import connection
# Create your views here.
from user_app.models import SiteUser

from customer_app.models import Customer_Details

from purchase_app.views import check_admin_roles

from purchase_app.models import Purchase_Details
from .models import Dispatch, Product_Details_Dispatch
from django.core.mail import send_mail
from Hsco import settings
import requests
import json
from ess_app.models import Employee_Analysis_month
from ess_app.models import Employee_Analysis_date



def add_dispatch_details(request):
    # form = Customer_Details_Form(request.POST or None, request.FILES or None)
    cust_sugg=Customer_Details.objects.all()


    if request.user.role == 'Super Admin':
        user_list=SiteUser.objects.filter(Q(id=request.user.id) | Q(group__icontains=request.user.name),modules_assigned__icontains='Dispatch Module', is_deleted=False)

    elif request.user.role == 'Admin':
        user_list = SiteUser.objects.filter(Q(id=request.user.id) | Q(admin=request.user.name),
                                            modules_assigned__icontains='Dispatch Module', is_deleted=False)
    elif request.user.role == 'Manager':
        user_list = SiteUser.objects.filter(Q(id=request.user.id) | Q(manager=request.user.name),
                                            modules_assigned__icontains='Dispatch Module', is_deleted=False)
    else: #display colleague

        list_group = SiteUser.objects.get(id=request.user.id).manager
        user_list = SiteUser.objects.filter(Q(id=request.user.id) | Q(manager=list_group),
                                            modules_assigned__icontains='Dispatch Module', is_deleted=False)

    # user_list=SiteUser.objects.filter(group__icontains=request.user.name)

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

        second_person = request.POST.get('second_person')
        third_person = request.POST.get('third_person')
        second_contact_no = request.POST.get('second_contact_no')
        third_contact_no = request.POST.get('third_contact_no')
        dispatch_id = request.POST.get('dispatch_id')
        date_of_dispatch = request.POST.get('date_of_dispatch')
        dispatch_by = request.POST.get('dispatch_by')
        packed_by = request.POST.get('packed_by')
        hamal_name = request.POST.get('hamal_name')
        no_bundles = request.POST.get('no_bundles')
        transport_name = request.POST.get('transport_name')
        lr_no = request.POST.get('lr_no')
        photo_lr_no = request.POST.get('photo_lr_no')
        channel_of_dispatch = request.POST.get('channel_of_dispatch')
        notes = request.POST.get('notes')

        item2 = Dispatch()
        item = Customer_Details()
        if Customer_Details.objects.filter(customer_name=customer_name,
                                           contact_no=contact_no).count() > 0:

            item2.crm_no = Customer_Details.objects.filter(customer_name=customer_name,
                                                           contact_no=contact_no).first()
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
            item.contact_no = contact_no
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

        item2.user_id = SiteUser.objects.get(id=request.user.pk)
        # item2.crm_no_id = item.pk
        # item2.second_person=second_person
        # item2.third_person=third_person
        # item2.second_contact_no=second_contact_no
        # item2.third_contact_no=third_contact_no
        item2.second_person = customer_name  # new1
        item2.second_contact_no = contact_no  # new2
        item2.dispatch_id = dispatch_id
        if date_of_dispatch != '':
            item2.date_of_dispatch = date_of_dispatch
            # item.save(update_fields=['date_of_dispatch'])

        item2.dispatch_by = dispatch_by
        item2.packed_by = packed_by
        item2.hamal_name = hamal_name
        item2.no_bundles = no_bundles
        item2.transport_name = transport_name
        item2.lr_no = lr_no
        item2.photo_lr_no = photo_lr_no
        item2.channel_of_dispatch = channel_of_dispatch
        item2.notes = notes

        item2.save()

        current_stage_in_db = Dispatch.objects.get(id=item2.pk).current_stage  # updatestage1
        if (current_stage_in_db == '' or current_stage_in_db == None):
            Dispatch.objects.filter(id=item2.pk).update(current_stage='dispatch q')

        # current_stage_in_db = Dispatch.objects.get(id=item2.pk).current_stage  # updatestage1
        if (current_stage_in_db == 'dispatch q') and (dispatch_by != '' or dispatch_by != None):
            Dispatch.objects.filter(id=item2.pk).update(current_stage='dispatch but lr not updated')

        if (current_stage_in_db == 'dispatch but lr not updated') and (lr_no != '' or lr_no != None):
            Dispatch.objects.filter(id=item2.pk).update(current_stage='dispatch completed')

        # send_mail('Feedback Form','Click on the link to give feedback http://139.59.76.87/'+str(request.user.pk)+'/'+str(item.id)+'/'+str(item2.id) , settings.EMAIL_HOST_USER, [customer_email_id])

        # message = 'Click on the link to give feedback http://139.59.76.87/'+str(request.user.pk)+'/'+str(item.id)+'/'+str(item2.id)
        #
        #
        # url = "http://smshorizon.co.in/api/sendsms.php?user=" + settings.user + "&apikey=" + settings.api + "&mobile=" + contact_no + "&message=" + message + "&senderid=" + settings.senderid + "&type=txt"
        # payload = ""
        # headers = {'content-type': 'application/x-www-form-urlencoded'}
        #
        # response = requests.request("GET", url, data=json.dumps(payload), headers=headers)
        # x = response.text


        return redirect('/dispatch_view')

    context = {
        'cust_sugg': cust_sugg,
        'user_list': user_list,
    }
    return render(request,'forms/dis_mod_form.html',context)

def report_dis_mod(request):
    if request.method =='POST':
        selected_list = request.POST.getlist('checks[]')
        start_date = request.POST.get('date1')
        end_date = request.POST.get('date2')
        string = ','.join(selected_list)
        print(selected_list)
        request.session['start_date']= start_date
        request.session['end_date']= end_date
        request.session['string']= string
        request.session['selected_list']= selected_list
        return redirect('/final_report_dis_mod/')
    return render(request,"report/report_dis_mod_form.html",)

def final_report_dis_mod(request):
    start_date = request.session.get('start_date')
    end_date = request.session.get('end_date')
    string = request.session.get('string')
    selected_list = request.session.get('selected_list')

    try:
        del request.session['start_date']
        del request.session['end_date']
        del request.session['string']
        del request.session['selected_list']
    except:
        pass
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT  " + string + " from dispatch_app_dispatch , customer_app_customer_details"
                                  "  where dispatch_app_dispatch.crm_no_id = customer_app_customer_details.id and entry_timedate between '" + start_date + "' and '" + end_date + "';")
        row = cursor.fetchall()
        final_row = [list(x) for x in row]
        list3 = []
        for i in row:
            list3.append(list(i))
    try:
        del request.session['start_date']
        del request.session['end_date']
        del request.session['string']
        del request.session['selected_list']
    except:
        pass

    context = {
        'final_row': final_row,
        'selected_list': selected_list,
    }

    return render(request,"report/final_report_dis_mod.html",context)

def dispatch_view(request):
    context={}
    if request.method=='POST' :
        if'submit1' in request.POST:
            start_date = request.POST.get('date1')
            end_date = request.POST.get('date2')
            if check_admin_roles(request):  # For ADMIN
                dispatch_list = Dispatch.objects.filter(user_id__group__icontains=request.user.name,
                                                        user_id__is_deleted=False,entry_timedate__range=[start_date, end_date]).order_by('-id')
            else:  # For EMPLOYEE
                dispatch_list = Dispatch.objects.filter(user_id=request.user.pk,entry_timedate__range=[start_date, end_date]).order_by('-id')
            # dispatch_list = Dispatch.objects.filter()
            context = {
                'dispatch_list': dispatch_list,
                'search_msg': 'Search result for date range: ' + start_date + ' TO ' + end_date,
            }
            return render(request, "manager/dispatch_view.html", context)
        elif 'submit2' in request.POST:
            contact = request.POST.get('contact')
            if check_admin_roles(request):  # For ADMIN
                dispatch_list = Dispatch.objects.filter(user_id__group__icontains=request.user.name,
                                                        user_id__is_deleted=False,second_contact_no__icontains=contact).order_by('-id')
            else:  # For EMPLOYEE
                dispatch_list = Dispatch.objects.filter(user_id=request.user.pk,second_contact_no__icontains=contact).order_by('-id')
            # dispatch_list = Dispatch.objects.filter(customer_no=contact)
            context = {
                'dispatch_list': dispatch_list,
                'search_msg': 'Search result for Customer Contact No: ' + contact,
            }
            return render(request, "manager/dispatch_view.html", context)

        elif 'submit3' in request.POST:
            email = request.POST.get('email')
            if check_admin_roles(request):  # For ADMIN
                dispatch_list = Dispatch.objects.filter(user_id__group__icontains=request.user.name,
                                                        user_id__is_deleted=False,company_email__icontains=email).order_by('-id')
            else:  # For EMPLOYEE
                dispatch_list = Dispatch.objects.filter(user_id=request.user.pk,company_email__icontains=email).order_by('-id')
            # dispatch_list = Dispatch.objects.filter(customer_email=email)
            context = {
                'dispatch_list': dispatch_list,
                'search_msg': 'Search result for Customer Email ID: ' + email,
            }
            return render(request, "manager/dispatch_view.html", context)
        elif 'submit4' in request.POST:
            customer = request.POST.get('customer')
            if check_admin_roles(request):  # For ADMIN
                dispatch_list = Dispatch.objects.filter(user_id__group__icontains=request.user.name,
                                                        user_id__is_deleted=False,second_person__icontains=customer).order_by('-id')
            else:  # For EMPLOYEE
                dispatch_list = Dispatch.objects.filter(user_id=request.user.pk,second_person__icontains=customer).order_by('-id')
            # dispatch_list = Dispatch.objects.filter(customer_name=customer)
            context = {
                'dispatch_list': dispatch_list,
                'search_msg': 'Search result for Customer Name: ' + customer,
            }
            return render(request, "manager/dispatch_view.html", context)

        elif  'submit5' in request.POST:
            company = request.POST.get('company')
            if check_admin_roles(request):  # For ADMIN
                dispatch_list = Dispatch.objects.filter(user_id__group__icontains=request.user.name,
                                                        user_id__is_deleted=False,second_company_name__icontains=company).order_by('-id')
            else:  # For EMPLOYEE
                dispatch_list = Dispatch.objects.filter(user_id=request.user.pk,second_company_name__icontains=company).order_by('-id')
            # dispatch_list = Dispatch.objects.filter(company_name=company)
            context = {
                'dispatch_list': dispatch_list,
                'search_msg': 'Search result for Company Name: ' + company,
            }
            return render(request, "manager/dispatch_view.html", context)
        elif request.method=='POST' and 'submit6' in request.POST:
            crm = request.POST.get('crm')
            if check_admin_roles(request):  # For ADMIN
                dispatch_list = Dispatch.objects.filter(user_id__group__icontains=request.user.name,
                                                        user_id__is_deleted=False,crm_no__pk=crm).order_by('-id')
            else:  # For EMPLOYEE
                dispatch_list = Dispatch.objects.filter(user_id=request.user.pk,crm_no__pk=crm).order_by('-id')
            # dispatch_list = Dispatch.objects.filter(crn_number=crm)
            context = {
                'dispatch_list': dispatch_list,
                'search_msg': 'Search result for CRM No. : ' + crm,
            }
            return render(request, "manager/dispatch_view.html", context)
    else:
        if request.user.role == 'Super Admin':     #For ADMIN
            dispatch_list = Dispatch.objects.filter(Q(user_id__pk=request.user.pk) | (Q(user_id__group__icontains=request.user.name)& Q(user_id__is_deleted=False))).order_by('-id')

            stage1 = Dispatch.objects.filter((Q(user_id__pk=request.user.pk) & Q(current_stage='dispatch q'))|(Q(user_id__group__icontains=request.user.name)& Q(user_id__is_deleted=False)& Q(current_stage='dispatch q')) ).values('current_stage').annotate(
                dcount=Count('current_stage'))

            stage2 = Dispatch.objects.filter((Q(user_id__pk=request.user.pk) & Q(current_stage='dispatch but lr not updated'))|(Q(user_id__group__icontains=request.user.name)& Q(user_id__is_deleted=False)& Q(current_stage='dispatch but lr not updated'))).values(
                'current_stage').annotate(dcount=Count('current_stage'))

            stage3 = Dispatch.objects.filter((Q(user_id__pk=request.user.pk) & Q(current_stage='dispatch completed'))|(Q(user_id__group__icontains=request.user.name)& Q(user_id__is_deleted=False)& Q(current_stage='dispatch completed'))).values(
                'current_stage').annotate(dcount=Count('current_stage'))

        elif request.user.role == 'Admin' or request.user.role == 'Manager':
            admin = SiteUser.objects.get(id=request.user.pk).admin
            dispatch_list = Dispatch.objects.filter(
                Q(user_id__admin=admin) | Q(dispatch_by=request.user.name) | Q(user_id__name=admin)).order_by('-id')

            stage1 = Dispatch.objects.filter(
                (Q(user_id__admin=admin) | Q(dispatch_by=request.user.name) | Q(user_id__name=admin)) & Q(
                    current_stage='dispatch q')).values('current_stage').annotate(
                dcount=Count('current_stage'))

            stage2 = Dispatch.objects.filter(
                (Q(user_id__admin=admin) | Q(dispatch_by=request.user.name) | Q(user_id__name=admin)) & Q(
                    current_stage='dispatch but lr not updated')).values(
                'current_stage').annotate(dcount=Count('current_stage'))

            stage3 = Dispatch.objects.filter(
                (Q(user_id__admin=admin) | Q(dispatch_by=request.user.name) | Q(user_id__name=admin)) & Q(
                    current_stage='dispatch completed')).values(
                'current_stage').annotate(dcount=Count('current_stage'))


        else:  #For EMPLOYEE
            admin=SiteUser.objects.get(id=request.user.pk).admin
            dispatch_list = Dispatch.objects.filter(Q(user_id__admin=admin)|Q(dispatch_by=request.user.name)|Q(dispatch_by=request.user.name)).order_by('-id')

            stage1 = Dispatch.objects.filter((Q(user_id__admin=admin)|Q(dispatch_by=request.user.name)|Q(user_id__name=admin))&Q(current_stage='dispatch q')).values('current_stage').annotate(
                dcount=Count('current_stage'))

            stage2 = Dispatch.objects.filter((Q(user_id__admin=admin)|Q(dispatch_by=request.user.name)|Q(user_id__name=admin))&Q(current_stage='dispatch but lr not updated')).values(
                'current_stage').annotate(dcount=Count('current_stage'))

            stage3 = Dispatch.objects.filter((Q(user_id__admin=admin)|Q(dispatch_by=request.user.name)|Q(user_id__name=admin))&Q(current_stage='dispatch completed')).values(
                'current_stage').annotate(dcount=Count('current_stage'))

        # dispatch_list = Dispatch.objects.all()

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
                print(stage3)
                print(stage3)
                print(stage3)
            context10d = {
                'stage3': stage3,
            }
            context.update(context10d)
        except:
            pass

        context2 = {
            'dispatch_list': dispatch_list,
        }
        context.update(context2)
        return render(request, "manager/dispatch_view.html", context)

def update_dispatch_details(request,update_id):
    dispatch_item=Dispatch.objects.get(id=update_id)
    product_list = Product_Details_Dispatch.objects.filter(dispatch_id=update_id)
    # customer_id = Dispatch.objects.get(id=update_id).crm_no

    customer_id = Customer_Details.objects.get(id=dispatch_item.crm_no)

    if request.user.role == 'Super Admin':
        user_list = SiteUser.objects.filter(group__icontains=request.user.name,
                                            modules_assigned__icontains='Dispatch Module', is_deleted=False)

    elif request.user.role == 'Admin':
        user_list = SiteUser.objects.filter(admin=request.user.name,
                                            modules_assigned__icontains='Dispatch Module', is_deleted=False)
    elif request.user.role == 'Manager':
        user_list = SiteUser.objects.filter(manager=request.user.name,
                                            modules_assigned__icontains='Dispatch Module', is_deleted=False)
    else:  # display colleague

        list_group = SiteUser.objects.get(id=request.user.id).manager
        user_list = SiteUser.objects.filter(manager=list_group,
                                            modules_assigned__icontains='Dispatch Module', is_deleted=False)

    # user_list=SiteUser.objects.filter(group__icontains=request.user.name)


    if request.method == 'POST' or request.method=='FILES':
        contact_no = request.POST.get('contact_no')
        customer_email_id = request.POST.get('customer_email_id')
        customer_name = request.POST.get('customer_name')
        company_name = request.POST.get('company_name')
        address = request.POST.get('customer_address')

        item2 = customer_id
        item2.customer_name = customer_name
        item2.contact_no = contact_no
        item2.save(update_fields=['customer_name','contact_no'])  #new3

        if company_name != '':
            item2.company_name = company_name
            item2.save(update_fields=['company_name'])
        if address != '':
            item2.address = address
            item2.save(update_fields=['address'])

        if customer_email_id != '':
            item2.customer_email_id = customer_email_id
            item2.save(update_fields=['customer_email_id'])


        date_of_dispatch = request.POST.get('date_of_dispatch')
        dispatch_by = request.POST.get('dispatch_by')
        packed_by = request.POST.get('packed_by')
        hamal_name = request.POST.get('hamal_name')
        no_bundles = request.POST.get('no_bundles')
        transport_name = request.POST.get('transport_name')
        lr_no = request.POST.get('lr_no')
        photo_lr_no = request.POST.get('photo_lr_no')
        channel_of_dispatch = request.POST.get('channel_of_dispatch')
        notes = request.POST.get('notes')

        try:
            print("purchase_id")

            purchase_id=Purchase_Details.objects.get(dispatch_id_assigned=update_id)

            purchase_id.second_person = customer_name
            purchase_id.second_contact_no = contact_no
            purchase_id.channel_of_dispatch = channel_of_dispatch
            # channel_of_dispatch = request.POST.get('channel_of_dispatch')
            purchase_id.save(update_fields=['second_person', 'second_contact_no','channel_of_dispatch' ])



            if company_name != '':
                purchase_id.second_company_name = company_name  # new2

                purchase_id.save(update_fields=['second_company_name'])


            if address != '':

                purchase_id.company_address = address  # new2

                purchase_id.save(update_fields=['company_address'])
            if customer_email_id != '':

                purchase_id.company_email = customer_email_id  # new2
                purchase_id.save(update_fields=['company_email'])

        except:
            pass

        item = Dispatch.objects.get(id=update_id)
        if company_name != '':
            item.second_company_name = company_name  # new2

            item2.company_name = company_name
            item2.save(update_fields=['company_name'])
            item.save(update_fields=['second_company_name'])
        if address != '':
            item2.address = address

            item.company_address = address  # new2
            item2.save(update_fields=['address'])
            item.save(update_fields=['company_address'])
        if customer_email_id != '':
            item2.customer_email_id = customer_email_id
            item.company_email = customer_email_id  # new2
            item.save(update_fields=['company_email'])
            item2.save(update_fields=['customer_email_id'])

        # item.dispatch_id = dispatch_id
        # item.second_person=second_person
        # item.third_person=third_person
        # item.second_contact_no=second_contact_no
        # item.third_contact_no=third_contact_no
        item.second_person=customer_name   #new4
        item.second_contact_no=contact_no   #new5
        # if date_of_dispatch != '':
        #     item.date_of_dispatch = date_of_dispatch
        #     item.save(update_fields=['date_of_dispatch'])
        from datetime import datetime

        datetime.today().strftime('%Y-%m-%d')
        if dispatch_by != None:
            item.dispatch_by = dispatch_by
            item.date_of_dispatch = datetime.today().strftime('%Y-%m-%d')
            item.save(update_fields=['date_of_dispatch'])
            item.save(update_fields=['dispatch_by', ]),


        item.packed_by = packed_by
        item.hamal_name = hamal_name
        item.no_bundles = no_bundles
        item.transport_name = transport_name
        item.lr_no = lr_no
        item.photo_lr_no = photo_lr_no
        item.channel_of_dispatch = channel_of_dispatch
        item.notes = notes



        current_stage_in_db = Dispatch.objects.get(id=update_id).current_stage  # updatestage3
        if (current_stage_in_db == 'dispatch but lr not updated') and (lr_no != '' and lr_no != None):
            Dispatch.objects.filter(id=update_id).update(current_stage='dispatch completed')
            product_list = ''' '''
            pro_lis = Product_Details_Dispatch.objects.filter(dispatch_id=dispatch_item.pk)

            for idx, item in enumerate(pro_lis):
                # for it in item:

                email_body_text = (
                    u"\nSr. No.: {},"
                    "\tModel: {},"
                    "\tSub Model: {}"
                    "\tbrand: {}"
                    "\tcapacity: {}"
                    "\tCost: {}"

                ).format(
                    idx + 1,
                    item.type_of_scale,
                    item.sub_model,
                    item.brand,
                    item.capacity,
                    item.value_of_goods,
                )
                product_list = product_list + '' + str(email_body_text)

            try:
                msg = "Dear " + customer_name + ", Your goods have been successfully dispatched through" \
                                                " " + transport_name + ", having LR Number " + lr_no + ". Please track the" \
                                                                                                       " details on the transporters website"+'\nHere is the list of product dispatched:\n' + product_list
                send_mail('Feedback Form',
                          msg, settings.EMAIL_HOST_USER,
                          [dispatch_item.company_email])
                print("send mail!!")
            except:
                print("exception occured!!")
                pass

            msg = "Dear " + customer_name + ", Your goods have been successfully dispatched through " + transport_name + ", having LR Number " + lr_no + ". Please track the details on the transporters website"

            url = "http://smshorizon.co.in/api/sendsms.php?user=" + settings.user + "&apikey=" + settings.api + "&mobile=" + contact_no + "&message=" + msg + "&senderid=" + settings.senderid + "&type=txt"
            payload = ""
            headers = {'content-type': 'application/x-www-form-urlencoded'}

            response = requests.request("GET", url, data=json.dumps(payload), headers=headers)
            x = response.text






        if (current_stage_in_db == 'dispatch q') and (dispatch_by != '' and dispatch_by != None):
            Dispatch.objects.filter(id=update_id).update(current_stage='dispatch but lr not updated')
            dispatch_by_id=SiteUser.objects.get(name=dispatch_by).id

            value_of_goods=Product_Details_Dispatch.objects.filter(dispatch_id=update_id).aggregate(Sum('value_of_goods'))
            total_amt=value_of_goods['value_of_goods__sum']

            if Employee_Analysis_date.objects.filter(Q(entry_date=datetime.now().date()),
                                                     Q(user_id=dispatch_by_id)).count() > 0:
                Employee_Analysis_date.objects.filter(user_id=dispatch_by_id, entry_date__month=datetime.now().month,
                                                      year=datetime.now().year).update(
                    total_dispatch_done_today=F("total_dispatch_done_today") + total_amt)
                # ead.total_sales_done_today=.filter(category_id_id=id).update(total_views=F("total_views") + value_of_goods)

                # ead.save(update_fields=['total_sales_done_today'])

            else:
                ead = Employee_Analysis_date()
                ead.user_id = SiteUser.objects.get(id=dispatch_by_id)
                ead.total_dispatch_done_today = total_amt
                # ead.total_dispatch_done_today = value_of_goods
                ead.manager_id = SiteUser.objects.get(id=dispatch_by_id).group
                ead.month = datetime.now().month
                ead.year = datetime.now().year
                ead.save()

            if Employee_Analysis_month.objects.filter(Q(entry_date__month=datetime.now().month),
                                                      Q(user_id=dispatch_by_id)).count() > 0:
                Employee_Analysis_month.objects.filter(user_id=dispatch_by_id, entry_date__month=datetime.now().month,
                                                       year=datetime.now().year).update(
                    total_dispatch_done=F("total_dispatch_done") + total_amt)
                # ead.total_sales_done_today=.filter(category_id_id=id).update(total_views=F("total_views") + value_of_goods)

                # ead.save(update_fields=['total_sales_done_today'])

            else:
                ead = Employee_Analysis_month()
                ead.user_id = SiteUser.objects.get(id=dispatch_by_id)
                ead.total_dispatch_done = total_amt
                # ead.total_dispatch_done = value_of_goods
                ead.manager_id = SiteUser.objects.get(id=dispatch_by_id).group
                ead.month = datetime.now().month
                ead.year = datetime.now().year
                ead.save()









        # item.save(update_fields=['dispatch_id', ]),

        item.save(update_fields=['second_person','third_person','second_contact_no','third_contact_no', ]),
        item.save(update_fields=['second_person','second_contact_no', ])

        item.save(update_fields=['packed_by', ]),
        item.save(update_fields=['hamal_name', ]),
        item.save(update_fields=['no_bundles', ]),
        item.save(update_fields=['transport_name', ]),
        item.save(update_fields=['lr_no', ]),
        item.save(update_fields=['photo_lr_no', ]),
        item.save(update_fields=['channel_of_dispatch', ]),
        item.save(update_fields=['notes', ]),
        item.save(update_fields=['second_company_name', ]),
        item.save(update_fields=['company_address', ]),
        item.save(update_fields=['company_email', ]),
        dispatch_item = Dispatch.objects.get(id=update_id)
        product_list = Product_Details_Dispatch.objects.filter(dispatch_id=update_id)

        context = {
            'dispatch_item': dispatch_item,
            'product_list': product_list,
        }
        return render(request, "update_forms/update_dis_mod_form.html", context)

    context = {
            'dispatch_item': dispatch_item,
            'product_list': product_list,
            'user_list': user_list,
        }
    return render(request, "update_forms/update_dis_mod_form.html", context)
       # item.save(update_fields=[''])


        #return redirect('/dispatch_view')

    # context={
    #     'dispatch_item':dispatch_item,
    #     'product_list':product_list,
    # }
    # return render(request, "update_forms/update_dis_mod_form.html",context)

def dispatch_logs(request):
    return render(request,"logs/dispatch_logs.html",)

def dispatch_analytics(request):
    mon = datetime.now().month
    this_month = Employee_Analysis_month.objects.all().values('entry_date').annotate(data_sum=Sum('total_dispatch_done'))
    this_lis_date = []
    this_lis_sum = []
    for i in this_month:
        x = i
        this_lis_date.append(x['entry_date'].strftime("%B-%Y"))
        this_lis_sum.append(x['data_sum'])

    from django.db.models import Max
    # Generates a "SELECT MAX..." query
    value = Employee_Analysis_month.objects.aggregate(Max('total_dispatch_done'))
    print(value['total_dispatch_done__max'])
    try:
        value = Employee_Analysis_month.objects.get(total_sales_done=value['total_dispatch_done__max'])
    except:
        pass

    value_low = Employee_Analysis_month.objects.aggregate(Min('total_dispatch_done'))
    print(value_low['total_dispatch_done__min'])
    try:
        value_low = Employee_Analysis_month.objects.filter(total_sales_done=value_low['total_dispatch_done__min']).order_by('id').first()
    except:
        pass
    context = {

        'this_lis_date': this_lis_date,
        'this_lis_sum': this_lis_sum,
        'value': value,
        'value_low': value_low,

    }
    return render(request,"analytics/dispatch_analytics.html",)

def dispatch_employee_graph(request,user_id):
    from django.db.models import Sum

    # user_id = request.user.pk

    # current month
    mon = datetime.now().month
    this_month = Employee_Analysis_date.objects.filter(user_id=user_id,entry_date__month=mon).values('entry_date',
                                                                                                         'total_dispatch_done_today')
    this_lis_date = []
    this_lis_sum = []
    for i in this_month:
        x = i
        this_lis_date.append(x['entry_date'].strftime('%Y-%m-%d'))
        this_lis_sum.append(x['total_dispatch_done_today'])

    # previous month sales
    mon = (datetime.now().month) - 1
    previous_month = Employee_Analysis_date.objects.filter(user_id=user_id,entry_date__month=mon).values('entry_date',
                                                                                                         'total_dispatch_done_today')
    previous_lis_date = []
    previous_lis_sum = []
    for i in previous_month:
        x = i
        previous_lis_date.append(x['entry_date'].strftime('%Y-%m-%d'))
        previous_lis_sum.append(x['total_dispatch_done_today'])

    if request.method == 'POST':
        start_date = request.POST.get('date1')
        end_date = request.POST.get('date2')
        qs = Employee_Analysis_date.objects.filter(user_id=user_id,entry_date__range=(start_date, end_date)).values(
            'entry_date','total_dispatch_done_today')
        lis_date = []
        lis_sum = []
        for i in qs:
            x = i
            lis_date.append(x['entry_date'].strftime('%Y-%m-%d'))
            lis_sum.append(x['total_dispatch_done_today'])

        context = {
            'final_list': lis_date,
            'final_list2': lis_sum,
            'previous_lis_date': previous_lis_date,
            'previous_lis_sum': previous_lis_sum,
            'this_lis_date': this_lis_date,
            'this_lis_sum': this_lis_sum,
            # 'rep_feedback': rep_feedback,
        }
        return render(request, "graphs/dispatch_employee_graph.html", context)
    else:

        qs = Employee_Analysis_date.objects.filter(user_id=user_id,entry_date__month=datetime.now().month).values(
            'entry_date','total_dispatch_done_today')
        lis_date = []
        lis_sum = []
        for i in qs:
            x = i
            lis_date.append(x['entry_date'].strftime('%Y-%m-%d'))
            lis_sum.append(x['total_dispatch_done_today'])
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
            # 'rep_feedback': rep_feedback,
            # 'feeback': feeback,
        }
        return render(request,"graphs/dispatch_employee_graph.html",context)



def load_dispatch_done(request,):
    selected = request.GET.get('loc_id')
    if selected=='true':
        dispatch_list = Dispatch.objects.filter(~Q(dispatch_by=None))

    else:
        dispatch_list = Dispatch.objects.filter(dispatch_by=None)
    context = {
        'dispatch_list': dispatch_list,
    }

    return render(request, 'AJAX/load_dispatch_done.html', context)

def load_dispatch_done_manager(request,):
    selected = request.GET.get('loc_id')

    if selected=='true':
        dispatch_list = Employee_Analysis_month.objects.filter(manager_id__icontains=request.user.name,user_id__is_deleted=False,user_id__modules_assigned__icontains='Dispatch Module')
        # dispatch_list = Employee_Analysis_month.objects.filter(user_id__group=str(request.user.name))
        print("dispatch_list22")
        print(dispatch_list)
        context = {
            'dispatch_list2': dispatch_list,
            'manager': True,
        }

        return render(request, 'AJAX/load_dispatch_done_manager.html', context)
    else:
        if check_admin_roles(request):  # For ADMIN
            dispatch_list = Dispatch.objects.filter(Q(user_id__pk=request.user.pk) | (
                        Q(user_id__group__icontains=request.user.name) & Q(user_id__is_deleted=False))).order_by('-id')


        else:  # For EMPLOYEE
            admin = SiteUser.objects.get(id=request.user.pk).admin
            dispatch_list = Dispatch.objects.filter(
                Q(user_id__admin=admin) | Q(dispatch_by=request.user.name)).order_by('-id')



        context = {
            'dispatch_list': dispatch_list,
            'manager': False,
        }

        return render(request, 'AJAX/load_dispatch_done_manager.html', context)

def load_dispatch_stages_list(request):
    selected_stage = request.GET.get('selected_stage')

    if check_admin_roles(request):  # For ADMIN


        dispatch_list = Dispatch.objects.filter((Q(user_id__pk=request.user.pk) & Q(current_stage='dispatch q')) | (
                    Q(user_id__group__icontains=request.user.name) & Q(user_id__is_deleted=False) & Q(
                current_stage=selected_stage)))



    else:  # For EMPLOYEE
        admin = SiteUser.objects.get(id=request.user.pk).admin


        dispatch_list = Dispatch.objects.filter(
            (Q(user_id__admin=admin) | Q(dispatch_by=request.user.name)) & Q(current_stage=selected_stage))

    # if check_admin_roles(request):  # For ADMIN
    #     dispatch_list = Dispatch.objects.filter(user_id__group__icontains=request.user.name,
    #                                             user_id__is_deleted=False,current_stage=selected_stage ).order_by('-id')
    # else:  # For EMPLOYEE
    #     manager = SiteUser.objects.get(id=request.user.pk).manager
    #     dispatch_list = Dispatch.objects.filter(user_id__manager=manager,current_stage=selected_stage).order_by('-id')

    context = {
        'dispatch_list': dispatch_list,
    }
    context.update(context)
    return render(request, 'AJAX/load_dispatch_stage.html', context)


def edit_dispatch_product(request,product_id_rec):

    pro_dispatch=Product_Details_Dispatch.objects.get(id=product_id_rec)

    if request.method == 'POST':

        serial_no_scale = request.POST.get('serial_no_scale')

        if serial_no_scale != None and serial_no_scale!= '':
            Product_Details_Dispatch.objects.filter(id=product_id_rec).update(serial_no_scale=serial_no_scale)
            try:
                Product_Details.objects.filter(product_dispatch_id=product_id_rec).update(serial_no_scale=serial_no_scale)
            except:
                pass



        return redirect('/edit_dispatch_product/'+str(product_id_rec))

    context = {
        'product_id': pro_dispatch,
    }

    return render(request,'edit_product/dispatch_product.html',context)






