from django.db.models import Q, F
from django.http import HttpResponse
from django.shortcuts import render, redirect

from customer_app.models import Customer_Details,type_purchase

from purchase_app.views import check_admin_roles
from user_app.models import SiteUser

from ess_app.models import Employee_Analysis_month, Employee_Analysis_date
from .forms import AMC_Feedback_Form
from .models import Amc_After_Sales, AMC_Feedback
from django.db import connection
from django.core.mail import send_mail
from Hsco import settings
import requests
import json
import datetime


def add_amc_after_sales(request):
    cust_sugg = Customer_Details.objects.all()
    type_purchase2 = type_purchase.objects.all()
    if request.method == 'POST':
        address = request.POST.get('customer_address')
        contact_no = request.POST.get('contact_no')
        # amcno = request.POST.get('amcno')
        customer_name = request.POST.get('customer_name')
        company_name = request.POST.get('company_name')
        # customer_no = request.POST.get('customer_no')
        customer_email_id = request.POST.get('customer_email_id')
        # second_person = request.POST.get('second_person')
        # third_person = request.POST.get('third_person')
        # second_contact_no = request.POST.get('second_contact_no')
        # third_contact_no = request.POST.get('third_contact_no')
        type_of_scale = request.POST.get('type_of_scale')
        serial_no_scale = request.POST.get('serial_no_scale')
        contract_valid_in_years = request.POST.get('contract_valid_in_years')
        contract_amount = request.POST.get('contract_amount')
        contract_no_reporting_breakdown = request.POST.get('contract_no_reporting_breakdown')
        contract_start_date = request.POST.get('contract_start_date')
        contract_end_date = request.POST.get('contract_end_date')
        visit_1 = request.POST.get('visit_1')
        repot_1 = request.POST.get('repot_1')
        visit_2 = request.POST.get('visit_2')
        repot_2 = request.POST.get('repot_2')
        visit_3 = request.POST.get('visit_3')
        repot_3 = request.POST.get('repot_3')
        visit_4 = request.POST.get('visit_4')
        repot_4 = request.POST.get('repot_4')

        item2 = Amc_After_Sales()
        item = Customer_Details()
        if Customer_Details.objects.filter(Q(customer_name=customer_name),Q(contact_no=contact_no)).count() > 0:

            item2.crm_no = Customer_Details.objects.filter(Q(customer_name=customer_name),Q(contact_no=contact_no)).first()

            item3 = Customer_Details.objects.filter(customer_name=customer_name, contact_no=contact_no).first()
            if company_name != '':
                item2.second_company_name = company_name  # new2

                item3.company_name = company_name
                item3.save(update_fields=['company_name'])
                # item2.save(update_fields=['second_company_name'])
            if address != '':
                item3.address = address

                item2.company_address = address  # new2
                item3.save(update_fields=['address'])
                # item2.save(update_fields=['company_address'])
            if customer_email_id != '':
                item3.customer_email_id = customer_email_id
                item2.company_email = customer_email_id  # new2
                item3.save(update_fields=['customer_email_id'])
                # item2.save(update_fields=['company_email'])

        else:
            item.customer_name = customer_name

            item.contact_no = contact_no


            if company_name != '':
                item2.second_company_name = company_name  # new2
                item.company_name = company_name
            if address != '':
                item.address = address
                item2.company_address = address  # new2
            item.second_contact_no = contact_no
            if customer_email_id != '':
                item2.company_email = customer_email_id  # new2
                item.customer_email_id = customer_email_id

            # item.user_id = SiteUser.objects.get(id=request.user.pk)
            # item.manager_id = SiteUser.objects.get(id=request.user.pk).group

            item.save()

            item2.crm_no = Customer_Details.objects.get(id=item.pk)
        # item2.amcno = amcno
        # item2.customer_name = customer_name
        # item2.company_name = company_name
        # item2.crm_no = customer_no
        # item2.customer_email_id = customer_email_id
        # item2.second_person=second_person
        # item2.third_person=third_person
        # item2.second_contact_no=second_contact_no
        # item2.third_contact_no=third_contact_no
        item2.second_person = customer_name  # new1
        item2.second_contact_no = contact_no  # new2
        item2.type_of_scale = type_of_scale
        item2.serial_no_scale = serial_no_scale
        item2.contract_valid_in_years = contract_valid_in_years
        item2.contract_amount = contract_amount
        item2.contract_no_reporting_breakdown = contract_no_reporting_breakdown
        item2.contract_start_date = contract_start_date
        item2.contract_end_date = contract_end_date
        if visit_1 != '':
            item2.visit_1 = visit_1
        item2.repot_1 = repot_1
        if visit_2 != '':
            item2.visit_2 = visit_2
        item2.repot_2 = repot_2
        if visit_3 != '':
            item2.visit_3 = visit_3
        item2.repot_3 = repot_3
        if visit_4 != '':
            item2.visit_4 = visit_4
        item2.repot_4 = repot_4
        item2.user_id = SiteUser.objects.get(id=request.user.pk)
        item2.manager_id = SiteUser.objects.get(id=request.user.pk).group
        item2.save()

        # Amc_After_Sales.objects.filter(id=id).update(total_cost=F("total_cost") + contract_amount)
        # Employee_Analysis_month.objects.filter(user_id=request.user.pk, entry_date__month=datetime.now().month,
        #                                        year=datetime.now().year).update(
        #     total_reparing_done=F("total_reparing_done") + contract_amount)
        #
        # Employee_Analysis_date.objects.filter(user_id=request.user.pk, entry_date__month=datetime.now().month,
        #                                       year=datetime.now().year).update(
        #     total_reparing_done_today=F("total_reparing_done_today") + contract_amount)



        if Customer_Details.objects.filter(Q(customer_name=customer_name),
                                           Q(contact_no=contact_no)).count() > 0:

            crm_no = Customer_Details.objects.filter(Q(customer_name=customer_name),
                                                           Q(contact_no=contact_no)).first()

            send_mail('Feedback Form', 'Click on the link to give feedback http://139.59.76.87/feedback_amc/' + str(
                request.user.pk) + '/' + str(crm_no.id) + '/' + str(item2.id), settings.EMAIL_HOST_USER,
                      [crm_no.customer_email_id])

            message = 'Click on the link to give feedback http://139.59.76.87/feedback_amc/' + str(
                request.user.pk) + '/' + str(crm_no.id) + '/' + str(item2.id)

            url = "http://smshorizon.co.in/api/sendsms.php?user=" + settings.user + "&apikey=" + settings.api + "&mobile=" + crm_no.contact_no + "&message=" + message + "&senderid=" + settings.senderid + "&type=txt"
            payload = ""
            headers = {'content-type': 'application/x-www-form-urlencoded'}

            response = requests.request("GET", url, data=json.dumps(payload), headers=headers)
            x = response.text



        else:
            send_mail('Feedback Form', 'Click on the link to give feedback http://139.59.76.87/feedback_amc/' + str(
                request.user.pk) + '/' + str(item.id) + '/' + str(item2.id), settings.EMAIL_HOST_USER,
                      [item.customer_email_id])

            message = 'Click on the link to give feedback http://139.59.76.87/feedback_amc/' + str(
                request.user.pk) + '/' + str(item.id) + '/' + str(item2.id)

            url = "http://smshorizon.co.in/api/sendsms.php?user=" + settings.user + "&apikey=" + settings.api + "&mobile=" + item.contact_no + "&message=" + message + "&senderid=" + settings.senderid + "&type=txt"
            payload = ""
            headers = {'content-type': 'application/x-www-form-urlencoded'}

            response = requests.request("GET", url, data=json.dumps(payload), headers=headers)
            x = response.text




        return redirect('/amc_views')
    context = {
        'type_purchase': type_purchase2,
        'cust_sugg': cust_sugg,
    }
    return render(request,'forms/amc_form.html', context)

def report_amc(request):
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
        return redirect('/final_report_amc/')
    return render(request, "report/report_amc_form.html",)

def final_report_amc(request):
    start_date =    request.session.get('start_date')
    end_date =      request.session.get('end_date')
    string =        request.session.get('string')
    selected_list = request.session.get('selected_list')


    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT  " + string + " from amc_visit_app_amc_after_sales , customer_app_customer_details"
                                          "  where amc_visit_app_amc_after_sales.crm_no_id = customer_app_customer_details.id and entry_timedate between '" + start_date + "' and '" + end_date + "';")
        row = cursor.fetchall()

        final_row= [list(x) for x in row]
        list3=[]
        for i in row:
            list3.append(list(i))
    try:
        del request.session['start_date']
        del request.session['end_date']
        del request.session['string']
        del request.session['selected_list']
    except:
        pass

    context={
        'final_row':final_row,
        'selected_list':selected_list,
    }
    return render(request,"report/amc_final_report.html",context)

def amc_views(request):
    if request.method=='POST' :
        if'submit1' in request.POST:
            start_date = request.POST.get('date1')
            end_date = request.POST.get('date2')
            if check_admin_roles(request):  # For ADMIN
                amc_list = Amc_After_Sales.objects.filter(user_id__group__icontains=request.user.name,
                                                          user_id__is_deleted=False,entry_timedate__range=[start_date, end_date]).order_by('-id')
            else:  # For EMPLOYEE
                amc_list = Amc_After_Sales.objects.filter(user_id=request.user.pk,entry_timedate__range=[start_date, end_date]).order_by('-id')
            # amc_list = Amc_After_Sales.objects.filter()
            context = {
                'amc_list': amc_list,
                'search_msg': 'Search result for date range: ' + start_date + ' TO ' + end_date,
            }
            return render(request, "manager/amc_view.html", context)
        elif 'submit2' in request.POST:
            contact = request.POST.get('contact')
            if check_admin_roles(request):  # For ADMIN
                amc_list = Amc_After_Sales.objects.filter(user_id__group__icontains=request.user.name,
                                                          user_id__is_deleted=False,second_contact_no__icontains=contact).order_by('-id')
            else:  # For EMPLOYEE
                amc_list = Amc_After_Sales.objects.filter(user_id=request.user.pk,second_contact_no__icontains=contact).order_by('-id')
            # amc_list = Amc_After_Sales.objects.filter(customer_no=contact)
            context = {
                'amc_list': amc_list,
                'search_msg': 'Search result for Customer Contact No: ' + contact,
            }
            return render(request, "manager/amc_view.html",context )

        elif 'submit3' in request.POST:
            email = request.POST.get('email')
            if check_admin_roles(request):  # For ADMIN
                amc_list = Amc_After_Sales.objects.filter(user_id__group__icontains=request.user.name,
                                                          user_id__is_deleted=False,company_email__icontains=email).order_by('-id')
            else:  # For EMPLOYEE
                amc_list = Amc_After_Sales.objects.filter(user_id=request.user.pk,company_email__icontains=email).order_by('-id')
            # dispatch_list = Amc_After_Sales.objects.filter(customer_email_id=email)
            context = {
                'amc_list': amc_list,
                'search_msg': 'Search result for Customer Email ID: ' + email,
            }
            return render(request, "manager/amc_view.html",context )
        elif 'submit4' in request.POST:
            customer = request.POST.get('customer')
            if check_admin_roles(request):  # For ADMIN
                amc_list = Amc_After_Sales.objects.filter(user_id__group__icontains=request.user.name,
                                                          user_id__is_deleted=False,second_person__icontains=customer).order_by('-id')
            else:  # For EMPLOYEE
                amc_list = Amc_After_Sales.objects.filter(user_id=request.user.pk,second_person__icontains=customer).order_by('-id')

            # dispatch_list = Amc_After_Sales.objects.filter(customer_name=customer)
            context = {
                'amc_list': amc_list,
                'search_msg': 'Search result for Customer Name: ' + customer,
            }
            return render(request, "manager/amc_view.html",context )

        elif  'submit5' in request.POST:
            company = request.POST.get('company')
            if check_admin_roles(request):  # For ADMIN
                amc_list = Amc_After_Sales.objects.filter(user_id__group__icontains=request.user.name,
                                                          user_id__is_deleted=False,
                                                          second_company_name__icontains=company).order_by('-id')
            else:  # For EMPLOYEE
                amc_list = Amc_After_Sales.objects.filter(user_id=request.user.pk,second_company_name__icontains=company).order_by('-id')

            # dispatch_list = Amc_After_Sales.objects.filter(customer_name=customer)
            context = {
                'amc_list': amc_list,
                'search_msg': 'Search result for Company Name: ' + company,
            }
            return render(request, "manager/amc_view.html", context)


            # dispatch_list = Amc_After_Sales.objects.filter(company_name=company)
            # context = {
            #     'amc_list': amc_list,
            # }
            # return render(request, "manager/amc_view.html",context )
        elif request.method=='POST' and 'submit6' in request.POST:
            crm = request.POST.get('crm')
            if check_admin_roles(request):  # For ADMIN
                amc_list = Amc_After_Sales.objects.filter(user_id__group__icontains=request.user.name,
                                                          user_id__is_deleted=False,crm_no__pk=crm).order_by('-id')
            else:  # For EMPLOYEE
                amc_list = Amc_After_Sales.objects.filter(user_id=request.user.pk,crm_no__pk=crm).order_by('-id')
            # amc_list = Amc_After_Sales.objects.all()

            # context = {
            #     'amc_list': amc_list,
            # }
            #
            # dispatch_list = Amc_After_Sales.objects.filter(crn_number=crm)
            context = {
                'amc_list': amc_list,
                'search_msg': 'Search result for CRM No. : ' + crm,
            }
            return render(request, "manager/amc_view.html",context )
    else:
        if request.user.role == 'Admin' or request.user.role == 'Super Admin':     #For ADMIN
            amc_list = Amc_After_Sales.objects.filter(Q(user_id__group__icontains=request.user.name,user_id__is_deleted=False) | Q(user_id__name__icontains=request.user.name)).order_by('-id')
        elif request.user.role == 'Manager':
            admin = SiteUser.objects.get(id=request.user.pk).admin
            amc_list = Amc_After_Sales.objects.filter(Q(user_id__admin=admin, user_id__is_deleted=False)| Q(user_id__name__icontains=request.user.name)).order_by(
                '-id')

        else:  #For EMPLOYEE
            manager = SiteUser.objects.get(id=request.user.pk).manager
            amc_list = Amc_After_Sales.objects.filter(Q(user_id__manager=manager,user_id__is_deleted=False)| Q(user_id__name__icontains=request.user.name)).order_by('-id')
        # amc_list = Amc_After_Sales.objects.all()

        context = {
            'amc_list': amc_list,

        }
        return render(request, "manager/amc_view.html",context )

def amc_logs(request):
    return render(request,"logs/amc_logs.html")

def update_amc_form(request,update_id):
    amc_list=Amc_After_Sales.objects.get(id=update_id)
    customer_id = Amc_After_Sales.objects.get(id=update_id).crm_no

    customer_id = Customer_Details.objects.get(id=customer_id)

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
        item2.save(update_fields=['customer_name','contact_no'])  #new3



        # amcno = request.POST.get('amcno')
        # customer_name = request.POST.get('customer_name')
        company_name = request.POST.get('company_name')
        # customer_no = request.POST.get('customer_no')
        type_of_scale = request.POST.get('type_of_scale')
        # second_person=request.POST.get('second_person')
        # third_person=request.POST.get('third_person')
        # second_contact_no=request.POST.get('second_contact_no')
        # third_contact_no=request.POST.get('third_contact_no')
        serial_no_scale = request.POST.get('serial_no_scale')
        contract_valid_in_years = request.POST.get('contract_valid_in_years')
        contract_amount = request.POST.get('contract_amount')
        contract_no_reporting_breakdown = request.POST.get('contract_no_reporting_breakdown')
        contract_start_date = request.POST.get('contract_start_date')
        contract_end_date = request.POST.get('contract_end_date')
        visit_1 = request.POST.get('visit_1')
        repot_1 = request.POST.get('repot_1')
        visit_2 = request.POST.get('visit_2')
        repot_2 = request.POST.get('repot_2')
        visit_3 = request.POST.get('visit_3')
        repot_3 = request.POST.get('repot_3')
        visit_4 = request.POST.get('visit_4')
        repot_4 = request.POST.get('repot_4')


        item = Amc_After_Sales.objects.get(id=update_id)
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
            item2.save(update_fields=['customer_email_id'])
            item.save(update_fields=['company_email', ]),

        # item.amcno = amcno
        item.customer_name = customer_name
        item.company_name = company_name
        # item.customer_no = customer_no
        item.type_of_scale = type_of_scale
        # item.second_person=second_person
        # item.third_person=third_person
        # item.second_contact_no=second_contact_no
        # item.third_contact_no=third_contact_no
        item.second_person=customer_name   #new4
        item.second_contact_no=contact_no   #new5
        item.serial_no_scale = serial_no_scale
        item.contract_valid_in_years = contract_valid_in_years
        item.contract_amount = contract_amount
        item.contract_no_reporting_breakdown = contract_no_reporting_breakdown
        item.contract_start_date = contract_start_date
        item.contract_end_date = contract_end_date



        if visit_1 != None and visit_1 != '' :
            item.visit_1 = visit_1
            item.save(update_fields=['visit_1',])
            print("visit_1")
            print(visit_1)

        item2.repot_1 = repot_1
        if visit_2 != '':
            item.visit_2 = visit_2
            item.save(update_fields=['visit_2',])
        item2.repot_2 = repot_2
        if visit_3 != '':
            item.visit_3 = visit_3
            item.save(update_fields=['visit_3',])
        item2.repot_3 = repot_3
        if visit_4 != '':
            item.visit_4 = visit_4
            item.save(update_fields=['visit_4',])

        item.repot_1 = repot_1
        item.repot_2 = repot_2
        item.repot_3 = repot_3
        item.repot_4 = repot_4
        item.save(update_fields=['contract_amount','type_of_scale','serial_no_scale',
                                 'contract_valid_in_years','contract_amount','contract_no_reporting_breakdown','contract_start_date',
                                 'contract_end_date','repot_1','repot_2','repot_3','repot_4','second_person','third_person',
                                 'second_contact_no','third_contact_no',])
        item.save(update_fields=['second_person','second_contact_no', ])

        # item2.save(update_fields=['company_address', ]),
        # item2.save(update_fields=['company_email', ]),

        return redirect('/amc_views')
    context={
        'amc_list':amc_list

    }
    return render(request,"update_forms/updated_amc_form.html",context)

def feedback_amc(request,user_id,customer_id,amc_id):
    feedback_form = AMC_Feedback_Form(request.POST or None)
    if request.method == 'POST':
        satisfied_with_work = request.POST.get('satisfied_with_work')
        speed_of_performance = request.POST.get('speed_of_performance')
        price_of_amc = request.POST.get('price_of_amc')
        overall_interaction = request.POST.get('overall_interaction')
        about_hsco = request.POST.get('about_hsco')
        any_suggestion = request.POST.get('any_suggestion')

        item = AMC_Feedback()
        item.satisfied_with_work = satisfied_with_work
        item.speed_of_performance = speed_of_performance
        item.price_of_amc = price_of_amc
        item.overall_interaction = overall_interaction
        item.about_hsco = about_hsco
        item.any_suggestion = any_suggestion
        item.user_id = SiteUser.objects.get(id=user_id)
        item.customer_id = Customer_Details.objects.get(id=customer_id)
        item.amc_id = Amc_After_Sales.objects.get(id=amc_id)
        try:
            item.save()

            amc = Amc_After_Sales.objects.get(id=amc_id)

            amc.avg_feedback = (float(item.satisfied_with_work) + float(item.speed_of_performance)  + float(item.price_of_amc)  + float(item.overall_interaction) )/ float(4.0)
            amc.feedback_given = True
            amc.save(update_fields=['avg_feedback', 'feedback_given'])

            if Employee_Analysis_month.objects.filter(Q(entry_date__month=datetime.now().month),
                                                      Q(user_id=SiteUser.objects.get(id=user_id))).count() > 0:
                Employee_Analysis_month.objects.filter(user_id=user_id, entry_date__month=datetime.now().month,
                                                       year=datetime.now().year).update(
                    start_rating_feedback_amc=(F("start_rating_feedback_amc") + amc.avg_feedback) / 2.0)
                # ead.total_sales_done_today=.filter(category_id_id=id).update(total_views=F("total_views") + value_of_goods)

                # ead.save(update_fields=['total_sales_done_today'])

            else:
                ead = Employee_Analysis_month()
                ead.user_id = SiteUser.objects.get(id=user_id)
                ead.start_rating_feedback_amc = Amc_After_Sales.objects.get(id=amc_id).avg_feedback
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
    return render(request,'feedback/feedback_amc.html',context)


