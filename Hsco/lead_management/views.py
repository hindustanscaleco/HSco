from datetime import datetime
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.paginator import Paginator
from django.db import connection
from django.db.models import Sum, Q, Count
from django.core.files.base import ContentFile
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect
from customer_app.models import type_purchase
from stock_management_system_app.models import Product
from django.contrib.auth.decorators import login_required

from Hsco import settings
from user_app.models import SiteUser
from customer_app.models import Log
from .forms import Deal_detailForm, Customer_detailForm, Pi_sectionForm, Follow_up_sectionForm, History_followupForm, Payment_detailsForm
from .form2 import Customer_detail_disabledForm
from customer_app.models import Customer_Details
from .models import Lead, Pi_section, IndiamartLeadDetails, History_followup, Follow_up_section, Followup_product, \
    Auto_followup_details, Payment_details
from .models import Lead, Pi_section, Pi_product, Pi_History
from customer_app.models import sub_model, main_model, sub_sub_model
import requests
import json
from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from .utils import send_html_mail
from purchase_app.models import Purchase_Details
from dispatch_app.models import Dispatch
from purchase_app.models import Product_Details
from dispatch_app.models import Product_Details_Dispatch
from django.core.mail import EmailMessage

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

    if request.user.role == 'Super Admin':  # For ADMIN
        lead_list = Lead.objects.all().order_by('-id')
        paginator = Paginator(lead_list, 15)  # Show 25 contacts per page
        page = request.GET.get('page')
        lead_list = paginator.get_page(page)
    else:
        admin = SiteUser.objects.get(id=request.user.pk).admin
        lead_list = Lead.objects.filter(Q(owner_of_opportunity__admin=admin)).order_by('-id')
        paginator = Paginator(lead_list, 15)  # Show 25 contacts per page
        page = request.GET.get('page')
        lead_list = paginator.get_page(page)
    cust_sugg = Customer_Details.objects.all()

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
    else:
        admin = SiteUser.objects.get(id=request.user.pk).admin
        total_stages = Lead.objects.filter(Q(owner_of_opportunity__admin=admin)).values('current_stage').annotate(dcount=Count('current_stage'))
    admin = SiteUser.objects.get(id=request.user.pk).admin
    # lead = Pi_section.objects.filter(lead_id=Lead.objects.filter(Q(owner_of_opportunity__admin=admin)))


    try:
        po_no_payment = Pi_section.objects.filter(lead_id__current_stage='PO Issued - Payment not done',
                                                   lead_id__owner_of_opportunity__admin=admin).values(
            'grand_total').annotate(data_sum=Sum('grand_total'))
        po_no_payment_total = 0.0
        for x in po_no_payment:
            po_no_payment_total += float(x['data_sum'])

        po_payment_done = Pi_section.objects.filter(lead_id__current_stage='PO Issued - Payment Done - Dispatch Pending',
                                                   lead_id__owner_of_opportunity__admin=admin).values(
            'grand_total').annotate(data_sum=Sum('grand_total'))
        po_payment_done_total = 0.0
        for x in po_payment_done:
            po_payment_done_total += float(x['data_sum'])

        dispatch_done_stage = Pi_section.objects.filter(lead_id__current_stage='Dispatch Done - Closed',
                                                   lead_id__owner_of_opportunity__admin=admin).values(
            'grand_total').annotate(data_sum=Sum('grand_total'))
        dispatch_done_stage_total = 0.0
        for x in dispatch_done_stage:
            dispatch_done_stage_total += float(x['data_sum'])

        lost_stage = Pi_section.objects.filter(lead_id__current_stage='Lost',
                                                   lead_id__owner_of_opportunity__admin=admin).values(
            'grand_total').annotate(data_sum=Sum('grand_total'))
        lost_stage_total = 0.0
        for x in lost_stage:
            lost_stage_total += float(x['data_sum'])

        not_relevant_stage = Pi_section.objects.filter(lead_id__current_stage='Not Relevant',
                                                   lead_id__owner_of_opportunity__admin=admin).values(
            'grand_total').annotate(data_sum=Sum('grand_total'))
        not_relevant_stage_total = 0.0
        for x in not_relevant_stage:
            not_relevant_stage_total += float(x['data_sum'])

        postponed_stage = Pi_section.objects.filter(lead_id__current_stage='Postponed',
                                                   lead_id__owner_of_opportunity__admin=admin).values(
            'grand_total').annotate(data_sum=Sum('grand_total'))
        postponed_stage_total = 0.0
        for x in postponed_stage:
            postponed_stage_total += float(x['data_sum'])

        pi_sent_stage = Pi_section.objects.filter(lead_id__current_stage='PI Sent & Follow-up',
                                                   lead_id__owner_of_opportunity__admin=admin).values(
            'grand_total').annotate(data_sum=Sum('grand_total'))
        pi_sent_stage_total = 0.0
        for x in pi_sent_stage:
            pi_sent_stage_total += float(x['data_sum'])

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
    except:
        pass

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

    if request.method == 'POST':
        if 'fetch_lead' in request.POST:

            url = "https://mapi.indiamart.com/wservce/enquiry/listing/GLUSR_MOBILE/" + mobile + "/GLUSR_MOBILE_KEY/" + api + "/Start_Time/" + from_date + "/End_Time/" + to_date + "/"
            response = requests.get(url=url).json()
            lead_count = len(response)

            from_date =  request.POST.get('from_date_form')
            to_date =  request.POST.get('to_date_form')
            import time
            conv = time.strptime(from_date, "%d-%b-%Y")
            conv2 = time.strptime(to_date, "%d-%b-%Y")

        if 'sort_submit' in request.POST:
            YEAR = request.POST.get('YEAR')
            MONTH = request.POST.get('MONTH')



            if request.user.role == 'Super Admin':  # For ADMIN
                lead_list = Lead.objects.filter(entry_timedate__month = MONTH , entry_timedate__year = YEAR).order_by('-id')
                lead_list_count = Lead.objects.filter(entry_timedate__month = MONTH , entry_timedate__year = YEAR).count()
                paginator = Paginator(lead_list, 15)  # Show 25 contacts per page
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
                paginator = Paginator(lead_list, 15)  # Show 25 contacts per page
                page = request.GET.get('page')
                lead_list = paginator.get_page(page)
                context = {
                    'lead_list': lead_list,
                    'lead_list_count': True if lead_list_count != 0 else False,
                    'lead_lis': False if lead_list_count != 0 else True,
                }


            return render(request, 'lead_management/lead_home.html', context)

        if 'sub1' in request.POST:
            if request.user.role == 'Super Admin':  # For ADMIN
                lead_list = Lead.objects.filter(current_stage='Not Yet Initiated').order_by('-id')
                lead_list_count = Lead.objects.filter(current_stage='Not Yet Initiated').count()
                paginator = Paginator(lead_list, 15)  # Show 25 contacts per page
                page = request.GET.get('page')
                lead_list = paginator.get_page(page)
                context44 = {
                    'lead_list': lead_list,
                    'lead_list_count': True if lead_list_count != 0 else False,
                }
                context.update(context44)
            else:
                admin = SiteUser.objects.get(id=request.user.pk).admin
                lead_list = Lead.objects.filter(Q(owner_of_opportunity__admin=admin) and Q(current_stage='Not Yet Initiated')).order_by(
                    '-id')
                lead_list_count = Lead.objects.filter(
                    Q(owner_of_opportunity__admin=admin) and Q(current_stage='Not Yet Initiated')).count()
                paginator = Paginator(lead_list, 15)  # Show 25 contacts per page
                page = request.GET.get('page')
                lead_list = paginator.get_page(page)
                context44 = {
                    'lead_list': lead_list,
                    'lead_list_count': True if lead_list_count != 0 else False,
                }
                context.update(context44)

        if 'sub2' in request.POST:
            if request.user.role == 'Super Admin':  # For ADMIN
                lead_list = Lead.objects.filter(current_stage='Customer Called').order_by('-id')
                lead_list_count = Lead.objects.filter(current_stage='Customer Called').count()
                paginator = Paginator(lead_list, 15)  # Show 25 contacts per page
                page = request.GET.get('page')
                lead_list = paginator.get_page(page)
                context44 = {
                    'lead_list': lead_list,
                    'lead_list_count': True if lead_list_count != 0 else False,
                }
                context.update(context44)
            else:
                admin = SiteUser.objects.get(id=request.user.pk).admin
                lead_list = Lead.objects.filter(Q(owner_of_opportunity__admin=admin) and Q(current_stage='Customer Called')).order_by(
                    '-id')
                lead_list_count = Lead.objects.filter(
                    Q(owner_of_opportunity__admin=admin) and Q(current_stage='Customer Called')).count()
                paginator = Paginator(lead_list, 15)  # Show 25 contacts per page
                page = request.GET.get('page')
                lead_list = paginator.get_page(page)
                context44 = {
                    'lead_list': lead_list,
                    'lead_list_count': True if lead_list_count != 0 else False,
                }
                context.update(context44)

        if 'sub3' in request.POST:
            cur_stage='PI Sent & Follow-up'
            if request.user.role == 'Super Admin':  # For ADMIN
                lead_list = Lead.objects.filter(current_stage=cur_stage).order_by('-id')
                lead_list_count = Lead.objects.filter(current_stage=cur_stage).count()
                paginator = Paginator(lead_list, 15)  # Show 25 contacts per page
                page = request.GET.get('page')
                lead_list = paginator.get_page(page)
                context44 = {
                    'lead_list': lead_list,
                    'lead_list_count': True if lead_list_count != 0 else False,
                }
                context.update(context44)
            else:
                admin = SiteUser.objects.get(id=request.user.pk).admin
                lead_list = Lead.objects.filter(Q(owner_of_opportunity__admin=admin) and Q(current_stage=cur_stage)).order_by(
                    '-id')
                lead_list_count = Lead.objects.filter(
                    Q(owner_of_opportunity__admin=admin) and Q(current_stage=cur_stage)).count()
                paginator = Paginator(lead_list, 15)  # Show 25 contacts per page
                page = request.GET.get('page')
                lead_list = paginator.get_page(page)
                context44 = {
                    'lead_list': lead_list,
                    'lead_list_count': True if lead_list_count != 0 else False,
                }
                context.update(context44)

        if 'sub4' in request.POST:
            cur_stage='PO Issued - Payment not done'
            if request.user.role == 'Super Admin':  # For ADMIN
                lead_list = Lead.objects.filter(current_stage=cur_stage).order_by('-id')
                lead_list_count = Lead.objects.filter(current_stage=cur_stage).count()
                paginator = Paginator(lead_list, 15)  # Show 25 contacts per page
                page = request.GET.get('page')
                lead_list = paginator.get_page(page)
                context44 = {
                    'lead_list': lead_list,
                    'lead_list_count': True if lead_list_count != 0 else False,
                }
                context.update(context44)
            else:
                admin = SiteUser.objects.get(id=request.user.pk).admin
                lead_list = Lead.objects.filter(Q(owner_of_opportunity__admin=admin) and Q(current_stage=cur_stage)).order_by(
                    '-id')
                lead_list_count = Lead.objects.filter(
                    Q(owner_of_opportunity__admin=admin) and Q(current_stage=cur_stage)).count()
                paginator = Paginator(lead_list, 15)  # Show 25 contacts per page
                page = request.GET.get('page')
                lead_list = paginator.get_page(page)
                context44 = {
                    'lead_list': lead_list,
                    'lead_list_count': True if lead_list_count != 0 else False,
                }
                context.update(context44)

        if 'sub5' in request.POST:
            cur_stage='PO Issued - Payment Done - Dispatch Pending'
            if request.user.role == 'Super Admin':  # For ADMIN
                lead_list = Lead.objects.filter(current_stage=cur_stage).order_by('-id')
                lead_list_count = Lead.objects.filter(current_stage=cur_stage).count()
                paginator = Paginator(lead_list, 15)  # Show 25 contacts per page
                page = request.GET.get('page')
                lead_list = paginator.get_page(page)
                context44 = {
                    'lead_list': lead_list,
                    'lead_list_count': True if lead_list_count != 0 else False,
                }
                context.update(context44)
            else:
                admin = SiteUser.objects.get(id=request.user.pk).admin
                lead_list = Lead.objects.filter(Q(owner_of_opportunity__admin=admin) and Q(current_stage=cur_stage)).order_by(
                    '-id')
                lead_list_count = Lead.objects.filter(
                    Q(owner_of_opportunity__admin=admin) and Q(current_stage=cur_stage)).count()
                paginator = Paginator(lead_list, 15)  # Show 25 contacts per page
                page = request.GET.get('page')
                lead_list = paginator.get_page(page)
                context44 = {
                    'lead_list': lead_list,
                    'lead_list_count': True if lead_list_count != 0 else False,
                }
                context.update(context44)

        if 'sub6' in request.POST:
            cur_stage='Dispatch Done - Closed'
            if request.user.role == 'Super Admin':  # For ADMIN
                lead_list = Lead.objects.filter(current_stage=cur_stage).order_by('-id')
                lead_list_count = Lead.objects.filter(current_stage=cur_stage).count()
                paginator = Paginator(lead_list, 15)  # Show 25 contacts per page
                page = request.GET.get('page')
                lead_list = paginator.get_page(page)
                context44 = {
                    'lead_list': lead_list,
                    'lead_list_count': True if lead_list_count != 0 else False,
                }
                context.update(context44)
            else:
                admin = SiteUser.objects.get(id=request.user.pk).admin
                lead_list = Lead.objects.filter(Q(owner_of_opportunity__admin=admin) and Q(current_stage=cur_stage)).order_by(
                    '-id')
                lead_list_count = Lead.objects.filter(
                    Q(owner_of_opportunity__admin=admin) and Q(current_stage=cur_stage)).count()
                paginator = Paginator(lead_list, 15)  # Show 25 contacts per page
                page = request.GET.get('page')
                lead_list = paginator.get_page(page)
                context44 = {
                    'lead_list': lead_list,
                    'lead_list_count': True if lead_list_count != 0 else False,
                }
                context.update(context44)

        if 'sub7' in request.POST:
            cur_stage='Lost'
            if request.user.role == 'Super Admin':  # For ADMIN
                lead_list = Lead.objects.filter(current_stage=cur_stage).order_by('-id')
                lead_list_count = Lead.objects.filter(current_stage=cur_stage).count()
                paginator = Paginator(lead_list, 15)  # Show 25 contacts per page
                page = request.GET.get('page')
                lead_list = paginator.get_page(page)
                context44 = {
                    'lead_list': lead_list,
                    'lead_list_count': True if lead_list_count != 0 else False,
                }
                context.update(context44)
            else:
                admin = SiteUser.objects.get(id=request.user.pk).admin
                lead_list = Lead.objects.filter(Q(owner_of_opportunity__admin=admin) and Q(current_stage=cur_stage)).order_by(
                    '-id')
                lead_list_count = Lead.objects.filter(
                    Q(owner_of_opportunity__admin=admin) and Q(current_stage=cur_stage)).count()
                paginator = Paginator(lead_list, 15)  # Show 25 contacts per page
                page = request.GET.get('page')
                lead_list = paginator.get_page(page)
                context44 = {
                    'lead_list': lead_list,
                    'lead_list_count': True if lead_list_count != 0 else False,
                }
                context.update(context44)

        if 'sub8' in request.POST:
            cur_stage='Not Relevant'
            if request.user.role == 'Super Admin':  # For ADMIN
                lead_list = Lead.objects.filter(current_stage=cur_stage).order_by('-id')
                lead_list_count = Lead.objects.filter(current_stage=cur_stage).count()
                paginator = Paginator(lead_list, 15)  # Show 25 contacts per page
                page = request.GET.get('page')
                lead_list = paginator.get_page(page)
                context44 = {
                    'lead_list': lead_list,
                    'lead_list_count': True if lead_list_count != 0 else False,
                }
                context.update(context44)
            else:
                admin = SiteUser.objects.get(id=request.user.pk).admin
                lead_list = Lead.objects.filter(Q(owner_of_opportunity__admin=admin) and Q(current_stage=cur_stage)).order_by(
                    '-id')
                lead_list_count = Lead.objects.filter(
                    Q(owner_of_opportunity__admin=admin) and Q(current_stage=cur_stage)).count()
                paginator = Paginator(lead_list, 15)  # Show 25 contacts per page
                page = request.GET.get('page')
                lead_list = paginator.get_page(page)
                context44 = {
                    'lead_list': lead_list,
                    'lead_list_count': True if lead_list_count != 0 else False,
                }
                context.update(context44)

        if 'sub9' in request.POST:
            cur_stage='Postponed'
            if request.user.role == 'Super Admin':  # For ADMIN
                lead_list = Lead.objects.filter(current_stage=cur_stage).order_by('-id')
                lead_list_count = Lead.objects.filter(current_stage=cur_stage).count()
                paginator = Paginator(lead_list, 15)  # Show 25 contacts per page
                page = request.GET.get('page')
                lead_list = paginator.get_page(page)
                context44 = {
                    'lead_list': lead_list,
                    'lead_list_count': True if lead_list_count != 0 else False,
                }
                context.update(context44)
            else:
                admin = SiteUser.objects.get(id=request.user.pk).admin
                lead_list = Lead.objects.filter(Q(owner_of_opportunity__admin=admin) and Q(current_stage=cur_stage)).order_by(
                    '-id')
                lead_list_count = Lead.objects.filter(
                    Q(owner_of_opportunity__admin=admin) and Q(current_stage=cur_stage)).count()
                paginator = Paginator(lead_list, 15)  # Show 25 contacts per page
                page = request.GET.get('page')
                lead_list = paginator.get_page(page)
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

                paginator = Paginator(cust_list, 15)  # Show 25 contacts per page
                page = request.GET.get('page')
                cust_list = paginator.get_page(page)
            else:  # For EMPLOYEE
                cust_list = Lead.objects.filter(owner_of_opportunity=request.user.pk,
                                                entry_timedate__range=[start_date, end_date]).order_by('-customer_id')
                paginator = Paginator(cust_list, 15)  # Show 25 contacts per page
                page = request.GET.get('page')
                cust_list = paginator.get_page(page)
            # cust_list = Customer_Details.objects.filter()
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
                paginator = Paginator(cust_list, 15)  # Show 25 contacts per page
                page = request.GET.get('page')
                cust_list = paginator.get_page(page)
            else:  # For EMPLOYEE
                cust_list = Lead.objects.filter(owner_of_opportunity_id=request.user.pk, customer_id__contact_no__icontains=contact).order_by(
                    '-id')
                paginator = Paginator(cust_list, 15)  # Show 25 contacts per page
                page = request.GET.get('page')
                cust_list = paginator.get_page(page)
            # cust_list = Customer_Details.objects.filter(contact_no=contact)
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
                paginator = Paginator(cust_list, 15)  # Show 25 contacts per page
                page = request.GET.get('page')
                cust_list = paginator.get_page(page)
            else:  # For EMPLOYEE
                cust_list = Lead.objects.filter(owner_of_opportunity=request.user.pk, customer_id__customer_email_id__icontains=email).order_by(
                    '-id')
                paginator = Paginator(cust_list, 15)  # Show 25 contacts per page
                page = request.GET.get('page')
                cust_list = paginator.get_page(page)
            # cust_list = Customer_Details.objects.filter(customer_email_id=email)
            context = {
                'lead_list': cust_list,
                'search_msg': 'Search result for Customer Email ID: ' + email,
            }
            return render(request, 'lead_management/lead_home.html', context)
        elif 'submit4' in request.POST:
            customer = request.POST.get('customer')
            if check_admin_roles(request):  # For ADMIN
                cust_list = Lead.objects.filter(owner_of_opportunity__group__icontains=request.user.name,
                                                owner_of_opportunity__is_deleted=False, customer_id__second_person__icontains=customer).order_by(
                    '-id')
                paginator = Paginator(cust_list, 15)  # Show 25 contacts per page
                page = request.GET.get('page')
                cust_list = paginator.get_page(page)
            else:  # For EMPLOYEE
                cust_list = Lead.objects.filter(owner_of_opportunity=request.user.pk, customer_id__second_person__icontains=customer).order_by(
                    '-id')
                paginator = Paginator(cust_list, 15)  # Show 25 contacts per page
                page = request.GET.get('page')
                cust_list = paginator.get_page(page)
            # cust_list = Customer_Details.objects.filter(customer_name=customer)
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
                paginator = Paginator(cust_list, 15)  # Show 25 contacts per page
                page = request.GET.get('page')
                cust_list = paginator.get_page(page)
            else:  # For EMPLOYEE
                cust_list = Lead.objects.filter(owner_of_opportunity=request.user.pk,
                                                customer_id__company_name__icontains=company).order_by('-id')
                paginator = Paginator(cust_list, 15)  # Show 25 contacts per page
                page = request.GET.get('page')
                cust_list = paginator.get_page(page)
            # cust_list = Customer_Details.objects.filter(company_name=company)
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
                paginator = Paginator(cust_list, 15)  # Show 25 contacts per page
                page = request.GET.get('page')
                cust_list = paginator.get_page(page)
            else:  # For EMPLOYEE
                cust_list = Lead.objects.filter(owner_of_opportunity=request.user.pk, id__icontains=serial_no).order_by(
                    '-id')
                paginator = Paginator(cust_list, 15)  # Show 25 contacts per page
                page = request.GET.get('page')
                cust_list = paginator.get_page(page)
            # cust_list = Customer_Details.objects.filter(company_name=company)
            context = {
                'lead_list': cust_list,
                'search_msg': 'Search result for Sr no: ' + serial_no,
            }
            return render(request, 'lead_management/lead_home.html', context)


        if (lead_count > 1):
            for item in response:

                item3 = Customer_Details()
                item3.customer_name = item['SENDERNAME']
                item3.company_name = item['GLUSR_USR_COMPANYNAME']
                item3.address = item['ENQ_ADDRESS']
                item3.customer_email_id = item['SENDEREMAIL']
                item3.contact_no = item['MOB']
                item3.customer_industry = ''
                try:
                    item3.save()
                    item2 = Lead()
                    item2.customer_id = Customer_Details.objects.get(id=item3.pk)
                    item2.current_stage = 'Not Yet Initiated'
                    item2.new_existing_customer = 'New'
                    item2.date_of_initiation = time.strftime("%Y-%m-%d", conv2)
                    item2.channel = 'Indiamart'

                    item2.requirement = item['SUBJECT'] + item['ENQ_MESSAGE'] + item['PRODUCT_NAME']
                    try:
                        item2.save()
                        fp = Follow_up_section()
                        fp.lead_id = Lead.objects.get(id=item2.pk)
                        fp.save()
                    except Exception as e:
                        error_exist = True
                        error2 = e
                except Exception as e:
                    error_exist = True
                    error = e

            obj = IndiamartLeadDetails()
            obj.from_date = time.strftime("%Y-%m-%d", conv)
            obj.to_date = time.strftime("%Y-%m-%d", conv2)
            obj.lead_count = lead_count
            try:
                obj.save()
            except:
                print("error")
        elif(lead_count<0):
            row_count = response[0]
            if (row_count != None):
                error = row_count['Error_Message']
                error_exist = True


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

def add_lead(request):
    users = SiteUser.objects.all()
    if Lead.objects.all().count() == 0:
        latest_lead_id = 1
    else:
        latest_lead_id = Lead.objects.latest('id').id

    cust_sugg = Customer_Details.objects.all()
    form = Customer_detailForm()
    form2 = Deal_detailForm()
    if request.method == 'POST' or request.method=='FILES':
        customer_name = request.POST.get('customer_name')
        company_name = request.POST.get('company_name')
        address = request.POST.get('address')
        contact_no = request.POST.get('contact_no')
        customer_industry = request.POST.get('customer_email_id')
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
        if Customer_Details.objects.filter(customer_name=customer_name,
                                           contact_no=contact_no).count() > 0:

            item2.customer_id = Customer_Details.objects.filter(contact_no=contact_no).first()

            item3 = Customer_Details.objects.filter(customer_name=customer_name,
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
            new_cust = Customer_Details()

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
                item2.customer_id = Customer_Details.objects.get(id=new_cust.pk)
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

        item2.save()

        fp=Follow_up_section()
        fp.lead_id= Lead.objects.get(id=item2.pk)
        fp.save()
        return redirect('/update_view_lead/'+str(item2.id))
        # item.save()
    context={
        'form':form,
        'form2':form2,
        'latest_lead_id':latest_lead_id,
        'cust_sugg':cust_sugg,
        'users':users,
    }
    return render(request, 'lead_management/add_lead.html',context)

def update_view_lead(request,id):
    lead_id = Lead.objects.get(id=id)
    users = SiteUser.objects.all()


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
    customer_id = Customer_Details.objects.get(id=lead_id.customer_id)
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
    }
    form = Customer_detailForm(initial=customer_initial_data)
    form2 = Deal_detailForm(initial=deal_details_initial_data)
    form3 = Pi_sectionForm()
    form4 = Follow_up_sectionForm(initial={'email_auto_manual':hfu.auto_manual_mode,})

    if(history_follow!=None):
        wa_msg = history_follow.wa_msg
        email_msg = history_follow.email_msg
        sms_msg = history_follow.sms_msg
        is_email = 'is_email' if history_follow.is_email else ''
        wa_no = history_follow.wa_no if history_follow.wa_no else customer_id.contact_no
    else:
        wa_msg = ''
        email_msg = ''
        sms_msg = ''
        is_email = ''
        wa_no = ''


    form6 = History_followupForm(initial={'wa_no':wa_no,'email_subject':hfu.email_subject,'wa_msg':wa_msg,'email_msg':email_msg,
                                          'sms_msg':sms_msg,'is_email':is_email})
    form5 = Payment_detailsForm()
    context = {
        'form': form,
        'form2': form2,
        'form3': form3,
        'form4': form4,
        'form5': form5,
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
    }
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
            'discount_type': pi_id.discount_type,
        }
        form3 = Pi_sectionForm(initial=pi_initial_data)
        context2 = {
            'form': form,
            'form2': form2,
            'form3': form3,
            'lead_id': lead_id,
            'lead_pi_products': lead_pi_products,

        }
        context.update(context2)
    else:
        pass

    if request.method == 'POST' or request.method == 'FILES':
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


            item2 = Lead.objects.get(id=id)

            item3 = Customer_Details.objects.get(id=lead_id.customer_id)

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

            payment_channel = request.POST.get('payment_channel')
            payment_receipt = request.POST.get('payment_receipt')
            upload_pofile = request.POST.get('upload_pofile')
            payment_received_date = request.POST.get('payment_received_date')

            item2 = Lead.objects.get(id=id)


            item2.current_stage = current_stage
            item2.new_existing_customer = new_existing_customer
            item2.date_of_initiation = date_of_initiation
            item2.channel = channel
            item2.requirement = requirement
            item2.lost_reason = lost_reason
            item2.postponed_reason = postponed_reason
            item2.upload_requirement_file = upload_requirement_file
            item2.log_entered_by = request.user.name
            item2.owner_of_opportunity = SiteUser.objects.get(profile_name=owner_of_opportunity)
            item2.save(update_fields=['current_stage','new_existing_customer','date_of_initiation','channel',
                                      'requirement','upload_requirement_file','owner_of_opportunity','log_entered_by',
                                      'lost_reason','postponed_reason'])
            is_entered_purchase = Lead.objects.get(id=id).is_entered_purchase
            if (current_stage == 'PO Issued - Payment Done - Dispatch Pending' and is_entered_purchase == False):
                Lead.objects.filter(id=id).update(is_entered_purchase=True)
                purchase_det = Purchase_Details()
                purchase_det.second_company_name = lead_id.customer_id.company_name  # new2
                purchase_det.company_address = lead_id.customer_id.address  # new2
                purchase_det.company_email = lead_id.customer_id.customer_email_id  # new2
                purchase_det.crm_no = Customer_Details.objects.get(id=lead_id.customer_id.pk)
                purchase_det.new_repeat_purchase = new_existing_customer
                purchase_det.second_person = lead_id.customer_id.customer_name  # new1
                purchase_det.second_contact_no = lead_id.customer_id.contact_no  # new2
                purchase_det.date_of_purchase = item2.entry_timedate
                purchase_det.product_purchase_date = item2.entry_timedate
                purchase_det.sales_person = owner_of_opportunity
                purchase_det.user_id = SiteUser.objects.get(profile_name=owner_of_opportunity)
                # purchase_det.bill_no = bill_no
                # purchase_det.upload_op_file = upload_op_file
                # purchase_det.po_number = po_number
                purchase_det.channel_of_sales = channel
                purchase_det.industry = lead_id.customer_id.customer_industry
                purchase_det.value_of_goods = 0.0
                # purchase_det.channel_of_dispatch = channel_of_dispatch
                purchase_det.notes = "Entry From Lead Module\n"
                purchase_det.feedback_form_filled = False
                purchase_det.manager_id = SiteUser.objects.get(id=request.user.pk).group
                purchase_det.purchase_no = Purchase_Details.objects.latest('purchase_no').purchase_no + 1
                purchase_det.log_entered_by = request.user.profile_name
                purchase_det.save()

                Lead.objects.filter(id=id).update(purchase_id=purchase_det.pk)

                dispatch = Dispatch()
                dispatch.crm_no = Customer_Details.objects.get(id=lead_id.customer_id.pk)
                dispatch.second_person = lead_id.customer_id.customer_name  # new1
                dispatch.second_contact_no = lead_id.customer_id.contact_no  # new2
                dispatch.second_company_name = lead_id.customer_id.company_name  # new2
                dispatch.company_email = lead_id.customer_id.customer_email_id
                dispatch.company_address = lead_id.customer_id.address  # new2
                dispatch.notes = "Entry From Lead Module\n"  # new2
                dispatch.user_id = SiteUser.objects.get(id=request.user.pk)
                dispatch.manager_id = SiteUser.objects.get(id=request.user.pk).group
                if Dispatch.objects.all().count() == 0:
                    dispatch.dispatch_no = 1
                else:
                    dispatch.dispatch_no = Dispatch.objects.latest('dispatch_no').dispatch_no + 1
                dispatch.save()

                customer_id = Purchase_Details.objects.get(id=purchase_det.pk)
                customer_id.dispatch_id_assigned = Dispatch.objects.get(id=dispatch.pk)  # str(dispatch.pk + 00000)
                customer_id.save(update_fields=['dispatch_id_assigned'])

                pi_pro = Pi_product.objects.filter(lead_id=lead_id.pk)
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
                    if(item.product_total_cost == None or item.product_total_cost == ''):
                        item_pro.amount = 0.0
                    else:
                        item_pro.amount = item.product_total_cost
                    item_pro.purchase_id_id = customer_id
                    item_pro.user_id = SiteUser.objects.get(id=request.user.pk)
                    item_pro.manager_id = SiteUser.objects.get(id=request.user.pk).group
                    item_pro.log_entered_by = request.user.name

                    item_pro.save()


                    dispatch_id = Dispatch.objects.get(id=dispatch.id)
                    dispatch_pro = Product_Details_Dispatch()
                    dispatch_pro.user_id = SiteUser.objects.get(id=request.user.pk)
                    dispatch_pro.manager_id = SiteUser.objects.get(id=request.user.pk).group
                    dispatch_pro.quantity = item.quantity
                    dispatch_pro.type_of_scale = item.product_id.scale_type
                    dispatch_pro.model_of_purchase = item.product_id.main_category
                    dispatch_pro.sub_model = item.product_id.sub_category
                    dispatch_pro.sub_sub_model = item.product_id.sub_sub_category

                    dispatch_pro.brand = 'HSCO'
                    dispatch_pro.capacity = item.product_id.max_capacity
                    dispatch_pro.unit = 'Kg'
                    dispatch_pro.dispatch_id = dispatch_id
                    if (item.product_total_cost == None or item.product_total_cost == ''):
                        dispatch_pro.value_of_goods = 0.0
                    else:
                        dispatch_pro.value_of_goods = item.product_total_cost

                    dispatch_pro.save()

                    Product_Details.objects.filter(id=item_pro.pk).update(product_dispatch_id=dispatch_pro.pk)


                Purchase_Details.objects.filter(id=customer_id.pk).update(value_of_goods=Pi_section.objects.get(lead_id=id).grand_total)

                if True :
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



            return redirect('/update_view_lead/'+str(id))
        elif 'submit2' in request.POST:

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
            if call2 == 'on':
                call2 = 'True'
            else:
                call2 = 'False'
            if email == 'on':
                email = 'True'
            else:
                email = 'False'
            if whatsapp == 'on':
                whatsapp = 'True'
            else:
                whatsapp = 'False'

            pdf = request.FILES.get('pdf')
            if pdf != None:
                history = Pi_History()
                history.file = pdf
                history.lead_id = Lead.objects.get(id=id)
                history.log_entered_by = request.user.profile_name
                history.save()
                text_content = ''' <html><body>
                <span lang="EN-US" style="font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif">Hindustan Scale Company<u></u><u></u></span><br>
    <span lang="EN-US" style="font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif">Sales Enquiry -&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; +91-7045922250<u></u><u></u></span><br>
    <span lang="EN-US" style="font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif">Queries &amp; Repairs -&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; +91-7045922251<u></u><u></u></span><br>
    <span lang="EN-US" style="font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif">Feedback &amp; Complaints -&nbsp;&nbsp;&nbsp;&nbsp; +91-7045922252<u></u><u></u></span><br>
    <span lang="EN-US" style="font-size:12.0pt;font-family:&quot;Times New Roman&quot;,serif;color:#1f497d"><u></u>&nbsp;<u></u></span>
    <div class="row">
             <div class="col-md-5" style="padding:10px;">
<a href="http://www.hindustanscale.com/" target="_blank" data-saferedirecturl="https://www.google.com/url?q=http://www.hindustanscale.com/&amp;source=gmail&amp;ust=1585915082471000&amp;usg=AFQjCNHRZAgVIPbzu5iKqetrBZA5Gw5aDQ">
    <img  src="/media/pi_history_file/hsco.jpg" style="width: 50%; height:80px;"></a>
         </div>
        </div>
    <span style="font-size: 12.0pt;font-family: 'Times New Roman',serif; color: #ff6600;">An ISO 9001:2015 Certified Company</span>
    <div class="row">
             <div class="col-md-5" style="padding:10px;">
<img src="/media/pi_history_file/l.png" style="width: 100%;">
         </div>
        </div> </body></html>'''
                subject = 'Support'
                # pdf1 =
                email_send = EmailMessage(subject, 'testing', settings.EMAIL_HOST_USER, [lead_id.customer_id.customer_email_id])
                # msg = EmailMultiAlternatives(subject,'fdsklfhsd' , settings.EMAIL_HOST_USER,[lead_id.customer_id.customer_email_id])
                if email == 'True' :
                    # msg.attach(pdf, history.file.read(), 'application/pdf')

                    # email_send.content_subtype = "text/html"  # Main content is now text/html

                    email_send.attach_file(history.file.path)
                    print(history.file.path)
                    # msg.attach_file(pdf)
                    email_send.send()

            if whatsapp == 'True':
                return redirect('https://api.whatsapp.com/send?phone=91' + customer_id.contact_no + '&text=' + 'hi')

            if Pi_section.objects.filter(lead_id=id).count() > 0:

                item2 = Pi_section.objects.filter(lead_id=id).first()
                item2.discount = discount
                if upload_pi_file != None  or '':
                    item2.upload_pi_file = upload_pi_file
                item2.select_pi_template = select_pi_template
                item2.call = call
                item2.email = email
                item2.whatsapp = whatsapp
                item2.call2 = call2
                item2.select_gst_type = select_gst_type
                item2.discount_type = discount_type
                item2.log_entered_by = request.user.name
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
                        item2.grand_total = item2.round_up_total
                    elif discount_type == 'rupee' and discount != '' and discount != 0 and total_cost != '':
                        net_total = float(total_cost) - float(discount)
                        item2.net_total = net_total
                        item2.cgst_sgst = (9.0 * net_total)/100.0
                        igst = (18.0 * item2.net_total)/100.0
                        item2.igst = igst
                        item2.round_up_total = round(item2.net_total + pf_total + igst)
                        item2.grand_total = item2.round_up_total
                except:
                    print("product not added or debugging needed")


                item2.save(update_fields=['discount', 'upload_pi_file', 'select_pi_template', 'call','net_total','cgst_sgst','igst',
                                          'round_up_total','grand_total','total_cost','notes','pf_total',
                                        'email', 'whatsapp','call2','select_gst_type','discount_type','log_entered_by'  ])


            else :

                item2 = Pi_section()
                item2.discount = discount
                item2.upload_pi_file = upload_pi_file
                item2.select_pi_template = select_pi_template
                item2.call = call
                item2.email = email
                item2.whatsapp = whatsapp
                item2.call2 = call2
                item2.select_gst_type = select_gst_type
                item2.discount_type = discount_type
                item2.lead_id = Lead.objects.get(id=id)
                item2.log_entered_by = request.user.name
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
                        item2.grand_total = item2.round_up_total
                    elif discount_type == 'rupee' and discount != '' and discount != 0 and total_cost != '':
                        net_total = float(total_cost) - float(discount)
                        item2.net_total = net_total
                        item2.cgst_sgst = (9.0 * net_total)/100.0
                        igst = (18.0 * item2.net_total)/100.0
                        item2.igst = igst
                        item2.round_up_total = round(item2.net_total + pf_total + igst)
                        item2.grand_total = item2.round_up_total
                except:
                    print("product not added or debugging needed")

                item2.save()
                # if whatsapp == 'True':
                #     return redirect('https://api.whatsapp.com/send?phone=91' + customer_id.contact_no + '&text=' + 'hi')

        elif 'submit3' in request.POST:
            selected_fields = request.POST.getlist('checks[]')
            Follow_up_section.objects.filter(lead_id=id).update(fields=selected_fields)
            hfu = Follow_up_section.objects.filter(lead_id=id).last()
            context23 = {

                'hfu': hfu.fields,
            }
            context.update(context23)

        elif 'submit56' in request.POST:
            if(request.session['wa_msg']):
                wa_msg = request.session['wa_msg']
                sms_content = request.session['wa_content']
                wa_no = request.session['wa_no']
                try:
                    del request.session['wa_msg']
                    del request.session['wa_content']
                    del request.session['wa_no']
                except:
                    pass
            else:
                return render(request, 'lead_management/update_view_lead.html', context)

            return redirect('https://api.whatsapp.com/send?phone=91' + wa_no + '&text=' + wa_msg + '\n' + sms_content)

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

            if(len(selected_products)<1):

                context22={
                    'error':"No Product Selected\nPlease Select Products And Try Again",
                    'error_exist':True,
                }
                context.update(context22)
            elif(is_call!='on' and is_sms!='on' and is_whatsapp!='on' and is_email!='on' and is_call!='is_call' and is_sms!='is_sms' and is_whatsapp!='is_whatsapp' and is_email !='is_email'):
                context28 = {
                    'error': "Please Select Atleast One Medium For Followup",
                    'error_exist': True,
                }
                context.update(context28)
            elif (len(selected_fields)<6):

                context28 = {
                    'error': "Please Select Atleast One Product Field",
                    'error_exist': True,
                }
                context.update(context28)
            elif (email_auto_manual == 'Select Mode'):

                context28 = {
                    'error': "Please Select Follow Up Mode",
                    'error_exist': True,
                }
                context.update(context28)
            elif(email_auto_manual == 'Manual'):

                final_list = []
                Follow_up_section.objects.filter(lead_id=id).update(whatsappno=wa_no,)
                Follow_up_section.objects.filter(lead_id=id).update(auto_manual_mode=email_auto_manual,)

                history_follow= History_followup()
                history_follow.follow_up_section=Follow_up_section.objects.get(id=hfu.id)


                selected_fields2 = selected_fields.replace("'", "").strip('][').split(', ')  # convert string to list
                history_follow.fields = selected_fields2
                history_follow.product_ids = selected_products

                length_of_list = 1
                count_list = 0

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
                        print('item.partition(":")[0]')
                        print('item.partition(":")[0]')
                        print('"'+item.partition(":")[0]+'"')
                        if item.partition(":")[0] == 'Product Image ':
                            img_path = 'http://139.59.76.87:8000/media/'+item.partition(":")[2]
                            sms_content = sms_content + item.partition(":")[0] + ''' :''' + img_path + '''\n'''
                            wa_content = wa_content + item.partition(":")[0] + ''' :''' + img_path + '''\n'''
                            html_rows = html_rows + '''<td> <img height="150" width="150" src="'''+img_path+'''"> </td>'''
                            print('img_path')
                            print("'"+img_path+"'")
                            print("'"+img_path+"'")

                        elif item.partition(":")[0] == 'Product Brochure ':
                            bro_link = 'http://139.59.76.87:8000/media/'+item.partition(":")[2]
                            sms_content = sms_content + item.partition(":")[0] + ''' :''' + bro_link + '''\n'''
                            wa_content = wa_content + item.partition(":")[0] + ''' :''' + bro_link + '''\n'''
                            html_rows = html_rows + '''<td> <a href="'''+bro_link+'''" target="_blank">View Brochure</a> </td>'''
                        elif item.partition(":")[0] == 'Product Document ':
                            bro_link = 'http://139.59.76.87:8000/media/'+item.partition(":")[2]
                            sms_content = sms_content + item.partition(":")[0] + ''' :''' + bro_link + '''\n'''
                            wa_content = wa_content + item.partition(":")[0] + ''' :''' + bro_link + '''\n'''
                            html_rows = html_rows + '''<td> <a href="'''+bro_link+'''" target="_blank">View Brochure</a> </td>'''
                        else:
                            sms_content = sms_content + item.partition(":")[0] +''' :'''+item.partition(":")[2]+'''\n'''
                            wa_content = wa_content + item.partition(":")[0] +''' :'''+item.partition(":")[2]+'''\n'''
                            html_rows = html_rows + '''<td>''' + item.partition(":")[2] + '''</td>'''

                    html_rows = html_rows + '''</tr>'''



                if(is_email=='on' or is_email =='is_email'):
                    email_subject = request.POST.get('email_subject')
                    email_msg = request.POST.get('email_msg')
                    history_follow.is_email=True
                    history_follow.email_subject=email_subject
                    history_follow.email_msg=email_msg
                    Follow_up_section.objects.filter(lead_id=id).update(email_subject=email_subject, )

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
                    history_follow.file.save('AutoFollowup.html', file, save=False)
                    history_follow.html_content = html_content

                    send_html_mail(email_subject, html_content, settings.EMAIL_HOST_USER, [customer_id.customer_email_id, ])
                    context28 = {
                        'success': "Email Sent on email Id: "+customer_id.customer_email_id,
                        'success_exist': True,
                    }
                    context.update(context28)

                if(is_whatsapp=='on' or is_whatsapp=='is_whatsapp'):
                    history_follow.is_whatsapp = True
                    history_follow.wa_msg = wa_msg
                    history_follow.wa_no = wa_no
                    try:
                        del request.session['wa_msg']
                        del request.session['wa_content']
                        del request.session['wa_no']
                    except:
                        pass
                    request.session['wa_msg']=wa_msg
                    request.session['wa_content']=wa_content
                    request.session['wa_no']=wa_no
                    context28 = {
                        'success_2': "WhatsApp Redirect Successful On WhatsApp No : " + wa_no,
                        'success_exist_2': True,
                    }
                    context.update(context28)

                if(is_sms=='on' or is_sms=='is_sms'):
                    sms_msg = request.POST.get('sms_msg')
                    history_follow.is_sms = True
                    history_follow.sms_msg = sms_msg+'\n'+sms_content

                    url = "http://smshorizon.co.in/api/sendsms.php?user=" + settings.user + "&apikey=" + settings.api + "&mobile=" + customer_id.contact_no + "&message=" + sms_msg + "&senderid=" + settings.senderid + "&type=txt"
                    payload = ""
                    headers = {'content-type': 'application/x-www-form-urlencoded'}

                    response = requests.request("GET", url, data=json.dumps(payload), headers=headers)
                    x = response.text
                    print(x)
                    context28 = {
                        'success_4': "SMS Sent Successfully To : " + customer_id.contact_no,
                        'success_exist_4': True,
                    }
                    context.update(context28)

                if(is_call=='on' or is_call=='is_call'):
                    call_response = request.POST.get('call_response')
                    history_follow.is_call = True
                    history_follow.call_response = call_response
                    context28 = {
                        'success_5': "Call Response Recorded Successfully" ,
                        'success_exist_5': True,
                    }
                    context.update(context28)
                history_follow.log_entered_by = request.user.name

                history_follow.save()
            elif (email_auto_manual == 'Automatic'):

                if(Auto_followup_details.objects.filter(follow_up_history__follow_up_section__lead_id__id=lead_id.id).count()==0):
                    final_list = []
                    Follow_up_section.objects.filter(lead_id=id).update(whatsappno=wa_no, )
                    Follow_up_section.objects.filter(lead_id=id).update(auto_manual_mode=email_auto_manual, )

                    history_follow = History_followup()
                    history_follow.follow_up_section = Follow_up_section.objects.get(id=hfu.id)

                    selected_fields2 = selected_fields.replace("'", "").strip('][').split(
                        ', ')  # convert string to list
                    history_follow.fields = selected_fields2
                    history_follow.product_ids = selected_products
                    history_follow.is_manual_mode = False
                    history_follow.is_call = False
                    history_follow.is_whatsapp = False

                    length_of_list = 1
                    count_list = 0

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
                        history_follow.file.save('AutoFollowup.html', file, save=False)
                        history_follow.html_content= html_content



                    if(is_sms=='on' or is_sms=='is_sms'):
                        sms_msg = request.POST.get('sms_msg')
                        history_follow.is_sms = True
                        history_follow.sms_msg = sms_msg + '\n' + sms_content


                    history_follow.log_entered_by = request.user.name

                    history_follow.save()
                    afd= Auto_followup_details()
                    afd.follow_up_history = History_followup.objects.get(id=history_follow.pk)
                    afd.save()
                    context28 = {
                        'success_6': "Followup Will Be Done Automatically After Every 2 Days",
                        'success_exist_6': True,
                    }
                    context.update(context28)
                elif(Auto_followup_details.objects.filter(follow_up_history__follow_up_section__lead_id__id=lead_id.id).count()>0):
                    context28 = {
                        'error': "Auto Follow-Up is Already Set For This Lead\nTo Edit Auto Follow-Up Click On History Button In Follow-Up Section",
                        'error_exist': True,
                    }
                    context.update(context28)


    return render(request, 'lead_management/update_view_lead.html',context)

def load_wa(wa_no,wa_msg,sms_content):
    return redirect('https://api.whatsapp.com/send?phone=91' + wa_no + '&text=' + wa_msg + '\n' + sms_content)

def lead_report(request):
    if request.method =='POST' :
        selected_list = request.POST.getlist('checks[]')
        start_date = request.POST.get('date1')
        end_date = request.POST.get('date2')
        string = ','.join(selected_list)

        request.session['start_date'] = start_date
        request.session['end_date'] = end_date
        request.session['string'] = string
        request.session['selected_list'] = selected_list

        if 'submit1' in request.POST:
            table_name = 'Customer Details Section'
            request.session['table_name'] = table_name
        elif 'submit2' in request.POST:
            table_name = 'Deal Details Section'
            request.session['table_name'] = table_name
        elif 'submit3' in request.POST:
            table_name = 'PI Section'
            request.session['table_name'] = table_name
        elif 'submit4' in request.POST:
            table_name = 'Follow-up Section'
            request.session['table_name'] = table_name
        elif 'submit5' in request.POST:
            table_name = 'Payment Details Form'
            request.session['table_name'] = table_name
        return redirect('/final_lead_report/')
    return render(request,'lead_management/report_lead.html')

def final_lead_report(request):
    table_name = request.session.get('table_name')
    start_date = request.session.get('start_date')
    end_date = request.session.get('end_date')
    string = request.session.get('string')
    selected_list = request.session.get('selected_list')
    final_row_product = []
    final_row=[]
    context = {
        'final_row': final_row,
        'final_row_product': final_row_product,
        'selected_list': selected_list,
    }
    if table_name == 'Customer Details Section':
        # customer_list = Customer_Details.objects.filter(entry_timedate__range=(start_date, end_date)).values_list(string)
        with connection.cursor() as cursor:
            if string != '' :
                    cursor.execute("SELECT " +  string + " from customer_app_customer_details  PRODUCT  where "
                    " entry_timedate between'" + start_date + "' and '" + end_date + "';")
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
            del request.session['start_date']
            del request.session['end_date']
            del request.session['string']
            del request.session['selected_list']
        except:
            pass
    if table_name == 'Deal Details Section':

        # customer_list = Customer_Details.objects.filter(entry_timedate__range=(start_date, end_date)).values_list(string)
        with connection.cursor() as cursor:
            if string != '' :
                    cursor.execute("SELECT " +  string + " from lead_management_lead  PRODUCT  where "
                    " entry_timedate between '" + start_date + "' and '" + end_date + "';")
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
            del request.session['start_date']
            del request.session['end_date']
            del request.session['string']
            del request.session['selected_list']
        except:
            pass
    if table_name == 'PI Section':
        # customer_list = Customer_Details.objects.filter(entry_timedate__range=(start_date, end_date)).values_list(string)
        selected_list = ['lead_id','discount','discount_type','payment_channel','payment_received_date','notes','cgst_sgst','igst','grand_total','entry_timedate'
                         ,'quantity','P&F']


        with connection.cursor() as cursor:

            cursor.execute("SELECT PI.lead_id_id,discount,discount_type,payment_channel,payment_received_date,notes,cgst_sgst,igst,grand_total,PRODUCT.entry_timedate,"
                           "quantity,pf "
                           " from lead_management_pi_section PI, lead_management_pi_product PRODUCT where PRODUCT.lead_id_id = PI.lead_id_id and "
                           "PRODUCT.entry_timedate between'" + start_date + "' and '" + end_date + "';")
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
            del request.session['start_date']
            del request.session['end_date']
            del request.session['string']
            del request.session['selected_list']
        except:
            pass
    if table_name == 'Follow-up Section':
        # customer_list = Customer_Details.objects.filter(entry_timedate__range=(start_date, end_date)).values_list(string)
        selected_list = ['lead_id', 'whatsappno', 'fields', 'email_subject','product_id', 'scale_type', 'main_category','sub_category', 'sub_sub_category',
                         'hsn_code','max_capacity', 'accuracy', 'platform_size','product_desc','cost_price','selling_price','carton_size',
                         'entry_timedate']

        with connection.cursor() as cursor:

            cursor.execute(
                "SELECT FOLLOW.lead_id_id,whatsappno,fields,email_subject,product_id_id,scale_type,main_category,sub_category,sub_sub_category,hsn_code,"
                "max_capacity,accuracy,platform_size,product_desc,cost_price,selling_price,carton_size,PRODUCT.entry_timedate"
                " from lead_management_follow_up_section FOLLOW, lead_management_followup_product PRODUCT where PRODUCT.lead_id_id = FOLLOW.lead_id_id and "
                "PRODUCT.entry_timedate between'" + start_date + "' and '" + end_date + "';")
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
            del request.session['start_date']
            del request.session['end_date']
            del request.session['string']
            del request.session['selected_list']
        except:
            pass
    if table_name == 'Payment Details Form':
        # customer_list = Customer_Details.objects.filter(entry_timedate__range=(start_date, end_date)).values_list(string)
        with connection.cursor() as cursor:
            if string != '' :
                    cursor.execute("SELECT " +  string + " from lead_management_payment_details  PRODUCT  where "
                    " entry_timedate between'" + start_date + "' and '" + end_date + "';")
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
            del request.session['start_date']
            del request.session['end_date']
            del request.session['string']
            del request.session['selected_list']
        except:
            pass

    context={
        'final_row':final_row,
        'final_row_product':final_row_product,
        'selected_list':selected_list,
    }
    return render(request,"report/final_lead_report.html",context)

def select_product_followup(request,id):
    type_of_purchase_list =type_purchase.objects.all() #1
    lead_id = Lead.objects.get(id=id)
    products = Product.objects.all()
    context={}
    if request.method == 'POST' or request.method == 'FILES' :
        if 'product_id' in request.POST:
            is_last_product_yes = request.POST.get('is_last_product_yes')
            product_id = request.POST.get('product_id')

            requested_product = Product.objects.get(id=product_id)

            fol_pro=Followup_product()
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


            if is_last_product_yes == 'yes':
                return redirect('/update_view_lead/' + str(id))
            elif is_last_product_yes == 'no':
                return redirect('/select_product_followup/' + str(id))
        else:
            model_of_purchase_str = request.POST.get('model_of_purchase')
            type_of_scale_str = request.POST.get('type_of_scale')
            sub_model_str = request.POST.get('sub_model')
            sub_sub_model_str = request.POST.get('sub_sub_model')

            if (sub_sub_model == None or sub_sub_model == ""):
                product_avail = Product.objects.filter(scale_type=type_purchase.objects.get(id=type_of_scale_str).name, main_category=main_model.objects.get(id=model_of_purchase_str).name,
                                                       sub_category=sub_model.objects.get(id=sub_model_str).name)
            else:
                product_avail = Product.objects.filter(scale_type=type_purchase.objects.get(id=type_of_scale_str).id, main_category=main_model.objects.get(id=model_of_purchase_str).id,
                                                       sub_category=sub_model.objects.get(id=sub_model_str).id, sub_sub_category=sub_sub_model.objects.get(id=sub_sub_model_str).id)

            context23 = {
                'product_avail': product_avail,
            }
            context.update(context23)

    context2={
        'lead_id':lead_id,
        'type_purchase':type_of_purchase_list,
        'products':products,
    }
    context.update(context2)
    return render(request,'lead_management/select_product_followup.html', context)

def select_product(request,id):
    type_of_purchase_list =type_purchase.objects.all() #1
    lead_id = Lead.objects.get(id=id)
    products = Product.objects.all()
    if request.method == 'POST' or request.method == 'FILES':
        hsn_code = request.POST.get('hsn_code')
        pf = request.POST.get('pf')
        quantity = request.POST.get('quantity')
        is_last_product_yes = request.POST.get('is_last_product_yes')
        # model_of_purchase = request.POST.get('model_of_purchase')
        type_of_scale = request.POST.get('scale_type')
        main_category = request.POST.get('main_category')
        sub_category = request.POST.get('sub_category')
        sub_sub_category = request.POST.get('sub_sub_category')    #product code or sub_sub_category

        item = Pi_product()
        if sub_sub_category != '':
            item.product_id = Product.objects.get(scale_type=type_of_scale, main_category=main_category,
                                                  sub_category=sub_category, sub_sub_category=sub_sub_category)
        item.lead_id = Lead.objects.get(id=lead_id)
        item.quantity = quantity
        item.pf = pf
        item.log_entered_by = request.user.name
        if quantity != 'None' or quantity != '':
            item.product_total_cost = float(item.product_id.selling_price) * float(quantity)
        item.save()
        if is_last_product_yes == 'yes':
            return redirect('/update_view_lead/' + str(id))
        elif is_last_product_yes == 'no':
            return redirect('/select_product/' + str(id))
    context = {
        'lead_id': lead_id,
        'type_of_purchase_list': type_of_purchase_list,
        'products': products,
    }
    return render(request, 'lead_management/select_product.html', context)

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


def lead_follow_up_histroy(request,follow_up_id):
    context={}
    obj_list = History_followup.objects.filter(follow_up_section=follow_up_id).order_by("-entry_timedate")

    if request.method == 'POST':
        if 'sub1' in request.POST:
            delete_id = request.POST.get('delete_id')

            Auto_followup_details.objects.filter(follow_up_history__pk=delete_id).delete()
            History_followup.objects.filter(id=delete_id).update(is_auto_follow_deleted=True)
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

def pi_section_history(request,id):
    lead_id = Lead.objects.get(id=id)
    # lead_pi_id = Pi_section.objects.get(lead_id=id)
    lead_pi_history = Pi_History.objects.filter(lead_id=id).order_by('-id')
    context = {
        'lead_id': lead_id,
        'lead_pi_history': lead_pi_history,
    }
    return render(request,'lead_management/lead_history.html',context)

def lead_delete_product(request,id):
    leads = Pi_product.objects.filter(lead_id=id).order_by('-id')
    if request.method == 'POST' or request.method=='FILES':
        delete_id = request.POST.getlist('check[]')
        for i in delete_id:
            Pi_product.objects.filter(id=i).delete()
    context={
        'leads':leads,
    }
    return render(request,'lead_management/lead_delete_product.html',context)

def lead_analytics(request):
    #this month lead
    current_month_lead = Pi_section.objects.filter(lead_id__current_stage='PO Issued - Payment Done - Dispatch Pending',
                                                entry_timedate__month=datetime.now().month) \
        .values('entry_timedate').annotate(data_sum=Sum('grand_total'))
    current_month_lead_date = []
    current_month_lead_sum = []
    for i in current_month_lead:
        x = i
        current_month_lead_date.append(x['entry_timedate'].strftime('%Y-%m-%d'))
        current_month_lead_sum.append(x['data_sum'])

    #previous month lead
    mon = (datetime.now().month)
    if mon == 1:
        previous_mon = 12
    else:
        previous_mon = (datetime.now().month) - 1
    previous_month_lead = Pi_section.objects.filter(lead_id__current_stage='PO Issued - Payment Done - Dispatch Pending',
                                                   entry_timedate__month=previous_mon) \
        .values('entry_timedate').annotate(data_sum=Sum('grand_total'))
    previous_month_lead_date = []
    previous_month_lead_sum = []
    for i in previous_month_lead:
        x = i
        previous_month_lead_date.append(x['entry_timedate'].strftime('%Y-%m-%d'))
        previous_month_lead_sum.append(x['data_sum'])
    context = {
        'current_month_lead_date': current_month_lead_date,
        'current_month_lead_sum': current_month_lead_sum,
        'previous_month_lead_date': previous_month_lead_date,
        'previous_month_lead_sum': previous_month_lead_sum,

    }
    if request.method=='POST' and 'date1' in request.POST :
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
            'current_month_lead_date': current_month_lead_date,
            'current_month_lead_sum': current_month_lead_sum,
            'previous_month_lead_date': previous_month_lead_date,
            'previous_month_lead_sum': previous_month_lead_sum,
            'lead_conversion_date': lead_conversion_date,
            'lead_conversion_sum': lead_conversion_sum,

        }

    return render(request,'lead_management/lead_analytics.html',context)

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

def lead_pi_form(request):
    return render(request,'lead_management/lead_pi_form.html')

def alpha_pi_form(request):
    return render(request,'lead_management/alpha_pi_template.html')

def report_2(request):
    return render(request,'lead_management/report_2.html')



def download_pi_image(request):
    return render(request,'lead_management/download_pi_image.html')

def download_pi_pdf(request):
    return render(request,'lead_management/download_pi_pdf.html')

def lead_logs(request):
    lead_logs = Log.objects.filter(module_name='Lead Module').order_by('-id')
    print(lead_logs)
    print(lead_logs)
    print(lead_logs)
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
                log.save()

    except:
        pass


def download_pi_image(request,id):
    return render(request,'lead_management/download_pi_image.html')

def download_pi_pdf(request,id):
    lead_id=Lead.objects.get(id=id)
    todays_date = str(datetime.now().strftime("%Y-%m-%d"))
    pi_id = Pi_section.objects.get(lead_id=id)

    pi_products = Pi_product.objects.filter(lead_id=id)
    context={
        'lead_id':lead_id,
        'todays_date':todays_date,
        'pi_id':pi_id,
        'pi_products':pi_products,
    }
    return render(request,'lead_management/download_pi_pdf.html',context)

def download_pi_second_pdf(request,id):
    lead_id=Lead.objects.get(id=id)
    todays_date = str(datetime.now().strftime("%Y-%m-%d"))
    pi_id = Pi_section.objects.get(lead_id=id)

    pi_products = Pi_product.objects.filter(lead_id=id)
    context={
        'lead_id':lead_id,
        'todays_date':todays_date,
        'pi_id':pi_id,
        'pi_products':pi_products,
    }
    return render(request,'lead_management/download_pi_second_pdf.html',context)

@login_required(login_url='/')
def check_admin_roles(request):
    if request.user.role == 'Super Admin' or request.user.role == 'Admin' or request.user.role == 'Manager':
        return True
    else:
        return False