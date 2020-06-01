from datetime import datetime
from email.mime.text import MIMEText
from io import BytesIO

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.paginator import Paginator
from django.db import connection
from django.db.models import Sum, Q, Count, Min, F
from django.core.files.base import ContentFile, File
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect
from customer_app.models import type_purchase
from django.template.loader import get_template
from stock_management_system_app.models import Product
from django.contrib.auth.decorators import login_required

from Hsco import settings
from user_app.models import SiteUser
from customer_app.models import Log


from lead_management.email_content import user
from .forms import Deal_detailForm, Customer_detailForm, Pi_sectionForm, Follow_up_sectionForm, History_followupForm, Payment_detailsForm
from .form2 import Customer_detail_disabledForm
from customer_app.models import Customer_Details, Lead_Customer_Details
from .models import Lead, Pi_section, IndiamartLeadDetails, History_followup, Follow_up_section, Followup_product, \
    Auto_followup_details, Payment_details
from .models import Lead, Pi_section, Pi_product, Pi_History
from customer_app.models import sub_model, main_model, sub_sub_model
import requests
import json
from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from .utils import send_html_mail, send_text_mail
from purchase_app.models import Purchase_Details
from dispatch_app.models import Dispatch
from purchase_app.models import Product_Details
from dispatch_app.models import Product_Details_Dispatch
from django.core.mail import EmailMessage
from django.contrib import messages
from django.core.mail import get_connection
from django.core.mail.message import EmailMessage

from stock_management_system_app.models import Godown,GodownProduct

today_month = datetime.now().month

@login_required(login_url='/')
def lead_home(request):
    import requests
    import json

    mobile = '7045922250'
    api = 'MTU4MzQ5OTg1NS42MTU2IzI5OTI4NzM='
    last_date = IndiamartLeadDetails.objects.latest('to_date').to_date.strftime('%d-%b-%Y')
    from_date = last_date
    from datetime import datetime
    to_date = datetime.today().strftime('%d-%b-%Y')
    lead_count=0
    error2 = None
    error = None
    error_exist = False
    context={}
    response = None
    admin = SiteUser.objects.get(id=request.user.pk).admin

    if request.user.role == 'Super Admin':  # For SUPER ADMIN
        lead_list = Lead.objects.filter(Q(entry_timedate__month=today_month)).order_by('-id')
        # paginator = Paginator(lead_list, 200)  # Show 25 contacts per page
        # page = request.GET.get('page')
        # lead_list = paginator.get_page(page)
    elif request.user.role == 'Admin':  # For ADMIN
        lead_list = Lead.objects.filter((Q(owner_of_opportunity__profile_name=request.user.profile_name)& Q(entry_timedate__month=today_month)) | (Q(owner_of_opportunity__admin__icontains=request.user.profile_name)& Q(entry_timedate__month=today_month))).order_by('-id')
        # paginator = Paginator(lead_list, 200)  # Show 25 contacts per page
        # page = request.GET.get('page')
        # lead_list = paginator.get_page(page)
    elif request.user.role == 'Manager':  # For manager
        lead_list = Lead.objects.filter((Q(owner_of_opportunity__profile_name=request.user.profile_name)& Q(entry_timedate__month=today_month)) | (Q(owner_of_opportunity__manager__icontains=request.user.profile_name)& Q(entry_timedate__month=today_month))).order_by('-id')
        # paginator = Paginator(lead_list, 200)  # Show 25 contacts per page
        # page = request.GET.get('page')
        # lead_list = paginator.get_page(page)
    elif request.user.role == 'Employee': #for employee
        lead_list = Lead.objects.filter(Q(owner_of_opportunity__profile_name=request.user.profile_name)& Q(entry_timedate__month=today_month)).order_by('-id')
        # paginator = Paginator(lead_list, 200)  # Show 25 contacts per page
        # page = request.GET.get('page')
        # lead_list = paginator.get_page(page)
    cust_sugg = Lead_Customer_Details.objects.all()

    context23 = {
        'lead_list': lead_list,
        'lead_count': lead_count,
        'from_date': from_date,
        'to_date': to_date,
        'error': error,
        'error2': error2,
        'error_exist': error_exist,
        'cust_sugg': cust_sugg,
    }
    context.update(context23)
    if request.user.role == 'Super Admin':
        total_stages = Lead.objects.all().values('current_stage').annotate(dcount=Count('current_stage'))
    elif request.user.role == 'Admin':  # For ADMIN
        total_stages = Lead.objects.filter(Q(owner_of_opportunity__profile_name=request.user.profile_name) |  Q(owner_of_opportunity__admin__icontains=request.user.profile_name)).values('current_stage').annotate(dcount=Count('current_stage'))
    elif request.user.role == 'Manager':  # For manager
        total_stages = Lead.objects.filter(Q(owner_of_opportunity__profile_name=request.user.profile_name) | Q(owner_of_opportunity__manager__icontains=request.user.profile_name)).values('current_stage').annotate(dcount=Count('current_stage'))

    else: #for employee
        total_stages = Lead.objects.filter(Q(owner_of_opportunity__profile_name=request.user.profile_name)).values('current_stage').annotate(dcount=Count('current_stage'))

    admin = SiteUser.objects.get(id=request.user.pk).admin
    # lead = Pi_section.objects.filter(lead_id=Lead.objects.filter(Q(owner_of_opportunity__admin=admin)))

    superadmin_pi = Pi_section.objects.filter(Q(lead_id__current_stage='PO Issued - Payment not done'))
    admin_pi = Pi_section.objects.filter(Q(lead_id__current_stage='PO Issued - Payment not done')|
      Q(lead_id__owner_of_opportunity__profile_name=request.user.profile_name) |Q(lead_id__owner_of_opportunity__admin__icontains=request.user.profile_name) )
    manager_pi = Pi_section.objects.filter(Q(lead_id__current_stage='PO Issued - Payment not done')|
      Q(lead_id__owner_of_opportunity__profile_name=request.user.profile_name) |Q(lead_id__owner_of_opportunity__manager__icontains=request.user.profile_name))
    employee_pi = Pi_section.objects.filter(Q(lead_id__current_stage='PO Issued - Payment not done')|
      Q(lead_id__owner_of_opportunity__profile_name=request.user.profile_name) )
    if request.user.role == 'Super Admin':
        po_no_payment = Pi_section.objects.filter(Q(lead_id__current_stage='PO Issued - Payment not done')).values(
            'grand_total').annotate(data_sum=Sum('grand_total'))
        po_no_payment_total = 0.0
        try:
            for x in po_no_payment:
                po_no_payment_total += float(x['data_sum'])
        except:
            pass

        po_payment_done = Pi_section.objects.filter(Q(lead_id__current_stage='PO Issued - Payment Done - Dispatch Pending')).values(
            'grand_total').annotate(data_sum=Sum('grand_total'))
        po_payment_done_total = 0.0
        try:
            for x in po_payment_done:
                po_payment_done_total += float(x['data_sum'])
        except:
            pass

        dispatch_done_stage = Pi_section.objects.filter(Q(lead_id__current_stage='Dispatch Done - Closed')).values(
            'grand_total').annotate(data_sum=Sum('grand_total'))
        dispatch_done_stage_total = 0.0
        try:
            for x in dispatch_done_stage:
                dispatch_done_stage_total += float(x['data_sum'])
        except:
            pass
        lost_stage = Pi_section.objects.filter(Q(lead_id__current_stage='Lost')).values(
            'grand_total').annotate(data_sum=Sum('grand_total'))
        lost_stage_total = 0.0
        try:
            for x in lost_stage:
                lost_stage_total += float(x['data_sum'])
        except:
            pass
        not_relevant_stage = Pi_section.objects.filter(Q(lead_id__current_stage='Not Relevant')).values(
            'grand_total').annotate(data_sum=Sum('grand_total'))
        not_relevant_stage_total = 0.0
        try:
            for x in not_relevant_stage:
                not_relevant_stage_total += float(x['data_sum'])
        except:
            pass
        postponed_stage = Pi_section.objects.filter(Q(lead_id__current_stage='Postponed')).values(
            'grand_total').annotate(data_sum=Sum('grand_total'))
        postponed_stage_total = 0.0
        try:
            for x in postponed_stage:
                postponed_stage_total += float(x['data_sum'])
        except:
            pass
        pi_sent_stage = Pi_section.objects.filter(Q(lead_id__current_stage='PI Sent & Follow-up')).values(
            'grand_total').annotate(data_sum=Sum('grand_total'))
        pi_sent_stage_total = 0.0
        try:
            for x in pi_sent_stage:
                pi_sent_stage_total += float(x['data_sum'])
        except:
            pass
        context13={
            'po_no_payment_total': po_no_payment_total,
            'lost_stage_total': lost_stage_total,
            'po_payment_done_total': po_payment_done_total,
            'dispatch_done_stage_total': dispatch_done_stage_total,
            'not_relevant_stage_total': not_relevant_stage_total,
            'postponed_stage_total': postponed_stage_total,
            'pi_sent_stage_total': pi_sent_stage_total,
        }
        context.update(context13)
    elif request.user.role == 'Admin':
        po_no_payment = Pi_section.objects.filter(Q(lead_id__current_stage='PO Issued - Payment not done')&(Q(lead_id__owner_of_opportunity__profile_name=request.user.profile_name) |Q(lead_id__owner_of_opportunity__admin__icontains=request.user.profile_name))).values(
            'grand_total').annotate(data_sum=Sum('grand_total'))
        po_no_payment_total = 0.0
        try:
            for x in po_no_payment:
                po_no_payment_total += float(x['data_sum'])
        except:
            pass

        po_payment_done = Pi_section.objects.filter(Q(lead_id__current_stage='PO Issued - Payment Done - Dispatch Pending')&(Q(lead_id__owner_of_opportunity__profile_name=request.user.profile_name) |Q(lead_id__owner_of_opportunity__admin__icontains=request.user.profile_name))).values(
            'grand_total').annotate(data_sum=Sum('grand_total'))
        po_payment_done_total = 0.0
        try:
            for x in po_payment_done:
                po_payment_done_total += float(x['data_sum'])
        except:
            pass

        dispatch_done_stage = Pi_section.objects.filter(Q(lead_id__current_stage='Dispatch Done - Closed')&(Q(lead_id__owner_of_opportunity__profile_name=request.user.profile_name) |Q(lead_id__owner_of_opportunity__admin__icontains=request.user.profile_name))).values(
            'grand_total').annotate(data_sum=Sum('grand_total'))
        dispatch_done_stage_total = 0.0
        try:
            for x in dispatch_done_stage:
                dispatch_done_stage_total += float(x['data_sum'])
        except:
            pass
        lost_stage = Pi_section.objects.filter(Q(lead_id__current_stage='Lost')&(Q(lead_id__owner_of_opportunity__profile_name=request.user.profile_name) |Q(lead_id__owner_of_opportunity__admin__icontains=request.user.profile_name))).values(
            'grand_total').annotate(data_sum=Sum('grand_total'))
        lost_stage_total = 0.0
        try:
            for x in lost_stage:
                lost_stage_total += float(x['data_sum'])
        except:
            pass
        not_relevant_stage = Pi_section.objects.filter(Q(lead_id__current_stage='Not Relevant')&(Q(lead_id__owner_of_opportunity__profile_name=request.user.profile_name) |Q(lead_id__owner_of_opportunity__admin__icontains=request.user.profile_name))).values(
            'grand_total').annotate(data_sum=Sum('grand_total'))
        not_relevant_stage_total = 0.0
        try:
            for x in not_relevant_stage:
                not_relevant_stage_total += float(x['data_sum'])
        except:
            pass
        postponed_stage = Pi_section.objects.filter(Q(lead_id__current_stage='Postponed')&(Q(lead_id__owner_of_opportunity__profile_name=request.user.profile_name) |Q(lead_id__owner_of_opportunity__admin__icontains=request.user.profile_name))).values(
            'grand_total').annotate(data_sum=Sum('grand_total'))
        postponed_stage_total = 0.0
        try:
            for x in postponed_stage:
                postponed_stage_total += float(x['data_sum'])
        except:
            pass
        pi_sent_stage = Pi_section.objects.filter(Q(lead_id__current_stage='PI Sent & Follow-up')&(Q(lead_id__owner_of_opportunity__profile_name=request.user.profile_name) |Q(lead_id__owner_of_opportunity__admin__icontains=request.user.profile_name))).values(
            'grand_total').annotate(data_sum=Sum('grand_total'))
        pi_sent_stage_total = 0.0
        try:
            for x in pi_sent_stage:
                pi_sent_stage_total += float(x['data_sum'])
        except:
            pass
        context13={
            'po_no_payment_total': po_no_payment_total,
            'lost_stage_total': lost_stage_total,
            'po_payment_done_total': po_payment_done_total,
            'dispatch_done_stage_total': dispatch_done_stage_total,
            'not_relevant_stage_total': not_relevant_stage_total,
            'postponed_stage_total': postponed_stage_total,
            'pi_sent_stage_total': pi_sent_stage_total,
        }
        context.update(context13)
    elif request.user.role == 'Manager':
        po_no_payment = Pi_section.objects.filter(Q(lead_id__current_stage='PO Issued - Payment not done')&(Q(lead_id__owner_of_opportunity__profile_name=request.user.profile_name) |Q(lead_id__owner_of_opportunity__manager__icontains=request.user.profile_name))).values(
            'grand_total').annotate(data_sum=Sum('grand_total'))
        po_no_payment_total = 0.0
        try:
            for x in po_no_payment:
                po_no_payment_total += float(x['data_sum'])
        except:
            pass

        po_payment_done = Pi_section.objects.filter(Q(lead_id__current_stage='PO Issued - Payment Done - Dispatch Pending')&(Q(lead_id__owner_of_opportunity__profile_name=request.user.profile_name) |Q(lead_id__owner_of_opportunity__manager__icontains=request.user.profile_name))).values(
            'grand_total').annotate(data_sum=Sum('grand_total'))
        po_payment_done_total = 0.0
        try:
            for x in po_payment_done:
                po_payment_done_total += float(x['data_sum'])
        except:
            pass

        dispatch_done_stage = Pi_section.objects.filter(Q(lead_id__current_stage='Dispatch Done - Closed')&(Q(lead_id__owner_of_opportunity__profile_name=request.user.profile_name) |Q(lead_id__owner_of_opportunity__manager__icontains=request.user.profile_name))).values(
            'grand_total').annotate(data_sum=Sum('grand_total'))
        dispatch_done_stage_total = 0.0
        try:
            for x in dispatch_done_stage:
                dispatch_done_stage_total += float(x['data_sum'])
        except:
            pass
        lost_stage = Pi_section.objects.filter(Q(lead_id__current_stage='Lost')&(Q(lead_id__owner_of_opportunity__profile_name=request.user.profile_name) |Q(lead_id__owner_of_opportunity__manager__icontains=request.user.profile_name))).values(
            'grand_total').annotate(data_sum=Sum('grand_total'))
        lost_stage_total = 0.0
        try:
            for x in lost_stage:
                lost_stage_total += float(x['data_sum'])
        except:
            pass
        not_relevant_stage = Pi_section.objects.filter(Q(lead_id__current_stage='Not Relevant')&(Q(lead_id__owner_of_opportunity__profile_name=request.user.profile_name) |Q(lead_id__owner_of_opportunity__manager__icontains=request.user.profile_name))).values(
            'grand_total').annotate(data_sum=Sum('grand_total'))
        not_relevant_stage_total = 0.0
        try:
            for x in not_relevant_stage:
                not_relevant_stage_total += float(x['data_sum'])
        except:
            pass
        postponed_stage = Pi_section.objects.filter(Q(lead_id__current_stage='Postponed')&(Q(lead_id__owner_of_opportunity__profile_name=request.user.profile_name) |Q(lead_id__owner_of_opportunity__manager__icontains=request.user.profile_name))).values(
            'grand_total').annotate(data_sum=Sum('grand_total'))
        postponed_stage_total = 0.0
        try:
            for x in postponed_stage:
                postponed_stage_total += float(x['data_sum'])
        except:
            pass
        pi_sent_stage = Pi_section.objects.filter(Q(lead_id__current_stage='PI Sent & Follow-up')&(Q(lead_id__owner_of_opportunity__profile_name=request.user.profile_name) |Q(lead_id__owner_of_opportunity__manager__icontains=request.user.profile_name))).values(
            'grand_total').annotate(data_sum=Sum('grand_total'))
        pi_sent_stage_total = 0.0
        try:
            for x in pi_sent_stage:
                pi_sent_stage_total += float(x['data_sum'])
        except:
            pass
        context13={
            'po_no_payment_total': po_no_payment_total,
            'lost_stage_total': lost_stage_total,
            'po_payment_done_total': po_payment_done_total,
            'dispatch_done_stage_total': dispatch_done_stage_total,
            'not_relevant_stage_total': not_relevant_stage_total,
            'postponed_stage_total': postponed_stage_total,
            'pi_sent_stage_total': pi_sent_stage_total,
        }
        context.update(context13)
    elif request.user.role == 'Employee':
        po_no_payment = Pi_section.objects.filter(Q(lead_id__current_stage='PO Issued - Payment not done')&Q(lead_id__owner_of_opportunity__profile_name=request.user.profile_name)).values(
            'grand_total').annotate(data_sum=Sum('grand_total'))
        po_no_payment_total = 0.0
        try:
            for x in po_no_payment:
                po_no_payment_total += float(x['data_sum'])
        except:
            pass

        po_payment_done = Pi_section.objects.filter(Q(lead_id__current_stage='PO Issued - Payment Done - Dispatch Pending')&Q(lead_id__owner_of_opportunity__profile_name=request.user.profile_name)).values(
            'grand_total').annotate(data_sum=Sum('grand_total'))
        po_payment_done_total = 0.0
        try:
            for x in po_payment_done:
                po_payment_done_total += float(x['data_sum'])
        except:
            pass

        dispatch_done_stage = Pi_section.objects.filter(Q(lead_id__current_stage='Dispatch Done - Closed')&Q(lead_id__owner_of_opportunity__profile_name=request.user.profile_name)).values(
            'grand_total').annotate(data_sum=Sum('grand_total'))
        dispatch_done_stage_total = 0.0
        try:
            for x in dispatch_done_stage:
                dispatch_done_stage_total += float(x['data_sum'])
        except:
            pass
        lost_stage = Pi_section.objects.filter(Q(lead_id__current_stage='Lost')&Q(lead_id__owner_of_opportunity__profile_name=request.user.profile_name)).values(
            'grand_total').annotate(data_sum=Sum('grand_total'))
        lost_stage_total = 0.0
        try:
            for x in lost_stage:
                lost_stage_total += float(x['data_sum'])
        except:
            pass
        not_relevant_stage = Pi_section.objects.filter(Q(lead_id__current_stage='Not Relevant')&Q(lead_id__owner_of_opportunity__profile_name=request.user.profile_name)).values(
            'grand_total').annotate(data_sum=Sum('grand_total'))
        not_relevant_stage_total = 0.0
        try:
            for x in not_relevant_stage:
                not_relevant_stage_total += float(x['data_sum'])
        except:
            pass
        postponed_stage = Pi_section.objects.filter(Q(lead_id__current_stage='Postponed')&Q(lead_id__owner_of_opportunity__profile_name=request.user.profile_name)).values(
            'grand_total').annotate(data_sum=Sum('grand_total'))
        postponed_stage_total = 0.0
        try:
            for x in postponed_stage:
                postponed_stage_total += float(x['data_sum'])
        except:
            pass
        pi_sent_stage = Pi_section.objects.filter(Q(lead_id__current_stage='PI Sent & Follow-up')&Q(lead_id__owner_of_opportunity__profile_name=request.user.profile_name)).values(
            'grand_total').annotate(data_sum=Sum('grand_total'))
        pi_sent_stage_total = 0.0
        try:
            for x in pi_sent_stage:
                pi_sent_stage_total += float(x['data_sum'])
        except:
            pass
        context13={
            'po_no_payment_total': po_no_payment_total,
            'lost_stage_total': lost_stage_total,
            'po_payment_done_total': po_payment_done_total,
            'dispatch_done_stage_total': dispatch_done_stage_total,
            'not_relevant_stage_total': not_relevant_stage_total,
            'postponed_stage_total': postponed_stage_total,
            'pi_sent_stage_total': pi_sent_stage_total,
        }
        context.update(context13)

    for i in total_stages:
        x = i
        if x['current_stage'] == 'Not Yet Initiated':
            not_yet_stage = x['dcount']
            context1 = {
                'not_yet_stage': not_yet_stage,
            }
            context.update(context1)
        if x['current_stage'] == 'Dispatch Done - Closed':
            dispatch_stage = x['dcount']
            context2 = {
                'dispatch_stage': dispatch_stage,
            }
            context.update(context2)
        if x['current_stage'] == 'Customer Called':
            cust_called_stage = x['dcount']
            context3 = {
                'cust_called_stage': cust_called_stage,
            }
            context.update(context3)
        if x['current_stage'] == 'PO Issued - Payment not done':
            po_no_payment = x['dcount']
            context5 = {
                'po_no_payment': po_no_payment,
            }
            context.update(context5)
        if x['current_stage'] == 'PO Issued - Payment Done - Dispatch Pending':
            po_payment_done = x['dcount']
            context4 = {
                'po_payment_done': po_payment_done,
            }
            context.update(context4)
        if x['current_stage'] == 'Lost':
            lost_stage = x['dcount']
            context6 = {
                'lost_stage': lost_stage,
            }
            context.update(context6)
        if x['current_stage'] == 'Not Relevant':
            not_relevant_stage = x['dcount']
            context7 = {
                'not_relevant_stage': not_relevant_stage,
            }
            context.update(context7)
        if x['current_stage'] == 'Postponed':
            postponed_stage = x['dcount']
            context8 = {
                'postponed_stage': postponed_stage,
            }
            context.update(context8)
        if x['current_stage'] == 'PI Sent & Follow-up':
            pi_sent_stage = x['dcount']
            context9 = {
                'pi_sent_stage': pi_sent_stage,
            }
            context.update(context9)
            
    if request.method == 'GET' and 'success' in request.method:
        success = request.GET['success']
        lead_count = request.GET['lead_count']
        if success == 'true':
            context22={
                'err':True,
                'lead_count':lead_count,
            }
        elif success == 'false':
            context22 = {
                'success_exist': False,
                'lead_count': lead_count,
            }
        context.update(context22)



    if request.method == 'POST':
        if 'fetch_lead' in request.POST:

            url = "https://mapi.indiamart.com/wservce/enquiry/listing/GLUSR_MOBILE/" + mobile + "/GLUSR_MOBILE_KEY/" + api + "/Start_Time/" + from_date + "/End_Time/" + to_date + "/"
            response = requests.get(url=url).json()
            lead_count = len(response)

            try:
                if lead_count == 1 and response[0]['Error_Message'] == 'It is advised to hit this API once in every 15 minutes,but it seems that you have crossed this limit. please try again after 15 minutes.':
                    messages.error(request,"Try after 15 minutes.")
                if lead_count == 1 and response[0]['Error_Message'] == 'There are no leads in the given time duration.please try for a different duration.':
                    messages.success(request, "Already Fetched!!!")
            except Exception as e:
                print('str(e)')
                print(str(e))
                pass


            from_date =  request.POST.get('from_date_form')
            to_date =  request.POST.get('to_date_form')
            import time
            try:
                conv = time.strptime(from_date, "%d-%b-%Y")
                conv2 = time.strptime(to_date, "%d-%b-%Y")

            except Exception as e:
                print("ssss"+str(e))
                context23 = {
                    'err2': 'Something Went Wrong!!!',
                }
                context.update(context23)

            if (lead_count > 1 and response != None):
                for item in response:

                    requirement = item['SUBJECT'] + item['ENQ_MESSAGE'] + item['PRODUCT_NAME'] if item[
                                                                                                      'SUBJECT'] != None and \
                                                                                                  item[
                                                                                                      'ENQ_MESSAGE'] != None and \
                                                                                                  item[
                                                                                                      'PRODUCT_NAME'] != None else \
                        item['SUBJECT'] + item['ENQ_MESSAGE'] if item['SUBJECT'] != None and item[
                            'ENQ_MESSAGE'] != None else item['SUBJECT']
                    clean_requirement = requirement.replace('<b>', '\n')[:115]


                    if (item['MOB'] != None and item['MOB'] != '' and len(item['MOB']) > 3):
                        clean_mob = item['MOB'].partition('-')[2]
                    else:
                        clean_mob = item['MOB']

                    if clean_mob!= None and clean_mob!='' and len(clean_mob)>3:
                        pass
                    else:
                        clean_mob = '0000000000'


                    entered_customer_name = item['SENDERNAME']
                    if entered_customer_name == None or entered_customer_name == '':
                        entered_customer_name = 'NA'

                    if Lead.objects.filter(requirement_indiamart_unique=clean_requirement,
                                           customer_id__contact_no=clean_mob,customer_id__customer_name=entered_customer_name,
                                           channel='IndiaMart', indiamart_time=item['DATE_R']).count() == 0:

                        if entered_customer_name == 'NA' and clean_mob == '0000000000' and (item['SENDEREMAIL']== '' or item['SENDEREMAIL'] == None or item['SENDEREMAIL'] == ' '):
                            lead_count = lead_count - 1
                        else:
                            cust_obj = Lead_Customer_Details.objects.filter(customer_name=entered_customer_name,
                                                                       contact_no=clean_mob)
                            if cust_obj.exists() and cust_obj.count() > 0:
                                if item['SENDEREMAIL']== '' and item['SENDEREMAIL'] == None and item['SENDEREMAIL'] == ' ':
                                    cust_obj.update(customer_email_id=item['SENDEREMAIL'])
                                if item['GLUSR_USR_COMPANYNAME']!=None and item['GLUSR_USR_COMPANYNAME']!='':
                                    cust_obj.update(company_name=item['GLUSR_USR_COMPANYNAME'])
                                if item['ENQ_ADDRESS']!=None and item['ENQ_ADDRESS']!='':
                                    cust_obj.update(address=item['ENQ_ADDRESS'])
                                for item23 in cust_obj:
                                    exist_cust = item23.pk
                                item3 = Lead_Customer_Details.objects.get(id=exist_cust)
                                new_existing_customer = 'Existing'
                            else:
                                item3 = Lead_Customer_Details()
                                item3.customer_name = entered_customer_name
                                item3.company_name = item['GLUSR_USR_COMPANYNAME']
                                item3.address = item['ENQ_ADDRESS']
                                item3.customer_email_id = item['SENDEREMAIL']

                                item3.contact_no = clean_mob
                                item3.customer_industry = ''
                                new_existing_customer = 'New'
                                try:
                                    item3.save()
                                except:
                                    pass

                            try:

                                if Lead.objects.filter(requirement_indiamart_unique = clean_requirement,customer_id=Lead_Customer_Details.objects.get(id=item3.pk),
                                                    channel='IndiaMart',indiamart_time=item['DATE_R']).count()==0:
                                    item2 = Lead()
                                    item2.new_existing_customer = new_existing_customer
                                    item2.customer_id = Lead_Customer_Details.objects.get(id=item3.pk)
                                    item2.current_stage = 'Not Yet Initiated'
                                    if item['QTYPE'] == 'B':
                                        item2.is_indiamart_purchased_lead = True
                                    else:
                                        item2.is_indiamart_purchased_lead = False

                                    item2.date_of_initiation = time.strftime("%Y-%m-%d", conv2)
                                    item2.channel = 'IndiaMart'
                                    item2.owner_of_opportunity = request.user

                                    # requirement = item['SUBJECT'] + item['ENQ_MESSAGE'] + item['PRODUCT_NAME']
                                    item2.requirement = requirement.replace('<b>', '\n')
                                    item2.indiamart_time = item['DATE_R']
                                    item2.requirement_indiamart_unique = clean_requirement
                                    try:
                                        item2.save()
                                        fp = Follow_up_section()
                                        fp.lead_id = Lead.objects.get(id=item2.pk)
                                        fp.save()
                                    except Exception as e:
                                        lead_count = lead_count -1
                                        # error_exist = True
                                        error_exist = False
                                        # error2 = e
                                        print('error2')
                                        print(error2)
                                else:
                                    print("lead already Exist")
                                    lead_count = lead_count - 1
                            except Exception as e:
                                # error_exist = True
                                lead_count = lead_count - 1
                                error_exist = False
                                error = e
                                print('e')
                                print(e)
                    else:
                        lead_count = lead_count - 1

                obj = IndiamartLeadDetails()
                obj.from_date = time.strftime("%Y-%m-%d", conv)
                obj.to_date = time.strftime("%Y-%m-%d", conv2)
                obj.lead_count = lead_count
                try:
                    obj.save()
                    return redirect('/lead_home/?success=true&lead_count='+obj.lead_count)

                except:
                    context23 = {
                        'err': True,
                    }
                    context.update(context23)
            elif (lead_count < 0):
                row_count = response
                if (row_count != None):
                    error = row_count
                    error_exist = True
                    print('error_exist')
                    print(error)
                    context23 = {
                        'error': error,
                        'error2': error2,
                        'error_exist': error_exist,
                    }
                    context.update(context23)

        if 'sort_submit' in request.POST:
            YEAR = request.POST.get('YEAR')
            MONTH = request.POST.get('MONTH')



            if request.user.role == 'Super Admin':  # For ADMIN
                lead_list = Lead.objects.filter(entry_timedate__month = MONTH , entry_timedate__year = YEAR).order_by('-id')
                lead_list_count = Lead.objects.filter(entry_timedate__month = MONTH , entry_timedate__year = YEAR).count()
                paginator = Paginator(lead_list, 200)  # Show 25 contacts per page
                page = request.GET.get('page')
                lead_list = paginator.get_page(page)
                context={
                    'lead_list': lead_list,
                    'lead_list_count': True if lead_list_count != 0 else False ,
                    'lead_lis': False if lead_list_count != 0 else True,
                }

            else:
                admin = SiteUser.objects.get(id=request.user.pk).admin
                lead_list = Lead.objects.filter(Q(owner_of_opportunity__admin=admin) and Q(entry_timedate__month = MONTH , entry_timedate__year = YEAR)).order_by('-id')
                lead_list_count = Lead.objects.filter(Q(owner_of_opportunity__admin=admin) and Q(entry_timedate__month = MONTH , entry_timedate__year = YEAR)).count()
                paginator = Paginator(lead_list, 200)  # Show 25 contacts per page
                page = request.GET.get('page')
                lead_list = paginator.get_page(page)
                context = {
                    'lead_list': lead_list,
                    'lead_list_count': True if lead_list_count != 0 else False,
                    'lead_lis': False if lead_list_count != 0 else True,
                }


            return render(request, 'lead_management/lead_home.html', context)

        if 'delete_lead_id' in request.POST:
            delete_lead_id = request.POST.getlist('delete_lead_id')
            Lead.objects.filter(pk__in=delete_lead_id).delete()
            return redirect('/lead_home/')

        if 'sub1' in request.POST:
            if request.user.role == 'Super Admin':  # For ADMIN
                lead_list = Lead.objects.filter(current_stage='Not Yet Initiated').order_by('-id')
                lead_list_count = Lead.objects.filter(current_stage='Not Yet Initiated').count()
                # paginator = Paginator(lead_list, 200)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # lead_list = paginator.get_page(page)

            elif request.user.role == 'Admin':  # For ADMIN
                lead_list = Lead.objects.filter(Q(current_stage='Not Yet Initiated')&(Q(owner_of_opportunity__profile_name=request.user.profile_name) | Q(
                    owner_of_opportunity__admin__icontains=request.user.profile_name))).order_by('-id')
                lead_list_count = Lead.objects.filter(Q(current_stage='Not Yet Initiated')&(Q(owner_of_opportunity__profile_name=request.user.profile_name) | Q(
                    owner_of_opportunity__admin__icontains=request.user.profile_name))).count()
                # paginator = Paginator(lead_list, 200)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # lead_list = paginator.get_page(page)
            elif request.user.role == 'Manager':  # For manager
                lead_list = Lead.objects.filter(Q(current_stage='Not Yet Initiated')&(Q(owner_of_opportunity__profile_name=request.user.profile_name) | Q(
                    owner_of_opportunity__manager__icontains=request.user.profile_name))).order_by('-id')
                lead_list_count = Lead.objects.filter(Q(current_stage='Not Yet Initiated')&(Q(owner_of_opportunity__profile_name=request.user.profile_name) | Q(
                    owner_of_opportunity__manager__icontains=request.user.profile_name))).count()
                # paginator = Paginator(lead_list, 200)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # lead_list = paginator.get_page(page)
            else:  # for employee
                lead_list = Lead.objects.filter(Q(current_stage='Not Yet Initiated')&Q(owner_of_opportunity__profile_name=request.user.profile_name)).order_by('-id')
                lead_list_count = Lead.objects.filter(Q(current_stage='Not Yet Initiated') &Q(owner_of_opportunity__profile_name=request.user.profile_name)).count()
                # paginator = Paginator(lead_list, 200)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # lead_list = paginator.get_page(page)
            context44 = {
                'lead_list': lead_list,
                'lead_list_count': True if lead_list_count != 0 else False,
            }
            context.update(context44)

        if 'sub2' in request.POST:
            if request.user.role == 'Super Admin':  # For ADMIN
                lead_list = Lead.objects.filter(current_stage='Customer Called').order_by('-id')
                lead_list_count = Lead.objects.filter(current_stage='Customer Called').count()
                # paginator = Paginator(lead_list, 200)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # lead_list = paginator.get_page(page)

            elif request.user.role == 'Admin':  # For ADMIN
                lead_list = Lead.objects.filter(Q(current_stage='Customer Called') & (Q(
                    owner_of_opportunity__profile_name=request.user.profile_name) | Q(
                    owner_of_opportunity__admin__icontains=request.user.profile_name))).order_by('-id')
                lead_list_count = Lead.objects.filter(Q(current_stage='Customer Called') & (Q(
                    owner_of_opportunity__profile_name=request.user.profile_name) | Q(
                    owner_of_opportunity__admin__icontains=request.user.profile_name))).count()
                # paginator = Paginator(lead_list, 200)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # lead_list = paginator.get_page(page)
            elif request.user.role == 'Manager':  # For manager
                lead_list = Lead.objects.filter(Q(current_stage='Customer Called') & (Q(
                    owner_of_opportunity__profile_name=request.user.profile_name) | Q(
                    owner_of_opportunity__manager__icontains=request.user.profile_name))).order_by('-id')
                lead_list_count = Lead.objects.filter(Q(current_stage='Customer Called') & (Q(
                    owner_of_opportunity__profile_name=request.user.profile_name) | Q(
                    owner_of_opportunity__manager__icontains=request.user.profile_name))).count()
                # paginator = Paginator(lead_list, 200)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # lead_list = paginator.get_page(page)
            else:  # for employee
                lead_list = Lead.objects.filter(Q(current_stage='Customer Called') & Q(
                    owner_of_opportunity__profile_name=request.user.profile_name)).order_by('-id')
                lead_list_count = Lead.objects.filter(Q(current_stage='Customer Called') & Q(
                    owner_of_opportunity__profile_name=request.user.profile_name)).count()
                # paginator = Paginator(lead_list, 200)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # lead_list = paginator.get_page(page)
            context44 = {
                'lead_list': lead_list,
                'lead_list_count': True if lead_list_count != 0 else False,
            }
            context.update(context44)

        if 'sub3' in request.POST:
            if request.user.role == 'Super Admin':  # For ADMIN
                lead_list = Lead.objects.filter(current_stage='PI Sent & Follow-up').order_by('-id')
                lead_list_count = Lead.objects.filter(current_stage='PI Sent & Follow-up').count()
                # paginator = Paginator(lead_list, 200)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # lead_list = paginator.get_page(page)

            elif request.user.role == 'Admin':  # For ADMIN
                lead_list = Lead.objects.filter(Q(current_stage='PI Sent & Follow-up') & (Q(
                    owner_of_opportunity__profile_name=request.user.profile_name) | Q(
                    owner_of_opportunity__admin__icontains=request.user.profile_name))).order_by('-id')
                lead_list_count = Lead.objects.filter(Q(current_stage='PI Sent & Follow-up') & (Q(
                    owner_of_opportunity__profile_name=request.user.profile_name) | Q(
                    owner_of_opportunity__admin__icontains=request.user.profile_name))).count()
                # paginator = Paginator(lead_list, 200)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # lead_list = paginator.get_page(page)
            elif request.user.role == 'Manager':  # For manager
                lead_list = Lead.objects.filter(Q(current_stage='PI Sent & Follow-up') & (Q(
                    owner_of_opportunity__profile_name=request.user.profile_name) | Q(
                    owner_of_opportunity__manager__icontains=request.user.profile_name))).order_by('-id')
                lead_list_count = Lead.objects.filter(Q(current_stage='PI Sent & Follow-up') & (Q(
                    owner_of_opportunity__profile_name=request.user.profile_name) | Q(
                    owner_of_opportunity__manager__icontains=request.user.profile_name))).count()
                # paginator = Paginator(lead_list, 200)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # lead_list = paginator.get_page(page)
            else:  # for employee
                lead_list = Lead.objects.filter(Q(current_stage='PI Sent & Follow-up') & Q(
                    owner_of_opportunity__profile_name=request.user.profile_name)).order_by('-id')
                lead_list_count = Lead.objects.filter(Q(current_stage='PI Sent & Follow-up') & Q(
                    owner_of_opportunity__profile_name=request.user.profile_name)).count()
                # paginator = Paginator(lead_list, 200)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # lead_list = paginator.get_page(page)
            context44 = {
                'lead_list': lead_list,
                'lead_list_count': True if lead_list_count != 0 else False,
            }
            context.update(context44)

        if 'sub4' in request.POST:
            if request.user.role == 'Super Admin':  # For ADMIN
                lead_list = Lead.objects.filter(current_stage='PO Issued - Payment not done').order_by('-id')
                lead_list_count = Lead.objects.filter(current_stage='PO Issued - Payment not done').count()
                # paginator = Paginator(lead_list, 200)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # lead_list = paginator.get_page(page)

            elif request.user.role == 'Admin':  # For ADMIN
                lead_list = Lead.objects.filter(Q(current_stage='PO Issued - Payment not done') & (Q(
                    owner_of_opportunity__profile_name=request.user.profile_name) | Q(
                    owner_of_opportunity__admin__icontains=request.user.profile_name))).order_by('-id')
                lead_list_count = Lead.objects.filter(Q(current_stage='PO Issued - Payment not done') & (Q(
                    owner_of_opportunity__profile_name=request.user.profile_name) | Q(
                    owner_of_opportunity__admin__icontains=request.user.profile_name))).count()
                # paginator = Paginator(lead_list, 200)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # lead_list = paginator.get_page(page)
            elif request.user.role == 'Manager':  # For manager
                lead_list = Lead.objects.filter(Q(current_stage='PO Issued - Payment not done') & (Q(
                    owner_of_opportunity__profile_name=request.user.profile_name) | Q(
                    owner_of_opportunity__manager__icontains=request.user.profile_name))).order_by('-id')
                lead_list_count = Lead.objects.filter(Q(current_stage='PO Issued - Payment not done') & Q(
                    owner_of_opportunity__profile_name=request.user.profile_name) | (Q(
                    owner_of_opportunity__manager__icontains=request.user.profile_name))).count()
                # paginator = Paginator(lead_list, 200)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # lead_list = paginator.get_page(page)
            else:  # for employee
                lead_list = Lead.objects.filter(Q(current_stage='PO Issued - Payment not done') & Q(
                    owner_of_opportunity__profile_name=request.user.profile_name)).order_by('-id')
                lead_list_count = Lead.objects.filter(Q(current_stage='PO Issued - Payment not done') & Q(
                    owner_of_opportunity__profile_name=request.user.profile_name)).count()
                # paginator = Paginator(lead_list, 200)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # lead_list = paginator.get_page(page)
            context44 = {
                'lead_list': lead_list,
                'lead_list_count': True if lead_list_count != 0 else False,
            }
            context.update(context44)

        if 'sub5' in request.POST:
            if request.user.role == 'Super Admin':  # For ADMIN
                lead_list = Lead.objects.filter(current_stage='PO Issued - Payment Done - Dispatch Pending').order_by(
                    '-id')
                lead_list_count = Lead.objects.filter(
                    current_stage='PO Issued - Payment Done - Dispatch Pending').count()
                # paginator = Paginator(lead_list, 200)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # lead_list = paginator.get_page(page)

            elif request.user.role == 'Admin':  # For ADMIN
                lead_list = Lead.objects.filter(Q(current_stage='PO Issued - Payment Done - Dispatch Pending') & (Q(
                    owner_of_opportunity__profile_name=request.user.profile_name) | Q(
                    owner_of_opportunity__admin__icontains=request.user.profile_name))).order_by('-id')
                lead_list_count = Lead.objects.filter(Q(current_stage='PO Issued - Payment Done - Dispatch Pending') & (Q(
                    owner_of_opportunity__profile_name=request.user.profile_name) | Q(
                    owner_of_opportunity__admin__icontains=request.user.profile_name))).count()
                # paginator = Paginator(lead_list, 200)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # lead_list = paginator.get_page(page)
            elif request.user.role == 'Manager':  # For manager
                lead_list = Lead.objects.filter(Q(current_stage='PO Issued - Payment Done - Dispatch Pending') & (Q(
                    owner_of_opportunity__profile_name=request.user.profile_name) | Q(
                    owner_of_opportunity__manager__icontains=request.user.profile_name))).order_by('-id')
                lead_list_count = Lead.objects.filter(Q(current_stage='PO Issued - Payment Done - Dispatch Pending') & (Q(
                    owner_of_opportunity__profile_name=request.user.profile_name) | Q(
                    owner_of_opportunity__manager__icontains=request.user.profile_name))).count()
                # paginator = Paginator(lead_list, 200)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # lead_list = paginator.get_page(page)
            else:  # for employee
                lead_list = Lead.objects.filter(Q(current_stage='PO Issued - Payment Done - Dispatch Pending') & Q(
                    owner_of_opportunity__profile_name=request.user.profile_name)).order_by('-id')
                lead_list_count = Lead.objects.filter(Q(current_stage='PO Issued - Payment Done - Dispatch Pending') & Q(
                    owner_of_opportunity__profile_name=request.user.profile_name)).count()
                # paginator = Paginator(lead_list, 200)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # lead_list = paginator.get_page(page)
            context44 = {
                'lead_list': lead_list,
                'lead_list_count': True if lead_list_count != 0 else False,
            }
            context.update(context44)

        if 'sub6' in request.POST:
            if request.user.role == 'Super Admin':  # For ADMIN
                lead_list = Lead.objects.filter(current_stage='Dispatch Done - Closed').order_by('-id')
                lead_list_count = Lead.objects.filter(current_stage='Dispatch Done - Closed').count()
                # paginator = Paginator(lead_list, 200)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # lead_list = paginator.get_page(page)

            elif request.user.role == 'Admin':  # For ADMIN
                lead_list = Lead.objects.filter(Q(current_stage='Dispatch Done - Closed') &(Q(
                    owner_of_opportunity__profile_name=request.user.profile_name) | Q(
                    owner_of_opportunity__admin__icontains=request.user.profile_name))).order_by('-id')
                lead_list_count = Lead.objects.filter(Q(current_stage='Dispatch Done - Closed') & (Q(
                    owner_of_opportunity__profile_name=request.user.profile_name) | Q(
                    owner_of_opportunity__admin__icontains=request.user.profile_name))).count()
                # paginator = Paginator(lead_list, 200)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # lead_list = paginator.get_page(page)
            elif request.user.role == 'Manager':  # For manager
                lead_list = Lead.objects.filter(Q(current_stage='Dispatch Done - Closed') & (Q(
                    owner_of_opportunity__profile_name=request.user.profile_name) | Q(
                    owner_of_opportunity__manager__icontains=request.user.profile_name))).order_by('-id')
                lead_list_count = Lead.objects.filter(Q(current_stage='Dispatch Done - Closed') & (Q(
                    owner_of_opportunity__profile_name=request.user.profile_name) | Q(
                    owner_of_opportunity__manager__icontains=request.user.profile_name))).count()
                # paginator = Paginator(lead_list, 200)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # lead_list = paginator.get_page(page)
            else:  # for employee
                lead_list = Lead.objects.filter(Q(current_stage='Dispatch Done - Closed') & Q(
                    owner_of_opportunity__profile_name=request.user.profile_name)).order_by('-id')
                lead_list_count = Lead.objects.filter(Q(current_stage='Dispatch Done - Closed') & Q(
                    owner_of_opportunity__profile_name=request.user.profile_name)).count()
                # paginator = Paginator(lead_list, 200)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # lead_list = paginator.get_page(page)
            context44 = {
                'lead_list': lead_list,
                'lead_list_count': True if lead_list_count != 0 else False,
            }
            context.update(context44)

        if 'sub7' in request.POST:
            if request.user.role == 'Super Admin':  # For ADMIN
                lead_list = Lead.objects.filter(current_stage='Lost').order_by('-id')
                lead_list_count = Lead.objects.filter(current_stage='Lost').count()
                # paginator = Paginator(lead_list, 200)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # lead_list = paginator.get_page(page)

            elif request.user.role == 'Admin':  # For ADMIN
                lead_list = Lead.objects.filter(Q(current_stage='Lost') & (Q(
                    owner_of_opportunity__profile_name=request.user.profile_name) | Q(
                    owner_of_opportunity__admin__icontains=request.user.profile_name))).order_by('-id')
                lead_list_count = Lead.objects.filter(Q(current_stage='Lost') & (Q(
                    owner_of_opportunity__profile_name=request.user.profile_name) | Q(
                    owner_of_opportunity__admin__icontains=request.user.profile_name))).count()
                # paginator = Paginator(lead_list, 200)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # lead_list = paginator.get_page(page)
            elif request.user.role == 'Manager':  # For manager
                lead_list = Lead.objects.filter(Q(current_stage='Lost') & (Q(
                    owner_of_opportunity__profile_name=request.user.profile_name) | Q(
                    owner_of_opportunity__manager__icontains=request.user.profile_name))).order_by('-id')
                lead_list_count = Lead.objects.filter(Q(current_stage='Lost') & (Q(
                    owner_of_opportunity__profile_name=request.user.profile_name) | Q(
                    owner_of_opportunity__manager__icontains=request.user.profile_name))).count()
                # paginator = Paginator(lead_list, 200)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # lead_list = paginator.get_page(page)
            else:  # for employee
                lead_list = Lead.objects.filter(Q(current_stage='Lost') & Q(
                    owner_of_opportunity__profile_name=request.user.profile_name)).order_by('-id')
                lead_list_count = Lead.objects.filter(Q(current_stage='Lost') & Q(
                    owner_of_opportunity__profile_name=request.user.profile_name)).count()
                # paginator = Paginator(lead_list, 200)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # lead_list = paginator.get_page(page)
            context44 = {
                'lead_list': lead_list,
                'lead_list_count': True if lead_list_count != 0 else False,
            }
            context.update(context44)
        if 'sub8' in request.POST:
            if request.user.role == 'Super Admin':  # For ADMIN
                lead_list = Lead.objects.filter(current_stage='Not Relevant').order_by('-id')
                lead_list_count = Lead.objects.filter(current_stage='Not Relevant').count()
                # paginator = Paginator(lead_list, 200)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # lead_list = paginator.get_page(page)

            elif request.user.role == 'Admin':  # For ADMIN
                lead_list = Lead.objects.filter(Q(current_stage='Not Relevant') & (Q(
                    owner_of_opportunity__profile_name=request.user.profile_name) | Q(
                    owner_of_opportunity__admin__icontains=request.user.profile_name))).order_by('-id')
                lead_list_count = Lead.objects.filter(Q(current_stage='Not Relevant') & (Q(
                    owner_of_opportunity__profile_name=request.user.profile_name) | Q(
                    owner_of_opportunity__admin__icontains=request.user.profile_name))).count()
                # paginator = Paginator(lead_list, 200)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # lead_list = paginator.get_page(page)
            elif request.user.role == 'Manager':  # For manager
                lead_list = Lead.objects.filter(Q(current_stage='Not Relevant') & (Q(
                    owner_of_opportunity__profile_name=request.user.profile_name) | Q(
                    owner_of_opportunity__manager__icontains=request.user.profile_name))).order_by('-id')
                lead_list_count = Lead.objects.filter(Q(current_stage='Not Relevant') & (Q(
                    owner_of_opportunity__profile_name=request.user.profile_name) | Q(
                    owner_of_opportunity__manager__icontains=request.user.profile_name))).count()
                # paginator = Paginator(lead_list, 200)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # lead_list = paginator.get_page(page)
            else:  # for employee
                lead_list = Lead.objects.filter(Q(current_stage='Not Relevant') & Q(
                    owner_of_opportunity__profile_name=request.user.profile_name)).order_by('-id')
                lead_list_count = Lead.objects.filter(Q(current_stage='Not Relevant') & Q(
                    owner_of_opportunity__profile_name=request.user.profile_name)).count()
                # paginator = Paginator(lead_list, 200)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # lead_list = paginator.get_page(page)
            context44 = {
                'lead_list': lead_list,
                'lead_list_count': True if lead_list_count != 0 else False,
            }
            context.update(context44)
        if 'sub9' in request.POST:
            if request.user.role == 'Super Admin':  # For ADMIN
                lead_list = Lead.objects.filter(current_stage='Postponed').order_by('-id')
                lead_list_count = Lead.objects.filter(current_stage='Postponed').count()
                # paginator = Paginator(lead_list, 200)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # lead_list = paginator.get_page(page)

            elif request.user.role == 'Admin':  # For ADMIN
                lead_list = Lead.objects.filter(Q(current_stage='Postponed') & (Q(
                    owner_of_opportunity__profile_name=request.user.profile_name) | Q(
                    owner_of_opportunity__admin__icontains=request.user.profile_name))).order_by('-id')
                lead_list_count = Lead.objects.filter(Q(current_stage='Postponed') & (Q(
                    owner_of_opportunity__profile_name=request.user.profile_name) | Q(
                    owner_of_opportunity__admin__icontains=request.user.profile_name))).count()
                # paginator = Paginator(lead_list, 200)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # lead_list = paginator.get_page(page)
            elif request.user.role == 'Manager':  # For manager
                lead_list = Lead.objects.filter(Q(current_stage='Postponed') & (Q(
                    owner_of_opportunity__profile_name=request.user.profile_name) | Q(
                    owner_of_opportunity__manager__icontains=request.user.profile_name))).order_by('-id')
                lead_list_count = Lead.objects.filter(Q(current_stage='Postponed') & (Q(
                    owner_of_opportunity__profile_name=request.user.profile_name) | Q(
                    owner_of_opportunity__manager__icontains=request.user.profile_name))).count()
                # paginator = Paginator(lead_list, 200)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # lead_list = paginator.get_page(page)
            else:  # for employee
                lead_list = Lead.objects.filter(Q(current_stage='Postponed') & Q(
                    owner_of_opportunity__profile_name=request.user.profile_name)).order_by('-id')
                lead_list_count = Lead.objects.filter(Q(current_stage='Postponed') & Q(
                    owner_of_opportunity__profile_name=request.user.profile_name)).count()
                # paginator = Paginator(lead_list, 200)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # lead_list = paginator.get_page(page)


            context44 = {
                'lead_list': lead_list,
                'lead_list_count': True if lead_list_count != 0 else False,
            }
            context.update(context44)



        if 'submit1' in request.POST:
            start_date = request.POST.get('date1')
            end_date = request.POST.get('date2')
            if check_admin_roles(request):  # For ADMIN
                cust_list = Lead.objects.filter(owner_of_opportunity__group__icontains=request.user.name,
                                                owner_of_opportunity__is_deleted=False,
                                                entry_timedate__range=[start_date, end_date]).order_by('-id')

                # paginator = Paginator(cust_list, 15)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # cust_list = paginator.get_page(page)
            else:  # For EMPLOYEE
                cust_list = Lead.objects.filter(owner_of_opportunity=request.user.pk,
                                                entry_timedate__range=[start_date, end_date]).order_by('-customer_id')
                # paginator = Paginator(cust_list, 15)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # cust_list = paginator.get_page(page)
            # cust_list = Lead_Customer_Details.objects.filter()
            context = {
                'lead_list': cust_list,
                'search_msg': 'Search result for date range: ' + start_date + ' TO ' + end_date,
            }
            return render(request, 'lead_management/lead_home.html', context)
        elif 'submit2' in request.POST:
            contact = request.POST.get('contact')
            if check_admin_roles(request):  # For ADMIN
                cust_list = Lead.objects.filter(owner_of_opportunity__group__icontains=request.user.name,
                                                owner_of_opportunity__is_deleted=False, customer_id__contact_no__icontains=contact).order_by(
                    '-id')
                # paginator = Paginator(cust_list, 15)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # cust_list = paginator.get_page(page)
            else:  # For EMPLOYEE
                cust_list = Lead.objects.filter(owner_of_opportunity_id=request.user.pk, customer_id__contact_no__icontains=contact).order_by(
                    '-id')
                # paginator = Paginator(cust_list, 15)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # cust_list = paginator.get_page(page)
            # cust_list = Lead_Customer_Details.objects.filter(contact_no=contact)
            context = {
                'lead_list': cust_list,
                'search_msg': 'Search result for Customer Contact No: ' + contact,
            }
            return render(request, 'lead_management/lead_home.html', context)

        elif 'submit3' in request.POST:
            email = request.POST.get('email')
            if check_admin_roles(request):  # For ADMIN
                cust_list = Lead.objects.filter(owner_of_opportunity__group__icontains=request.user.name,
                                                owner_of_opportunity__is_deleted=False, customer_id__customer_email_id__icontains=email).order_by(
                    '-id')
                # paginator = Paginator(cust_list, 15)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # cust_list = paginator.get_page(page)
            else:  # For EMPLOYEE
                cust_list = Lead.objects.filter(owner_of_opportunity=request.user.pk, customer_id__customer_email_id__icontains=email).order_by(
                    '-id')
                # paginator = Paginator(cust_list, 15)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # cust_list = paginator.get_page(page)
            # cust_list = Lead_Customer_Details.objects.filter(customer_email_id=email)
            context = {
                'lead_list': cust_list,
                'search_msg': 'Search result for Customer Email ID: ' + email,
            }
            return render(request, 'lead_management/lead_home.html', context)
        elif 'submit4' in request.POST:
            customer = request.POST.get('customer')
            if check_admin_roles(request):  # For ADMIN
                cust_list = Lead.objects.filter(owner_of_opportunity__group__icontains=request.user.name,
                                                owner_of_opportunity__is_deleted=False, customer_id__customer_name__icontains=customer).order_by(
                    '-id')
                # paginator = Paginator(cust_list, 15)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # cust_list = paginator.get_page(page)
            else:  # For EMPLOYEE
                cust_list = Lead.objects.filter(owner_of_opportunity=request.user.pk, customer_id__customer_name__icontains=customer).order_by(
                    '-id')
                # paginator = Paginator(cust_list, 15)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # cust_list = paginator.get_page(page)
            # cust_list = Lead_Customer_Details.objects.filter(customer_name=customer)
            context = {
                'lead_list': cust_list,
                'search_msg': 'Search result for Customer Name: ' + customer,
            }
            return render(request, 'lead_management/lead_home.html', context)

        elif 'submit5' in request.POST:
            company = request.POST.get('company')
            if check_admin_roles(request):  # For ADMIN
                cust_list = Lead.objects.filter(owner_of_opportunity__group__icontains=request.user.name,
                                                owner_of_opportunity__is_deleted=False,
                                                customer_id__company_name__icontains=company).order_by('-id')
                # paginator = Paginator(cust_list, 15)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # cust_list = paginator.get_page(page)
            else:  # For EMPLOYEE
                cust_list = Lead.objects.filter(owner_of_opportunity=request.user.pk,
                                                customer_id__company_name__icontains=company).order_by('-id')
                # paginator = Paginator(cust_list, 15)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # cust_list = paginator.get_page(page)
            # cust_list = Lead_Customer_Details.objects.filter(company_name=company)
            context = {
                'lead_list': cust_list,
                'search_msg': 'Search result for Company Name: ' + company,
            }
            return render(request, 'lead_management/lead_home.html', context)

        elif 'submit7' in request.POST:
            serial_no = request.POST.get('serial_no')
            if check_admin_roles(request):  # For ADMIN
                cust_list = Lead.objects.filter(owner_of_opportunity__group__icontains=request.user.name,
                                                owner_of_opportunity__is_deleted=False, id__icontains=serial_no).order_by(
                    '-id')
                # paginator = Paginator(cust_list, 15)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # cust_list = paginator.get_page(page)
            else:  # For EMPLOYEE
                cust_list = Lead.objects.filter(owner_of_opportunity=request.user.pk, id__icontains=serial_no).order_by(
                    '-id')
                # paginator = Paginator(cust_list, 15)  # Show 25 contacts per page
                # page = request.GET.get('page')
                # cust_list = paginator.get_page(page)
            # cust_list = Lead_Customer_Details.objects.filter(company_name=company)
            context = {
                'lead_list': cust_list,
                'search_msg': 'Search result for Sr no: ' + serial_no,
            }
            return render(request, 'lead_management/lead_home.html', context)

    context23 = {
        'lead_count': lead_count,
        'from_date': from_date,
        'to_date': to_date,
        'error': error,
        'error2': error2,
        'error_exist': error_exist,
    }
    context.update(context23)



    return render(request,'lead_management/lead_home.html',context)

@login_required(login_url='/')
def add_lead(request):
    context={}
    users = SiteUser.objects.filter(modules_assigned__icontains='Lead Module',)
    under_admin_users = SiteUser.objects.filter(modules_assigned__icontains='Lead Module',admin__icontains=request.user.profile_name)
    under_manager_users = SiteUser.objects.filter(modules_assigned__icontains='Lead Module',manager__icontains=request.user.profile_name)
    if Lead.objects.all().count() == 0:
        latest_lead_id = 1
    else:
        latest_lead_id = Lead.objects.latest('id').id

    cust_sugg = Lead_Customer_Details.objects.all()
    form = Customer_detailForm()
    form2 = Deal_detailForm()
    if request.method == 'POST' or request.method=='FILES':
        customer_name = request.POST.get('customer_name')
        company_name = request.POST.get('company_name')
        address = request.POST.get('address')
        contact_no = request.POST.get('contact_no')
        customer_industry = request.POST.get('customer_industry')
        customer_email_id = request.POST.get('customer_email_id')
        customer_gst_no = request.POST.get('customer_gst_no')

        current_stage = request.POST.get('current_stage')
        new_existing_customer = request.POST.get('new_existing_customer')
        date_of_initiation = request.POST.get('date_of_initiation')
        channel = request.POST.get('channel')
        requirement = request.POST.get('requirement')
        upload_requirement_file = request.FILES.get('upload_requirement_file')
        owner_of_opportunity = request.POST.get('owner_of_opportunity')
        lost_reason = request.POST.get('lost_reason')
        postponed_reason = request.POST.get('postponed_reason')



        item2 = Lead()
        if Lead_Customer_Details.objects.filter(customer_name=customer_name,
                                           contact_no=contact_no).count() > 0:

            item2.customer_id = Lead_Customer_Details.objects.filter(contact_no=contact_no).first()

            item3 = Lead_Customer_Details.objects.filter(customer_name=customer_name,
                                                    contact_no=contact_no).first()
            if company_name != '' and company_name != None:
                item3.company_name = company_name
                item3.save(update_fields=['company_name'])
            if address != '' and address != None:
                item3.address = address
                item3.save(update_fields=['address'])
            if customer_email_id != '' and customer_email_id != None:
                item3.customer_email_id = customer_email_id
                item3.save(update_fields=['customer_email_id'])
            if customer_gst_no != '' and customer_gst_no != None:
                item3.customer_gst_no = customer_gst_no
                item3.save(update_fields=['customer_gst_no'])
            if customer_industry != '' and customer_industry != None:
                item3.customer_industry = customer_industry
                item3.save(update_fields=['customer_industry'])
        else:
            new_cust = Lead_Customer_Details()

            new_cust.customer_name = customer_name
            if company_name != '':
                new_cust.company_name = company_name
            if address != '':
                new_cust.address = address
            new_cust.contact_no = contact_no
            if customer_email_id != '':
                new_cust.customer_email_id = customer_email_id
            if customer_gst_no != '':
                new_cust.customer_gst_no = customer_gst_no
            if customer_industry != '':
                new_cust.customer_industry = customer_industry
            try:
                new_cust.save()
                item2.customer_id = Lead_Customer_Details.objects.get(id=new_cust.pk)
            except:
                pass


        item2.current_stage = current_stage
        item2.new_existing_customer = new_existing_customer
        item2.date_of_initiation = date_of_initiation
        item2.channel = channel
        item2.requirement = requirement
        item2.lost_reason = lost_reason
        item2.postponed_reason = postponed_reason
        item2.owner_of_opportunity = SiteUser.objects.filter(profile_name=owner_of_opportunity).first()
        item2.upload_requirement_file = upload_requirement_file
        item2.log_entered_by = request.user.name

        try:
            item2.save()

            fp=Follow_up_section()
            fp.lead_id= Lead.objects.get(id=item2.pk)
            fp.save()
            return redirect('/update_view_lead/'+str(item2.id))
        except:
            context25={
                'already_exist':True,
            }
            context.update(context25)

        # item.save()
    context22={
        'form':form,
        'form2':form2,
        'latest_lead_id':latest_lead_id,
        'cust_sugg':cust_sugg,
        'users':users,
        'under_admin_users':under_admin_users,
        'under_manager_users':under_manager_users,
    }
    context.update(context22)
    return render(request, 'lead_management/add_lead.html',context)

@login_required(login_url='/')
def update_view_lead(request,id):
    if len(str(id)) == 1 :
        email_pi_id = '000'+str(id)
    elif len(str(id)) == 2 :
        email_pi_id = '00'+str(id)
    elif len(str(id)) == 3 :
        email_pi_id = '0'+str(id)
    elif len(str(id)) == 4 :
        email_pi_id = str(id)
    else:
        email_pi_id = id

    lead_id = Lead.objects.get(id=id)
    users = SiteUser.objects.filter(Q(modules_assigned__icontains='Lead Module')& ~Q(profile_name=lead_id.owner_of_opportunity.profile_name))
    under_admin_users = SiteUser.objects.filter(Q(modules_assigned__icontains='Lead Module')&
                          Q(admin__icontains=request.user.profile_name)& ~Q(profile_name=lead_id.owner_of_opportunity.profile_name))
    under_manager_users = SiteUser.objects.filter(Q(modules_assigned__icontains='Lead Module')&
                          Q(manager__icontains=request.user.profile_name) & ~Q(profile_name=lead_id.owner_of_opportunity.profile_name))

    lead_pi_products = Pi_product.objects.filter(lead_id=id)
    hfu = Follow_up_section.objects.filter(lead_id=id).last()
    history_follow = History_followup.objects.filter(follow_up_section__id=hfu.id).last()

    followup_products_list = Followup_product.objects.filter(lead_id=id)

    table = ''
    table2 = ''
    total = 0.0
    try:
        for product in lead_pi_products:
            single_product_total = float(product.product_id.selling_price) * (product.quantity)
            total += single_product_total
            row = '<tr> <td>'+ str(product.quantity) +' </td><td>'+ str(product.product_id.hsn_code)+'</td><td>'+ str(product.product_id.sub_sub_category)+'</td><td><img src="'+str(product.product_id.product_image.url)+'" height="100" width="100"></td><td>'+str(product.product_id.product_desc) +'</td><td>'+str(product.product_id.selling_price) +'</td><td>'+str(single_product_total) +'</td>  </tr>'
            row2 = '<tr> <td>'+ str(product.quantity) +' </td><td>'+ str(product.product_id.hsn_code)+'</td><td>'+str(product.product_id.product_desc) +'</td><td></td><td></td>  </tr>'
            table+=row
            table2+=row2
    except:
        pass
    customer_id = Lead_Customer_Details.objects.get(id=lead_id.customer_id)
    customer_initial_data = {
        'customer_name': customer_id.customer_name,
        'company_name': customer_id.company_name,
        'contact_no': customer_id.contact_no,
        'customer_email_id': customer_id.customer_email_id,
        'address': customer_id.address,
        'customer_industry': customer_id.customer_industry,
        'customer_gst_no': customer_id.customer_gst_no,
    }
    deal_details_initial_data = {
        'current_stage': lead_id.current_stage,
        'new_existing_customer': lead_id.new_existing_customer,
        'date_of_initiation': lead_id.date_of_initiation,
        'channel': lead_id.channel,
        'requirement': lead_id.requirement,
        'upload_requirement_file': lead_id.upload_requirement_file,
        'owner_of_opportunity': lead_id.owner_of_opportunity,
        'owner_of_opportunity_employee': lead_id.owner_of_opportunity,
        'lost_reason': lead_id.lost_reason,
        'postponed_reason': lead_id.postponed_reason,
        'postpond_time_date': lead_id.postpond_time_date,
    }

    form = Customer_detailForm(initial=customer_initial_data)
    form2 = Deal_detailForm(initial=deal_details_initial_data)
    form3 = Pi_sectionForm()

    form4 = Follow_up_sectionForm(initial={'email_auto_manual':hfu.auto_manual_mode,})

    if(history_follow!=None):
        wa_msg = history_follow.wa_msg
        email_msg = history_follow.email_msg
        call_response = history_follow.call_response
        sms_msg = history_follow.sms_msg
        is_email = 'is_email' if history_follow.is_email else ''
        is_call = 'is_call' if history_follow.is_call else ''
        is_sms = 'is_sms' if history_follow.is_sms else ''
        is_whatsapp = 'is_whatsapp' if history_follow.is_whatsapp else ''

        wa_no = history_follow.wa_no if history_follow.wa_no != None and history_follow.wa_no !='' else customer_id.contact_no
    else:
        wa_msg = ''
        email_msg = ''
        sms_msg = ''
        is_email = ''
        is_call = ''
        is_sms = ''
        is_whatsapp = ''
        wa_no = customer_id.contact_no
        call_response = ''


    form6 = History_followupForm(initial={'wa_no':wa_no,'email_subject':hfu.email_subject,'wa_msg':wa_msg,'email_msg':email_msg,
                                          'sms_msg':sms_msg,'is_email':is_email,'call_response':call_response,'is_call':is_call,'is_sms':is_sms,'is_whatsapp':is_whatsapp})

    if request.user.role == 'Employee':

        work_area_godowns = Godown.objects.filter(Q(godown_admin__profile_name=request.user.admin) | Q(goddown_assign_to__profile_name=request.user.profile_name))
    elif request.user.role == 'Manager':
        work_area_godowns = Godown.objects.filter(Q(godown_admin__profile_name=request.user.admin) | Q(goddown_assign_to__profile_name=request.user.profile_name))
    elif request.user.role == 'Admin':
        work_area_godowns = Godown.objects.filter(godown_admin__profile_name=request.user.profile_name)
    elif request.user.role == 'Super Admin':
        work_area_godowns = Godown.objects.all()
    context = {
        'under_admin_users': under_admin_users,
        'under_manager_users': under_manager_users,
        'form': form,
        'form2': form2,
        'form3': form3,
        'form4': form4,
        'lead_id': lead_id,
        'lead_pi_products': lead_pi_products,
       'followup_products_list': followup_products_list,
        'hfu':hfu.fields,
        'hfu_id':hfu.id,
        'form6':form6,
        'users':users,
        'auto_manual_mode':hfu.auto_manual_mode,
        'customer_id':customer_id,
        'history_follow':history_follow,
        'work_area_godowns':work_area_godowns,
    }

    try:
        payment_id = Payment_details.objects.get(lead_id=id)
        payment_detail_initial_data = {
            'payment_channel': payment_id.payment_channel,
            'payment_receipt': payment_id.payment_receipt,
            'upload_pofile': payment_id.upload_pofile,
            'payment_recived_date': payment_id.payment_recived_date,
            'Payment_notes': payment_id.Payment_notes
        }
        form5 = Payment_detailsForm(initial=payment_detail_initial_data)
        context1 = {
        'form5': form5,
        'payment_id':payment_id,
        }
        context.update(context1)
    except:
        form5 = Payment_detailsForm()
        context1 = {
            'form5': form5,
        }
        context.update(context1)

    if Pi_section.objects.filter(lead_id=id).count() > 0:
        pi_id = Pi_section.objects.get(lead_id=id)

        pi_initial_data = {
            'discount': pi_id.discount,
            'upload_pi_file': pi_id.upload_pi_file,
            'call': pi_id.call,
            'payment_channel': pi_id.payment_channel,
            'payment_receipt': pi_id.payment_receipt,
            'upload_po_file': pi_id.upload_po_file,
            'payment_received_date': pi_id.payment_received_date,
            'notes': pi_id.notes,
            'select_gst_type': pi_id.select_gst_type,
            'select_pi_template': pi_id.select_pi_template,
            'discount_type': pi_id.discount_type,
            'first_submit': pi_id.first_submit,
            'grand_total': '' if pi_id.grand_total == 0.0 else pi_id.grand_total,
        }


        form3 = Pi_sectionForm(initial=pi_initial_data)
        context2 = {
            'form': form,
            'form2': form2,
            'form3': form3,
            'lead_id': lead_id,
            'pi_id': pi_id,
            'lead_pi_products': lead_pi_products,

        }
        context.update(context2)
    else:
        pass



    if request.method == 'POST' or request.method == 'FILES':
        email = request.session.get('email')
        email_type = request.session.get('email_type')
        try:
            del request.session['context_sess']
        except:
            pass

        if 'send_submit' in request.POST :
            delete_id = request.POST.getlist('check[]')
            godown_ids = request.POST.getlist('selected_dodown')


            pi_pro = Pi_product.objects.filter(pk__in=delete_id)
            list_count = 0;
            for item in pi_pro:

                product_id = Product.objects.filter(scale_type=item.product_id.scale_type,main_category=item.product_id.main_category,
                                                 sub_category=item.product_id.sub_category,sub_sub_category=item.product_id.sub_sub_category)
                if product_id.count()>0:
                    for item2 in product_id:
                        product_id = item2
                else:

                    messages.error(request, "Product Having Scale Type:"+item.product_id.scale_type.name+"Main Category:"+item.product_id.main_category.name+" Sub Category:"+item.product_id.sub_category.name+"Sub Sub Category:"+item.product_id.sub_sub_category.name+" Does Not Exist In Product Database")
                    return redirect('/update_view_lead/' + str(id))
                godown = Godown.objects.get(id=godown_ids[list_count])
                godown_product_exist = GodownProduct.objects.filter(godown_id=godown.id,product_id=product_id.id)
                required_quantity = item.quantity
                quantity_available=0.0
                if (godown_product_exist.count()>0):
                    for item3 in godown_product_exist:
                        quantity_available = item3.quantity
                else:

                    messages.error(request,"Product Having Sub Category:"+product_id.sub_category.name+" and Sub Sub Category:"+product_id.sub_sub_category.name+" Does Not Exist in Godown:"+godown.name_of_godown)
                    return redirect('/update_view_lead/' + str(id))

                if (quantity_available > required_quantity):
                    is_sufficient_stock = False
                else:

                    messages.error(request,"Insufficient Stock in Godown: " + Godown.objects.get(
                            id=godown_ids[list_count]).name_of_godown + " Please Select Different Godown And Try Again")
                    return redirect('/update_view_lead/' + str(id))
                list_count = list_count + 1
            list_count = 0;
            if lead_id.customer_id.contact_no == '0000000000' or len(lead_id.customer_id.contact_no) < 10:
                messages.error(request, "Contact Number Is Not Valid!!!")

                return redirect('/update_view_lead/' + str(id))


            if (len(delete_id)>0):
                current_stage = lead_id.current_stage
                is_entered_purchase = lead_id.is_entered_purchase
                if (current_stage == 'PO Issued - Payment Done - Dispatch Pending' and is_entered_purchase == False):
                    lead_customer = Lead_Customer_Details.objects.get(id=lead_id.customer_id.pk)
                    if Customer_Details.objects.filter(contact_no=lead_customer.contact_no,customer_name=lead_customer.customer_name).count()>0:
                        sales_customer = Customer_Details.objects.filter(contact_no=lead_customer.contact_no,customer_name=lead_customer.customer_name).order_by('-id')[0]
                    else:
                        sales_customer = Customer_Details()
                        sales_customer.contact_no = lead_customer.contact_no
                        sales_customer.customer_name = lead_customer.customer_name
                        sales_customer.company_name = lead_customer.company_name
                        sales_customer.address = lead_customer.address
                        sales_customer.customer_email_id = lead_customer.customer_email_id
                        sales_customer.customer_gst_no = lead_customer.customer_gst_no
                        sales_customer.customer_industry = lead_customer.customer_industry
                        sales_customer.save()

                    purchase_det = Purchase_Details()
                    purchase_det.second_company_name = lead_id.customer_id.company_name  # new2
                    purchase_det.company_address = lead_id.customer_id.address  # new2
                    purchase_det.bill_address = lead_id.customer_id.address  # new2
                    purchase_det.shipping_address = lead_id.customer_id.address  # new2
                    purchase_det.company_email = lead_id.customer_id.customer_email_id  # new2
                    purchase_det.crm_no = sales_customer
                    purchase_det.new_repeat_purchase = lead_id.new_existing_customer
                    purchase_det.second_person = lead_id.customer_id.customer_name  # new1
                    purchase_det.second_contact_no = lead_id.customer_id.contact_no  # new2
                    purchase_det.date_of_purchase = lead_id.entry_timedate
                    purchase_det.product_purchase_date = lead_id.entry_timedate
                    purchase_det.sales_person = lead_id.owner_of_opportunity.name
                    purchase_det.user_id = SiteUser.objects.get(name=lead_id.owner_of_opportunity.name)
                    purchase_det.upload_op_file = Payment_details.objects.get(lead_id=id).upload_pofile
                    purchase_det.channel_of_sales = ''
                    purchase_det.channel_of_dispatch = ''
                    purchase_det.industry = lead_id.customer_id.customer_industry
                    purchase_det.value_of_goods = 0.0
                    purchase_det.channel_of_marketing = lead_id.channel
                    purchase_det.notes = "Entry From Lead Module\n"
                    purchase_det.feedback_form_filled = False
                    purchase_det.manager_id = SiteUser.objects.get(id=request.user.pk).group
                    purchase_det.purchase_no = Purchase_Details.objects.latest('purchase_no').purchase_no + 1
                    purchase_det.log_entered_by = request.user.profile_name
                    purchase_det.save()

                    Lead.objects.filter(id=id).update(purchase_id=purchase_det.pk)
                    Lead_Customer_Details.objects.filter(id=lead_id.customer_id.pk).update(is_entered_in_purchased=True)

                    # dispatch = Dispatch()
                    # dispatch.crm_no = Lead_Customer_Details.objects.get(id=lead_id.customer_id.pk)
                    # dispatch.second_person = lead_id.customer_id.customer_name  # new1
                    # dispatch.second_contact_no = lead_id.customer_id.contact_no  # new2
                    # dispatch.second_company_name = lead_id.customer_id.company_name  # new2
                    # dispatch.company_email = lead_id.customer_id.customer_email_id
                    # dispatch.company_address = lead_id.customer_id.address  # new2
                    # dispatch.notes = "Entry From Lead Module\n"  # new2
                    # dispatch.user_id = SiteUser.objects.get(id=request.user.pk)
                    # dispatch.manager_id = SiteUser.objects.get(id=request.user.pk).group
                    # if Dispatch.objects.all().count() == 0:
                    #     dispatch.dispatch_no = 1
                    # else:
                    #     dispatch.dispatch_no = Dispatch.objects.latest('dispatch_no').dispatch_no + 1
                    # dispatch.save()

                    customer_id = Purchase_Details.objects.get(id=purchase_det.pk)
                    # customer_id.dispatch_id_assigned = Dispatch.objects.get(id=dispatch.pk)  # str(dispatch.pk + 00000)
                    # customer_id.save(update_fields=['dispatch_id_assigned'])

                    # pi_pro = Pi_product.objects.filter(pk__in=delete_id)
                    total_purchase_product_cost = 0.0
                    list_count=0
                    for item in pi_pro:
                        item_pro = Product_Details()

                        item_pro.quantity = item.quantity

                        item_pro.type_of_scale = item.product_id.scale_type
                        item_pro.model_of_purchase = item.product_id.main_category
                        item_pro.sub_model = item.product_id.sub_category
                        item_pro.sub_sub_model = item.product_id.sub_sub_category
                        item_pro.brand = 'HSCO'
                        item_pro.capacity = item.product_id.max_capacity
                        item_pro.unit = 'Kg'
                        item_pro.godown_id = Godown.objects.get(id=godown_ids[list_count])
                        if (item.product_total_cost == None or item.product_total_cost == ''):
                            item_pro.amount = 0.0
                            total_purchase_product_cost = total_purchase_product_cost + 0.0

                        else:
                            item_pro.amount = item.product_total_cost
                            total_purchase_product_cost = total_purchase_product_cost + item.product_total_cost

                        item_pro.purchase_id_id = customer_id
                        item_pro.user_id = SiteUser.objects.get(id=request.user.pk)
                        item_pro.manager_id = SiteUser.objects.get(id=request.user.pk).group
                        item_pro.log_entered_by = request.user.name

                        item_pro.save()

                        product_id = Product.objects.get(scale_type=item.product_id.scale_type,
                                                         main_category=item.product_id.main_category,
                                                         sub_category=item.product_id.sub_category,
                                                         sub_sub_category=item.product_id.sub_sub_category).id
                        GodownProduct.objects.filter(godown_id=Godown.objects.get(id=godown_ids[list_count]).id,
                                                     product_id=product_id).update(
                            quantity=F("quantity") - item.quantity)

                        list_count=list_count+1
                    # for item in pi_pro:
                    #
                    #     list_count = list_count + 1

                        # dispatch_id = Dispatch.objects.get(id=dispatch.id)
                        # dispatch_pro = Product_Details_Dispatch()
                        # dispatch_pro.user_id = SiteUser.objects.get(id=request.user.pk)
                        # dispatch_pro.manager_id = SiteUser.objects.get(id=request.user.pk).group
                        # dispatch_pro.quantity = item.quantity
                        # dispatch_pro.type_of_scale = item.product_id.scale_type
                        # dispatch_pro.model_of_purchase = item.product_id.main_category
                        # dispatch_pro.sub_model = item.product_id.sub_category
                        # dispatch_pro.sub_sub_model = item.product_id.sub_sub_category
                        #
                        # dispatch_pro.brand = 'HSCO'
                        # dispatch_pro.capacity = item.product_id.max_capacity
                        # dispatch_pro.unit = 'Kg'
                        # dispatch_pro.dispatch_id = dispatch_id
                        # if (item.product_total_cost == None or item.product_total_cost == ''):
                        #     dispatch_pro.value_of_goods = 0.0
                        # else:
                        #     dispatch_pro.value_of_goods = item.product_total_cost
                        #
                        # dispatch_pro.save()
                        #
                        # Product_Details.objects.filter(id=item_pro.pk).update(product_dispatch_id=dispatch_pro.pk)
                    try:
                        del request.session['enable_auto_edit']
                        del request.session['lead_url']
                    except:
                        pass

                    request.session['enable_auto_edit'] = True
                    request.session['lead_url'] = '/update_view_lead/'+str(id)
                    try:

                        # Purchase_Details.objects.filter(id=customer_id.pk).update(value_of_goods=Pi_section.objects.get(lead_id=id).grand_total)
                        Purchase_Details.objects.filter(id=customer_id.pk).update(value_of_goods=total_purchase_product_cost)
                        Lead.objects.filter(id=id).update(is_entered_purchase=True,current_stage='Dispatch Done - Closed')
                    except Exception as e :
                        # context22 = {
                        #     'error': "Submit PI Details First!!!",
                        #     'error_exist': True,
                        # }
                        # context.update(context22)
                        # try:
                        #     del request.session['context_sess']
                        # except:
                        #     pass
                        # request.session['context_sess'] = context22
                        messages.error(request,"Submit PI Details First!!!")
                        return redirect('/update_view_lead/' + str(id))


                    if True:
                        Purchase_Details.objects.filter(id=id).update(is_last_product=True)

                        product_list = ''' '''
                        pro_lis = Product_Details.objects.filter(purchase_id_id=customer_id)

                        for idx, item in enumerate(pro_lis):
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
                                item.amount,
                            )
                            product_list = product_list + '' + str(email_body_text)
                        try:
                            import smtplib
                            sent_from = settings.EMAIL_HOST_USER
                            to = [customer_id.company_email]
                            subject = 'Your HSCo Purchase'

                            message = 'Dear ' + str(
                                customer_id.second_person) + ',' \
                                                             ' Thank you for purchasing from HSCo, Your Purchase ID is ' + str(
                                customer_id.purchase_no) + '.' \
                                                           ' Ww will love to hear your feedback to help us improve' \
                                                           ' our customer experience. Please click on the link' \
                                                           ' below: \n http://139.59.76.87/feedback_purchase/' + str(
                                request.user.pk) + '/' + str(
                                customer_id.crm_no.pk) + '/' + str(
                                customer_id.id) + '\n For more details contact us on - 7045922250 \n Order Details:\n ' + product_list

                            body = message

                            email_text = """\
                                        From: %s
                                        To: %s
                                        Subject: %s
    
                                        %s
                                        """ % (sent_from, customer_id.company_email, subject, body)

                            try:
                                server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                                server.ehlo()
                                server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
                                server.sendmail(sent_from, to, email_text)
                                server.close()
                                print('Email sent!')
                            except:
                                print('Something went wrong...Email not send!!!')

                        except:
                            print("exception occured!!")
                            pass

                        message = 'Dear ' + str(
                            customer_id.second_person) + ',' \
                                                         ' Thank you for purchasing from HSCo, Your Purchase ID is ' + str(
                            customer_id.purchase_no) + '.' \
                                                       ' WE will love to hear your feedback to help us improve' \
                                                       ' our customer experience. Please click on the link' \
                                                       ' below: \n http://139.59.76.87/feedback_purchase/' + str(
                            request.user.pk) + '/' + str(
                            customer_id.crm_no.pk) + '/' + str(
                            customer_id.id) + '\n For more details contact us on - 7045922250'

                        url = "http://smshorizon.co.in/api/sendsms.php?user=" + settings.user + "&apikey=" + settings.api + "&mobile=" + customer_id.second_contact_no + "&message=" + message + "&senderid=" + settings.senderid + "&type=txt"
                        payload = ""
                        headers = {'content-type': 'application/x-www-form-urlencoded'}

                        response = requests.request("GET", url, data=json.dumps(payload), headers=headers)
                        x = response.text
                        del_all_sessions(request)
                        request.session['expand_deal_detail'] = True
                        return redirect('/update_customer_details/' + str(purchase_det.pk))

            else:
                context22 = {
                    'error': "No Product Selected\nPlease Select Products And Try Again",
                    'error_exist': True,
                }
                context.update(context22)
                try:
                    del request.session['context_sess']
                except:
                    pass
                request.session['context_sess'] = context22
                return redirect('/update_view_lead/' + str(id))

        if 'file_pdf' in request.POST and (email == 'True' or email == True) and email_type == 'internal_pi':
            try:
                del request.session['download_pdf_exist']
            except:
                pass
            try:
                del request.session['select_pi_template_session']
            except:
                pass
            request.session['is_file_pdf'] = True
            val = request.POST
            text='Hello Sir/Madam \nPFA\nThanks\nSales Team - HSCo\n\n'
            with get_connection(
                    host='webmail.hindustanscale.com',
                    port=587,
                    username='pi@hindustanscale.com',
                    password='Hindustan@@1234',
                    use_tls=True
            ) as connection:

                email_send = EmailMessage('Proforma Invoice for Enquiry Number '+email_pi_id, '',
                                      settings.EMAIL_HOST_USER3, [lead_id.customer_id.customer_email_id],connection=connection)
                part1 = MIMEText(text, 'plain')
                part2 = MIMEText(user(request), 'html')
                email_send.attach(part1)
                email_send.attach(part2)
                email_send.attach('ProformaInvoice.pdf', val.get('file_pdf'), 'application/pdf')
                email_send.send()

            history = Pi_History()
            lead_id = Lead.objects.get(id=id)
            todays_date = str(datetime.now().strftime("%Y-%m-%d"))
            history.medium_of_selection = 'Email'
            pi_id = Pi_section.objects.get(lead_id=id)

            pi_products = Pi_product.objects.filter(lead_id=id)
            context22 = {
                'lead_id': lead_id,
                'todays_date': todays_date,
                'pi_id': pi_id,
                'pi_products': pi_products,
            }
            template = get_template('lead_management/download_pi_pdf.html')
            html = template.render(context22)
            file_pdf = ContentFile(html)
            # file =  file_pdf.save('AutoFollowup.pdf', file_pdf, save=False)
            history.pi_history_file.save('PI.html', file_pdf, save=False)
            history.lead_id = Lead.objects.get(id=id)
            history.log_entered_by = request.user.profile_name
            history.medium_of_selection = 'Email'
            history.call_detail = ''
            history.save()
            messages.success(request, "Email Sent on email Id: "+customer_id.customer_email_id)

            try:
                del request.session['email']
            except:
                pass

            try:
                del request.session['email_type']
            except:
                pass

        if 'submit' in request.POST:
            customer_name = request.POST.get('customer_name')
            company_name = request.POST.get('company_name')
            address = request.POST.get('address')
            contact_no = request.POST.get('contact_no')
            customer_industry = request.POST.get('customer_industry')
            customer_email_id = request.POST.get('customer_email_id')
            customer_gst_no = request.POST.get('customer_gst_no')
            current_stage = request.POST.get('current_stage')
            new_existing_customer = request.POST.get('new_existing_customer')
            date_of_initiation = request.POST.get('date_of_initiation')
            channel = request.POST.get('channel')
            requirement = request.POST.get('requirement')
            upload_requirement_file = request.FILES.get('upload_requirement_file')
            owner_of_opportunity = request.POST.get('owner_of_opportunity')
            lost_reason = request.POST.get('lost_reason')
            postponed_reason = request.POST.get('postponed_reason')

            payment_channel = request.POST.get('payment_channel')
            payment_receipt = request.POST.get('payment_receipt')
            upload_pofile = request.POST.get('upload_pofile')
            payment_received_date = request.POST.get('payment_received_date')

            del_all_sessions(request)
            request.session['expand_customer'] = True




            item2 = Lead.objects.get(id=id)

            item3 = Lead_Customer_Details.objects.get(id=lead_id.customer_id)

            if customer_name != '' and customer_name != None:
                item3.customer_name = customer_name
                item3.save(update_fields=['customer_name'])
            if contact_no != '' and contact_no != None:
                item3.contact_no = contact_no
                item3.save(update_fields=['contact_no'])
            if company_name != '' and company_name != None:
                item3.company_name = company_name
                item3.save(update_fields=['company_name'])
            if address != '' and address != None:
                item3.address = address
                item3.save(update_fields=['address'])
            if customer_email_id != '' and customer_email_id != None:
                item3.customer_email_id = customer_email_id
                item3.save(update_fields=['customer_email_id'])
            if customer_gst_no != '' and customer_gst_no != None:
                item3.customer_gst_no = customer_gst_no
                item3.save(update_fields=['customer_gst_no'])
            if customer_industry != '' and customer_industry != None:
                item3.customer_industry = customer_industry
                item3.save(update_fields=['customer_industry'])
            messages.success(request, 'Customer Details Saved Successfully!!!')
            return redirect('/update_view_lead/'+str(id))

        if 'submit1' in request.POST:                                            #for customer and deal details section

            new_existing_customer = request.POST.get('new_existing_customer')
            date_of_initiation = request.POST.get('date_of_initiation')
            channel = request.POST.get('channel')
            requirement = request.POST.get('requirement')
            upload_requirement_file = request.FILES.get('upload_requirement_file')
            owner_of_opportunity = request.POST.get('owner_of_opportunity')
            lost_reason = request.POST.get('lost_reason')
            postponed_reason = request.POST.get('postponed_reason')
            current_stage = request.POST.get('current_stage')
            postpond_time_date = request.POST.get('postpond_time_date')

            payment_channel = request.POST.get('payment_channel')
            payment_receipt = request.POST.get('payment_receipt')
            upload_pofile = request.POST.get('upload_pofile')
            payment_received_date = request.POST.get('payment_received_date')

            del_all_sessions(request)
            request.session['expand_deal_detail'] = True


            item2 = Lead.objects.get(id=id)

            if (current_stage=='Dispatch Done - Closed'):
                if(not item2.is_entered_purchase):
                    # context22 = {
                    #     'error': 'Make Entry In Purchase Module And Try Again!!!',
                    #     'error_exist': True,
                    # }
                    # context.update(context22)
                    # try:
                    #     del request.session['context_sess']
                    # except:
                    #     pass
                    # request.session['context_sess'] = context22
                    messages.error(request,'Make Entry In Purchase Module And Try Again!!!')
                    return redirect('/update_view_lead/' + str(id))

            item2.current_stage = current_stage
            item2.new_existing_customer = new_existing_customer
            item2.date_of_initiation = date_of_initiation
            item2.channel = channel
            item2.requirement = requirement
            item2.lost_reason = lost_reason
            item2.postponed_reason = postponed_reason
            if upload_requirement_file != '' and upload_requirement_file != None:
                item2.upload_requirement_file = upload_requirement_file
            if postpond_time_date != '' and postpond_time_date != None:
                item2.postpond_time_date = postpond_time_date
            item2.log_entered_by = request.user.name
            if owner_of_opportunity != None and owner_of_opportunity != 'None':
                item2.owner_of_opportunity = SiteUser.objects.get(profile_name=owner_of_opportunity)
            item2.save(update_fields=['current_stage','new_existing_customer','date_of_initiation','channel',
                                      'requirement','upload_requirement_file','owner_of_opportunity','log_entered_by',
                                      'lost_reason','postponed_reason','postpond_time_date'])

            messages.success(request, 'Deal Details Saved Successfully!!!')

            return redirect('/update_view_lead/'+str(id))

        elif 'submit2' in request.POST:
            del_all_sessions(request)
            request.session['expand_pi_section'] = True


            #for pi section
            discount = request.POST.get('discount')
            upload_pi_file = request.FILES.get('upload_pi_file')
            select_pi_template = request.POST.get('select_pi_template')
            select_gst_type = request.POST.get('select_gst_type')
            call = request.POST.get('call')
            email = request.POST.get('email')
            whatsapp = request.POST.get('whatsapp')
            call2 = request.POST.get('call2')
            discount_type = request.POST.get('discount_type')
            grand_total = request.POST.get('grand_total')
            email_type = request.POST.get('email_type_check')

            try:
                del request.session['download_pdf_exist']
            except:
                pass

            try:
                del request.session['select_pi_template_session']
            except:
                pass
            if select_pi_template != None:
                request.session['download_pdf_exist'] = True
            request.session['select_pi_template_session'] = select_pi_template

            if email_type == 'internal_pi':
                request.session['email_type'] = 'internal_pi'
                Pi_section.objects.filter(lead_id=id).update(show_external_pi_first=False)
            elif email_type == 'external_pi':
                request.session['email_type'] = 'external_pi'
                Pi_section.objects.filter(lead_id=id).update(show_external_pi_first=True)

            if call2 == 'on':
                call2 = 'True'
            else:
                call2 = 'False'
            if email == 'on':
                email = 'True'
                request.session['email'] = True

            else:
                email = 'False'
                request.session['email'] = False

            if whatsapp == 'on':
                whatsapp = 'True'
            else:
                whatsapp = 'False'
            pdf = request.FILES.get('pdf')

            if (call2 == 'True' or call2 == True):
                history = Pi_History()
                history.lead_id = Lead.objects.get(id=id)
                history.log_entered_by = request.user.profile_name
                history.medium_of_selection = 'Call'
                history.call_detail = call
                history.save()

            try:
                text = 'Hello Sir/Madam \nPFA\nThanks\nSales Team - HSCo\n\n'

                if email == 'True' and upload_pi_file == None and email_type == 'external_pi':
                    pi_file = Pi_section.objects.filter(lead_id=id).latest('pk').upload_pi_file

                    pi_file = pi_file
                    history = Pi_History()

                    history.pi_history_file = pi_file
                    history.lead_id = Lead.objects.get(id=id)
                    history.log_entered_by = request.user.profile_name
                    history.medium_of_selection = 'Email'
                    history.save()
                    with get_connection(
                            host='webmail.hindustanscale.com',
                            port=587,
                            username='pi@hindustanscale.com',
                            password='Hindustan@@1234',
                            use_tls=True
                    ) as connection:

                        email_send = EmailMessage('Proforma Invoice for Enquiry Number '+email_pi_id, '',
                                                  settings.EMAIL_HOST_USER3, [lead_id.customer_id.customer_email_id],
                                                  connection=connection)
                        part1 = MIMEText(text, 'plain')
                        part2 = MIMEText(user(request), 'html')
                        email_send.attach(part1)
                        email_send.attach(part2)
                        email_send.attach_file(history.pi_history_file.path)
                        email_send.send()


                    messages.success(request, "Email Sent on email Id: " + customer_id.customer_email_id)
                elif email == 'True' and upload_pi_file !=None and email_type == 'external_pi':
                    pi_file = upload_pi_file
                    history = Pi_History()

                    history.pi_history_file = pi_file
                    history.lead_id = Lead.objects.get(id=id)
                    history.log_entered_by = request.user.profile_name
                    history.medium_of_selection = 'Email'
                    history.save()
                    with get_connection(
                            host='webmail.hindustanscale.com',
                            port=587,
                            username='pi@hindustanscale.com',
                            password='Hindustan@@1234',
                            use_tls=True
                    ) as connection:

                        email_send = EmailMessage('Proforma Invoice for Enquiry Number '+email_pi_id, '',
                                                  settings.EMAIL_HOST_USER3, [lead_id.customer_id.customer_email_id],
                                                  connection=connection)
                        part1 = MIMEText(text, 'plain')
                        part2 = MIMEText(user(request), 'html')
                        email_send.attach(part1)
                        email_send.attach(part2)
                        email_send.attach_file(history.pi_history_file.path)
                        email_send.send()

                    messages.success(request, "Email Sent on email Id: " + customer_id.customer_email_id)

            except Exception as pi_file_error:
                print(pi_file_error)



            if Pi_section.objects.filter(lead_id=id).count() > 0:

                item2 = Pi_section.objects.filter(lead_id=id).first()
                item2.discount = discount

                if upload_pi_file != None and select_pi_template != '':
                    item2.upload_pi_file = upload_pi_file

                if select_pi_template != None and select_pi_template !=  '':
                    item2.select_pi_template = select_pi_template
                item2.call = call
                item2.email = email
                item2.whatsapp = whatsapp
                item2.call2 = call2
                item2.select_gst_type = select_gst_type
                item2.discount_type = discount_type
                item2.first_submit = True
                item2.log_entered_by = request.user.name
                if grand_total != None and grand_total != '' and grand_total != 'None' and float(grand_total) != float(item2.grand_total):
                    item2.grand_total = float(grand_total)

                else:
                    try:
                        total = Pi_product.objects.filter(lead_id=id).values('product_total_cost')
                        total_cost = 0.0
                        for x in total:
                            total_cost += x['product_total_cost']
                        item2.total_cost = total_cost


                        product_pf = Pi_product.objects.filter(lead_id=id).values('pf')
                        pf_total = 0.0
                        for x in product_pf:
                            pf_total += float(x['pf'])
                        item2.pf_total = pf_total
                        if discount_type == 'percent' and discount != '' and discount != 0 and total_cost != '':
                            total_discount = (float(total_cost) * float(discount))/100.0  #converting discount percentage to discount total
                            net_total = float(total_cost) - float(total_discount)
                            item2.net_total = net_total
                            item2.cgst_sgst = (9.0 * net_total) / 100.0
                            igst = (18.0 * net_total) / 100.0
                            item2.igst = igst
                            item2.round_up_total = round(net_total + pf_total + igst)
                            item2.grand_total = round(net_total + pf_total + igst)
                        elif discount_type == 'rupee' and discount != '' and total_cost != '':
                            net_total = float(total_cost) - float(discount)
                            item2.net_total = net_total
                            item2.cgst_sgst = (9.0 * net_total)/100.0
                            igst = (18.0 * item2.net_total)/100.0
                            item2.igst = igst
                            item2.round_up_total = round(item2.net_total + pf_total + igst)
                            item2.grand_total = round(item2.net_total + pf_total + igst)
                    except:
                        print("product not added or debugging needed")

                messages.success(request, 'PI Details Saved Successfully!!!')

                item2.save(update_fields=['discount', 'upload_pi_file', 'select_pi_template', 'call','net_total','cgst_sgst','igst',
                                          'round_up_total','grand_total','total_cost','notes','pf_total',
                                        'email', 'whatsapp','call2','select_gst_type','discount_type','log_entered_by','first_submit','grand_total'  ])



            else :

                item2 = Pi_section()
                if email_type == 'internal_pi':
                    item2.show_external_pi_first = False
                elif email_type == 'external_pi':
                    item2.show_external_pi_first = True

                item2.discount = discount
                item2.upload_pi_file = upload_pi_file
                item2.select_pi_template = select_pi_template
                item2.call = call
                item2.email = email
                item2.whatsapp = whatsapp
                item2.first_submit = True
                item2.call2 = call2
                if select_gst_type != '':
                    item2.select_gst_type = select_gst_type
                if discount_type != '':
                    item2.discount_type = discount_type
                item2.lead_id = Lead.objects.get(id=id)
                item2.log_entered_by = request.user.name

                if grand_total != None and grand_total != '' and grand_total != 'None' :
                    item2.grand_total = float(grand_total)
                else:
                    try:
                        total = Pi_product.objects.filter(lead_id=id).values('product_total_cost')
                        total_cost = 0.0
                        for x in total:
                            total_cost += x['product_total_cost']
                        item2.total_cost = total_cost

                        product_pf = Pi_product.objects.filter(lead_id=id).values('pf')
                        pf_total = 0.0
                        for x in product_pf:
                            pf_total += float(x['pf'])

                        item2.pf_total = pf_total
                        if discount_type == 'percent' and discount != '' and discount != 0 and total_cost != '':
                            total_discount = (float(total_cost) * float(
                                discount)) / 100.0  # converting discount percentage to discount total
                            net_total = float(total_cost) - float(total_discount)
                            item2.net_total = net_total
                            item2.cgst_sgst = (9.0 * net_total) / 100.0
                            igst = (18.0 * net_total) / 100.0
                            item2.igst = igst
                            item2.round_up_total = round(net_total + pf_total + igst)
                            item2.grand_total = item2.round_up_total
                        elif discount_type == 'rupee' and discount != '' and total_cost != '':
                            net_total = float(total_cost) - float(discount)
                            item2.net_total = net_total
                            item2.cgst_sgst = (9.0 * net_total) / 100.0
                            igst = (18.0 * item2.net_total) / 100.0
                            item2.igst = igst
                            item2.round_up_total = round(item2.net_total + pf_total + igst)
                            item2.grand_total = item2.round_up_total
                    except:
                        print("product not added or debugging needed")

                item2.save()
                messages.success(request, 'PI Details Saved Successfully!!!')

            return redirect('/update_view_lead/'+str(lead_id.id))

        elif 'submit3' in request.POST:
            selected_fields = request.POST.getlist('checks[]')
            Follow_up_section.objects.filter(lead_id=id).update(fields=selected_fields)
            del_all_sessions(request)
            request.session['expand_followup'] = True
            messages.success(request,"Products Fields Saved")
            return redirect('/update_view_lead/' + str(id))


        elif 'submit56' in request.POST:
            if(request.session['wa_msg']):
                wa_msg = request.session['wa_msg']
                sms_content = request.session['wa_content']
                wa_no = request.session['wa_no']
                try:
                    del request.session['wa_msg']
                except:
                    pass
                return redirect('https://api.whatsapp.com/send?phone=+91' + wa_no + '&text=' + wa_msg + '\n' + sms_content)

        if 'submit_payment' in request.POST:
            payment_channel = request.POST.get("payment_channel")
            payment_receipt = request.FILES.get("payment_receipt")
            upload_pofile = request.FILES.get("upload_pofile")
            payment_received_date = request.POST.get("payment_recived_date")
            Payment_notes = request.POST.get("Payment_notes")

            if Payment_details.objects.filter(lead_id=id).count() == 0:
                item10 = Payment_details()
            else:
                item10 = Payment_details.objects.get(lead_id=id)
            item10.lead_id=Lead.objects.get(id=id)
            item10.payment_channel = payment_channel
            if payment_receipt != None and payment_receipt != '':
                item10.payment_receipt = payment_receipt
            if upload_pofile != None and upload_pofile != '':
                item10.upload_pofile = upload_pofile
            item10.payment_recived_date = payment_received_date
            item10.Payment_notes = Payment_notes

            if Payment_details.objects.filter(lead_id=id).count()==0:
                item10.save()
            else:
                item10.save(
                    update_fields=['payment_channel', 'payment_receipt', 'upload_pofile', 'payment_recived_date', 'Payment_notes'])



            del_all_sessions(request)
            request.session['expand_payment'] = True
            messages.success(request, 'Payment Details Saved Successfully!!!')

            return redirect('/update_view_lead/' + str(id))


        elif 'submit5' in request.POST:

            is_email = request.POST.get('is_email')
            is_whatsapp = request.POST.get('is_whatsapp')
            is_call = request.POST.get('is_call')
            is_sms = request.POST.get('is_sms')
            wa_msg = request.POST.get('wa_msg')
            wa_no = request.POST.get('wa_no')
            email_auto_manual = request.POST.get('email_auto_manual')
            selected_products = request.POST.getlist('checks_pro[]')
            selected_fields = Follow_up_section.objects.get(lead_id=id).fields

            del_all_sessions(request)
            request.session['expand_followup'] = True

            if wa_no == '0000000000' or len(wa_no) < 10 or len(customer_id.contact_no) < 10 or customer_id.contact_no == '0000000000' or customer_id.contact_no == '' or customer_id.contact_no == None:

                messages.error(request, "Contact Number Is  Invalid!!!")
                return redirect('/update_view_lead/' + str(id))

            if (selected_products!=None and len(selected_products)<5 and email_auto_manual == 'Manual' and not (is_call!='on' or is_call!='is_call')):

                messages.error(request, "No Product Selected\nPlease Select Products And Try Again")
                return redirect('/update_view_lead/' + str(id))
            elif not (is_call!='on' or is_call!='is_call'):
                messages.error(request, "No Product Selected\nPlease Select Products And Try Again")
                return redirect('/update_view_lead/' + str(id))

            if(is_call!='on' and is_sms!='on' and is_whatsapp!='on' and is_email!='on' and is_call!='is_call' and is_sms!='is_sms' and is_whatsapp!='is_whatsapp' and is_email !='is_email'):

                messages.error(request, "Please Select Atleast One Medium For Followup")
                return redirect('/update_view_lead/' + str(id))

            if (selected_fields != None and len(selected_fields) < 6):
                messages.error(request, "Please Select Atleast One Product Field")
                return redirect('/update_view_lead/' + str(id))

            if (email_auto_manual == 'Select Mode'):

                # context28 = {
                #     'error': "Please Select Follow Up Mode",
                #     'error_exist': True,
                # }
                # context.update(context28)
                # try:
                #     del request.session['context_sess']
                # except:
                #     pass
                # request.session['context_sess']=context28
                messages.error(request, "Please Select Follow Up Mode")
                return redirect('/update_view_lead/' + str(id))
            if(email_auto_manual == 'Manual'):

                final_list = []
                Follow_up_section.objects.filter(lead_id=id).update(whatsappno=wa_no,)
                Follow_up_section.objects.filter(lead_id=id).update(auto_manual_mode=email_auto_manual,)

                history_follow= History_followup()
                history_follow.follow_up_section=Follow_up_section.objects.get(id=hfu.id)
                history_follow.lead_id = Lead.objects.get(id=id)
                selected_fields2 = selected_fields.replace("'", "").strip('][').split(
                    ', ') if selected_fields != None and len(selected_fields) > 4 else None

                history_follow.fields = selected_fields2 if selected_fields2 != None else ''
                history_follow.product_ids = selected_products
                length_of_list = 1
                count_list = 0
                if selected_fields2!= None:


                    html_head = '''<thead> '''
                    for item in selected_fields2:
                        pro_list = Followup_product.objects.filter(lead_id=id,pk__in=selected_products).values_list(item, flat=True)
                        list_pro = []
                        item=item.replace('product_id_id__','').replace('_',' ').title().replace('Category','Model')
                        if (count_list == 0):
                            for ite, lt in enumerate(pro_list):
                                if (ite == 0):
                                    html_head = html_head + '''<th style="border: solid gray; background-color: gray; color: white;">''' + item + '''</th>'''
                                final_list.append([item + ' : ' + str(lt)])
                            count_list = count_list + 1
                        else:
                            for ite, lt in enumerate(pro_list):
                                if (ite == 0):
                                    html_head = html_head + '''<th style="border: solid gray; background-color: gray; color: white;">''' + item + '''</th>'''
                                final_list[ite] = final_list[ite] + [item + ' : ' + str(lt)]
                                # final_list[ite].append(list_pro)
                    html_head = html_head + '''</thead> '''

                    html_rows = ''''''
                    count = 1
                    sms_content=''''''
                    wa_content=''''''
                    for count_for,single in enumerate(final_list):
                        html_rows = html_rows + '''<tr> '''
                        count = count + 1
                        sms_content=sms_content+'''\nProduct No-'''+str(count_for+1)+''':'''
                        wa_content=wa_content+'''\nProduct No - '''+str(count_for+1)+''':\n______________________________________________________\n'''
                        for item in single:
                            if item.partition(":")[0] == 'Product Image ':
                                img_path = 'http://139.59.76.87/media/'+item.partition(":")[2][1:]
                                sms_content = sms_content + item.partition(":")[0] + ''' :''' + img_path + '''\n'''
                                wa_content = wa_content + item.partition(":")[0] + ''' :''' + img_path + '''\n'''
                                html_rows = html_rows + '''<td> <img height="150" width="150" src="'''+img_path+'''"> </td>'''


                            elif item.partition(":")[0] == 'Product Brochure ':
                                bro_link = 'http://139.59.76.87/media/'+item.partition(":")[2][1:]
                                sms_content = sms_content + item.partition(":")[0] + ''' :''' + bro_link + '''\n'''
                                wa_content = wa_content + item.partition(":")[0] + ''' :''' + bro_link + '''\n'''
                                html_rows = html_rows + '''<td> <a href="'''+bro_link+'''" target="_blank">View Brochure</a> </td>'''
                            elif item.partition(":")[0] == 'Product Document ':
                                bro_link = 'http://139.59.76.87/media/'+item.partition(":")[2][1:]
                                sms_content = sms_content + item.partition(":")[0] + ''' :''' + bro_link + '''\n'''
                                wa_content = wa_content + item.partition(":")[0] + ''' :''' + bro_link + '''\n'''
                                html_rows = html_rows + '''<td> <a href="'''+bro_link+'''" target="_blank">View Brochure</a> </td>'''
                            else:
                                sms_content = sms_content + item.partition(":")[0] +''' :'''+item.partition(":")[2]+'''\n'''
                                wa_content = wa_content + item.partition(":")[0] +''' :'''+item.partition(":")[2]+'''\n'''
                                html_rows = html_rows + '''<td>''' + item.partition(":")[2] + '''</td>'''

                        html_rows = html_rows + '''</tr>'''
                    context_session={}


                if(is_email=='on' or is_email =='is_email'):
                    email_subject = request.POST.get('email_subject')
                    email_msg = request.POST.get('email_msg')
                    history_follow.is_email=True
                    history_follow.email_subject=email_subject
                    history_follow.email_msg=email_msg
                    Follow_up_section.objects.filter(lead_id=id).update(email_subject=email_subject, )
                    if selected_fields2 != None:
                        html_content='''<html>
        <head>
          <title>
            HSCO
          </title>
        
          <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        
          <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
          <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
          <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
          <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
          <link href='https://fonts.googleapis.com/css?family=Poppins' rel='stylesheet'>
        
        <body>
        
        <style>
            .border_class {
            border:1px solid black;
            height:45px;
            text-align:center;
            vertical-align: middle;
            line-height: 45px;
            }
          table {
          border-collapse: collapse;
          width: 100%;
          font-size: 12px;
          border-color: black;
          color: black;
        }
        th {
          font-size: 13px;
            border: 1px solid black;
            text-align: left;
            padding:5px;
        }
    td {
      border: 1px solid black;
      padding: 3px;
      font-size: 13px;
      padding: 5px;
      text-align: center;
    }
    
    
                </style>
    
                              <div class="card shadow">
    
    <div class="card-body row" style="padding: 15px;color: black; font-weight: 300; font-size: 14px;">
        <!--<div class="col-xl-4 col-md-1 mb-1" style="border-right: 1px solid black;"><center> Product Name: {{list.product_name}} </center></div>-->
    
                  </div>
              </style>
                                  <div class="card shadow">
        
        <div class="card-body row" style="padding: 15px;color: black; font-weight: 300; font-size: 14px;">
            <!--<div class="col-xl-4 col-md-1 mb-1" style="border-right: 1px solid black;"><center> Product Name: {{list.product_name}} </center></div>-->
            
            <h4>'''+email_msg+'''</h4>
            
            <table style="font-size: 14px;">
            
            '''+html_head+''' 
            
        '''+html_rows+''' 
        </table>
                      </div>
                                  </div>
        </body>
        </html>'''

                        file = ContentFile(html_content)
                        history_follow.followup_history_file.save('AutoFollowup.html', file, save=False)
                        history_follow.html_content = html_content
                        send_html_mail(email_subject, html_content, settings.EMAIL_HOST_USER,
                                       [customer_id.customer_email_id, ])

                    else:
                        send_text_mail(email_subject, email_msg, settings.EMAIL_HOST_USER, [customer_id.customer_email_id, ])

                    # context28 = {
                    #     'success': "Email Sent on email Id: "+customer_id.customer_email_id,
                    #     'success_exist': True,
                    # }
                    # context_session.update(context28)
                    messages.success(request,"Email Sent on email Id: "+customer_id.customer_email_id)


                if(is_whatsapp=='on' or is_whatsapp=='is_whatsapp'):
                    history_follow.is_whatsapp = True
                    history_follow.wa_msg = wa_msg
                    history_follow.wa_no = wa_no
                    try:
                        del request.session['wa_msg']

                    except:
                        pass
                    try:
                        del request.session['wa_content']

                    except:
                        pass
                    try:

                        del request.session['wa_no']
                    except:
                        pass
                    request.session['wa_msg']=wa_msg
                    request.session['wa_content']=wa_content
                    request.session['wa_no']=wa_no
                    # context28 = {
                    #     'success_2': "WhatsApp Redirect Successful On WhatsApp No : " + wa_no,
                    #     'success_exist_2': True,
                    # }
                    # context_session.update(context28)
                    messages.success(request,"WhatsApp Redirect Successful On WhatsApp No : " + wa_no)


                if(is_sms=='on' or is_sms=='is_sms'):
                    sms_msg = request.POST.get('sms_msg')
                    history_follow.is_sms = True
                    history_follow.sms_msg = sms_msg
                    history_follow.sms_con = sms_content

                    url = "http://smshorizon.co.in/api/sendsms.php?user=" + settings.user + "&apikey=" + settings.api + "&mobile=" + customer_id.contact_no + "&message=" + sms_msg+'\n'+sms_content + "&senderid=" + settings.senderid + "&type=txt"
                    payload = ""
                    headers = {'content-type': 'application/x-www-form-urlencoded'}

                    response = requests.request("GET", url, data=json.dumps(payload), headers=headers)
                    x = response.text
                    print(x)
                    # context28 = {
                    #     'success_4': "SMS Sent Successfully To : " + customer_id.contact_no,
                    #     'success_exist_4': True,
                    # }
                    # context_session.update(context28)
                    messages.success(request,"SMS Sent Successfully To : " + customer_id.contact_no)


                if(is_call=='on' or is_call=='is_call'):
                    call_response = request.POST.get('call_response')
                    history_follow.is_call = True
                    history_follow.call_response = call_response
                    # context28 = {
                    #     'success_5': "Call Response Recorded Successfully" ,
                    #     'success_exist_5': True,
                    # }
                    # context_session.update(context28)
                    messages.success(request,"Call Response Recorded Successfully")


                history_follow.log_entered_by = request.user.name

                history_follow.save()

                return redirect('/update_view_lead/' + str(id))



            if (email_auto_manual == 'Automatic'):

                if(Auto_followup_details.objects.filter(follow_up_history__follow_up_section__lead_id__id=lead_id.id).count()==0):
                    final_list = []
                    Follow_up_section.objects.filter(lead_id=id).update(whatsappno=wa_no, )
                    Follow_up_section.objects.filter(lead_id=id).update(auto_manual_mode=email_auto_manual, )

                    history_follow = History_followup()
                    history_follow.follow_up_section = Follow_up_section.objects.get(id=hfu.id)
                    history_follow.lead_id = Lead.objects.get(id=id)

                    selected_fields2 = selected_fields.replace("'", "").strip('][').split(
                        ', ') if selected_fields != None and len(selected_fields) > 4 else None

                    history_follow.fields = selected_fields2 if selected_fields2 != None else ''
                    history_follow.product_ids = selected_products
                    history_follow.is_manual_mode = False
                    history_follow.is_call = False
                    history_follow.is_whatsapp = False
                    Lead.objects.filter(id=id).update(is_manual_mode_followup=False)

                    length_of_list = 1
                    count_list = 0
                    if selected_fields2 != None:

                        html_head = '''<thead> '''
                        for item in selected_fields2:
                            pro_list = Followup_product.objects.filter(lead_id=id, pk__in=selected_products).values_list(
                                item, flat=True)
                            list_pro = []
                            item = item.replace('product_id_id__', '').replace('_', ' ').title().replace('Category',
                                                                                                         'Model')
                            if (count_list == 0):
                                for ite, lt in enumerate(pro_list):
                                    if (ite == 0):
                                        html_head = html_head + '''<th style="border: solid gray; background-color: gray; color: white;">''' + item + '''</th>'''
                                    final_list.append([item + ' : ' + str(lt)])
                                count_list = count_list + 1
                            else:
                                for ite, lt in enumerate(pro_list):
                                    if (ite == 0):
                                        html_head = html_head + '''<th style="border: solid gray; background-color: gray; color: white;">''' + item + '''</th>'''
                                    final_list[ite] = final_list[ite] + [item + ' : ' + str(lt)]
                                    # final_list[ite].append(list_pro)
                        html_head = html_head + '''</thead> '''

                        html_rows = ''''''
                        count = 1
                        sms_content = ''''''
                        wa_content = ''''''
                        for count_for, single in enumerate(final_list):
                            html_rows = html_rows + '''<tr> '''
                            count = count + 1
                            sms_content = sms_content + '''\nProduct No-''' + str(count_for + 1) + ''':'''
                            wa_content = wa_content + '''\nProduct No - ''' + str(
                                count_for + 1) + ''':\n______________________________________________________\n'''
                            for item in single:
                                sms_content = sms_content + item.partition(":")[0] + ''' :''' + item.partition(":")[
                                    2] + '''\n'''
                                wa_content = wa_content + item.partition(":")[0] + ''' :''' + item.partition(":")[
                                    2] + '''\n'''
                                html_rows = html_rows + '''<td>''' + item.partition(":")[2] + '''</td>'''
                            html_rows = html_rows + '''</tr>'''



                    if(is_email=='on' or is_email =='is_email'):
                        email_subject = request.POST.get('email_subject')
                        email_msg = request.POST.get('email_msg')
                        history_follow.is_email = True
                        history_follow.email_subject = email_subject
                        history_follow.email_msg = email_msg
                        Follow_up_section.objects.filter(lead_id=id).update(email_subject=email_subject, )
                        if selected_fields2 != None:
                            html_content = '''<html>
                            <head>
                              <title>
                                HSCO
                              </title>
    
                              <meta name="viewport" content="width=device-width, initial-scale=1">
                            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    
                              <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
                              <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
                              <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
                              <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
                              <link href='https://fonts.googleapis.com/css?family=Poppins' rel='stylesheet'>
    
                            <body>
    
                            <style>
                                .border_class {
                                border:1px solid black;
                                height:45px;
                                text-align:center;
                                vertical-align: middle;
                                line-height: 45px;
                                }
                              table {
                              border-collapse: collapse;
                              width: 100%;
                              font-size: 12px;
                              border-color: black;
                              color: black;
                            }
                            th {
                              font-size: 13px;
                                border: 1px solid black;
                                text-align: left;
                                padding:5px;
                            }
                        td {
                          border: 1px solid black;
                          padding: 3px;
                          font-size: 13px;
                          padding: 5px;
                          text-align: center;
                        }
    
    
                                    </style>
    
                                                  <div class="card shadow">
    
                        <div class="card-body row" style="padding: 15px;color: black; font-weight: 300; font-size: 14px;">
                            <!--<div class="col-xl-4 col-md-1 mb-1" style="border-right: 1px solid black;"><center> Product Name: {{list.product_name}} </center></div>-->
    
                                      </div>
                                  </style>
                                                      <div class="card shadow">
    
                            <div class="card-body row" style="padding: 15px;color: black; font-weight: 300; font-size: 14px;">
                                <!--<div class="col-xl-4 col-md-1 mb-1" style="border-right: 1px solid black;"><center> Product Name: {{list.product_name}} </center></div>-->
    
                                <h4>''' + email_msg + '''</h4>
    
                                <table style="font-size: 14px;">
    
                                ''' + html_head + ''' 
    
                            ''' + html_rows + ''' 
                            </table>
                                          </div>
                                                      </div>
                            </body>
                            </html>'''

                            file = ContentFile(html_content)
                            history_follow.followup_history_file.save('AutoFollowup.html', file, save=False)
                            history_follow.html_content= html_content

                    if(is_sms=='on' or is_sms=='is_sms'):
                        sms_msg = request.POST.get('sms_msg')
                        history_follow.is_sms = True
                        history_follow.sms_msg = sms_msg
                        history_follow.sms_con = sms_content

                    history_follow.log_entered_by = request.user.name

                    history_follow.save()
                    afd= Auto_followup_details()
                    afd.follow_up_history = History_followup.objects.get(id=history_follow.pk)
                    afd.save()
                    # context28 = {
                    #     'success_6': "Followup Will Be Done Automatically After Every 2 Days",
                    #     'success_exist_6': True,
                    # }
                    # try:
                    #     del request.session['context_sess']
                    # except:
                    #     pass
                    messages.success(request,"Followup Will Be Done Automatically After Every 2 Days")

                    # request.session['context_sess'] = context28
                    return redirect('/update_view_lead/' + str(id))
                elif(Auto_followup_details.objects.filter(follow_up_history__follow_up_section__lead_id__id=lead_id.id).count()>0):
                    context28 = {
                        'error': "Auto Follow-Up is Already Set For This Lead\nTo Edit Auto Follow-Up Click On History Button In Follow-Up Section",
                        'error_exist': True,
                    }
                    context.update(context28)
                    messages.error(request,"Auto Follow-Up is Already Set For This Lead\nTo Edit Auto Follow-Up Click On History Button In Follow-Up Section")

    return render(request, 'lead_management/update_view_lead.html',context)


@login_required(login_url='/')
def del_all_sessions(request):
    try:
        del request.session['expand_customer']
    except:
        pass
    try:
        del request.session['expand_payment']
    except:
        pass
    try:
        del request.session['expand_deal_detail']
    except:
        pass
    try:
        del request.session['expand_pi_section']
    except:
        pass
    try:
        del request.session['expand_followup']
    except:
        pass

@login_required(login_url='/')
def load_wa(wa_no,wa_msg,sms_content):
    return redirect('https://api.whatsapp.com/send?phone=91' + wa_no + '&text=' + wa_msg + '\n' + sms_content)

@login_required(login_url='/')
def lead_report(request):

    return render(request,'lead_management/report_lead.html')

@login_required(login_url='/')
def report_2(request):
    try:
        del request.session['start_date']
        del request.session['end_date']
        del request.session['string_cust_detail']
        del request.session['string_deal_detail']
        del request.session['string_pi_history']
        del request.session['string_follow_up']
        del request.session['string_pay_detail']
    except:
        pass
    if request.method =='POST' :
        cust_detail = request.POST.getlist('cust_detail[]')
        deal_detail = request.POST.getlist('deal_detail[]')
        pi_history = request.POST.getlist('pi_history[]')
        follow_up = request.POST.getlist('follow_up[]')
        pay_detail = request.POST.getlist('pay_detail[]')
        start_date = request.POST.get('date1')
        end_date = request.POST.get('date2')
        string_cust_detail = ','.join(cust_detail)
        string_deal_detail = ','.join(deal_detail)
        string_pi_history = ','.join(pi_history)
        string_follow_up = ','.join(follow_up)
        string_pay_detail = ','.join(pay_detail)

        request.session['start_date'] = start_date
        request.session['end_date'] = end_date
        request.session['string_cust_detail'] = string_cust_detail
        request.session['string_cust_detail_list'] = cust_detail
        request.session['string_deal_detail'] = string_deal_detail
        request.session['string_deal_detail_list'] = deal_detail
        request.session['string_pi_history'] = string_pi_history
        request.session['string_pi_history_list'] = pi_history
        request.session['string_follow_up'] = string_follow_up
        request.session['string_follow_up_list'] = follow_up
        request.session['string_pay_detail'] = string_pay_detail
        request.session['string_pay_detail_list'] = pay_detail

        # return redirect('/final_lead_report/')
        return redirect('/final_lead_report_test/')
    return render(request,'lead_management/report_2.html')

@login_required(login_url='/')
def final_lead_report(request):
    start_date = request.session.get('start_date')
    end_date = request.session.get('end_date')
    string_cust_detail = request.session.get('string_cust_detail')
    string_cust_detail_list = request.session.get('string_cust_detail_list')
    string_deal_detail = request.session.get('string_deal_detail')
    string_deal_detail_list = request.session.get('string_deal_detail_list')
    string_pi_history = request.session.get('string_pi_history')
    string_pi_history_list = ['pi_history_file', 'time', 'call_detail', 'medium_of_selection']
    string_follow_up = request.session.get('string_follow_up')
    string_follow_up_list = ['wa_no', 'wa_msg', 'email_subject', 'email_msg', 'followup_history_file', 'sms_msg', 'call_response']
    string_pay_detail = request.session.get('string_pay_detail')
    string_pay_detail_list = request.session.get('string_pay_detail_list')
    final_row_product = []
    final_row=[]
    selected_list=[]

    if string_pi_history != '':
        string_pi_history = 'pi_history_file, time, call_detail, medium_of_selection'
    if string_follow_up != '':
        string_follow_up = 'wa_no, wa_msg, email_subject, email_msg, followup_history_file, sms_msg, call_response'
    with connection.cursor() as cursor:
        if string_cust_detail != '' and string_deal_detail != '' and string_pi_history != '' and string_follow_up != '' and string_pay_detail != '':

            selected_list = string_cust_detail_list + string_deal_detail_list + string_pi_history_list + string_follow_up_list + string_pay_detail_list

            cursor.execute("SELECT " + (
            string_cust_detail + "," + string_deal_detail+ "," + string_pi_history+ "," + string_follow_up+ "," + string_pay_detail) +
            " from customer_app_lead_customer_details , lead_management_lead  , lead_management_pi_history  ,"
            " lead_management_history_followup  , lead_management_payment_details  where lead_management_pi_history.lead_id_id = lead_management_lead.id "
            " and lead_management_history_followup.lead_id_id = lead_management_lead.id and lead_management_payment_details.lead_id_id = lead_management_lead.id and lead_management_lead.customer_id_id = customer_app_lead_customer_details.id and "
            " lead_management_lead.entry_timedate between '" + start_date + "' and '" + end_date + "';")

            row = cursor.fetchall()
            final_row_product = [list(x) for x in row]
            repairing_data = []
            for i in row:
                repairing_data.append(list(i))

            final_row = [list(x) for x in row]
            repairing_data = []
            for i in row:
                repairing_data.append(list(i))
        elif  string_deal_detail != '' and string_cust_detail != '' and string_pi_history != '' and string_follow_up != '':
            selected_list =  string_cust_detail_list + string_deal_detail_list + string_pi_history_list + string_follow_up_list

            cursor.execute("SELECT " +(string_cust_detail + ","+ string_deal_detail+ ","+ string_pi_history+ "," + string_follow_up )+ " from  "
            "lead_management_lead , customer_app_lead_customer_details, lead_management_pi_history PI , lead_management_history_followup FOLLOWUP "
            "  where lead_management_lead.customer_id_id = customer_app_lead_customer_details.id and PI.lead_id_id = lead_management_lead.id "
            "and FOLLOWUP.lead_id_id = lead_management_lead.id and lead_management_lead.entry_timedate between '" + start_date + "' and '" + end_date + "';")
            row = cursor.fetchall()
            final_row_product = [list(x) for x in row]
            repairing_data = []
            for i in row:
                repairing_data.append(list(i))

            final_row = [list(x) for x in row]
            repairing_data = []
            for i in row:
                repairing_data.append(list(i))
        elif  string_deal_detail != '' and string_cust_detail != '' and string_pi_history != '':
            selected_list =string_cust_detail_list +string_deal_detail_list +   string_pi_history_list

            cursor.execute("SELECT " +(string_cust_detail + ","+ string_deal_detail+ ","+ string_pi_history )+ " from  lead_management_lead  , customer_app_lead_customer_details, lead_management_pi_history  "
            "  where lead_management_lead.customer_id_id = customer_app_lead_customer_details.id and lead_management_pi_history.lead_id_id = lead_management_lead.id "
            "and lead_management_lead.entry_timedate between '" + start_date + "' and '" + end_date + "';")
            row = cursor.fetchall()
            final_row_product = [list(x) for x in row]
            repairing_data = []
            for i in row:
                repairing_data.append(list(i))

            final_row = [list(x) for x in row]
            repairing_data = []
            for i in row:
                repairing_data.append(list(i))
        elif  string_deal_detail != '' and string_cust_detail != '':
            selected_list =  string_cust_detail_list + string_deal_detail_list

            cursor.execute("SELECT " +(string_cust_detail + ","+ string_deal_detail )+ " from  lead_management_lead  , customer_app_lead_customer_details  "
                                "  where lead_management_lead.customer_id_id = customer_app_lead_customer_details.id and lead_management_lead.entry_timedate between '" + start_date + "' and '" + end_date + "';")
            row = cursor.fetchall()
            final_row_product = [list(x) for x in row]
            repairing_data = []
            for i in row:
                repairing_data.append(list(i))

            final_row = [list(x) for x in row]
            repairing_data = []
            for i in row:
                repairing_data.append(list(i))
        elif  string_deal_detail != '' :
            selected_list = string_deal_detail_list

            cursor.execute("SELECT " + string_deal_detail + " from  lead_management_lead "
                                "  where lead_management_lead.entry_timedate between '" + start_date + "' and '" + end_date + "';")
            row = cursor.fetchall()
            final_row_product = [list(x) for x in row]
            repairing_data = []
            for i in row:
                repairing_data.append(list(i))

            final_row = [list(x) for x in row]
            repairing_data = []
            for i in row:
                repairing_data.append(list(i))

    # if table_name == 'Customer Details Section':
    #     # customer_list = Lead_Customer_Details.objects.filter(entry_timedate__range=(start_date, end_date)).values_list(string)
    #     with connection.cursor() as cursor:
    #         if string != '' :
    #                 cursor.execute("SELECT " +  string + " from customer_app_lead_customer_details  PRODUCT  where "
    #                 " entry_timedate between'" + start_date + "' and '" + end_date + "';")
    #                 row = cursor.fetchall()
    #                 final_row_product = [list(x) for x in row]
    #                 repairing_data = []
    #                 for i in row:
    #                     repairing_data.append(list(i))
    #
    #                 final_row = [list(x) for x in row]
    #                 repairing_data = []
    #                 for i in row:
    #                     repairing_data.append(list(i))
    #
    #     try:
    #         del request.session['start_date']
    #         del request.session['end_date']
    #         del request.session['string']
    #         del request.session['selected_list']
    #     except:
    #         pass
    # if table_name == 'Deal Details Section':
    #
    #     # customer_list = Lead_Customer_Details.objects.filter(entry_timedate__range=(start_date, end_date)).values_list(string)
    #     with connection.cursor() as cursor:
    #         if string != '' :
    #                 cursor.execute("SELECT " +  string + " from lead_management_lead  PRODUCT  where "
    #                 " entry_timedate between '" + start_date + "' and '" + end_date + "';")
    #                 row = cursor.fetchall()
    #                 final_row_product = [list(x) for x in row]
    #                 repairing_data = []
    #                 for i in row:
    #                     repairing_data.append(list(i))
    #
    #                 final_row = [list(x) for x in row]
    #                 repairing_data = []
    #                 for i in row:
    #                     repairing_data.append(list(i))
    #
    #     try:
    #         del request.session['start_date']
    #         del request.session['end_date']
    #         del request.session['string']
    #         del request.session['selected_list']
    #     except:
    #         pass
    # if table_name == 'PI Section':
    #     # customer_list = Lead_Customer_Details.objects.filter(entry_timedate__range=(start_date, end_date)).values_list(string)
    #     selected_list = ['lead_id','discount','discount_type','payment_channel','payment_received_date','notes','cgst_sgst','igst','grand_total','entry_timedate'
    #                      ,'quantity','P&F']
    #
    #
    #     with connection.cursor() as cursor:
    #
    #         cursor.execute("SELECT PI.lead_id_id,discount,discount_type,payment_channel,payment_received_date,notes,cgst_sgst,igst,grand_total,PRODUCT.entry_timedate,"
    #                        "quantity,pf "
    #                        " from lead_management_pi_section PI, lead_management_pi_product PRODUCT where PRODUCT.lead_id_id = PI.lead_id_id and "
    #                        "PRODUCT.entry_timedate between'" + start_date + "' and '" + end_date + "';")
    #         row = cursor.fetchall()
    #         final_row_product = [list(x) for x in row]
    #         repairing_data = []
    #         for i in row:
    #             repairing_data.append(list(i))
    #
    #         final_row = [list(x) for x in row]
    #         repairing_data = []
    #         for i in row:
    #             repairing_data.append(list(i))
    #     try:
    #         del request.session['start_date']
    #         del request.session['end_date']
    #         del request.session['string']
    #         del request.session['selected_list']
    #     except:
    #         pass
    # if table_name == 'Follow-up Section':
    #     # customer_list = Lead_Customer_Details.objects.filter(entry_timedate__range=(start_date, end_date)).values_list(string)
    #     selected_list = ['lead_id', 'whatsappno', 'fields', 'email_subject','product_id', 'scale_type', 'main_category','sub_category', 'sub_sub_category',
    #                      'hsn_code','max_capacity', 'accuracy', 'platform_size','product_desc','cost_price','selling_price','carton_size',
    #                      'entry_timedate']
    #
    #     with connection.cursor() as cursor:
    #
    #         cursor.execute(
    #             "SELECT FOLLOW.lead_id_id,whatsappno,fields,email_subject,product_id_id,scale_type,main_category,sub_category,sub_sub_category,hsn_code,"
    #             "max_capacity,accuracy,platform_size,product_desc,cost_price,selling_price,carton_size,PRODUCT.entry_timedate"
    #             " from lead_management_follow_up_section FOLLOW, lead_management_followup_product PRODUCT where PRODUCT.lead_id_id = FOLLOW.lead_id_id and "
    #             "PRODUCT.entry_timedate between'" + start_date + "' and '" + end_date + "';")
    #         row = cursor.fetchall()
    #         final_row_product = [list(x) for x in row]
    #         repairing_data = []
    #         for i in row:
    #             repairing_data.append(list(i))
    #
    #         final_row = [list(x) for x in row]
    #         repairing_data = []
    #         for i in row:
    #             repairing_data.append(list(i))
    #
    #     try:
    #         del request.session['start_date']
    #         del request.session['end_date']
    #         del request.session['string']
    #         del request.session['selected_list']
    #     except:
    #         pass
    # if table_name == 'Payment Details Form':
    #     # customer_list = Lead_Customer_Details.objects.filter(entry_timedate__range=(start_date, end_date)).values_list(string)
    #     with connection.cursor() as cursor:
    #         if string != '' :
    #                 cursor.execute("SELECT " +  string + " from lead_management_payment_details  PRODUCT  where "
    #                 " entry_timedate between'" + start_date + "' and '" + end_date + "';")
    #                 row = cursor.fetchall()
    #                 final_row_product = [list(x) for x in row]
    #                 repairing_data = []
    #                 for i in row:
    #                     repairing_data.append(list(i))
    #
    #                 final_row = [list(x) for x in row]
    #                 repairing_data = []
    #                 for i in row:
    #                     repairing_data.append(list(i))
    #
    #     try:
    #         del request.session['start_date']
    #         del request.session['end_date']
    #         del request.session['string']
    #         del request.session['selected_list']
    #     except:
    #         pass

    try:
        del request.session['start_date']
        del request.session['end_date']
        del request.session['string_cust_detail']
        del request.session['string_deal_detail']
        del request.session['string_pi_history']
        del request.session['string_follow_up']
        del request.session['string_pay_detail']
    except:
        pass
    context={
        'final_row':final_row,
        'final_row_product':final_row_product,
        'selected_list':selected_list,
    }
    return render(request,"report/final_lead_report.html",context)

@login_required(login_url='/')
def final_lead_report_test(request):
    start_date = request.session.get('start_date')
    end_date = request.session.get('end_date')
    # start_date = '2020-05-01'
    # end_date = '2020-05-15'

    string_cust_detail = request.session.get('string_cust_detail')
    string_cust_detail_list = request.session.get('string_cust_detail_list')
    string_deal_detail = request.session.get('string_deal_detail')
    string_deal_detail_list = request.session.get('string_deal_detail_list')
    string_pi_history = request.session.get('string_pi_history')
    string_pi_history_list = ['pi_history_file', 'entry_timedate_time', 'call_detail', 'medium_of_selection']
    string_follow_up = request.session.get('string_follow_up')
    string_follow_up_list = ['wa_no', 'wa_msg', 'email_subject', 'email_msg', 'followup_history_file', 'sms_msg', 'call_response']
    string_pay_detail = request.session.get('string_pay_detail')
    string_pay_detail_list = request.session.get('string_pay_detail_list')
    if  string_cust_detail_list:
        string_cust_detail_list=['id'] + string_cust_detail_list
    if  string_deal_detail_list:
        string_deal_detail_list=['id'] + string_deal_detail_list
    if string_pay_detail != '':
        string_pay_detail_list=['lead_id_id'] +string_pay_detail_list
    context ={}

    from .models import Pi_section
    # cust_list = Lead_Customer_Details.objects.filter(entry_timedate__range=(start_date, end_date)).values(*string_cust_detail_list)
    # if string_deal_detail_list and  string_pi_history != '':

    if string_follow_up != '' and string_pi_history != '' and string_pay_detail != '' and string_cust_detail_list and string_deal_detail_list:

        lead_list = Lead.objects.filter(entry_timedate__range=(start_date, end_date)).values(*string_deal_detail_list)

        for lead in lead_list:
            # names3 = Payment_details.objects.filter(lead_id_id__in=lead_list.values('id')).values(*string_pay_detail_list)
            # for item in names3:
            #     if lead['id'] == item['lead_id_id']:
            #         lead.update(item)
            # print(lead)

            if 'owner_of_opportunity_id' in lead_list :
                lead['owner_of_opportunity_id'] = SiteUser.objects.get(id=lead['owner_of_opportunity_id']).profile_name

            # if   Lead.objects.get(id=lead['id']).upload_requirement_file:
            #     lead['upload_requirement_file'] = Lead.objects.get(id=lead['id']).upload_requirement_file.path
            names = Pi_History.objects.filter(lead_id_id=lead['id']).values()
            names2 = History_followup.objects.filter(lead_id_id=lead['id']).values()
            names3 = Payment_details.objects.filter(lead_id_id__in=lead_list.values('id')).values(*string_pay_detail_list)
            names4 = Lead_Customer_Details.objects.filter(id__in=lead_list.values('customer_id__id')).values(*string_cust_detail_list)

            lead['pi_history'] = list(names)
            lead['followup_history'] = list(names2)
            lead['payment_details'] = list(names3)
            lead['customer_details'] = list(names4)

    elif string_follow_up != '' and string_pi_history != '' and string_pay_detail != ''  and string_deal_detail_list:
        lead_list = Lead.objects.filter(entry_timedate__range=(start_date, end_date)).values(*string_deal_detail_list)

        for lead in lead_list:
            if 'owner_of_opportunity_id' in lead_list :
                lead['owner_of_opportunity_id'] = SiteUser.objects.get(id=lead['owner_of_opportunity_id']).profile_name
            elif   Lead.objects.get(id=lead['id']).upload_requirement_file:
                lead['upload_requirement_file'] = Lead.objects.get(id=lead['id']).upload_requirement_file.path
            names = Pi_History.objects.filter(lead_id_id=lead['id']).values()
            names2 = History_followup.objects.filter(lead_id_id=lead['id']).values()
            names3 = Payment_details.objects.filter(lead_id_id__in=lead_list.values('id')).values(*string_pay_detail_list)

            lead['pi_history'] = list(names)
            lead['followup_history'] = list(names2)
            lead['payment_details'] = list(names3)

    elif string_follow_up != '' and string_pi_history != ''   and string_deal_detail_list:
        lead_list = Lead.objects.filter(entry_timedate__range=(start_date, end_date)).values(*string_deal_detail_list)

        for lead in lead_list:
            if 'owner_of_opportunity_id' in lead_list :
                lead['owner_of_opportunity_id'] = SiteUser.objects.get(id=lead['owner_of_opportunity_id']).profile_name
            elif   Lead.objects.get(id=lead['id']).upload_requirement_file:
                lead['upload_requirement_file'] = Lead.objects.get(id=lead['id']).upload_requirement_file.path
            names = Pi_History.objects.filter(lead_id_id=lead['id']).values()
            names2 = History_followup.objects.filter(lead_id_id=lead['id']).values()

            lead['pi_history'] = list(names)
            lead['followup_history'] = list(names2)

    elif  string_pi_history != ''   and string_deal_detail_list:
        lead_list = Lead.objects.filter(entry_timedate__range=(start_date, end_date)).values(*string_deal_detail_list)

        for lead in lead_list:
            if 'owner_of_opportunity_id' in lead_list :
                lead['owner_of_opportunity_id'] = SiteUser.objects.get(id=lead['owner_of_opportunity_id']).profile_name
            elif   Lead.objects.get(id=lead['id']).upload_requirement_file:
                lead['upload_requirement_file'] = Lead.objects.get(id=lead['id']).upload_requirement_file.path
            names = Pi_History.objects.filter(lead_id_id=lead['id']).values()

            lead['pi_history'] = list(names)

    elif string_follow_up != ''  and string_deal_detail_list:
        lead_list = Lead.objects.filter(entry_timedate__range=(start_date, end_date)).values(*string_deal_detail_list)

        for lead in lead_list:
            if 'owner_of_opportunity_id' in lead_list :
                lead['owner_of_opportunity_id'] = SiteUser.objects.get(id=lead['owner_of_opportunity_id']).profile_name
            elif   Lead.objects.get(id=lead['id']).upload_requirement_file:
                lead['upload_requirement_file'] = Lead.objects.get(id=lead['id']).upload_requirement_file.path
            names2 = History_followup.objects.filter(lead_id_id=lead['id']).values()

            lead['followup_history'] = list(names2)

    elif string_deal_detail_list:
        lead_list = Lead.objects.filter(entry_timedate__range=(start_date, end_date)).values(*string_deal_detail_list)
        for lead in lead_list:
            # names = Pi_section.objects.filter(lead_id_id=lead['id']).values()
            if 'owner_of_opportunity_id' in lead_list :
                lead['owner_of_opportunity_id'] = SiteUser.objects.get(id=lead['owner_of_opportunity_id'])
            if  'upload_requirement_file' in lead_list  and Lead.objects.get(id=lead['id']).upload_requirement_file:
                lead['upload_requirement_file'] = Lead.objects.get(id=lead['id']).upload_requirement_file.path


    elif string_pi_history != '':
        lead_list = Lead.objects.filter(entry_timedate__range=(start_date, end_date)).values('id')
        for lead in lead_list:
            names = Pi_History.objects.filter(lead_id_id=lead['id']).values(*string_pi_history_list)
            lead['pi_history'] = list(names)

    elif string_follow_up != '':

        lead_list = Lead.objects.filter(entry_timedate__range=(start_date, end_date)).values('id')
        for lead in lead_list:
            names =  History_followup.objects.filter(lead_id_id=lead['id']).values(*string_follow_up_list)
            lead['followup_history'] = list(names)

    elif string_pay_detail != '':

        lead_list = Lead.objects.filter(entry_timedate__range=(start_date, end_date)).values('id')
        for lead in lead_list:
            names =  Payment_details.objects.filter(lead_id_id=lead['id']).values(*string_pay_detail_list)
            lead['payment_details'] = list(names)
        pay_detail_list = Lead.objects.filter(entry_timedate__range=(start_date, end_date)).values('id')

    elif string_cust_detail_list != '':
        lead_list = Lead_Customer_Details.objects.filter(entry_timedate__range=(start_date, end_date)).values(*string_cust_detail_list)
    context1 = {
        'lead_list': lead_list,
    }
    context.update(context1)
    # if string_deal_detail_list:
    #     deal_detail_list = Lead.objects.filter(entry_timedate__range=(start_date, end_date)).values(*string_deal_detail_list)
    #     for lead in deal_detail_list:
    #         # names = Pi_section.objects.filter(lead_id_id=lead['id']).values()
    #         if 'owner_of_opportunity_id' in deal_detail_list :
    #             lead['owner_of_opportunity_id'] = SiteUser.objects.get(id=lead['owner_of_opportunity_id'])
    #         if  'upload_requirement_file' in deal_detail_list  and Lead.objects.get(id=lead['id']).upload_requirement_file:
    #             lead['upload_requirement_file'] = Lead.objects.get(id=lead['id']).upload_requirement_file.path
    #
    # if string_cust_detail_list != '':
    #     cust_list = Lead_Customer_Details.objects.filter(entry_timedate__range=(start_date, end_date)).values(*string_cust_detail_list)
    #
    # if string_pi_history != '':
    #     pi_history_list = Lead.objects.filter(entry_timedate__range=(start_date, end_date)).values('id')
    #     for lead in pi_history_list:
    #         names = Pi_History.objects.filter(lead_id_id=lead['id']).values(*string_pi_history_list)
    #         lead['pi_history'] = list(names)
    #
    # if string_follow_up != '':
    #
    #     follow_up_list = Lead.objects.filter(entry_timedate__range=(start_date, end_date)).values('id')
    #     for lead in follow_up_list:
    #         names =  History_followup.objects.filter(lead_id_id=lead['id']).values(*string_follow_up_list)
    #         print(names)
    #         lead['followup_history'] = list(names)
    #
    # if string_pay_detail != '':
    #
    #     pay_detail_list = Lead.objects.filter(entry_timedate__range=(start_date, end_date)).values('id')
    #     for lead in pay_detail_list:
    #         names =  Payment_details.objects.filter(lead_id_id=lead['id']).values(*string_pay_detail_list)
    #         lead['payment_detail'] = list(names)
    #
    # if string_deal_detail_list and string_cust_detail_list != '' :
    #
    #     from itertools import chain
    #     # lead_list = list(chain(deal_detail_list, cust_list))
    #
    #     context1 = {
    #         'lead_list': lead_list,
    #     }
    #     context.update(context1)
    # elif string_pi_history != '' and string_follow_up != '' :
    #
    #     from itertools import chain
    #     # lead_list = list(chain(pi_history_list, follow_up_list))
    #
    #
    #     context1 = {
    #         'lead_list': lead_list,
    #     }
    #     context.update(context1)
    # elif string_pi_history != '':
    #     lead_list = pi_history_list
    #     context1 = {
    #         'lead_list': lead_list,
    #     }
    #     context.update(context1)
    # elif string_follow_up != '':
    #     lead_list = follow_up_list
    #     context1 = {
    #         'lead_list': lead_list,
    #     }
    #     context.update(context1)
    # elif string_pay_detail != '':
    #     lead_list = pay_detail_list
    #     context1 = {
    #         'lead_list': lead_list,
    #     }
    #     context.update(context1)
    # elif string_cust_detail_list != '':
    #     lead_list = cust_list
    #     context1 = {
    #         'lead_list': lead_list,
    #     }
    #     context.update(context1)
    # try:
    #     del request.session['start_date']
    #     del request.session['end_date']
    #     del request.session['string_cust_detail']
    #     del request.session['string_deal_detail']
    #     del request.session['string_pi_history']
    #     del request.session['string_follow_up']
    #     del request.session['string_pay_detail']
    # except:
    #     pass


    return render(request,"report/final_lead_report_test.html",context)


@login_required(login_url='/')
def select_product_followup(request,id):
    type_of_purchase_list =type_purchase.objects.all() #1
    lead_id = Lead.objects.get(id=id)
    # products = Product.objects.all()
    context={}
    del_all_sessions(request)
    request.session['expand_followup'] = True
    if request.method == 'POST' or request.method == 'FILES' :
        if 'submit' in request.POST:
            is_last_product_yes = request.POST.get('is_last_product_yes')
            model_of_purchase_str = request.POST.get('model_of_purchase')
            type_of_scale_str = request.POST.get('type_of_scale')
            sub_model_str = request.POST.get('sub_model')
            sub_sub_model_str = request.POST.get('sub_sub_model')
            try:
                if (sub_sub_model_str == None or sub_sub_model_str == ""):
                    print('first')
                    product_avail = Product.objects.get(scale_type__id=type_purchase.objects.get(id=type_of_scale_str).id, main_category__id=main_model.objects.get(id=model_of_purchase_str).id,
                                                 sub_category__id=sub_model.objects.get(id=sub_model_str).id, sub_sub_category=None)
                    print(product_avail)
                    print(product_avail)
                    print(product_avail)
                elif (sub_sub_model_str != None or sub_sub_model_str != ""):
                    print('second')
                    product_avail = Product.objects.get(scale_type__id=type_purchase.objects.get(id=type_of_scale_str).id, main_category__id=main_model.objects.get(id=model_of_purchase_str).id,
                                                 sub_category__id=sub_model.objects.get(id=sub_model_str).id, sub_sub_category__id=sub_sub_model.objects.get(id=sub_sub_model_str).id)
                requested_product = product_avail
                fol_pro = Followup_product()
                fol_pro.product_id = requested_product
                fol_pro.lead_id = Lead.objects.get(id=id)
                fol_pro.scale_type = requested_product.scale_type
                fol_pro.main_category = requested_product.main_category
                fol_pro.sub_category = requested_product.sub_category
                fol_pro.sub_sub_category = requested_product.sub_sub_category
                fol_pro.hsn_code = requested_product.hsn_code
                fol_pro.max_capacity = requested_product.max_capacity
                fol_pro.accuracy = requested_product.accuracy
                fol_pro.platform_size = requested_product.platform_size
                fol_pro.product_desc = requested_product.product_desc
                fol_pro.cost_price = requested_product.cost_price
                fol_pro.selling_price = requested_product.selling_price
                fol_pro.carton_size = requested_product.carton_size
                fol_pro.log_entered_by = request.user.name

                fol_pro.save()


                context23 = {
                    'product_avail': True,
                }
                context.update(context23)

            except Exception as e:
                print(e)
                messages.success(request, "Selected Product does not exist in product master !!!")

                return redirect('/select_product_followup/' + str(id))
            if is_last_product_yes == 'yes':
                return redirect('/update_view_lead/' + str(id))
            elif is_last_product_yes == 'no':
                return redirect('/select_product_followup/' + str(id))

    context2={
        'lead_id':lead_id,
        'type_purchase':type_of_purchase_list,

    }
    context.update(context2)
    return render(request,'lead_management/select_product_followup.html', context)

def upload_requirement_hsc(request):
    context={}
    if request.method == 'POST' or request.method == 'FILES':
        customer_name = request.POST.get('full_name')
        contact_no = request.POST.get('phone_no')
        customer_email_id = request.POST.get('email_id')

        requirement = request.POST.get('requirement')
        company_name = request.POST.get('company_name')
        upload_requirement_file = request.FILES.get('req_file')

        item2 = Lead()
        if Lead_Customer_Details.objects.filter(customer_name=customer_name,
                                           contact_no=contact_no).count() > 0:


            item2.customer_id = Lead_Customer_Details.objects.filter(contact_no=contact_no).first()

            item3 = Lead_Customer_Details.objects.filter(customer_name=customer_name,
                                                    contact_no=contact_no).first()

            if customer_email_id != '' and customer_email_id != None:
                item3.customer_email_id = customer_email_id
                item3.save(update_fields=['customer_email_id'])
            if company_name != '' :
                item3.company_name = company_name
                item3.save(update_fields=['company_name'])

            item2.new_existing_customer = 'New'


        else:
            new_cust = Lead_Customer_Details()

            new_cust.customer_name = customer_name

            new_cust.contact_no = contact_no
            if customer_email_id != '':
                new_cust.customer_email_id = customer_email_id
            if company_name != '' :
                new_cust.company_name = company_name
            try:
                new_cust.save()
                item2.customer_id = Lead_Customer_Details.objects.get(id=new_cust.pk)
            except Exception as e:
                context22 = {
                    'error_65': str(e),
                    'error_exist_65': True,
                }

                context.update(context22)
            item2.new_existing_customer = 'Existing'


        item2.current_stage = 'Not Yet Initiated'
        from datetime import datetime


        item2.date_of_initiation = datetime.today().strftime('%Y-%m-%d')
        item2.channel = 'Website'
        item2.requirement = requirement
        item2.requirement_indiamart_unique = requirement[:115]
        item2.upload_requirement_file = upload_requirement_file
        if SiteUser.objects.filter(modules_assigned__icontains='Hsco Website Leads',role='Employee').count()>0:
            item2.owner_of_opportunity = SiteUser.objects.filter(modules_assigned__icontains='Hsco Website Leads',
                                                                 role='Employee').first()

            item2.log_entered_by = SiteUser.objects.filter(modules_assigned__icontains='Hsco Website Leads',
                                                           role='Employee').first().name
        elif SiteUser.objects.filter(modules_assigned__icontains='Hsco Website Leads',role='Manager').count()>0:
            item2.owner_of_opportunity = SiteUser.objects.filter(modules_assigned__icontains='Hsco Website Leads',
                                                                 role='Manager').first()

            item2.log_entered_by = SiteUser.objects.filter(modules_assigned__icontains='Hsco Website Leads',
                                                           role='Manager').first().name
        else:
            item2.owner_of_opportunity = SiteUser.objects.filter(modules_assigned__icontains='Hsco Website Leads',role='Admin').first()

            item2.log_entered_by = SiteUser.objects.filter(modules_assigned__icontains='Hsco Website Leads',role='Admin').first().name


        try:
            item2.save()

            fp = Follow_up_section()
            fp.lead_id = Lead.objects.get(id=item2.pk)
            fp.save()
            context22 = {
                'success_65': "Thank You For Interest, Our Team Will Get In Touch With You Soon!!!",
                'success_exist_65': True,
            }

            context.update(context22)


        except Exception as e:
            context22 = {
                'error_65': str(e),
                'error_exist_65': True,
            }

            context.update(context22)
        #return redirect('/requirement.hindustanscale.com/')


    return render(request,'lead_management/upload_requirement_hsc.html',context)


@login_required(login_url='/')
def select_product(request,id):
    type_of_purchase_list =type_purchase.objects.all() #1
    lead_id = Lead.objects.get(id=id)
    products = Product.objects.all()
    context={}
    del_all_sessions(request)
    request.session['expand_pi_section'] = True
    if request.method == 'POST' or request.method == 'FILES':
        hsn_code = request.POST.get('hsn_code')
        pf = request.POST.get('pf')
        quantity = request.POST.get('quantity')
        is_last_product_yes = request.POST.get('is_last_product_yes')
        # model_of_purchase = request.POST.get('model_of_purchase')
        rate = request.POST.get('rate')
        type_of_scale = request.POST.get('scale_type')
        main_category = request.POST.get('main_category')
        sub_category = request.POST.get('sub_category')
        sub_sub_category = request.POST.get('sub_sub_category')    #product code or sub_sub_category

        item = Pi_product()
        # if sub_sub_category != '':
        #     item.product_id = Product.objects.get(scale_type=type_of_scale, main_category=main_category,
        #                                           sub_category=sub_category, sub_sub_category=sub_sub_category)
        try:
            if (sub_sub_category != None and sub_sub_category != ""):
                item.product_id = Product.objects.get(scale_type=type_of_scale, main_category=main_category,
                                                      sub_category=sub_category, sub_sub_category=sub_sub_category)
                item.lead_id = Lead.objects.get(id=lead_id)
                item.quantity = quantity
                item.pf = pf
                item.log_entered_by = request.user.name
                if quantity != 'None' or quantity != '':
                    item.product_total_cost = float(rate) * float(quantity)
                item.save()
            elif (sub_category != None and sub_category != ""):
                item.product_id = Product.objects.get(scale_type=type_of_scale, main_category=main_category,
                                                      sub_category=sub_category, sub_sub_category=None)
                item.lead_id = Lead.objects.get(id=lead_id)
                item.quantity = quantity
                item.pf = pf
                item.log_entered_by = request.user.name
                if quantity != 'None' or quantity != '':
                    item.product_total_cost = float(rate) * float(quantity)
                item.save()

            if is_last_product_yes == 'yes':
                return redirect('/update_view_lead/' + str(id))
            elif is_last_product_yes == 'no':
                return redirect('/select_product/' + str(id))
        except:
            msg = "Selected Product does not exist in product master !!!"
            context1={
                'msg':msg,
            }
            context.update(context1)
        del_all_sessions(request)
        request.session['expand_pi_section'] = True


    context2 = {
        'lead_id': lead_id,
        'type_of_purchase_list': type_of_purchase_list,
        'products': products,
    }
    context.update(context2)
    return render(request, 'lead_management/select_product.html', context)

@login_required(login_url='/')
def lead_manager_view(request):
    loggedin_user = SiteUser.objects.get(id=request.user.id).name
    u_list=Pi_section.objects.filter(lead_id__owner_of_opportunity__admin=loggedin_user).values_list("lead_id__owner_of_opportunity").distinct()
    users_list = []
    for item in u_list:
        for ite in item:
            users_list.append(ite)
    currentMonth = datetime.now().month
    result_list=[]
    from itertools import chain
    for item in users_list:
        pi_list=Pi_section.objects.filter(lead_id__owner_of_opportunity__id=item,entry_timedate__month=currentMonth).distinct().extra(select={
            'converted': "select SUM(grand_total) from lead_management_pi_section INNER JOIN lead_management_lead on "
                         "lead_management_lead.id=lead_management_pi_section.lead_id_id INNER JOIN user_app_siteuser on "
                         "user_app_siteuser.id=lead_management_lead.owner_of_opportunity_id where user_app_siteuser.id='"+str(item)+"' "
                         "and lead_management_lead.current_stage = 'PO Issued - Payment Done - Dispatch Pending'",
            'lost': "select SUM(grand_total) from lead_management_pi_section INNER JOIN lead_management_lead on "
                         "lead_management_lead.id=lead_management_pi_section.lead_id_id INNER JOIN user_app_siteuser on "
                         "user_app_siteuser.id=lead_management_lead.owner_of_opportunity_id where user_app_siteuser.id='" + str(
                item) + "' "
                        "and lead_management_lead.current_stage = 'Lost'",
            'postponed': "select SUM(grand_total) from lead_management_pi_section INNER JOIN lead_management_lead on "
                         "lead_management_lead.id=lead_management_pi_section.lead_id_id INNER JOIN user_app_siteuser on "
                         "user_app_siteuser.id=lead_management_lead.owner_of_opportunity_id where user_app_siteuser.id='" + str(
                item) + "' "
                        "and lead_management_lead.current_stage = 'Postponed'",

        }).values_list('lead_id__owner_of_opportunity__profile_name', 'converted', 'lost', 'postponed')
        result_list.append(list(chain(pi_list,)))

    context={
        'pi_list':result_list,
    }
    return render(request,'lead_management/lead_manager.html',context)


@login_required(login_url='/')
def lead_follow_up_histroy(request,follow_up_id):
    context={}
    obj_list = History_followup.objects.filter(follow_up_section=follow_up_id).order_by("-entry_timedate")
    del_all_sessions(request)
    request.session['expand_followup'] = True
    if request.method == 'POST':
        if 'sub1' in request.POST:
            delete_id = request.POST.get('delete_id')

            Auto_followup_details.objects.filter(follow_up_history__pk=delete_id).delete()
            History_followup.objects.filter(id=delete_id).update(is_auto_follow_deleted=True)
            Lead.objects.filter(id=Follow_up_section.objects.get(id=History_followup.objects.get(id=delete_id).follow_up_section).lead_id).update(is_manual_mode_followup=True)
            obj_list = History_followup.objects.filter(follow_up_section=follow_up_id).order_by("-entry_timedate")
            Follow_up_section.objects.filter(id=History_followup.objects.get(id=delete_id).follow_up_section.pk).update(auto_manual_mode='Select Mode')
            context2 = {
                'obj_list': obj_list,
                'is_deleted': True,
                'msg': 'Auto Follow-up Cancelled Successfully',
            }
            context.update(context2)



    context23={
        'obj_list':obj_list,
    }
    context.update(context23)

    return render(request,'lead_management/follow_up_history.html',context)

@login_required(login_url='/')
def pi_section_history(request,id):
    try:
        lead_id = Lead.objects.get(id=id)
        # lead_pi_id = Pi_section.objects.get(lead_id=id)
        lead_pi_history = Pi_History.objects.filter(lead_id=id).order_by('-id')
        del_all_sessions(request)

        request.session['expand_pi_section'] = True
        context = {
            'lead_id': lead_id,
            'lead_pi_history': lead_pi_history,
        }
    except:
        pass
    return render(request,'lead_management/lead_history.html',context)

@login_required(login_url='/')
def lead_delete_product(request,id):
    leads = Pi_product.objects.filter(lead_id=id).order_by('-id')
    if request.method == 'POST' or request.method=='FILES':
        delete_id = request.POST.getlist('check[]')
        for i in delete_id:
            Pi_product.objects.filter(id=i).delete()

        del_all_sessions(request)

        request.session['expand_pi_section'] = True

        return redirect('/update_view_lead/'+str(id))
    context={
        'leads':leads,
    }
    return render(request,'lead_management/lead_delete_product.html',context)

@login_required(login_url='/')
def followup_delete_product(request,id):
    followup_products_list = Followup_product.objects.filter(lead_id=id)
    if request.method == 'POST' :
        delete_id = request.POST.getlist('check[]')
        for i in delete_id:
            Followup_product.objects.filter(id=i).delete()

        del_all_sessions(request)

        request.session['expand_followup'] = True

        return redirect('/update_view_lead/'+str(id))
    context={
        'followup_products_list':followup_products_list,
    }
    return render(request,'lead_management/followup_delete_product.html',context)

@login_required(login_url='/')
def lead_analytics(request):
    try:
        highest_lead_day_list = Pi_section.objects.filter().values('entry_timedate').order_by('entry_timedate').annotate(data_sum=Sum('grand_total'))
        print(highest_lead_day_list)
        maxPricedItem = max(highest_lead_day_list, key=lambda x: x['data_sum'])
        minPricedItem = min(highest_lead_day_list, key=lambda x: x['data_sum'])

        context={
            'maxPricedItem':maxPricedItem,
            'minPricedItem':minPricedItem,
        }

        mon = (datetime.now().month)
        if mon == 1:
            previous_mon = 12
        else:
            previous_mon = (datetime.now().month) - 1

        #this month lead
        current_month_lead = Pi_section.objects.filter(lead_id__current_stage='PO Issued - Payment Done - Dispatch Pending',
                                                    entry_timedate__month=datetime.now().month) \
            .values('entry_timedate').annotate(data_sum=Sum('grand_total'))


        #previous month lead
        previous_month_lead = Pi_section.objects.filter(lead_id__current_stage='PO Issued - Payment Done - Dispatch Pending',
                                                       entry_timedate__month=previous_mon) \
            .values('entry_timedate').annotate(data_sum=Sum('grand_total'))

        if request.method=='POST'   :
            if 'date1' in request.POST :
                start_date = request.POST.get('date1')
                lead_conversion = Pi_section.objects.filter(lead_id__current_stage='PO Issued - Payment Done - Dispatch Pending',
                                                            entry_timedate__month=datetime.strptime(start_date, '%Y-%m-%d').month) \
                    .values('entry_timedate').annotate(data_sum=Sum('grand_total'))

                lead_conversion_date = []
                lead_conversion_sum = []
                for i in lead_conversion:
                    x = i
                    lead_conversion_date.append(x['entry_timedate'].strftime('%Y-%m-%d'))
                    lead_conversion_sum.append(x['data_sum'])


                context = {

                    'lead_conversion_date': lead_conversion_date,
                    'lead_conversion_sum': lead_conversion_sum,

                }
            if 'sub1' in request.POST:
                # this month lead
                current_month_lead = Pi_section.objects.filter(
                    lead_id__current_stage='Not Yet Initiated',
                    entry_timedate__month=datetime.now().month) \
                    .values('entry_timedate').annotate(data_sum=Count('grand_total'))

                # previous month lead
                previous_month_lead = Pi_section.objects.filter(
                    lead_id__current_stage='Not Yet Initiated',
                    entry_timedate__month=previous_mon) \
                    .values('entry_timedate').annotate(data_sum=Count('grand_total'))
            elif 'sub2' in request.POST:
                # this month lead
                current_month_lead = Pi_section.objects.filter(
                    lead_id__current_stage='Customer Called',
                    entry_timedate__month=datetime.now().month) \
                    .values('entry_timedate').annotate(data_sum=Count('grand_total'))

                # previous month lead
                previous_month_lead = Pi_section.objects.filter(
                    lead_id__current_stage='Customer Called',
                    entry_timedate__month=previous_mon) \
                    .values('entry_timedate').annotate(data_sum=Count('grand_total'))
            elif 'sub3' in request.POST:
                # this month lead
                current_month_lead = Pi_section.objects.filter(
                    lead_id__current_stage='PI Sent & Follow-up',
                    entry_timedate__month=datetime.now().month) \
                    .values('entry_timedate').annotate(data_sum=Sum('grand_total'))

                # previous month lead
                previous_month_lead = Pi_section.objects.filter(
                    lead_id__current_stage='PI Sent & Follow-up',
                    entry_timedate__month=previous_mon) \
                    .values('entry_timedate').annotate(data_sum=Sum('grand_total'))
            elif 'sub4' in request.POST:
                # this month lead
                current_month_lead = Pi_section.objects.filter(
                    lead_id__current_stage='PO Issued - Payment not done',
                    entry_timedate__month=datetime.now().month) \
                    .values('entry_timedate').annotate(data_sum=Sum('grand_total'))

                # previous month lead
                previous_month_lead = Pi_section.objects.filter(
                    lead_id__current_stage='PO Issued - Payment not done',
                    entry_timedate__month=previous_mon) \
                    .values('entry_timedate').annotate(data_sum=Sum('grand_total'))
            elif 'sub5' in request.POST:
                # this month lead
                current_month_lead = Pi_section.objects.filter(
                    lead_id__current_stage='PO Issued - Payment Done - Dispatch Pending',
                    entry_timedate__month=datetime.now().month) \
                    .values('entry_timedate').annotate(data_sum=Sum('grand_total'))

                # previous month lead
                previous_month_lead = Pi_section.objects.filter(
                    lead_id__current_stage='PO Issued - Payment Done - Dispatch Pending',
                    entry_timedate__month=previous_mon) \
                    .values('entry_timedate').annotate(data_sum=Sum('grand_total'))
            elif 'sub6' in request.POST:
                # this month lead
                current_month_lead = Pi_section.objects.filter(
                    lead_id__current_stage='Dispatch Done - Closed',
                    entry_timedate__month=datetime.now().month) \
                    .values('entry_timedate').annotate(data_sum=Sum('grand_total'))

                # previous month lead
                previous_month_lead = Pi_section.objects.filter(
                    lead_id__current_stage='Dispatch Done - Closed',
                    entry_timedate__month=previous_mon) \
                    .values('entry_timedate').annotate(data_sum=Sum('grand_total'))
            elif 'sub7' in request.POST:
                # this month lead
                current_month_lead = Pi_section.objects.filter(
                    lead_id__current_stage='Lost',
                    entry_timedate__month=datetime.now().month) \
                    .values('entry_timedate').annotate(data_sum=Sum('grand_total'))

                # previous month lead
                previous_month_lead = Pi_section.objects.filter(
                    lead_id__current_stage='Lost',
                    entry_timedate__month=previous_mon) \
                    .values('entry_timedate').annotate(data_sum=Sum('grand_total'))
            elif 'sub8' in request.POST:
                # this month lead
                current_month_lead = Pi_section.objects.filter(
                    lead_id__current_stage='Not Relevant',
                    entry_timedate__month=datetime.now().month) \
                    .values('entry_timedate').annotate(data_sum=Sum('grand_total'))

                # previous month lead
                previous_month_lead = Pi_section.objects.filter(
                    lead_id__current_stage='Not Relevant',
                    entry_timedate__month=previous_mon) \
                    .values('entry_timedate').annotate(data_sum=Sum('grand_total'))
            elif 'sub9' in request.POST:
                # this month lead
                current_month_lead = Pi_section.objects.filter(
                    lead_id__current_stage='Postponed',
                    entry_timedate__month=datetime.now().month) \
                    .values('entry_timedate').annotate(data_sum=Sum('grand_total'))

                # previous month lead
                previous_month_lead = Pi_section.objects.filter(
                    lead_id__current_stage='Postponed',
                    entry_timedate__month=previous_mon) \
                    .values('entry_timedate').annotate(data_sum=Sum('grand_total'))


        if request.user.role == 'Super Admin':
            total_stages = Lead.objects.all().values('current_stage').annotate(dcount=Count('current_stage'))
        else:
            admin = SiteUser.objects.get(id=request.user.pk).admin
            total_stages = Lead.objects.filter(Q(owner_of_opportunity__admin=admin)).values('current_stage').annotate(dcount=Count('current_stage'))
        admin = SiteUser.objects.get(id=request.user.pk).admin


        po_no_payment = Pi_section.objects.filter(lead_id__current_stage='PO Issued - Payment not done',
                                                   lead_id__owner_of_opportunity__admin=admin).values(
            'grand_total').annotate(data_sum=Sum('grand_total'))
        po_no_payment_total = 0.0
        try:
            for x in po_no_payment:
                po_no_payment_total += float(x['data_sum'])
        except:
            pass

        po_payment_done = Pi_section.objects.filter(lead_id__current_stage='PO Issued - Payment Done - Dispatch Pending',
                                                   lead_id__owner_of_opportunity__admin=admin).values(
            'grand_total').annotate(data_sum=Sum('grand_total'))
        po_payment_done_total = 0.0
        try:
            for x in po_payment_done:
                po_payment_done_total += float(x['data_sum'])
        except:
            pass

        dispatch_done_stage = Pi_section.objects.filter(lead_id__current_stage='Dispatch Done - Closed',
                                                   lead_id__owner_of_opportunity__admin=admin).values(
            'grand_total').annotate(data_sum=Sum('grand_total'))
        dispatch_done_stage_total = 0.0
        try:
            for x in dispatch_done_stage:
                dispatch_done_stage_total += float(x['data_sum'])
        except:
            pass
        lost_stage = Pi_section.objects.filter(lead_id__current_stage='Lost',
                                                   lead_id__owner_of_opportunity__admin=admin).values(
            'grand_total').annotate(data_sum=Sum('grand_total'))
        lost_stage_total = 0.0
        try:
            for x in lost_stage:
                lost_stage_total += float(x['data_sum'])
        except:
            pass
        not_relevant_stage = Pi_section.objects.filter(lead_id__current_stage='Not Relevant',
                                                   lead_id__owner_of_opportunity__admin=admin).values(
            'grand_total').annotate(data_sum=Sum('grand_total'))
        not_relevant_stage_total = 0.0
        try:
            for x in not_relevant_stage:
                not_relevant_stage_total += float(x['data_sum'])
        except:
            pass
        postponed_stage = Pi_section.objects.filter(lead_id__current_stage='Postponed',
                                                   lead_id__owner_of_opportunity__admin=admin).values(
            'grand_total').annotate(data_sum=Sum('grand_total'))
        postponed_stage_total = 0.0
        try:
            for x in postponed_stage:
                postponed_stage_total += float(x['data_sum'])
        except:
            pass
        pi_sent_stage = Pi_section.objects.filter(lead_id__current_stage='PI Sent & Follow-up',
                                                   lead_id__owner_of_opportunity__admin=admin).values(
            'grand_total').annotate(data_sum=Sum('grand_total'))
        pi_sent_stage_total = 0.0
        try:
            for x in pi_sent_stage:
                pi_sent_stage_total += float(x['data_sum'])
        except:
            pass
        context13={
            'po_no_payment_total': po_no_payment_total,
            'lost_stage_total': lost_stage_total,
            'po_payment_done_total': po_payment_done_total,
            'dispatch_done_stage_total': dispatch_done_stage_total,
            'not_relevant_stage_total': not_relevant_stage_total,
            'postponed_stage_total': postponed_stage_total,
            'pi_sent_stage_total': pi_sent_stage_total,
        }
        context.update(context13)

        for i in total_stages:
            x = i
            if x['current_stage'] == 'Not Yet Initiated':
                not_yet_stage = x['dcount']
                context1 = {
                    'not_yet_stage': not_yet_stage,
                }
                context.update(context1)
            if x['current_stage'] == 'Dispatch Done - Closed':
                dispatch_stage = x['dcount']
                context2 = {
                    'dispatch_stage': dispatch_stage,
                }
                context.update(context2)
            if x['current_stage'] == 'Customer Called':
                cust_called_stage = x['dcount']
                context3 = {
                    'cust_called_stage': cust_called_stage,
                }
                context.update(context3)
            if x['current_stage'] == 'PO Issued - Payment not done':
                po_no_payment = x['dcount']
                context5 = {
                    'po_no_payment': po_no_payment,
                }
                context.update(context5)
            if x['current_stage'] == 'PO Issued - Payment Done - Dispatch Pending':
                po_payment_done = x['dcount']
                context4 = {
                    'po_payment_done': po_payment_done,
                }
                context.update(context4)
            if x['current_stage'] == 'Lost':
                lost_stage = x['dcount']
                context6 = {
                    'lost_stage': lost_stage,
                }
                context.update(context6)
            if x['current_stage'] == 'Not Relevant':
                not_relevant_stage = x['dcount']
                context7 = {
                    'not_relevant_stage': not_relevant_stage,
                }
                context.update(context7)
            if x['current_stage'] == 'Postponed':
                postponed_stage = x['dcount']
                context8 = {
                    'postponed_stage': postponed_stage,
                }
                context.update(context8)
            if x['current_stage'] == 'PI Sent & Follow-up':
                pi_sent_stage = x['dcount']
                context9 = {
                    'pi_sent_stage': pi_sent_stage,
                }
                context.update(context9)
        previous_month_lead_date = []
        previous_month_lead_sum = []
        current_month_lead_date = []
        current_month_lead_sum = []
        for i in current_month_lead:
            x = i
            current_month_lead_date.append(x['entry_timedate'].strftime('%Y-%m-%d'))
            current_month_lead_sum.append(x['data_sum'])
        for i in previous_month_lead:
            x = i
            previous_month_lead_date.append(x['entry_timedate'].strftime('%Y-%m-%d'))
            previous_month_lead_sum.append(x['data_sum'])
        context14 = {
            'current_month_lead_date': current_month_lead_date,
            'current_month_lead_sum': current_month_lead_sum,
            'previous_month_lead_date': previous_month_lead_date,
            'previous_month_lead_sum': previous_month_lead_sum,

        }
        context.update(context14)
    except:
        pass

    return render(request,'lead_management/lead_analytics.html',context)

@login_required(login_url='/')
def lead_employee_graph(request,id):
    lead_conversion = Pi_section.objects.filter(lead_id__current_stage='PO Issued - Payment Done - Dispatch Pending',lead_id__owner_of_opportunity=SiteUser.objects.get(id=id),entry_timedate__month=datetime.now().month)\
            .values('entry_timedate').annotate(data_sum=Sum('grand_total'))

    lead_conversion_date = []
    lead_conversion_sum = []
    for i in lead_conversion:
        x = i
        lead_conversion_date.append(x['entry_timedate'].strftime('%Y-%m-%d'))
        lead_conversion_sum.append(x['data_sum'])

    lead_lost = Pi_section.objects.filter(lead_id__current_stage='Lost',
                                                lead_id__owner_of_opportunity=SiteUser.objects.get(id=id),
                                                entry_timedate__month=datetime.now().month) \
        .values('entry_timedate').annotate(data_sum=Sum('grand_total'))

    lead_lost_date = []
    lead_lost_sum = []
    for i in lead_lost:
        x = i
        lead_lost_date.append(x['entry_timedate'].strftime('%Y-%m-%d'))
        lead_lost_sum.append(x['data_sum'])

    lead_postponed = Pi_section.objects.filter(lead_id__current_stage='Postponed',
                                                lead_id__owner_of_opportunity=SiteUser.objects.get(id=id),
                                                entry_timedate__month=datetime.now().month) \
        .values('entry_timedate').annotate(data_sum=Sum('grand_total'))
    lead_postponed_date = []
    lead_postponed_sum = []
    for i in lead_postponed:
        x = i
        lead_postponed_date.append(x['entry_timedate'].strftime('%Y-%m-%d'))
        lead_postponed_sum.append(x['data_sum'])
    context = {

        'lead_conversion_date': lead_conversion_date,
        'lead_conversion_sum': lead_conversion_sum,
        'lead_lost_date': lead_lost_date,
        'lead_lost_sum': lead_lost_sum,
        'lead_postponed_date': lead_postponed_date,
        'lead_postponed_sum': lead_postponed_sum,
    }
    if request.method=='POST' and 'date1' in request.POST :
        start_date = request.POST.get('date1')
        lead_conversion = Pi_section.objects.filter(lead_id__current_stage='PO Issued - Payment Done - Dispatch Pending',
            lead_id__owner_of_opportunity=SiteUser.objects.get(id=id), entry_timedate__month=datetime.strptime(start_date, '%Y-%m-%d').month) \
            .values('entry_timedate').annotate(data_sum=Sum('grand_total'))

        lead_conversion_date = []
        lead_conversion_sum = []
        for i in lead_conversion:
            x = i
            lead_conversion_date.append(x['entry_timedate'].strftime('%Y-%m-%d'))
            lead_conversion_sum.append(x['data_sum'])

        lead_lost = Pi_section.objects.filter(lead_id__current_stage='Lost',
                                              lead_id__owner_of_opportunity=SiteUser.objects.get(id=id),
                                              entry_timedate__month=datetime.strptime(start_date, '%Y-%m-%d').month) \
            .values('entry_timedate').annotate(data_sum=Sum('grand_total'))

        lead_lost_date = []
        lead_lost_sum = []
        for i in lead_lost:
            x = i
            lead_lost_date.append(x['entry_timedate'].strftime('%Y-%m-%d'))
            lead_lost_sum.append(x['data_sum'])

        lead_postponed = Pi_section.objects.filter(lead_id__current_stage='Postponed',
                                                   lead_id__owner_of_opportunity=SiteUser.objects.get(id=id),
                                                   entry_timedate__month=datetime.strptime(start_date, '%Y-%m-%d').month) \
            .values('entry_timedate').annotate(data_sum=Sum('grand_total'))
        lead_postponed_date = []
        lead_postponed_sum = []
        for i in lead_postponed:
            x = i
            lead_postponed_date.append(x['entry_timedate'].strftime('%Y-%m-%d'))
            lead_postponed_sum.append(x['data_sum'])
        context = {

            'lead_conversion_date': lead_conversion_date,
            'lead_conversion_sum': lead_conversion_sum,
            'lead_lost_date': lead_lost_date,
            'lead_lost_sum': lead_lost_sum,
            'lead_postponed_date': lead_postponed_date,
            'lead_postponed_sum': lead_postponed_sum,
        }

    return render(request,'lead_management/lead_employee_graph.html', context)

@login_required(login_url='/')
def lead_pi_form(request):
    return render(request,'lead_management/lead_pi_form.html')

@login_required(login_url='/')
def alpha_pi_form(request):
    return render(request,'lead_management/alpha_pi_template.html')




@login_required(login_url='/')
def download_pi_image(request):
    return render(request,'lead_management/download_pi_image.html')




@login_required(login_url='/')
def lead_logs(request):
    lead_logs = Log.objects.filter(module_name='Lead Module').order_by('-id')
    paginator = Paginator(lead_logs, 15)  # Show 25 contacts per page
    page = request.GET.get('page')
    lead_logs = paginator.get_page(page)

    context={
    'lead_logs': lead_logs,

    }
    return render(request,"logs/lead_logs.html",context)



@receiver(pre_save, sender=Lead)
def lead_handler(sender, instance, update_fields=None, **kwargs):
    try:
        if instance.id == None or instance.id == '' or instance.id == 'None' :
            #########for insert action##########
            new_instance = instance
            log = Log()
            # log.entered_by = instance.entered_by
            log.entered_by = new_instance.log_entered_by
            log.module_name = 'Lead Module'
            log.action_type = 'Insert'
            log.table_name = 'Lead'
            log.reference = 'Lead No: ' + str(new_instance.id)

            # log.action = old_list
            log.save()
        elif instance.id != None or instance.id !='' or instance.id !='None':
            #########for update action##########
            old_instance = instance
            new_instance = Lead.objects.get(id=instance.id)

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
                    if value != '' and str(value) != getattr(instance, key):
                        old_list.append(key + ':Old value= ' + str(value) + ', New value=' + getattr(instance, key))
                log = Log()

                log.entered_by = instance.log_entered_by
                log.module_name = 'Lead Module'
                log.action_type = 'Update'
                log.table_name = 'Lead'

                log.reference = 'Lead No: '+str(new_instance.id)

                log.action = old_list
                if old_list != []:
                    log.save()
    except:
        pass

@receiver(pre_save, sender=Pi_section)
def Pi_section_handler(sender, instance, update_fields=None, **kwargs):
    try:
        if instance.id == None or instance.id == '' or instance.id == 'None' :
            #########for insert action##########
            new_instance = instance
            log = Log()
            # log.entered_by = instance.entered_by
            log.entered_by = new_instance.log_entered_by
            log.module_name = 'Lead Module'
            log.action_type = 'Insert'
            log.table_name = 'Pi_section'
            log.reference = 'Pi_section No: ' + str(new_instance.id)

            # log.action = old_list
            log.save()
        elif instance.id != None or instance.id !='' or instance.id !='None':
            #########for update action##########
            old_instance = instance
            new_instance = Lead.objects.get(id=instance.id)

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
                    if value != '' and str(value) != getattr(instance, key):
                        old_list.append(key + ':Old value= ' + str(value) + ', New value=' + getattr(instance, key))
                log = Log()

                log.entered_by = instance.log_entered_by
                log.module_name = 'Lead Module'
                log.action_type = 'Update'
                log.table_name = 'Pi_section'

                log.reference = 'Pi_section No: '+str(new_instance.id)

                log.action = old_list
                if old_list != []:
                    log.save()
    except:
        pass

@receiver(pre_save, sender=Pi_product)
def pi_product_handler(sender, instance, update_fields=None, **kwargs):
    try:
        if instance.id == None or instance.id == '' or instance.id == 'None' :
            #########for insert action##########
            new_instance = instance
            log = Log()
            # log.entered_by = instance.entered_by
            log.entered_by = new_instance.log_entered_by
            log.module_name = 'Lead Module'
            log.action_type = 'Insert'
            log.table_name = 'Pi_product'
            log.reference = 'Pi_product No: ' + str(new_instance.id)

            # log.action = old_list
            log.save()
        elif instance.id != None or instance.id !='' or instance.id !='None':
            #########for update action##########
            old_instance = instance
            new_instance = Lead.objects.get(id=instance.id)

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
                    if value != '' and str(value) != getattr(instance, key):
                        old_list.append(key + ':Old value= ' + str(value) + ', New value=' + getattr(instance, key))
                log = Log()

                log.entered_by = instance.log_entered_by
                log.module_name = 'Lead Module'
                log.action_type = 'Update'
                log.table_name = 'Pi_product'

                log.reference = 'Pi_product No: '+str(new_instance.id)

                log.action = old_list
                if old_list != []:
                    log.save()
    except:
        pass

@receiver(pre_save, sender=Pi_History)
def Pi_History_handler(sender, instance, update_fields=None, **kwargs):
    try:
        if instance.id == None or instance.id == '' or instance.id == 'None' :
            #########for insert action##########
            new_instance = instance
            log = Log()
            # log.entered_by = instance.entered_by
            log.entered_by = new_instance.log_entered_by
            log.module_name = 'Lead Module'
            log.action_type = 'Insert'
            log.table_name = 'Pi_History'
            log.reference = 'Pi_History No: ' + str(new_instance.id)

            # log.action = old_list
            log.save()
        elif instance.id != None or instance.id !='' or instance.id !='None':
            #########for update action##########
            old_instance = instance
            new_instance = Lead.objects.get(id=instance.id)

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
                    if value != '' and str(value) != getattr(instance, key):
                        old_list.append(key + ':Old value= ' + str(value) + ', New value=' + getattr(instance, key))
                log = Log()
                log.entered_by = instance.log_entered_by
                log.module_name = 'Lead Module'
                log.action_type = 'Update'
                log.table_name = 'Pi_History'

                log.reference = 'Pi_History No: '+str(new_instance.id)

                log.action = old_list
                if old_list != []:
                    log.save()
    except:
        pass

@receiver(pre_save, sender=Follow_up_section)
def Follow_up_section_handler(sender, instance, update_fields=None, **kwargs):
    try:
        if instance.id == None or instance.id == '' or instance.id == 'None' :
            #########for insert action##########
            new_instance = instance
            log = Log()
            # log.entered_by = instance.entered_by
            log.entered_by = new_instance.log_entered_by
            log.module_name = 'Lead Module'
            log.action_type = 'Insert'
            log.table_name = 'Follow_up_section'
            log.reference = 'Follow_up_section No: ' + str(new_instance.id)

            # log.action = old_list
            log.save()
        elif instance.id != None or instance.id !='' or instance.id !='None':
            #########for update action##########
            old_instance = instance
            new_instance = Lead.objects.get(id=instance.id)

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
                    if value != '' and str(value) != getattr(instance, key):
                        old_list.append(key + ':Old value= ' + str(value) + ', New value=' + getattr(instance, key))
                log = Log()

                log.entered_by = instance.log_entered_by
                log.module_name = 'Lead Module'
                log.action_type = 'Update'
                log.table_name = 'Follow_up_section'

                log.reference = 'Follow_up_section No: '+str(new_instance.id)

                log.action = old_list
                if old_list != []:
                    log.save()
    except:
        pass

@receiver(pre_save, sender=History_followup)
def History_followup_handler(sender, instance, update_fields=None, **kwargs):
    try:
        if instance.id == None or instance.id == '' or instance.id == 'None' :
            #########for insert action##########
            new_instance = instance
            log = Log()
            # log.entered_by = instance.entered_by
            log.entered_by = new_instance.log_entered_by
            log.module_name = 'Lead Module'
            log.action_type = 'Insert'
            log.table_name = 'History_followup'
            log.reference = 'History_followup No: ' + str(new_instance.id)

            # log.action = old_list
            log.save()
        elif instance.id != None or instance.id !='' or instance.id !='None':
            #########for update action##########
            old_instance = instance
            new_instance = Lead.objects.get(id=instance.id)

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
                    if value != '' and str(value) != getattr(instance, key):
                        old_list.append(key + ':Old value= ' + str(value) + ', New value=' + getattr(instance, key))
                log = Log()

                log.entered_by = instance.log_entered_by
                log.module_name = 'Lead Module'
                log.action_type = 'Update'
                log.table_name = 'History_followup'

                log.reference = 'History_followup No: '+str(new_instance.id)

                log.action = old_list
                if old_list != []:
                    log.save()
    except:
        pass

@receiver(pre_save, sender=Followup_product)
def Followup_product_handler(sender, instance, update_fields=None, **kwargs):
    try:
        if instance.id == None or instance.id == '' or instance.id == 'None' :
            #########for insert action##########
            new_instance = instance
            log = Log()
            # log.entered_by = instance.entered_by
            log.entered_by = new_instance.log_entered_by
            log.module_name = 'Lead Module'
            log.action_type = 'Insert'
            log.table_name = 'Followup_product'
            log.reference = 'Followup_product No: ' + str(new_instance.id)

            # log.action = old_list
            log.save()
        elif instance.id != None or instance.id !='' or instance.id !='None':
            #########for update action##########
            old_instance = instance
            new_instance = Lead.objects.get(id=instance.id)

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
                    if value != '' and str(value) != getattr(instance, key):
                        old_list.append(key + ':Old value= ' + str(value) + ', New value=' + getattr(instance, key))
                log = Log()

                log.entered_by = instance.log_entered_by
                log.module_name = 'Lead Module'
                log.action_type = 'Update'
                log.table_name = 'Followup_product'

                log.reference = 'Followup_product No: '+str(new_instance.id)

                log.action = old_list
                if old_list != []:
                    log.save()
    except:
        pass

@receiver(pre_save, sender=Payment_details)
def Payment_details_handler(sender, instance, update_fields=None, **kwargs):
    try:
        if instance.id == None or instance.id == '' or instance.id == 'None' :
            #########for insert action##########
            new_instance = instance
            log = Log()
            # log.entered_by = instance.entered_by
            log.entered_by = new_instance.log_entered_by
            log.module_name = 'Lead Module'
            log.action_type = 'Insert'
            log.table_name = 'Payment_details'
            log.reference = 'Payment_details No: ' + str(new_instance.id)

            # log.action = old_list
            log.save()
        elif instance.id != None or instance.id !='' or instance.id !='None':
            #########for update action##########
            old_instance = instance
            new_instance = Lead.objects.get(id=instance.id)

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
                    if value != '' and str(value) != getattr(instance, key):
                        old_list.append(key + ':Old value= ' + str(value) + ', New value=' + getattr(instance, key))
                log = Log()

                log.entered_by = instance.log_entered_by
                log.module_name = 'Lead Module'
                log.action_type = 'Update'
                log.table_name = 'Payment_details'
                log.reference = 'Payment_details No: '+str(new_instance.id)

                log.action = old_list
                if old_list != []:
                    log.save()
    except:
        pass


@login_required(login_url='/')
def download_pi_image(request,id):
    lead_id = Lead.objects.get(id=id)
    todays_date = str(datetime.now().strftime("%Y-%m-%d"))
    pi_id = Pi_section.objects.get(lead_id=id)

    pi_products = Pi_product.objects.filter(lead_id=id)
    context = {
        'lead_id': lead_id,
        'todays_date': todays_date,
        'pi_id': pi_id,
        'pi_products': pi_products,
    }
    return render(request,'lead_management/download_pi_image.html',context)

import os
def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those
    resources
    """
    # use short variable names
    sUrl = settings.STATIC_URL      # Typically /static/
    sRoot = settings.STATIC_ROOT    # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL       # Typically /static/media/
    mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/

    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri  # handle absolute uri (ie: http://some.tld/foo.png)

    # make sure that file exists
    if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
    return path


@login_required(login_url='/')
def download_pi_pdf(request,id,download):
    lead_id=Lead.objects.get(id=id)
    todays_date = str(datetime.now().strftime("%Y-%m-%d"))
    pi_id = Pi_section.objects.get(lead_id=id)

    pi_products = Pi_product.objects.filter(lead_id=id)
    context={
        'lead_id':lead_id,
        'todays_date':todays_date,
        'pi_id':pi_id,
        'pi_products':pi_products,
        'download':True if download == 1 else False,
    }
    try:
        del request.session['download_pdf_exist']
    except:
        pass
    # template = get_template('lead_management/download_pi_pdf.html')
    # html = template.render(context)
    # result = BytesIO()
    # pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1", "ignore")), result)
    # pisaStatus = pisa.CreatePDF(
    #     html, dest=result, link_callback=link_callback)
    # pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)

    # email_send = EmailMessage('subject', 'testing', settings.EMAIL_HOST_USER, [lead_id.customer_id.customer_email_id])
    # email_send.attach('invoicex.pdf', result.getvalue(), 'application/pdf')
    # email_send.send()

    # pi = Pi_History()
    # file = ContentFile(result.getvalue())
    # pi.file.save('AutoFollowup.pdf', file, save=False)
    # # pi.file = result.getvalue()
    # pi.lead_id = Lead.objects.get(id=id)
    # pi.save()

    return render(request,'lead_management/download_pi_pdf.html',context)

@login_required(login_url='/')
def download_pi_second_pdf(request,id,download):
    lead_id=Lead.objects.get(id=id)
    todays_date = str(datetime.now().strftime("%Y-%m-%d"))
    pi_id = Pi_section.objects.get(lead_id=id)

    pi_products = Pi_product.objects.filter(lead_id=id)
    context={
        'lead_id':lead_id,
        'todays_date':todays_date,
        'pi_id':pi_id,
        'pi_products':pi_products,
        'download': True if download == 1 else False,
    }
    try:
        del request.session['download_pdf_exist']
    except:
        pass
    return render(request,'lead_management/download_pi_second_pdf.html',context)

@login_required(login_url='/')
def get_pi_product_details(request):
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
    return render(request, 'AJAX/get_pi_product_details.html',context)

@login_required(login_url='/')
def check_admin_roles(request):
    if request.user.role == 'Super Admin' or request.user.role == 'Admin' or request.user.role == 'Manager':
        return True
    else:
        return False