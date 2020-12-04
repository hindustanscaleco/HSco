from django.contrib import messages
from django.core.paginator import Paginator
from django.db import connection
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from customer_app.models import Customer_Details
from user_app.models import SiteUser
from dispatch_app.models import Dispatch
from dispatch_app.models import Product_Details_Dispatch
from ess_app.models import Employee_Analysis_month, Employee_Analysis_date
from purchase_app.forms import Purchase_Details_Form, Feedback_Form
from ess_app.models import Employee_Leave
from django.db.models import Q, F, Min, Avg
from django.db.models import Sum
from ess_app.models import Employee_Analysis_date
from django.contrib.auth.decorators import login_required
from customer_app.models import Log, sub_sub_model
from email.mime.text import MIMEText
from django.core.mail import send_mail, EmailMessage
from lead_management.email_content import user
from customer_app.models import type_purchase,main_model,sub_model,sub_sub_model

from ess_app.models import Defects_Warning

from stock_management_system_app.models import Godown

from stock_management_system_app.models import GodownProduct

from stock_management_system_app.models import Product

from stock_management_system_app.models import GodownTransactions

from stock_management_system_app.models import AGProducts

from stock_management_system_app.models import AcceptGoods
from .models import  Purchase_Details, Feedback, Product_Details
from purchase_app.forms import Product_Details_Form
from _datetime import datetime
from django.core.mail import send_mail
from Hsco import settings
import requests
import json
from django.db.models.functions import TruncMonth
from django.db.models import Count
from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
today_month = datetime.now().month

@receiver(pre_save, sender=Purchase_Details)
def purchase_handler(sender, instance, update_fields=None, **kwargs):
    try:
        if instance.id == None or instance.id == '' or instance.id == 'None' :
            #########for insert action##########
            new_instance = instance
            log = Log()

            log.entered_by = new_instance.log_entered_by
            log.module_name = 'Purchase Module'
            log.action_type = 'Insert'
            log.table_name = 'Purchase_Details'

            log.reference = 'Purchase No: ' + str(new_instance.purchase_no)

            # log.action = old_list
            log.save()
        elif instance.id != None or instance.id !='' or instance.id !='None':

            #########for update action##########
            old_instance = instance
            new_instance = Purchase_Details.objects.get(id=instance.id)

            track = instance.tracker.changed()
            if 'log_entered_by' in track :
                del track['log_entered_by']
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
                    if value != '' and str(value) != getattr(instance,key):
                        old_list.append(key +':Old value= '+str(value) + ', New value='+getattr(instance,key) )
                log = Log()
                log.entered_by = instance.log_entered_by
                log.module_name = 'Purchase Module'
                log.action_type = 'Update'
                log.table_name = 'Purchase_Details'

                log.reference = 'Purchase No: '+str(new_instance.purchase_no)

                log.action = old_list
                if old_list != []:
                    log.save()

    except:
        pass

@receiver(pre_save, sender=Product_Details)
def purchase_product_handler(sender, instance, update_fields=None, **kwargs):
    try:
        if instance.id == None or instance.id == '' or instance.id == 'None' :
            #########for insert action##########
            new_instance = instance
            log = Log()
            purchase = Purchase_Details.objects.get(id=new_instance.purchase_id_id)

            log.entered_by = new_instance.log_entered_by
            # log.entered_by = SiteUser.objects.get(id=new_instance.user_id_id).profile_name
            log.module_name = 'Purchase Module'
            log.action_type = 'Insert'
            log.table_name = 'Product_Details'

            log.reference = 'Purchase No: ' + str(purchase.purchase_no)

            # log.action = old_list
            log.save()
        elif instance.id != None or instance.id !='' or instance.id !='None':

            #########for update action##########
            old_instance = instance
            new_instance = Product_Details.objects.get(id=instance.id)

            track = instance.tracker.changed()
            if 'log_entered_by' in track :
                del track['log_entered_by']
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
                    if value != '' and str(value) != getattr(instance,key):
                        old_list.append(key +':Old value= '+str(value) + ', New value='+getattr(instance,key) )
                    # old_list.append('Old value: ' + key )
                log = Log()
                purchase = Purchase_Details.objects.get(id=new_instance.purchase_id_id)
                log.entered_by = instance.log_entered_by
                log.module_name = 'Purchase Module'
                log.action_type = 'Update'
                log.table_name = 'Product_Details'
                log.reference = 'Purchase No: '+str(purchase.purchase_no)+ ', Product id:' +str(new_instance.id)
                log.action = old_list
                if old_list != []:
                    log.save()

    except:
        pass

@login_required(login_url='/')
def add_purchase_details(request):
    if 'purchase_id' in request.session:
        if request.session.get('product_saved'):
            pass

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
                                            modules_assigned__icontains='Customer Module', is_deleted=False)




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
        bill_address = request.POST.get('bill_address')
        shipping_address = request.POST.get('shipping_address')
        upload_op_file = request.FILES.get('upload_op_file')
        po_number = request.POST.get('po_number')
        channel_of_sales = request.POST.get('channel_of_sales')
        industry = request.POST.get('industry')
        # value_of_goods = request.POST.get('value_of_goods')
        channel_of_dispatch = request.POST.get('channel_of_dispatch')
        notes = request.POST.get('notes')
        channel_of_marketing = request.POST.get('channel_of_marketing')

        total_pf = request.POST.get('total_pf')
        gst_id = request.POST.get('gst_id')
        payment_mode = request.POST.get('payment_mode')
        bank_name = request.POST.get('bank_name')
        cheque_no = request.POST.get('cheque_no')
        cheque_date = request.POST.get('cheque_date')

        neft_bank_name = request.POST.get('neft_bank_name')
        neft_date = request.POST.get('neft_date')
        reference_no = request.POST.get('reference_no')

        credit_pending_amount = request.POST.get('credit_pending_amount')
        credit_authorised_by = request.POST.get('credit_authorised_by')
        # feedback_form_filled = request.POST.get('feedback_form_filled')

        item2 = Purchase_Details()
        item = Customer_Details()
        if Customer_Details.objects.filter(customer_name=customer_name,contact_no=contact_no).count() > 0:

            item2.crm_no = Customer_Details.objects.filter(customer_name=customer_name,contact_no=contact_no).first()
            item3 = Customer_Details.objects.filter(customer_name=customer_name,contact_no=contact_no).first()
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
            import sys
            try:
                item.save()
                item2.crm_no = Customer_Details.objects.get(id=item.pk)


            except:
                print("Unexpected error:", sys.exc_info()[0])
                pass
        site_user_id=SiteUser.objects.get(profile_name=sales_person).pk
        # item2.crm_no = Customer_Details.objects.get(id=item.pk)
        if gst_id == 'on':
            item2.is_gst = True
        item2.total_pf = float(total_pf)

        item2.neft_bank_name = neft_bank_name
        item2.reference_no = reference_no
        if neft_date != None and neft_date != '':
            item2.neft_date = neft_date

        item2.credit_pending_amount = float(credit_pending_amount)
        item2.credit_authorised_by = credit_authorised_by

        item2.payment_mode = payment_mode
        item2.bank_name = bank_name
        item2.cheque_no = cheque_no
        if cheque_date != None and cheque_date != '':
            item2.cheque_date = cheque_date
        if channel_of_marketing != None and channel_of_marketing != '':
            item2.channel_of_marketing = channel_of_marketing

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
        item2.bill_address = bill_address
        item2.shipping_address = shipping_address
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
        item2.purchase_no = Purchase_Details.objects.latest('purchase_no').purchase_no+1
        item2.log_entered_by = request.user.profile_name


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
            dispatch.second_company_name = company_name  # new2
            dispatch.company_email = customer_email_id
            dispatch.company_address = address  # new2
            dispatch.channel_of_dispatch = channel_of_dispatch   # new2
            dispatch.bill_address = bill_address   # new2
            dispatch.shipping_address = shipping_address   # new2
            if notes != None or notes != 'None' or notes != '':
                dispatch.notes = notes   # new2
            dispatch.user_id = SiteUser.objects.get(id=request.user.pk)
            dispatch.manager_id = SiteUser.objects.get(id=request.user.pk).group
            if Dispatch.objects.all().count() == 0:
                dispatch.dispatch_no = 1
            else:
                dispatch.dispatch_no = Dispatch.objects.latest('dispatch_no').dispatch_no + 1
            # dispatch.customer_email = customer_email_id
            # dispatch.customer_name = customer_name
            # dispatch.company_name = company_name
            # dispatch.customer_address = address

            dispatch.save()
            current_stage_in_db = Dispatch.objects.get(id=dispatch.pk).current_stage  # updatestage1
            if (current_stage_in_db == '' or current_stage_in_db == None):
                Dispatch.objects.filter(id=dispatch.pk).update(current_stage='dispatch q')


            # dispatch2 = Dispatch.objects.get(id=dispatch.pk)
            # dispatch2.dispatch_id = dispatch.pk
            # dispatch2.save(update_fields=['dispatch_id'])
            customer_id = Purchase_Details.objects.get(id=item2.pk)
            customer_id.dispatch_id_assigned = Dispatch.objects.get(id=dispatch.pk) #str(dispatch.pk + 00000)
            customer_id.save(update_fields=['dispatch_id_assigned'])

        # customer_id = Purchase_Details.objects.get(id=item2.pk)
        # customer_id.dispatch_id_assigned = Dispatch.objects.get(id=dispatch.pk)  # str(dispatch.pk + 00000)
        # customer_id.save(update_fields=['dispatch_id_assigned'])




        # send_mail('Feedback Form','Click on the link to give feedback http://139.59.76.87/feedback_purchase/'+str(request.user.pk)+'/'+str(item.id)+'/'+str(item2.id) , settings.EMAIL_HOST_USER, [customer_email_id])

        if Employee_Analysis_date.objects.filter(Q(entry_date=datetime.now().date()),Q(user_id=site_user_id)).count() > 0:
            Employee_Analysis_date.objects.filter(user_id=site_user_id,entry_date=datetime.now().date(),year = datetime.now().year).update(total_sales_done_today=F("total_sales_done_today") + 0.0)
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

        return redirect('/add_product_details/'+str(item2.pk))



    context = {
        'form': form,
        'cust_sugg': cust_sugg,
        'sales_person_sugg': sales_person_sugg,
    }

    return render(request,'forms/cust_mod_form.html',context)

@login_required(login_url='/')
def quick_purchase_entry(request):
    global_count=0
    try:
        del request.session['global_count_sess']
    except:
        pass
    request.session['global_count_sess'] = global_count
    if request.user.role == 'Super Admin':
        godowns = Godown.objects.filter(default_godown_purchase=False)

    elif request.user.role == 'Admin':
        godowns = Godown.objects.filter(Q(default_godown_purchase=False)&Q(godown_admin__id = request.user.id ))

    elif request.user.role == 'Manager':
        godowns = Godown.objects.filter(Q(default_godown_purchase=False)&Q(godown_admin__profile_name = request.user.admin))

    else:
        godowns = Godown.objects.filter(Q(default_godown_purchase=False)&Q(godown_admin__profile_name = request.user.admin))
    type_of_purchase_list = type_purchase.objects.all()  # 1
    if request.method == 'POST':
        quantity = float(request.POST.get('quantity'))
        model_of_purchase = request.POST.get('model_of_purchase')
        type_of_scale = request.POST.get('type_of_scale')
        sub_model = request.POST.get('sub_model')
        sub_sub_model = request.POST.get('sub_sub_model')
        serial_no_scale = request.POST.get('serial_no_scale')
        brand = request.POST.get('brand')
        capacity = request.POST.get('capacity')
        unit = request.POST.get('unit')
        value_of_goods = request.POST.get('value_of_goods')
        is_last_product_yes = request.POST.get('is_last_product_yes')
        godown = request.POST.get('godown')
        global_count = request.POST.get('global_count')
        from datetime import datetime


        item2 = Purchase_Details.objects.filter(sales_person=request.user.profile_name,is_quick_entry=True,date_of_purchase=datetime.today().strftime('%Y-%m-%d'))
        if item2.count()>0:

            if value_of_goods == '' or value_of_goods == None:
                value_of_goods = 0.0
            item2.update(value_of_goods=F("value_of_goods") + value_of_goods)
            item2 = Purchase_Details.objects.get(sales_person=request.user.profile_name,is_quick_entry=True,date_of_purchase=datetime.today().strftime('%Y-%m-%d'))

        else:
            item2 = Purchase_Details()

            cust_val =Customer_Details.objects.filter(customer_name = "Small Sale",contact_no = '0000000000')
            if cust_val.count()>0:
                item = Customer_Details.objects.get(customer_name = "Small Sale",contact_no = '0000000000')
            else:
                item = Customer_Details()
                item.customer_name = "Small Sale"

                item2.second_company_name = "Small Sale"  # new2
                item.company_name = "Small Sale"

                item.address = "Small Sale"
                item2.company_address = "Small Sale"  # new2
                item.contact_no = '0000000000'
                item2.company_email = ''  # new2
                item.customer_email_id = ''


                item.save()
            item2.crm_no = Customer_Details.objects.get(id=item.pk)
            item2.crm_no = Customer_Details.objects.get(id=item.pk)

            site_user_id = SiteUser.objects.get(profile_name=request.user.profile_name).pk
            # item2.crm_no = Customer_Details.objects.get(id=item.pk)
            item2.new_repeat_purchase = 'New'
            item2.second_person = "Small Sale"  # new1
            # item2.third_person=third_person
            item2.second_contact_no = "0000000000"  # new2
            item2.payment_mode = "Cash"
            # item2.third_contact_no=third_contact_no
            item2.date_of_purchase = datetime.today().strftime('%Y-%m-%d')
            item2.product_purchase_date = datetime.today().strftime('%Y-%m-%d')
            item2.sales_person = request.user.profile_name
            item2.user_id = SiteUser.objects.get(id=site_user_id)
            item2.bill_no = ''
            item2.bill_address = ''
            item2.shipping_address = ''
            item2.upload_op_file = ''
            item2.po_number = ''
            item2.channel_of_sales = "Retail Through Physical Store"
            item2.industry = "Small Sale"
            if value_of_goods == '' or value_of_goods == None:
                value_of_goods = 0.0
            item2.value_of_goods = value_of_goods
            item2.channel_of_dispatch = "Franchisee Store"
            item2.notes = "Small Sale"
            item2.feedback_form_filled = False
            item2.is_quick_entry = True
            # item2.user_id = SiteUser.objects.get(id=request.user.pk)
            item2.manager_id = SiteUser.objects.get(id=request.user.pk).group
            item2.purchase_no = Purchase_Details.objects.latest('purchase_no').purchase_no + 1
            item2.log_entered_by = request.user.profile_name

            item2.save()

        if value_of_goods == '' or value_of_goods == None:
            value_of_goods=0.0

        item = Product_Details()

        item.quantity = quantity

        item.type_of_scale = type_of_scale
        # if model_of_purchase != None and model_of_purchase != '':
        item.model_of_purchase = model_of_purchase
        item.sub_model = sub_model
        item.sub_sub_model = sub_sub_model
        item.serial_no_scale = serial_no_scale
        item.brand = brand
        item.capacity = capacity
        item.unit = unit
        item.amount = value_of_goods
        item.purchase_id_id = item2.pk
        item.user_id = SiteUser.objects.get(id=request.user.pk)
        item.manager_id = SiteUser.objects.get(id=request.user.pk).group
        item.log_entered_by = request.user.name
        item.godown_id = Godown.objects.get(id=godown)

        if Employee_Analysis_date.objects.filter(Q(entry_date=datetime.now().date()),
                                                 Q(user_id=SiteUser.objects.get(id=request.user.pk))).count() > 0:
            Employee_Analysis_date.objects.filter(user_id=item2.user_id,
                                                  entry_date=datetime.now().date(),
                                                  year=datetime.now().year).update(
                total_sales_done_today=F("total_sales_done_today") + value_of_goods)
            # ead.total_sales_done_today=.filter(category_id_id=id).update(total_views=F("total_views") + value_of_goods)

            # ead.save(update_fields=['total_sales_done_today'])

        else:
            ead = Employee_Analysis_date()
            ead.user_id = SiteUser.objects.get(id=request.user.pk)
            ead.total_sales_done_today = value_of_goods
            ead.manager_id = SiteUser.objects.get(id=request.user.pk).group

            ead.month = datetime.now().month
            ead.year = datetime.now().year
            ead.save()

        if Employee_Analysis_month.objects.filter(Q(entry_date__month=datetime.now().month),Q(user_id=SiteUser.objects.get(id=request.user.pk))).count() > 0:
            Employee_Analysis_month.objects.filter(user_id=SiteUser.objects.get(id=request.user.pk),entry_date__month=datetime.now().month,year = datetime.now().year).update(total_sales_done=F("total_sales_done") + value_of_goods)
            # ead.total_sales_done_today=.filter(category_id_id=id).update(total_views=F("total_views") + value_of_goods)

            # ead.save(update_fields=['total_sales_done_today'])

        else:
            ead = Employee_Analysis_month()
            ead.user_id = SiteUser.objects.get(id=request.user.pk)
            ead.total_sales_done = value_of_goods
            # ead.total_dispatch_done = value_of_goods
            ead.manager_id = SiteUser.objects.get(id=request.user.pk).group
            ead.month = datetime.now().month
            ead.year = datetime.now().year
            ead.save()



        try:
            if sub_sub_model != '':
                product_id = Product.objects.get(scale_type__name=type_of_scale, main_category__name=model_of_purchase,
                                                 sub_category__name=sub_model, sub_sub_category__name=sub_sub_model)

                if GodownProduct.objects.filter(godown_id=godown, product_id=product_id).count() > 0:
                    if GodownProduct.objects.get(godown_id=godown, product_id=product_id).quantity > quantity:
                        GodownProduct.objects.filter(godown_id=godown, product_id=product_id).update(
                            quantity=F("quantity") - quantity)
            elif sub_model != '':
                product_id = Product.objects.get(scale_type__name=type_of_scale, main_category__name=model_of_purchase,
                                                 sub_category__name=sub_model, sub_sub_category__name=None)
                if GodownProduct.objects.filter(godown_id=godown, product_id=product_id).count() > 0:
                    if GodownProduct.objects.get(godown_id=godown, product_id=product_id).quantity > quantity:
                        GodownProduct.objects.filter(godown_id=godown, product_id=product_id).update(
                            quantity=F("quantity") - quantity)
        except:
            messages.success(request, "Selected Product does not exist in product master !!!")
            return redirect('/quick_purchase_entry/' )
        item.save()

        if is_last_product_yes == 'yes':
            try:
                del request.session['global_count_sess']
            except:
                pass
            return redirect('/view_customer_details/' )
        elif is_last_product_yes == 'no':
            try:
                del request.session['global_count_sess']
            except:
                pass
            request.session['global_count_sess'] = global_count
            return redirect('/quick_purchase_entry/')
    context={
        'global_count':global_count,
        'godowns': godowns,
        'type_purchase': type_of_purchase_list,  # 2
    }
    return render(request, 'dashboardnew/add_product.html', context)

@login_required(login_url='/')
def edit_product_customer(request,product_id_rec):
    purchase = Product_Details.objects.get(id=product_id_rec)
    purchase_id = Purchase_Details.objects.get(id=purchase.purchase_id)
    type_of_purchase_list = type_purchase.objects.all()  # 1

    # dispatch_id_assigned = str(purchase_id.dispatch_id_assigned)
    try:
        dispatch_id_assigned = str(purchase.dispatch_id_assigned)
    except:
        dispatch_id_assigned=None
    product_id = purchase

    if request.user.role == 'Super Admin':
        try:
            godowns = Godown.objects.filter(~Q(id=product_id.godown_id.id)&Q(default_godown_purchase=False))
        except:
            godowns = Godown.objects.filter(Q(default_godown_purchase=False))

    elif request.user.role == 'Admin':
        try:
            godowns = Godown.objects.filter(~Q(id=product_id.godown_id.id)&Q(default_godown_purchase=False)&Q(godown_admin__id = request.user.id) )
        except:
            godowns = Godown.objects.filter(Q(default_godown_purchase=False)&Q(godown_admin__id = request.user.id) )
    elif request.user.role == 'Manager':
        try:
            godowns = Godown.objects.filter(~Q(id=product_id.godown_id.id)&Q(default_godown_purchase=False)&Q(godown_admin__profile_name = request.user.admin))
        except:
            godowns = Godown.objects.filter(Q(default_godown_purchase=False)&Q(godown_admin__profile_name = request.user.admin))

    else:
        try:
            godowns = Godown.objects.filter(~Q(id=product_id.godown_id.id)&Q(default_godown_purchase=False)&Q(godown_admin__profile_name = request.user.admin))
        except:
            godowns = Godown.objects.filter(Q(default_godown_purchase=False)&Q(godown_admin__profile_name = request.user.admin))


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
        amount = request.POST.get('value_of_goods')
        godown = request.POST.get('godown')
        cost2 = purchase.amount
        if sub_sub_model != '' and sub_sub_model != 'None':
            godown_product_id = Product.objects.get(scale_type__name=type_of_scale, main_category__name=model_of_purchase,
                                                    sub_category__name=sub_model, sub_sub_category__name=sub_sub_model)
        else:
            godown_product_id = Product.objects.get(scale_type__name=type_of_scale,
                                                    main_category__name=model_of_purchase,
                                                    sub_category__name=sub_model)

        item = product_id


        # if product changed then update stock
        if item.type_of_scale != type_of_scale or item.model_of_purchase != model_of_purchase or item.sub_model != sub_model or item.sub_sub_model != sub_sub_model:
            product_id_new = Product.objects.get(id=godown_product_id.id)
            if item.sub_sub_model != '' and item.sub_sub_model != 'None':
                product_id_old = Product.objects.get(scale_type__name=item.type_of_scale,
                                                     main_category__name=item.model_of_purchase,
                                                     sub_category__name=item.sub_model, sub_sub_category__name=item.sub_sub_model)
            else:
                product_id_old = Product.objects.get(scale_type__name=item.type_of_scale,
                                                        main_category__name=item.model_of_purchase,
                                                        sub_category__name=item.sub_model)

            if GodownProduct.objects.filter(godown_id=godown, product_id=product_id_new).count() == 0:
                messages.error(request, "Selected Product does not exist In Selected Godown !!! ")
                return redirect("/edit_product_customer/" + str(product_id_rec))

            # adding old products quantity to old/current godown
            GodownProduct.objects.filter(godown_id=purchase.godown_id.id, product_id=product_id_old).update(
                quantity=F("quantity") + item.quantity)
            item3 = AcceptGoods()
            item3.from_godown = Godown.objects.get(id=purchase.godown_id.id)
            item3.good_added = True
            item3.log_entered_by = request.user.name
            item3.notes = 'Returned from Sales'
            item3.save()

            item2 = AGProducts()
            item2.type = 'Individual'
            item2.quantity = float(item.quantity)
            item2.godown_id = Godown.objects.get(id=purchase.godown_id.id)
            item2.accept_product_id = AcceptGoods.objects.get(id=item3.id)
            item2.godown_product_id = GodownProduct.objects.get(godown_id=purchase.godown_id.id,
                                                                product_id=product_id_old)
            item2.log_entered_by = request.user.name
            item2.save()

            new_transaction = GodownTransactions()
            new_transaction.accept_goods_id = AcceptGoods.objects.get(id=item3.id)
            new_transaction.notes = 'Product Returned from Sales by Emp id: ' + str(request.user.employee_number) + ',\nName: ' + str(request.user.profile_name) \
                                    + ', Contact: ' + str(request.user.mobile) + ',\nProduct changed' + \
                                    '\nPurchase Id:' + str(purchase_id.id)+ ', Purchase Product Id: ' + str(product_id.id)
            new_transaction.save()
            # subtracting new products quantity from current godown
            GodownProduct.objects.filter(godown_id=godown, product_id=product_id_new).update(
                quantity=F("quantity") - quantity)
            new_transaction = GodownTransactions()
            new_transaction.purchase_product_id = Product_Details.objects.get(id=product_id_rec)
            new_transaction.purchase_quantity = float(quantity)
            new_transaction.notes = 'Product Added to Sales by Emp id: ' + str(request.user.employee_number)+ ',\nName: ' + str(request.user.profile_name) \
                                    + ', Contact: ' + str(request.user.mobile) + ',\nProduct changed'+ \
                                    '\nPurchase Id:' + str(purchase_id.id)+ ', Purchase Product Id: ' + str(product_id.id)
            new_transaction.save()
        else:
            new_godown_name = Godown.objects.get(id=godown).name_of_godown
            # If godown is changed, add stored quantity in current godown and subtract new quantity from new godown
            if (quantity != '') or (godown != ''):
                if float(purchase.godown_id.id) != float(godown) and float(quantity) != float(purchase.quantity):
                    if GodownProduct.objects.filter(godown_id=godown, product_id=godown_product_id).count() == 0:
                        messages.error(request, "Selected Product does not exist In Selected Godown !!! ")
                        return redirect("/edit_product_customer/" + str(product_id_rec))

                    if (float(quantity)) > GodownProduct.objects.get(godown_id=godown,product_id=godown_product_id).quantity:
                        messages.error(request, "Insufficient stock !!! Available Quantity:" + str(
                            GodownProduct.objects.get(godown_id=godown, product_id=godown_product_id).quantity))
                        return redirect("/edit_product_customer/" + str(product_id_rec))
                    # adding stored quantity in current godown
                    GodownProduct.objects.filter(godown_id=purchase.godown_id.id,
                                                 product_id=godown_product_id).update(
                        quantity=F("quantity") + purchase.quantity)
                    item3 = AcceptGoods()
                    item3.from_godown = Godown.objects.get(id=purchase.godown_id.id)
                    item3.good_added = True
                    item3.log_entered_by = request.user.name
                    item3.notes = 'Returned from Sales'
                    item3.save()

                    item2 = AGProducts()
                    item2.type = 'Individual'
                    item2.quantity = purchase.quantity
                    item2.godown_id = Godown.objects.get(id=purchase.godown_id.id)
                    item2.accept_product_id = AcceptGoods.objects.get(id=item3.id)
                    item2.godown_product_id = GodownProduct.objects.get(godown_id=purchase.godown_id.id,
                                                                        product_id=godown_product_id)
                    item2.log_entered_by = request.user.name
                    item2.save()

                    new_transaction = GodownTransactions()
                    new_transaction.accept_goods_id = AcceptGoods.objects.get(id=item3.id)
                    new_transaction.notes = 'Product Returned from Sales by Emp id: ' + str(request.user.employee_number) + ',\nName: ' + str(request.user.profile_name) \
                                            + ', Contact: ' + str(request.user.mobile) + ',\nGodown changed:- Old: ' + str(purchase.godown_id.name_of_godown) + ', New: ' + str(new_godown_name) + \
                                            '\nPurchase Id:' + str(purchase_id.id)+ ', Purchase Product Id: ' + str(product_id.id)
                    new_transaction.save()

                    # subtracting new quantity from new godown
                    GodownProduct.objects.filter(godown_id=godown, product_id=godown_product_id).update(
                        quantity=F("quantity") - quantity)
                    new_transaction = GodownTransactions()
                    new_transaction.purchase_product_id = Product_Details.objects.get(id=product_id_rec)
                    new_transaction.purchase_quantity = quantity
                    new_transaction.notes = 'Product Added to Sales by Emp id: ' + str(request.user.employee_number) + ',\nName: ' + str(request.user.profile_name) \
                                            + ', Contact: ' + str(request.user.mobile) + ',\nGodown changed:- Old: ' + str(purchase.godown_id.name_of_godown) + ', New: ' + str(new_godown_name) + \
                                            '\nPurchase Id:' + str(purchase_id.id)+ ', Purchase Product Id: ' + str(product_id.id)
                    new_transaction.save()
                elif float(purchase.godown_id.id) != float(godown):
                    if GodownProduct.objects.filter(godown_id=godown, product_id=godown_product_id).count() == 0:
                        messages.error(request, "Selected Product does not exist In Selected Godown !!! ")
                        return redirect("/edit_product_customer/" + str(product_id_rec))

                    if (float(quantity)) > GodownProduct.objects.get(godown_id=godown,product_id=godown_product_id).quantity:
                        messages.error(request, "Insufficient stock !!! Available Quantity:" + str(
                            GodownProduct.objects.get(godown_id=godown, product_id=godown_product_id).quantity))
                        return redirect("/edit_product_customer/" + str(product_id_rec))
                    # adding stored quantity in current godown
                    GodownProduct.objects.filter(godown_id=purchase.godown_id.id,
                                                 product_id=godown_product_id).update(
                        quantity=F("quantity") + purchase.quantity)
                    item3 = AcceptGoods()
                    item3.from_godown = Godown.objects.get(id=purchase.godown_id.id)
                    item3.good_added = True
                    item3.log_entered_by = request.user.name
                    item3.notes = 'Returned from Sales'
                    item3.save()

                    item2 = AGProducts()
                    item2.type = 'Individual'
                    item2.quantity = purchase.quantity
                    item2.godown_id = Godown.objects.get(id=purchase.godown_id.id)
                    item2.accept_product_id = AcceptGoods.objects.get(id=item3.id)
                    item2.godown_product_id = GodownProduct.objects.get(godown_id=purchase.godown_id.id,
                                                                        product_id=godown_product_id.id)
                    item2.log_entered_by = request.user.name
                    item2.save()

                    new_transaction = GodownTransactions()
                    new_transaction.accept_goods_id = AcceptGoods.objects.get(id=item3.id)
                    new_transaction.notes = 'Product Returned from Sales by Emp id: ' + str(request.user.employee_number) + ',\nName: ' + str(request.user.profile_name) \
                                            + ', Contact: ' + str(request.user.mobile) + ',\nGodown changed:- Old: ' + str(purchase.godown_id.name_of_godown) + ', New: ' + str(new_godown_name) + \
                                            '\nPurchase Id:' + str(purchase_id.id)+ ', Purchase Product Id: ' + str(product_id.id)
                    new_transaction.save()

                    # subtracting new quantity from new godown
                    GodownProduct.objects.filter(godown_id=godown, product_id=godown_product_id.id).update(
                        quantity=F("quantity") - purchase.quantity)

                    new_transaction = GodownTransactions()
                    new_transaction.purchase_product_id = Product_Details.objects.get(id=product_id_rec)
                    new_transaction.purchase_quantity = quantity
                    new_transaction.notes = 'Product Added to Sales by Emp id: ' + str(request.user.employee_number) + ',\nName: ' + str(request.user.profile_name) \
                                            + ', Contact: ' + str(request.user.mobile) + ',\nGodown changed:- Old: ' + str(purchase.godown_id.name_of_godown) + ', New: ' + str(new_godown_name) + \
                                            '\nPurchase Id:' + str(purchase_id.id)+ ', Purchase Product Id: ' + str(product_id.id)
                    new_transaction.save()
                elif quantity != purchase.quantity:
                    # adding old quantity to current godown
                    if (float(quantity)-float(purchase.quantity)) > GodownProduct.objects.get(godown_id=purchase.godown_id.id,product_id=godown_product_id).quantity:
                        messages.error(request, "Insufficient stock !!! Available Quantity:" + str(
                            GodownProduct.objects.get(godown_id=godown, product_id=godown_product_id).quantity))
                        return redirect("/edit_product_customer/" + str(product_id_rec))

                    GodownProduct.objects.filter(godown_id=purchase.godown_id.id,
                                                 product_id=godown_product_id).update(
                        quantity=F("quantity") + purchase.quantity)

                    # subtracting new quantity from current godown
                    GodownProduct.objects.filter(godown_id=purchase.godown_id.id,
                                                 product_id=godown_product_id).update(
                        quantity=F("quantity") - quantity)

                    if quantity < purchase.quantity:
                        item3 = AcceptGoods()
                        item3.from_godown = Godown.objects.get(id=purchase.godown_id.id)
                        item3.good_added = True
                        item3.log_entered_by = request.user.name
                        item3.notes = 'Returned from Sales'
                        item3.save()

                        item2 = AGProducts()
                        item2.type = 'Individual'
                        item2.quantity = float(purchase.quantity) - float(quantity)
                        item2.godown_id = Godown.objects.get(id=purchase.godown_id.id)
                        item2.accept_product_id = AcceptGoods.objects.get(id=item3.id)
                        item2.godown_product_id = GodownProduct.objects.get(godown_id=purchase.godown_id.id,
                                                                            product_id=godown_product_id)
                        item2.log_entered_by = request.user.name
                        item2.save()

                        new_transaction = GodownTransactions()
                        new_transaction.accept_goods_id = AcceptGoods.objects.get(id=item3.id)
                        new_transaction.notes = 'Product Returned from Sales by Emp id: ' + str(request.user.employee_number) + ',\nName: ' + str(request.user.profile_name) \
                                                + ', Contact: ' + str(request.user.mobile) + ',\nQuantity changed:- Old: ' + str(purchase.quantity) + ', New: ' + str(quantity) + \
                                                '\nPurchase Id:' + str(purchase_id.id)+ ', Purchase Product Id: ' + str(product_id.id)
                        new_transaction.save()
                    elif quantity > purchase.quantity:
                        new_transaction = GodownTransactions()
                        new_transaction.purchase_product_id = Product_Details.objects.get(id=product_id_rec)
                        new_transaction.purchase_quantity = float(quantity) - float(purchase.quantity)
                        new_transaction.notes = 'Product Added to Sales by Emp id: ' + str(request.user.employee_number) + ',\nName: ' + str(request.user.profile_name) \
                                                + ', Contact: ' + str(request.user.mobile) + ',\nQuantity changed:- Old: ' + str(purchase.quantity) + ', New: ' + str(quantity) + \
                                                '\nPurchase Id:' + str(purchase_id.id)+ ', Purchase Product Id: ' + str(product_id.id)
                        new_transaction.save()
                else:
                    print('no godown changes')

            Purchase_Details.objects.filter(id=purchase_id.pk).update(value_of_goods=F("value_of_goods") - cost2)
            Employee_Analysis_month.objects.filter(user_id=purchase_id.user_id,
                                                   entry_date__month=product_id.entry_timedate.month,
                                                   year=product_id.entry_timedate.year).update(
                total_sales_done=F("total_sales_done") - cost2)

            Employee_Analysis_date.objects.filter(user_id=purchase_id.user_id,
                                                  entry_date=product_id.entry_timedate,
                                                  year=product_id.entry_timedate.year).update(
                total_sales_done_today=F("total_sales_done_today") - cost2)


        item.quantity = quantity
        item.type_of_scale = type_of_scale
        item.model_of_purchase = model_of_purchase
        item.sub_model = sub_model
        item.sub_sub_model = sub_sub_model
        item.serial_no_scale = serial_no_scale
        item.brand = brand
        item.capacity = capacity
        item.unit = unit
        item.amount = amount
        item.godown_id = Godown.objects.get(id=godown)
        item.log_entered_by = request.user.name
        # item.purchase_id_id = purchase_id
        # item.sales_person = sales_person
        # item.purchase_type = purchase_type
        # item.user_id = SiteUser.objects.get(id=request.user.pk)
        # item.manager_id = SiteUser.objects.get(id=request.user.pk).group
        item.save(update_fields=['log_entered_by','quantity', 'type_of_scale', 'model_of_purchase', 'sub_model','sub_sub_model',
                                 'serial_no_scale', 'brand', 'capacity', 'unit','amount','godown_id'
                                 ])

        Purchase_Details.objects.filter(id=purchase_id.pk).update(
            value_of_goods=F("value_of_goods") + amount)
        # Repairing_after_sales_service.objects.filter(id=reparing_id).update(total_cost=F("total_cost") + float(cost))
        # Repairing_after_sales_service.objects.filter(id=reparing_id).update(total_cost=F("total_cost") + 100.0)

        Employee_Analysis_month.objects.filter(user_id=purchase_id.user_id,
                                               entry_date__month=purchase_id.entry_timedate.month,
                                               year=purchase_id.entry_timedate.year).update(
            total_sales_done=F("total_sales_done") + amount)

        Employee_Analysis_date.objects.filter(user_id=purchase_id.user_id,
                                              entry_date__month=purchase_id.entry_timedate.month,
                                              year=purchase_id.entry_timedate.year).update(
            total_sales_done_today=F("total_sales_done_today") + amount)



        if product_id.product_dispatch_id != '' and product_id.product_dispatch_id != None:
            if Product_Details_Dispatch.objects.filter(id=product_id.product_dispatch_id.pk).count()>0:
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
                dispatch_pro.value_of_goods = amount
                dispatch_pro.godown_id = Godown.objects.get(id=product_id.godown_id.pk)

                # dispatch_pro.dispatch_id = dispatch_id
                # dispatch_pro.sales_person = sales_person
                # dispatch_pro.purchase_type = purchase_type
                dispatch_pro.save(
                    update_fields=['quantity', 'type_of_scale','value_of_goods', 'model_of_purchase', 'sub_model',
                                   'sub_sub_model',
                                   'serial_no_scale', 'brand', 'capacity', 'unit','godown_id'
                                   ])

        # try:
        #     # dispatch_id = Dispatch.objects.get(id=dispatch_id_assigned)
        #
        # except:
        #     pass

        return redirect('/update_customer_details/' + str(purchase_id.id))

    context = {
        'product_id': product_id,
        'godowns': godowns,
        'type_purchase': type_of_purchase_list,  # 2
    }

    return render(request,'edit_product/edit_product_customer.html',context)


@login_required(login_url='/')
def view_customer_details(request):
    date_today= datetime.now().strftime('%Y-%m-%d')
    message_list = Employee_Leave.objects.filter(entry_date=str(date_today))

    #for deleting purchase entries
    if request.method == 'POST' and 'delete_purchase_id' in request.POST:
        purchase_ids = request.POST.getlist('id[]')
        for id in purchase_ids[1:]:
            try:
                purchase_obj=Purchase_Details.objects.get(purchase_no=id)
                log = Log()
                log.entered_by = request.user.profile_name
                log.module_name = 'Purchase Module'
                log.action_type = 'Delete'
                log.table_name = 'Purchase_Details'
                log.reference = 'Purchase Id:' +str(id)
                log.save()
                Purchase_Details.objects.filter(purchase_no=id).delete()
            except:
                print('Purchase with this id does not exist: '+str(id))
                pass
        messages.success(request, "Deleted Successfully!")
        print('message sent!!!')
        return redirect('/view_customer_details/')

    if request.method == 'POST' and 'deleted' not in request.POST:
        if'submit1' in request.POST:
            start_date = request.POST.get('date1')
            end_date = request.POST.get('date2')
            if check_admin_roles(request):  # For ADMIN
                cust_list = Purchase_Details.objects.filter(Q(user_id__name=request.user.name)|Q(user_id__group__icontains=request.user.name),
                                                            user_id__is_deleted=False,entry_timedate__range=[start_date, end_date]).order_by('-purchase_no')
                # paginator = Paginator(cust_list, 15)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # cust_list = paginator.get_page(page)
            else:  # For EMPLOYEE
                cust_list = Purchase_Details.objects.filter(user_id=request.user.pk,entry_timedate__range=[start_date, end_date]).order_by('-purchase_no')
                # paginator = Paginator(cust_list, 15)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # cust_list = paginator.get_page(page)
            # cust_list = Customer_Details.objects.filter()
            context = {
                'customer_list': cust_list,
                'search_msg': 'Search result for date range: '+start_date+' TO '+end_date,
            }
            return render(request, 'dashboardnew/cm.html', context)
        elif 'submit2' in request.POST:
            contact = request.POST.get('contact')
            if check_admin_roles(request):  # For ADMIN
                cust_list = Purchase_Details.objects.filter(Q(user_id__name=request.user.name)|Q(user_id__group__icontains=request.user.name),
                                                            user_id__is_deleted=False,second_contact_no__icontains=contact).order_by('-purchase_no')
                # paginator = Paginator(cust_list, 15)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # cust_list = paginator.get_page(page)
            else:  # For EMPLOYEE
                cust_list = Purchase_Details.objects.filter(user_id=request.user.pk,second_contact_no__icontains=contact).order_by('-purchase_no')
                # paginator = Paginator(cust_list, 15)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # cust_list = paginator.get_page(page)
            # cust_list = Customer_Details.objects.filter(contact_no=contact)
            context = {
                'customer_list': cust_list,
                'search_msg': 'Search result for Customer Contact No: ' + contact,
            }
            return render(request, 'dashboardnew/cm.html', context)

        elif 'submit3' in request.POST:
            email = request.POST.get('email')
            if check_admin_roles(request):  # For ADMIN
                cust_list = Purchase_Details.objects.filter(Q(user_id__name=request.user.name)|Q(user_id__group__icontains=request.user.name),
                                                            user_id__is_deleted=False,company_email__icontains=email).order_by('-purchase_no')
                # paginator = Paginator(cust_list, 15)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # cust_list = paginator.get_page(page)
            else:  # For EMPLOYEE
                cust_list = Purchase_Details.objects.filter(user_id=request.user.pk,company_email__icontains=email).order_by('-purchase_no')
                # paginator = Paginator(cust_list, 15)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # cust_list = paginator.get_page(page)
            # cust_list = Customer_Details.objects.filter(customer_email_id=email)
            context = {
                'customer_list': cust_list,
                'search_msg': 'Search result for Customer Email ID: ' + email,
            }
            return render(request, 'dashboardnew/cm.html', context)
        elif 'submit4' in request.POST:
            customer = request.POST.get('customer')
            if check_admin_roles(request):  # For ADMIN
                cust_list = Purchase_Details.objects.filter(Q(user_id__name=request.user.name)|Q(user_id__group__icontains=request.user.name),
                                                            user_id__is_deleted=False,second_person__icontains=customer).order_by('-purchase_no')
                # paginator = Paginator(cust_list, 15)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # cust_list = paginator.get_page(page)
            else:  # For EMPLOYEE
                cust_list = Purchase_Details.objects.filter(user_id=request.user.pk,second_person__icontains=customer).order_by('-purchase_no')
                # paginator = Paginator(cust_list, 15)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # cust_list = paginator.get_page(page)
            # cust_list = Customer_Details.objects.filter(customer_name=customer)
            context = {
                'customer_list': cust_list,
                'search_msg': 'Search result for Customer Name: ' +customer,
            }
            return render(request, 'dashboardnew/cm.html', context)

        elif  'submit5' in request.POST:
            company = request.POST.get('company')
            if check_admin_roles(request):  # For ADMIN
                cust_list = Purchase_Details.objects.filter(Q(user_id__name=request.user.name)|Q(user_id__group__icontains=request.user.name),
                                                            user_id__is_deleted=False,second_company_name__icontains=company).order_by('-purchase_no')
                # paginator = Paginator(cust_list, 15)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # cust_list = paginator.get_page(page)
            else:  # For EMPLOYEE
                cust_list = Purchase_Details.objects.filter(user_id=request.user.pk,second_company_name__icontains=company).order_by('-purchase_no')
                # paginator = Paginator(cust_list, 15)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # cust_list = paginator.get_page(page)
            # cust_list = Customer_Details.objects.filter(company_name=company)
            context = {
                'customer_list': cust_list,
                'search_msg': 'Search result for Company Name: ' + company,
            }
            return render(request, 'dashboardnew/cm.html', context)
        elif request.method=='POST' and 'submit6' in request.POST:
            crm = request.POST.get('crm')
            if check_admin_roles(request):  # For ADMIN
                cust_list = Purchase_Details.objects.filter(Q(user_id__name=request.user.name)|Q(user_id__group__icontains=request.user.name),
                                                            user_id__is_deleted=False,crm_no__pk=crm).order_by('-purchase_no')
                # paginator = Paginator(cust_list, 15)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # cust_list = paginator.get_page(page)
            else:  # For EMPLOYEE
                cust_list = Purchase_Details.objects.filter(user_id=request.user.pk,crm_no__pk=crm).order_by('-purchase_no')
                # paginator = Paginator(cust_list, 15)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # cust_list = paginator.get_page(page)
            # cust_list = Customer_Details.objects.filter(crn_number=crm)
            context = {
                'customer_list': cust_list,
                'search_msg': 'Search result for CRM No. : ' + crm,
            }
            return render(request, 'dashboardnew/cm.html', context)
        elif  'submit7' in request.POST:
            purchase_no = request.POST.get('purchase_no')
            if check_admin_roles(request):  # For ADMIN
                cust_list = Purchase_Details.objects.filter(Q(user_id__name=request.user.name)|Q(user_id__group__icontains=request.user.name),
                                                            user_id__is_deleted=False,purchase_no__icontains=purchase_no).order_by('-purchase_no')
                # paginator = Paginator(cust_list, 15)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # cust_list = paginator.get_page(page)
            else:  # For EMPLOYEE
                cust_list = Purchase_Details.objects.filter(user_id=request.user.pk,purchase_no__icontains=purchase_no).order_by('-purchase_no')
                # paginator = Paginator(cust_list, 15)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # cust_list = paginator.get_page(page)
            # cust_list = Customer_Details.objects.filter(company_name=company)
            context = {
                'customer_list': cust_list,
                'search_msg': 'Search result for Purchase No: ' + purchase_no,
            }
            return render(request, 'dashboardnew/cm.html', context)

    elif 'deleted' in request.POST:
        if check_admin_roles(request):  # For ADMIN
            cust_list = Purchase_Details.objects.filter(user_id__group__icontains=request.user.name,
                                                        user_id__is_deleted=True,
                                                        user_id__modules_assigned__icontains='Customer Module').order_by(
                '-purchase_no')
        else:  # For EMPLOYEE
            cust_list = Purchase_Details.objects.filter(user_id=request.user.pk).order_by('-purchase_no')
            

        context = {
            'customer_list': cust_list,
            'message': message_list,
            'deleted': True,
        }
        return render(request, 'dashboardnew/cm.html', context)


    
    
    else:
        if check_admin_roles(request):  # For ADMIN
            cust_list = Purchase_Details.objects.filter(
                Q(user_id__name=request.user.name) | Q(user_id__group__icontains=request.user.name),
                user_id__is_deleted=False, user_id__modules_assigned__icontains='Customer Module',
                entry_timedate__month=today_month).order_by('-purchase_no')
            
        else:  # For EMPLOYEE
            cust_list = Purchase_Details.objects.filter(user_id=request.user.pk,
                                                        entry_timedate__month=today_month).order_by('-purchase_no')
            


        context = {
            'customer_list': cust_list,
            'message': message_list,
        }
        return render(request,'dashboardnew/cm.html',context )


@login_required(login_url='/')
def update_customer_details(request,id):
    purchase_id_id = Purchase_Details.objects.get(id=id)
    customer_id = Purchase_Details.objects.get(id=id).crm_no
    # customer_id = Customer_Details.objects.get(id=customer_id)
    product_id = Product_Details.objects.filter(purchase_id=id)
    context ={}
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
    except:
        feedback = None

    if request.method=='POST':
        customer_name = request.POST.get('customer_name')
        company_name = request.POST.get('company_name')
        address = request.POST.get('customer_address')
        contact_no = request.POST.get('contact_no')
        customer_email_id = request.POST.get('customer_email_id')

        channel_of_dispatch = request.POST.get('channel_of_dispatch')
        if channel_of_dispatch == None or channel_of_dispatch == '' or len(channel_of_dispatch) < 2:
            context22 = {
                'product_id': product_id,
                'customer_id': customer_id,
                'purchase_id_id': purchase_id_id,
                'feedback': feedback,
                'channel_error': True,
            }
            context.update(context22)
            return render(request, 'update_forms/update_cust_mod_form.html', context)
        else:

            item=customer_id

            item.customer_name = customer_name
            item.contact_no = contact_no
            if customer_id.contact_no != item.contact_no or customer_id.customer_name != item.customer_name :
                item.save(update_fields=['customer_name','contact_no'])  #new3


            date_of_purchase = request.POST.get('date_of_purchase')
            # second_person=request.POST.get('second_person')
            # third_person=request.POST.get('third_person')
            # second_contact_no=request.POST.get('second_contact_no')
            # third_contact_no=request.POST.get('third_contact_no')
            sales_person = request.POST.get('sales_person')
            bill_no = request.POST.get('bill_no')
            bill_address = request.POST.get('bill_address')
            shipping_address = request.POST.get('shipping_address')
            new_repeat_purchase = request.POST.get('new_repeat_purchase')
            upload_op_file = request.FILES.get('upload_op_file')
            po_number = request.POST.get('po_number')
            channel_of_sales = request.POST.get('channel_of_sales')
            industry = request.POST.get('industry')
            channel_of_marketing = request.POST.get('channel_of_marketing')
            # value_of_goods = request.POST.get('value_of_goods')
            notes = request.POST.get('notes')
            tax_amount = request.POST.get('tax_amount')
            total_amount = request.POST.get('total_amount')
            # value_of_goods = request.POST.get('value_of_goods')
            # feedback_form_filled = request.POST.get('feedback_form_filled')
            payment_mode = request.POST.get('payment_mode')
            total_pf = request.POST.get('total_pf')
            gst_id = request.POST.get('gst_id')

            bank_name = request.POST.get('bank_name')
            cheque_no = request.POST.get('cheque_no')
            cheque_date = request.POST.get('cheque_date')

            neft_bank_name = request.POST.get('neft_bank_name')
            neft_date = request.POST.get('neft_date')
            reference_no = request.POST.get('reference_no')

            credit_pending_amount = request.POST.get('credit_pending_amount')
            credit_authorised_by = request.POST.get('credit_authorised_by')
            item2 = purchase_id_id

            if gst_id == 'on':
                item2.is_gst = True
            else:
                item2.is_gst = False

            item2.payment_mode = payment_mode
            if total_pf != '':
                item2.total_pf = float(total_pf)

            item2.bank_name = bank_name
            item2.cheque_no = cheque_no
            if cheque_date != None and cheque_date != '':
                item2.cheque_date = cheque_date

            item2.neft_bank_name = neft_bank_name
            item2.reference_no = reference_no
            if neft_date != None and neft_date != '':
                item2.neft_date = neft_date

            if credit_pending_amount != '':
                item2.credit_pending_amount = float(credit_pending_amount)
            item2.credit_authorised_by = credit_authorised_by

            item2.total_amount = total_amount
            item2.tax_amount = tax_amount

            if channel_of_marketing != None and channel_of_marketing != '':
                item2.channel_of_marketing = channel_of_marketing

            item2.save(update_fields=['payment_mode','bank_name','cheque_no','cheque_date','channel_of_marketing','tax_amount',
                                      'total_pf','neft_bank_name','reference_no','neft_date','credit_pending_amount','credit_authorised_by','is_gst'])

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



            item2.date_of_purchase = date_of_purchase
            item2.second_person=customer_name   #new4
            # item2.third_person=third_person
            item2.second_contact_no=contact_no   #new5
            # item2.third_contact_no=third_contact_no
            item2.sales_person = sales_person
            item2.new_repeat_purchase = new_repeat_purchase
            item2.bill_no = bill_no
            item2.bill_address = bill_address
            item2.shipping_address = shipping_address
            if upload_op_file!= None and upload_op_file!="":
                item2.upload_op_file = upload_op_file
                item2.save(update_fields=['upload_op_file',])
            item2.po_number = po_number
            item2.channel_of_sales = channel_of_sales
            item2.industry = industry
            # item2.value_of_goods = value_of_goods


            if (purchase_id_id.dispatch_id_assigned == None and channel_of_dispatch != 'Franchisee Store')  or (item2.channel_of_dispatch =='Franchisee Store' and channel_of_dispatch != 'Franchisee Store') :
                dispatch = Dispatch()

                if Customer_Details.objects.filter(customer_name=customer_name,
                                                   contact_no=contact_no).count() > 0:

                    dispatch.crm_no = Customer_Details.objects.filter(customer_name=customer_name,
                                                                      contact_no=contact_no).first()

                else:
                    dispatch.crm_no = Customer_Details.objects.get(id=item.pk)

                dispatch.second_person = customer_name  # new1
                dispatch.second_contact_no = contact_no  # new2
                dispatch.second_company_name = company_name  # new2
                dispatch.company_email = customer_email_id
                dispatch.company_address = address  # new2
                dispatch.channel_of_dispatch = channel_of_dispatch  # new2
                dispatch.bill_address = bill_address  # new2
                dispatch.shipping_address = shipping_address  # new2
                dispatch.user_id = SiteUser.objects.get(id=request.user.pk)
                dispatch.manager_id = SiteUser.objects.get(id=request.user.pk).group
                if Dispatch.objects.all().count() == 0:
                    dispatch.dispatch_no = 1
                else:
                    dispatch.dispatch_no = Dispatch.objects.latest('dispatch_no').dispatch_no + 1
                # dispatch.customer_email = customer_email_id
                # dispatch.customer_name = customer_name
                # dispatch.company_name = company_name
                # dispatch.customer_address = address

                dispatch.save()
                current_stage_in_db = Dispatch.objects.get(id=dispatch.pk).current_stage  # updatestage1
                if (current_stage_in_db == '' or current_stage_in_db == None):
                    Dispatch.objects.filter(id=dispatch.pk).update(current_stage='dispatch q')

                # dispatch2 = Dispatch.objects.get(id=dispatch.pk)
                # dispatch2.dispatch_id = dispatch.pk
                # dispatch2.save(update_fields=['dispatch_id'])
                customer_id = Purchase_Details.objects.get(id=item2.pk)
                customer_id.dispatch_id_assigned = Dispatch.objects.get(id=dispatch.pk)  # str(dispatch.pk + 00000)
                customer_id.save(update_fields=['dispatch_id_assigned'])


                prod_list= list(Product_Details.objects.filter(purchase_id=customer_id.pk).values_list('id', flat=True))
                for item in prod_list:   #newold

                    oobj=Product_Details.objects.get(id=item)

                    dispatch_pro=Product_Details_Dispatch()

                    dispatch_pro.user_id = SiteUser.objects.get(id=request.user.pk)
                    dispatch_pro.manager_id = SiteUser.objects.get(id=request.user.pk).group
                    # dispatch_pro.product_name = product_name
                    dispatch_pro.quantity = oobj.quantity
                    dispatch_pro.type_of_scale = oobj.type_of_scale
                    dispatch_pro.model_of_purchase = oobj.model_of_purchase
                    dispatch_pro.sub_model = oobj.sub_model
                    dispatch_pro.sub_sub_model = oobj.sub_sub_model
                    dispatch_pro.serial_no_scale = oobj.serial_no_scale
                    dispatch_pro.brand = oobj.brand
                    dispatch_pro.capacity = oobj.capacity
                    dispatch_pro.unit = oobj.unit
                    dispatch_pro.value_of_goods = oobj.amount
                    dispatch_pro.dispatch_id = Dispatch.objects.get(id=dispatch.pk)
                    dispatch_pro.save()

                    #aaao

                    # nobj.__dict__ = oobj.__dict__.copy()
                    Product_Details.objects.filter(id=item).update(product_dispatch_id=dispatch_pro.pk)


            if item2.channel_of_dispatch != 'Franchisee Store' and channel_of_dispatch == 'Franchisee Store' :
                customer_id = Purchase_Details.objects.get(id=item2.pk)
                customer_id.dispatch_id_assigned = None  # str(dispatch.pk + 00000)
                customer_id.save(update_fields=['dispatch_id_assigned'])
                try:
                    Dispatch.objects.get(id=item2.dispatch_id_assigned.pk).delete()
                except:
                    pass





            item2.channel_of_dispatch = channel_of_dispatch
            item2.notes = notes
            # item2.feedback_form_filled = feedback_form_filled
            # item2.user_id = SiteUser.objects.get(id=request.user.pk)
            # item2.manager_id = SiteUser.objects.get(id=request.user.pk).group
            item2.log_entered_by = request.user.profile_name

            item2.save(update_fields=['log_entered_by','date_of_purchase','sales_person','bill_no','po_number','new_repeat_purchase',
                                      'channel_of_sales','shipping_address','bill_address','industry','channel_of_dispatch','notes','second_person',
                                      'second_contact_no','second_company_name','company_address','company_email',
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

            try:
                del request.session['enable_auto_edit']
                del request.session['lead_url']
            except:
                pass

            return redirect('/view_customer_details/')

    context2 = {
        'product_id':product_id,
        'customer_id': customer_id,
        'purchase_id_id': purchase_id_id,
        'feedback': feedback,
    }
    context.update(context2)


    return render(request,'update_forms/update_cust_mod_form.html',context)


@login_required(login_url='/')
def add_product_details(request,id):
    purchase = Purchase_Details.objects.get(id=id)
    purchase_id = purchase.id
    if request.user.role == 'Super Admin':
        godowns = Godown.objects.filter(default_godown_purchase=False)

    elif request.user.role == 'Admin':
        godowns = Godown.objects.filter(Q(default_godown_purchase=False)&Q(godown_admin__id = request.user.id ))

    elif request.user.role == 'Manager':
        godowns = Godown.objects.filter(Q(default_godown_purchase=False)&Q(godown_admin__profile_name = request.user.admin))

    else:
        godowns = Godown.objects.filter(Q(default_godown_purchase=False)&Q(godown_admin__profile_name = request.user.admin))

    type_of_purchase_list =type_purchase.objects.all() #1
    if 'purchase_id' in request.session:
        request.session['product_saved'] = False

    try:
        dispatch_id_assigned = str(purchase.dispatch_id_assigned)
    except:
        dispatch_id_assigned=None
    form = Product_Details_Form(request.POST or None)
    context = {
        'form': form,
        'purchase_id': purchase_id,
        'godowns': godowns,
        'type_purchase': type_of_purchase_list,  # 2
    }
    if request.method == 'POST':
        quantity = float(request.POST.get('quantity'))
        model_of_purchase = request.POST.get('model_of_purchase')
        type_of_scale = request.POST.get('type_of_scale')
        sub_model = request.POST.get('sub_model')
        sub_sub_model = request.POST.get('sub_sub_model')
        serial_no_scale = request.POST.get('serial_no_scale')
        brand = request.POST.get('brand')
        capacity = request.POST.get('capacity')
        unit = request.POST.get('unit')
        value_of_goods = request.POST.get('value_of_goods')
        is_last_product_yes = request.POST.get('is_last_product_yes')
        godown = request.POST.get('godown')

        if value_of_goods == '' or value_of_goods == None:
            value_of_goods=0.0

        item = Product_Details()

        item.quantity = quantity

        item.type_of_scale = type_of_scale
        # if model_of_purchase != None and model_of_purchase != '':
        item.model_of_purchase = model_of_purchase
        item.sub_model = sub_model
        item.sub_sub_model = sub_sub_model
        item.serial_no_scale = serial_no_scale
        item.brand = brand
        item.capacity = capacity
        item.unit = unit
        item.amount = value_of_goods
        item.purchase_id_id = Purchase_Details.objects.get(id=purchase_id)
        item.user_id = SiteUser.objects.get(id=request.user.pk)
        item.manager_id = SiteUser.objects.get(id=request.user.pk).group
        item.log_entered_by = request.user.name
        item.godown_id = Godown.objects.get(id=godown)
        if sub_sub_model != '' and sub_sub_model != None and sub_sub_model != 'None':
            product_id = Product.objects.get(scale_type__name=type_of_scale, main_category__name=model_of_purchase,
                                                  sub_category__name=sub_model, sub_sub_category__name=sub_sub_model)

            if GodownProduct.objects.filter(godown_id=godown, product_id=product_id).count() > 0 :
                    if GodownProduct.objects.get(godown_id=godown, product_id=product_id).quantity >= quantity :
                        GodownProduct.objects.filter(godown_id=godown,product_id=product_id).update(
                        quantity=F("quantity") - quantity)
                    elif GodownProduct.objects.get(godown_id=godown, product_id=product_id).quantity < quantity:
                        messages.success(request, "Insufficient stock !!! Available Quantity:" + str(
                            GodownProduct.objects.get(godown_id=godown, product_id=product_id).quantity))
                        return redirect('/add_product_details/' + str(purchase_id))
            else:
                messages.success(request, "Selected Product does not exist in selected godown !!!")

        elif sub_model != '':
            product_id = Product.objects.get(scale_type__name=type_of_scale, main_category__name=model_of_purchase,
                                                  sub_category__name=sub_model, sub_sub_category__name=None)
            if GodownProduct.objects.filter(godown_id=godown, product_id=product_id).count() > 0 :
                    if GodownProduct.objects.get(godown_id=godown, product_id=product_id).quantity >= quantity :
                        GodownProduct.objects.filter(godown_id=godown,product_id=product_id).update(
                        quantity=F("quantity") - quantity)
                    elif GodownProduct.objects.get(godown_id=godown, product_id=product_id).quantity < quantity:
                        messages.success(request, "Insufficient stock !!! Available Quantity:"+str(
                            GodownProduct.objects.get(godown_id=godown, product_id=product_id).quantity))
                        return redirect('/add_product_details/' + str(purchase_id))
            else:
                messages.success(request, "Selected Product does not exist in selected godown !!!")
        item.save()
        new_transaction = GodownTransactions()
        new_transaction.purchase_product_id = Product_Details.objects.get(id=item.id)
        new_transaction.purchase_quantity = quantity
        new_transaction.notes = 'Product Added to Sales by Emp id:' + str(request.user.employee_number) + ', Name' + str(request.user.profile_name) + ', Contact:-' + str(request.user.mobile)+ ', Purchase Product Id: ' + str(item.pk)
        new_transaction.save()




        if is_last_product_yes == 'yes':
            Purchase_Details.objects.filter(id=id).update(is_last_product=True)

            product_list = ''' '''
            pro_lis=  Product_Details.objects.filter(purchase_id_id=purchase_id)

            for idx,item in enumerate(pro_lis):
                # for it in item:

                email_body_text = (
                    u"\nSr. No.: {},"
                    "\tModel: {},"
                    "\tSub Model: {}"
                    "\tbrand: {}"
                    "\tcapacity: {}"
                    "\tCost: {}"

                ).format(
                    idx+1,
                    item.type_of_scale,
                    item.sub_model,
                    item.brand,
                    item.capacity,
                    item.amount,
                )
                product_list=product_list+''+ str(email_body_text)


            try:

                import smtplib



                sent_from = settings.EMAIL_HOST_USER
                to = [purchase.company_email]
                subject = 'Your HSCo Purchase'

                message= 'Dear ' + str(
                    purchase.second_person) + ',' \
                         ' Thank you for purchasing from HSCo, Your Purchase ID is ' + str(
                purchase.purchase_no) + '.' \
                         ' We will love to hear your feedback to help us improve' \
                       ' our customer experience. Please click on the link' \
                         ' below: <br> http://139.59.76.87/feedback_purchase/' + str(request.user.pk) + '/' + str(
                purchase.crm_no.pk) + '/' + str(
                purchase.id) + '<br> For more details contact us on - 7045922250 <br> Order Details:<br>     '+ product_list




                body = message

                email_text = """\
               
                %s
                """ % (body)

                try:
                    email_send = EmailMessage('Dispatched, Your Hsco Purchase is Dispatched from our end',
                                              user(request, email_text),
                                              settings.EMAIL_HOST_USER, to )
                    email_send.content_subtype = 'html'
                    email_send.send()
                    # server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                    # server.ehlo()
                    # server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
                    # server.sendmail(sent_from, to, email_text)
                    # server.close()

                    print('Email sent!')
                except:
                    print('Something went wrong...Email not send!!!')


            except:
                print("exception occured!!")
                pass


            message = 'Dear ' + str(
                purchase.second_person) + ',' \
                                          ' Thank you for purchasing from HSCo, Your Purchase ID is ' + str(
                purchase.purchase_no) + '.' \
                                        ' We will love to hear your feedback to help us improve' \
                                        ' our customer experience. Please click on the link' \
                                        ' below: \n http://139.59.76.87/feedback_purchase/' + str(
                request.user.pk) + '/' + str(
                purchase.crm_no.pk) + '/' + str(
                purchase.id) + '\n For more details contact us on - 7045922250'

            url = "http://smshorizon.co.in/api/sendsms.php?user=" + settings.user + "&apikey=" + settings.api + "&mobile=" + purchase.second_contact_no + "&message=" + message + "&senderid=" + settings.senderid + "&type=txt"
            payload = ""
            headers = {'content-type': 'application/x-www-form-urlencoded'}

            response = requests.request("GET", url, data=json.dumps(payload), headers=headers)
            x = response.text
            print(x)

        Purchase_Details.objects.filter(id=purchase_id).update(value_of_goods=F("value_of_goods") + value_of_goods)
        if purchase.is_gst == True:
            Purchase_Details.objects.filter(id=purchase_id).update(tax_amount=(F("value_of_goods")+F("total_pf")) * 0.18)
        Purchase_Details.objects.filter(id=purchase_id).update(total_amount=F("value_of_goods") + F("tax_amount") + F("total_pf"))

        # if Employee_Analysis_date.objects.filter(Q(entry_date=datetime.now().date()),Q(year=datetime.now.year()),
        #                                          Q(user_id=SiteUser.objects.get(id=request.user.pk))).count() > 0:
        #     Employee_Analysis_date.objects.filter(user_id=purchase.user_id,
        #                                           entry_date=datetime.now().date(),
        #                                           year=datetime.now().year).update(
        #         total_sales_done_today=F("total_sales_done_today") + value_of_goods)
        #     # ead.total_sales_done_today=.filter(category_id_id=id).update(total_views=F("total_views") + value_of_goods)

        #     # ead.save(update_fields=['total_sales_done_today'])

        # else:
        #     ead = Employee_Analysis_date()
        #     ead.user_id = SiteUser.objects.get(id=request.user.pk)
        #     ead.total_sales_done_today = value_of_goods
        #     ead.manager_id = SiteUser.objects.get(id=request.user.pk).group

        #     ead.month = datetime.now().month
        #     ead.year = datetime.now().year
        #     ead.save()


        # if Employee_Analysis_month.objects.filter(Q(entry_date__month=datetime.now().month),Q(year=datetime.now.year()),
        #                                           Q(user_id=SiteUser.objects.get(id=request.user.pk))).count() > 0:
        #     if Employee_Analysis_month.objects.get(user_id=purchase.user_id,
        #                                            entry_date__month=datetime.now().month,
        #                                            year=datetime.now().year).total_sales_done == None:
        #         Employee_Analysis_month.objects.filter(user_id=purchase.user_id,
        #                                                entry_date__month=datetime.now().month,
        #                                                year=datetime.now().year).update(
        #             total_sales_done=0)
        #     Employee_Analysis_month.objects.filter(user_id=purchase.user_id,
        #                                            entry_date__month=datetime.now().month,
        #                                            year=datetime.now().year).update(
        #         total_sales_done=F("total_sales_done") + value_of_goods)


        # else:
        #     ead = Employee_Analysis_month()
        #     ead.user_id = SiteUser.objects.get(id=request.user.pk)
        #     ead.total_sales_done = value_of_goods
        #     ead.manager_id = SiteUser.objects.get(id=request.user.pk).group

        #     ead.month = datetime.now().month
        #     ead.year = datetime.now().year
        #     ead.save()

        # Employee_Analysis_month.objects.filter(user_id=purchase.user_id,
        #                                        entry_date__month=datetime.now().month,
        #                                        year=datetime.now().year).update(
        #     total_sales_done=F("total_sales_done") + value_of_goods)
        #
        # Employee_Analysis_date.objects.filter(user_id=purchase.user_id,
        #                                       entry_date=datetime.now().date(),
        #                                       year=datetime.now().year).update(
        #     total_sales_done_today=F("total_sales_done_today") + value_of_goods)


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
            # dispatch_pro.model_of_purchase = model_of_purchase
            # dispatch_pro.sub_model = sub_model
            # dispatch_pro.sub_sub_model = sub_sub_model
            dispatch_pro.serial_no_scale = serial_no_scale
            dispatch_pro.brand = brand
            dispatch_pro.capacity = capacity
            dispatch_pro.unit = unit
            dispatch_pro.dispatch_id = dispatch_id
            dispatch_pro.value_of_goods = value_of_goods
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
        if is_last_product_yes == 'yes':
            return redirect('/update_customer_details/'+str(purchase_id))
        elif is_last_product_yes == 'no':
            return redirect('/add_product_details/'+str(purchase_id))



    try:
        default_godown = Godown.objects.get(default_godown_purchase=True)
        context1={
            'default_godown': default_godown,
        }
        context.update(context1)
    except:
        pass
    return render(request,'dashboardnew/add_product.html',context)


@login_required(login_url='/')
def report(request):
    if request.method =='POST':
        selected_purchase_list = request.POST.getlist('checks[]')
        selected_product_list = request.POST.getlist('products[]')
        selected_customer_list = request.POST.getlist('customer[]')
        payment_details = request.POST.get('payment_details')

        start_date = request.POST.get('date1')
        end_date = request.POST.get('date2')
        string = ','.join(selected_purchase_list)
        string_product = ','.join(selected_product_list)


        request.session['start_date'] = start_date
        request.session['end_date'] = end_date
        request.session['string'] = selected_purchase_list
        request.session['string_product'] = selected_product_list
        request.session['selected_list'] = selected_purchase_list
        request.session['selected_product_list'] = selected_product_list
        request.session['selected_customer_list'] = selected_customer_list
        request.session['payment_details'] = payment_details
        return redirect('/final_report/')
    return render(request,"report/report_cust_mod_form.html",)


@login_required(login_url='/')
def final_report(request):
    start_date = request.session.get('start_date')
    end_date = request.session.get('end_date')
    string_purchase = request.session.get('string') + ['crm_no_id'] + ['id']
    string_product = request.session.get('string_product')  + ['id'] + ['purchase_id']

    selected_customer_list = request.session.get('selected_customer_list')
    selected_list = request.session.get('selected_list') + ['crm_no_id']
    selected_product_list = request.session.get('selected_product_list') + ['Purchase ID']
    payment_details = request.session.get('payment_details')
    print('payment details')
    print(payment_details)
    final_row_product = []
    final_row = []

    for n, i in enumerate(selected_list):
        if i == 'purchase_app_purchase_details.id':
            selected_list[n] = 'Purchase ID'
        if i == 'customer_app_customer_details.id':
            selected_list[n] = 'Customer No'
        if i == 'today_date':
            selected_list[n] = 'Entry Date'
        if i == 'second_person':
            selected_list[n] = 'Customer Name'

    product_query = Product_Details.objects.filter(entry_timedate__range=(start_date, end_date)).values(*string_product)
    for product in product_query:
        sales_query = Purchase_Details.objects.filter(id=product['purchase_id']).values(*string_purchase)
        
        print(sales_query)
        try:
            if selected_customer_list:
                customer_query = Customer_Details.objects.filter(id=list(sales_query)[0]['crm_no_id']).values(*selected_customer_list)
                for item in customer_query:
                    product.update(item)
        except:
            print('no customer error')
            pass
        
        for item in sales_query:
            #payment details in sales report
            if payment_details != 'None':
                sale = Purchase_Details.objects.get(id=product['purchase_id'])
                if sale.payment_mode == 'Cash' or sale.payment_mode == 'Razorpay':
                    item['payment_mode'] = sale.payment_mode
                elif sale.payment_mode == 'Credit':
                    item['payment_mode'] = sale.payment_mode
                    item['credit_authorised_by'] = 'Authorised by: '+str(sale.credit_authorised_by)
                    item['credit_pending_amount'] = 'Pending Amount: '+str(sale.credit_pending_amount)
                elif sale.payment_mode == 'Cheque':
                    item['payment_mode'] = sale.payment_mode
                    item['bank_name'] = 'Bank Name: '+str(sale.bank_name)
                    item['cheque_no'] = 'Cheque No: '+str(sale.cheque_no)
                    item['cheque_date'] = 'Cheque Date: '+str(sale.cheque_date)
                elif sale.payment_mode == 'NEFT':
                    item['payment_mode'] = sale.payment_mode
                    item['neft_bank_name'] = 'Bank Name: '+str(sale.neft_bank_name)
                    item['neft_date'] = 'NEFT Date: '+str(sale.neft_date)
                    item['reference_no'] = 'Reference No: '+str(sale.reference_no)
            print(item)
            print('entry_timedate' in item)
            product.update(item)
        
        # print(product['id'])
        # print(Product_Details.objects.filter(id=product['id']).values('entry_timedate'))
        # for item in Product_Details.objects.filter(id=product['id']).values('entry_timedate'):
        #     product['entry_timedate'] = item['entry_timedate']
        # product['sales'] = sales_query

        # product['sales_customer'] = customer_query

    # with connection.cursor() as cursor:
    #     if string != '' and string_product != '':
    #
    #             cursor.execute("SELECT " + (string_product +","+ string) + " from purchase_app_product_details  PRODUCT , purchase_app_purchase_details "
    #              "REP , customer_app_customer_details CRM where PRODUCT.purchase_id_id = REP.id and REP.crm_no_id = CRM.id and "
    #             " PRODUCT.entry_timedate between'" + start_date + "' and '" + end_date + "';")
    #             row = cursor.fetchall()
    #             final_row_product = [list(x) for x in row]
    #             repairing_data = []
    #             for i in row:
    #                 repairing_data.append(list(i))
    #
    #             final_row = [list(x) for x in row]
    #             repairing_data = []
    #             for i in row:
    #                 repairing_data.append(list(i))

    # with connection.cursor() as cursor:
    #     if string!='':
    #         cursor.execute("SELECT  "+string+" from purchase_app_purchase_details , customer_app_customer_details"
    #                                 "  where purchase_app_purchase_details.crm_no_id = customer_app_customer_details.id and entry_timedate between '"+start_date+"' and '"+end_date+"';")
    #         row = cursor.fetchall()
    #
    #
    #         final_row= [list(x) for x in row]
    #         list3=[]
    #         for i in row:
    #             list3.append(list(i))
    #
    #     if string_product!='':
    #         cursor.execute("SELECT  " + (string_product) + " from purchase_app_product_details PRODUCT, purchase_app_purchase_details PURCHASE"
    #                                              "  where PRODUCT.purchase_id_id = PURCHASE.id and PRODUCT.entry_timedate between '" + start_date + "' and '" + end_date + "';")
    #         row = cursor.fetchall()
    #
    #         final_row_product = [list(x) for x in row]
    #         list3 = []
    #         for i in row:
    #             list3.append(list(i))

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
        'selected_product_list':selected_product_list+selected_list,
        'sales_query':product_query,
    }
    return render(request,"dashboardnew/final_report.html",context)


@login_required(login_url='/')
def manager_report(request) :
    employee_list = SiteUser.objects.all()
    context={
        'employee_list':employee_list,
    }
    return render(request, 'dashboardnew/manager_report.html',context)

# @login_required(login_url='/')
def feedbacka(request):
    return render(request, 'feedback/feedbacka.html')

@login_required(login_url='/')
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
    return render(request, 'analytics/purchase_analytics_new.html',context)

# @login_required(login_url='/')
def customer_employee_sales_graph(request,user_id):
    #x=Employee_Analysis_date.objects.annotate(date=TruncMonth('entry_timedate')).values('date').annotate(c=Count('id')).values('date', 'c')
    #print(x)

    feeback = Feedback.objects.filter(user_id=user_id)
    #this month sales
    knowledge_of_person = Feedback.objects.filter(user_id=user_id).aggregate(Avg('knowledge_of_person'))
    timeliness_of_person = Feedback.objects.filter(user_id=user_id).aggregate(Avg('timeliness_of_person'))
    price_of_product = Feedback.objects.filter(user_id=user_id).aggregate(Avg('price_of_product'))
    overall_interaction = Feedback.objects.filter(user_id=user_id).aggregate(Avg('overall_interaction'))




    mon = datetime.now().month

    # this_month = Employee_Analysis_date.objects.filter(user_id=user_id,entry_date__month=mon).values('entry_date',
    #                                                                                                      'total_sales_done_today').order_by('entry_date')
    this_month = Purchase_Details.objects.filter(sales_person=SiteUser.objects.get(id=user_id).profile_name,entry_timedate__month=datetime.now().month)\
        .values('entry_timedate').annotate(data_sum=Sum('value_of_goods'))
    this_lis_date = []
    this_lis_sum = []
    for i in this_month:
        x = i
        this_lis_date.append(x['entry_timedate'].strftime('%Y-%m-%d'))
        this_lis_sum.append(x['data_sum'])

    #previous month sales
    mon = (datetime.now().month)
    if mon == 1:
        previous_mon = 12
    else:
        previous_mon = (datetime.now().month) - 1
    previous_month = Purchase_Details.objects.filter(sales_person=SiteUser.objects.get(id=user_id).profile_name,entry_timedate__month=previous_mon)\
        .values('entry_timedate').annotate(data_sum=Sum('value_of_goods'))
    previous_lis_date = []
    previous_lis_sum = []
    for i in previous_month:
        x = i
        previous_lis_date.append(x['entry_timedate'].strftime('%Y-%m-%d'))
        previous_lis_sum.append(x['data_sum'])

    if request.method=='POST' and 'date1' in request.POST :
        start_date = request.POST.get('date1')
        end_date = request.POST.get('date2')

        qs = Purchase_Details.objects.filter(sales_person=SiteUser.objects.get(id=user_id).profile_name,entry_timedate__range=(start_date, end_date))\
        .values('entry_timedate').annotate(data_sum=Sum('value_of_goods'))
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
            'feeback': feeback,

        }
        try:
            knowledge_of_person_avg = round(knowledge_of_person['knowledge_of_person__avg'])
            timeliness_of_person_avg = round(timeliness_of_person['timeliness_of_person__avg'])
            overall_interaction_avg = round(overall_interaction['overall_interaction__avg'])
            price_of_product_avg = round(price_of_product['price_of_product__avg'])
            context23 = {
                'knowledge_of_person_avg': knowledge_of_person_avg,
                'timeliness_of_person_avg': timeliness_of_person_avg,
                'price_of_product_avg': price_of_product_avg,
                'overall_interaction_avg': overall_interaction_avg,
            }
            context.update(context23)
        except:
            pass
        return render(request, "graphs/sales_graph2.html", context)
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

        qs = Purchase_Details.objects.filter(sales_person=SiteUser.objects.get(id=user_id).profile_name,entry_timedate__month=datetime.now().month)\
        .values('entry_timedate').annotate(data_sum=Sum('value_of_goods'))
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
            'feeback': feeback,

        }
        try:
            knowledge_of_person_avg = round(knowledge_of_person['knowledge_of_person__avg'])
            timeliness_of_person_avg = round(timeliness_of_person['timeliness_of_person__avg'])
            overall_interaction_avg = round(overall_interaction['overall_interaction__avg'])
            price_of_product_avg = round(price_of_product['price_of_product__avg'])
            context2 = {
                'knowledge_of_person_avg': knowledge_of_person_avg,
                'timeliness_of_person_avg': timeliness_of_person_avg,
                'price_of_product_avg': price_of_product_avg,
                'overall_interaction_avg': overall_interaction_avg,
            }
            context.update(context2)
        except:
            pass
        return render(request,"graphs/sales_graph2.html",context)

# @login_required(login_url='/')
def feedback_purchase(request,user_id,customer_id,purchase_id):
    feedback_form = Feedback_Form(request.POST or None, request.FILES or None)
    if Purchase_Details.objects.get(id=purchase_id).feedback_form_filled:
        return HttpResponse('Feedback Already Submitted.')
    else:
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



@login_required(login_url='/')
def load_users(request):


    selected = request.GET.get('loc_id')
    sel_month = request.GET.get('sel_month')
    sel_year = request.GET.get('sel_year')
    sel_month_text = request.GET.get('sel_month_text')

    if selected=='true':
        if (sel_month == 0 or sel_month == 'true'):
            current_month = datetime.now().month
            current_year = datetime.now().year
            user_list = Employee_Analysis_month.objects.filter(entry_date__month=current_month,
                                                               entry_date__year=current_year,
                                                               manager_id__icontains=request.user.name,
                                                               user_id__is_deleted=False,
                                                               user_id__modules_assigned__icontains='Customer Module')
            if (user_list.count() == 0):
                error_exist_225 = True
                success_exist_225 = False
            else:
                error_exist_225 = False
                success_exist_225 = True
            context = {

                'error_exist_225': error_exist_225,
                'success_exist_225': success_exist_225,
                'error_msg_225': 'Select Valid Month And Year\n Showing Results For Current Month and Year.',
                'user_list': user_list,
                'manager': True,

            }


        else:
            current_month = sel_month
            current_year = sel_year

            user_list = Employee_Analysis_month.objects.filter(entry_date__month=current_month,
                                                               entry_date__year=current_year,
                                                               manager_id__icontains=request.user.name,
                                                               user_id__is_deleted=False,
                                                               user_id__modules_assigned__icontains='Customer Module')
            if(user_list.count() == 0):
                error_exist_225 = True
                success_exist_225 = False
            else:
                error_exist_225 = False
                success_exist_225 = True
            if(sel_month_text == 'Select Month'):
                error_msg_225 = 'Select Valid Month And Year'
            else:
                error_msg_225 = 'Result Not Found For ' + sel_month_text + ', ' + current_year



            context = {
                'error_exist_225': error_exist_225,
                'success_exist_225': success_exist_225,
                'success_msg_225': 'Results For ' + sel_month_text + ', ' + current_year,
                'error_msg_225': error_msg_225,
                'user_list': user_list,
                'manager': True,
            }

        return render(request, 'AJAX/load_users.html', context)
    else:
        if check_admin_roles(request):  # For ADMIN
            cust_list = Purchase_Details.objects.filter(
                Q(user_id__name=request.user.name) | Q(user_id__group__icontains=request.user.name),
                user_id__is_deleted=False, user_id__modules_assigned__icontains='Customer Module').order_by('-purchase_no')
        else:  # For EMPLOYEE
            cust_list = Purchase_Details.objects.filter(user_id=request.user.pk).order_by('-purchase_no')

        context = {
            'customer_list': cust_list,
            'manager': False,
        }

        return render(request, 'AJAX/load_users.html', context)

@login_required(login_url='/')
def check_admin_roles(request):
    if request.user.role == 'Super Admin' or request.user.role == 'Admin' or request.user.role == 'Manager':
        return True
    else:
        return False



@login_required(login_url='/')
def purchase_logs(request):
    purchase_logs = Log.objects.filter(module_name='Purchase Module').order_by('-id')
    paginator = Paginator(purchase_logs, 15)  # Show 25 contacts per page
    page = request.GET.get('page')
    purchase_logs = paginator.get_page(page)
    context={
    'purchase_logs': purchase_logs,

    }
    return render(request,"logs/purchase_logs.html",context)

def stock_does_not_exist(request):
    model_of_purchase = request.GET.get('model_of_purchase')
    type_of_scale = request.GET.get('type_of_scale')
    sub_model = request.GET.get('sub_model')
    sub_sub_model = request.GET.get('sub_sub_model')
    product_id = request.GET.get('product_id')

    godown = request.GET.get('godown')
    quantity =request.GET.get('quantity')
    godown = Godown.objects.get(id=godown)
    # print('stock')
    # print(request.GET)
    # print(model_of_purchase)
    # print(type_of_scale)
    # print(sub_model)
    # print(sub_sub_model)
    # print(quantity)
    quantity = float(quantity) if quantity != '' and quantity != None else 0
    context = {}
    if 'product_id' in request.GET:
        product_id = Product.objects.get(id=product_id)
        print(product_id)
    else:
        if sub_sub_model != '':
            product_id = Product.objects.get(scale_type__name=type_of_scale, main_category__name=model_of_purchase,
                                            sub_category__name=sub_model, sub_sub_category__name=sub_sub_model)
        elif sub_model != '':
            product_id = Product.objects.get(scale_type__name=type_of_scale, main_category__name=model_of_purchase,
                                            sub_category__name=sub_model, sub_sub_category__name=None)
    if GodownProduct.objects.filter(godown_id=godown, product_id=product_id).count() > 0:
        godown_product_quantity = GodownProduct.objects.get(godown_id=godown, product_id=product_id).quantity
        godown_product_critical_limit = GodownProduct.objects.get(godown_id=godown, product_id=product_id).critical_limit
        if quantity > godown_product_quantity:
            error1 = 'Insufficient Stock !!! Available Quantity:' + str(godown_product_quantity)
            context1 = {
                'error1_msg':error1,
                'error1':True,
            }
            context.update(context1)
        elif godown_product_quantity <= godown_product_critical_limit and quantity <= godown_product_quantity:
            error3 = 'Stock Below Critical Limit !!! Available Quantity:' + str(godown_product_quantity)
            context4 = {
                'error3_msg': error3,
                'error3': True,
            }
            context.update(context4)
        elif godown_product_quantity > godown_product_critical_limit and quantity <= godown_product_quantity:
            success_message = 'Stock Available !!! Available Quantity:' + str(godown_product_quantity)
            context4 = {
                'success_message': success_message,
                'success': True,
            }
            context.update(context4)



    else:
        error4 = 'Selected product does not exist in the selected godown !!!'
        context4 = {
            'error4_msg': error4,
            'error4': True,
        }
        context.update(context4)
    return render(request, 'AJAX/stock_does_not_exist.html',context)

def get_product_details(request):
    model_of_purchase = request.GET.get('model_of_purchase')
    type_of_scale = request.GET.get('type_of_scale')
    sub_model_var = request.GET.get('sub_model')
    sub_sub_model_var = request.GET.get('sub_sub_model')


    context={}

    if sub_sub_model_var != '' and sub_sub_model_var != None  and sub_model_var != 'None':
        sub_sub_model_var = sub_sub_model.objects.filter(id=sub_sub_model_var).first()

        product_id = Product.objects.get(scale_type__name=type_of_scale, main_category__name=model_of_purchase,
                                         sub_category__name=sub_model_var, sub_sub_category__name=sub_sub_model_var)
        context1={
            'product_id' : product_id,
        }
        context.update(context1)
    elif sub_model_var != '' and sub_model_var != None  and sub_model_var != 'None':
        sub_model_var = sub_model.objects.filter(id=sub_model_var).first()

        product_id = Product.objects.get(scale_type__name=type_of_scale, main_category__name=model_of_purchase,
                                         sub_category__name=sub_model_var, sub_sub_category__name=None)
        context2={
            'product_id' : product_id,
        }
        context.update(context2)
    return render(request, 'AJAX/get_product_details.html',context)


def return_product(type_of_scale,model_of_purchase,sub_model,sub_sub_model):
    pro_obj = Product.objects.get(scale_type=type_of_scale,
                        main_category=model_of_purchase,
                        sub_category=sub_model,
                        sub_sub_category=sub_sub_model)
    return pro_obj

def return_product_sub_model(type_of_scale,model_of_purchase,sub_model):
    pro_obj = Product.objects.get(scale_type=type_of_scale,
                        main_category=model_of_purchase,
                        sub_category=sub_model)
    return pro_obj

def return_godown_pro(godown_id,product):
    godown_pro = GodownProduct.objects.filter(godown_id=godown_id, product_id=product)
    return godown_pro

def autocomplete(request):
    if request.is_ajax():
        queryset = Customer_Details.objects.filter(customer_name__startswith=request.GET.get('search', None))
        print(queryset)
        print(queryset)
        print(queryset)
        list = []
        for i in queryset:
            list.append(i.customer_name)
        data = {
            'list': list,
        }
        return JsonResponse(data)




























