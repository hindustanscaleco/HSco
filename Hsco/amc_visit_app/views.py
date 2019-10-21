from django.http import HttpResponse
from django.shortcuts import render, redirect

from customer_app.models import Customer_Details

from purchase_app.views import check_admin_roles
from user_app.models import SiteUser
from .forms import AMC_Feedback_Form
from .models import Amc_After_Sales, AMC_Feedback
from django.db import connection
from django.core.mail import send_mail
from Hsco import settings
import requests
import json

def add_amc_after_sales(request):
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        company_name = request.POST.get('company_name')
        address = request.POST.get('address')
        contact_no = request.POST.get('contact_no')
        customer_email_id = request.POST.get('customer_email_id')

        item = Customer_Details()

        item.customer_name = customer_name
        item.company_name = company_name
        item.address = address
        item.contact_no = contact_no
        item.customer_email_id = customer_email_id

        item.save()

        amcno = request.POST.get('amcno')
        customer_name = request.POST.get('customer_name')
        company_name = request.POST.get('company_name')
        customer_no = request.POST.get('customer_no')
        customer_email_id = request.POST.get('customer_email_id')
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

        item2.crm_no_id = item.pk
        item2.amcno = amcno
        item2.customer_name = customer_name
        item2.company_name = company_name
        item2.customer_no = customer_no
        item2.customer_email_id = customer_email_id
        item2.type_of_scale = type_of_scale
        item2.serial_no_scale = serial_no_scale
        item2.contract_valid_in_years = contract_valid_in_years
        item2.contract_amount = contract_amount
        item2.contract_no_reporting_breakdown = contract_no_reporting_breakdown
        item2.contract_start_date = contract_start_date
        item2.contract_end_date = contract_end_date
        item2.visit_1 = visit_1
        item2.repot_1 = repot_1
        item2.visit_2 = visit_2
        item2.repot_2 = repot_2
        item2.visit_3 = visit_3
        item2.repot_3 = repot_3
        item2.visit_4 = visit_4
        item2.repot_4 = repot_4

        item2.save()
        send_mail('Feedback Form','Click on the link to give feedback' , settings.EMAIL_HOST_USER, [customer_email_id])

        message = 'message to be send with feedback link '


        #url = "http://smshorizon.co.in/api/sendsms.php?user=" + settings.user + "&apikey=" + settings.api + "&mobile=" + customer_no + "&message=" + message + "&senderid=" + settings.senderid + "&type=txt"
        payload = ""
        headers = {'content-type': 'application/x-www-form-urlencoded'}

        #response = requests.request("GET", url, data=json.dumps(payload), headers=headers)
        #x = response.text

        return redirect('/amc_views')


    context = {

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

    try:
        del request.session['start_date']
        del request.session['end_date']
        del request.session['string']
        del request.session['selected_list']
    except:
        pass
    with connection.cursor() as cursor:
        cursor.execute("SELECT  "+string+" from amc_visit_app_amc_after_sales where entry_timedate between '"+start_date+"' and '"+end_date+"';")
        row = cursor.fetchall()


        final_row= [list(x) for x in row]
        list3=[]
        for i in row:
            list3.append(list(i))


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
            amc_list = Amc_After_Sales.objects.filter(entry_timedate__range=[start_date, end_date])
            context = {
                'amc_list': amc_list,
            }
            return render(request, "manager/amc_view.html", context)
        elif 'submit2' in request.POST:
            contact = request.POST.get('contact')
            amc_list = Amc_After_Sales.objects.filter(customer_no=contact)
            context = {
                'amc_list': amc_list,
            }
            return render(request, "manager/amc_view.html",context )

        elif 'submit3' in request.POST:
            email = request.POST.get('email')
            dispatch_list = Amc_After_Sales.objects.filter(customer_email_id=email)
            context = {
                'dispatch_list': dispatch_list,
            }
            return render(request, "manager/amc_view.html",context )
        elif 'submit4' in request.POST:
            customer = request.POST.get('customer')
            dispatch_list = Amc_After_Sales.objects.filter(customer_name=customer)
            context = {
                'dispatch_list': dispatch_list,
            }
            return render(request, "manager/amc_view.html",context )

        elif  'submit5' in request.POST:
            company = request.POST.get('company')
            dispatch_list = Amc_After_Sales.objects.filter(company_name=company)
            context = {
                'dispatch_list': dispatch_list,
            }
            return render(request, "manager/amc_view.html",context )
        elif request.method=='POST' and 'submit6' in request.POST:
            crm = request.POST.get('crm')
            dispatch_list = Amc_After_Sales.objects.filter(crn_number=crm)
            context = {
                'dispatch_list': dispatch_list,
            }
            return render(request, "manager/amc_view.html",context )
    else:
        if check_admin_roles(request):     #For ADMIN
            amc_list = Amc_After_Sales.objects.filter(user_id__group__icontains=request.user.group,user_id__is_deleted=False).order_by('-id')
        else:  #For EMPLOYEE
            amc_list = Amc_After_Sales.objects.filter(user_id=request.user.pk).order_by('-id')
        # amc_list = Amc_After_Sales.objects.all()

        context = {
            'amc_list': amc_list,
        }
        return render(request, "manager/amc_view.html",context )


def amc_logs(request):
    return render(request,"logs/amc_logs.html")

    

def update_amc_form(request,update_id):
    amc_list=Amc_After_Sales.objects.get(id=update_id)
    if request.method == 'POST':
        amcno = request.POST.get('amcno')
        customer_name = request.POST.get('customer_name')
        company_name = request.POST.get('company_name')
        customer_no = request.POST.get('customer_no')
        customer_email_id = request.POST.get('customer_email_id')
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


        item = Amc_After_Sales.objects.get(id=update_id)

        item.amcno = amcno
        item.customer_name = customer_name
        item.company_name = company_name
        item.customer_no = customer_no
        item.customer_email_id = customer_email_id
        item.type_of_scale = type_of_scale
        item.serial_no_scale = serial_no_scale
        item.contract_valid_in_years = contract_valid_in_years
        item.contract_amount = contract_amount
        item.contract_no_reporting_breakdown = contract_no_reporting_breakdown
        item.contract_start_date = contract_start_date
        item.contract_end_date = contract_end_date
        item.visit_1 = visit_1
        item.repot_1 = repot_1
        item.visit_2 = visit_2
        item.repot_2 = repot_2
        item.visit_3 = visit_3
        item.repot_3 = repot_3
        item.visit_4 = visit_4
        item.repot_4 = repot_4
        item.save(update_fields=['contract_amount','visit_1','repot_1','visit_2','repot_2','visit_3','repot_3','visit_4','repot_4',])

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
        item.save()

        amc = Amc_After_Sales.objects.get(id=amc_id)
        amc.avg_feedback = ( satisfied_with_work + speed_of_performance + price_of_amc + overall_interaction) / 4.0
        amc.feedback_given = 'YES'
        amc.save(update_fields=['avg_feedback', 'feedback_given'])
        return HttpResponse('Feedback Submitted!!!')
    context = {
        'feedback_form': feedback_form,
    }
    return render(request,'feedback/feedback_amc.html',context)


