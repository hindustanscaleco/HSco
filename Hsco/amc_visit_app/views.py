from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import AMC_Feedback_Form
from .models import Amc_After_Sales, AMC_Feedback
from django.db import connection
from django.core.mail import send_mail
from Hsco import settings


def add_amc_after_sales(request):
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


        item = Amc_After_Sales()

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



        item.save()
        send_mail('Feedback Form','Click on the link to give feedback' , settings.EMAIL_HOST_USER, [customer_email_id])

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
        amc_list = Amc_After_Sales.objects.all()

        context = {
            'amc_list': amc_list,
        }
        return render(request, "manager/amc_view.html", )


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


def feedback_amc(request):
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
        item.save()

        return HttpResponse('Feedback Submitted!!!')
    context = {
        'feedback_form': feedback_form,
    }
    return render(request,'feedback/feedback_amc.html',context)


