from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render, redirect

from user_app.models import SiteUser

from .forms import Repairing_Feedback_Form
from .models import Repairing_after_sales_service, Repairing_Product, Repairing_Feedback
from django.core.mail import send_mail
from Hsco import settings
import datetime

def add_repairing_details(request):
    if request.method == 'POST' or request.method == 'FILES':
        repairingnumber = request.POST.get('repairingnumber')
        customer_no = request.POST.get('customer_no')
        previous_repairing_number = request.POST.get('previous_repairing_number')
        in_warranty = request.POST.get('in_warranty')
        date_of_purchase = request.POST.get('date_of_purchase')
        today_date = request.POST.get('today_date')
        name = request.POST.get('name')
        company_name = request.POST.get('company_name')
        phone_no = request.POST.get('phone_no')
        customer_email_id = request.POST.get('customer_email_id')
        location = request.POST.get('location')
        products_to_be_repaired = request.POST.get('products_to_be_repaired')

        total_cost = request.POST.get('total_cost')
        informed_on = request.POST.get('informed_on')
        informed_by = request.POST.get('informed_by')
        confirmed_estimate = request.POST.get('confirmed_estimate')
        repaired = request.POST.get('repaired')
        repaired_date = request.POST.get('repaired_date')
        delivery_date = request.POST.get('delivery_date')
        delivery_by = request.POST.get('delivery_by')
        feedback_given = request.POST.get('feedback_given')

        item = Repairing_after_sales_service()


        item.repairingnumber = repairingnumber
        item.customer_no = customer_no
        item.previous_repairing_number = previous_repairing_number
        item.in_warranty = in_warranty
        item.date_of_purchase = date_of_purchase
        item.today_date = today_date
        item.name = name
        item.company_name = company_name
        item.phone_no = phone_no
        item.customer_email_id = customer_email_id
        item.location = location
        item.products_to_be_repaired = products_to_be_repaired

        item.total_cost = total_cost
        item.informed_on = informed_on
        item.informed_by = informed_by
        item.confirmed_estimate = confirmed_estimate
        item.repaired = repaired
        item.repaired_date = repaired_date
        item.delivery_date = delivery_date
        item.delivery_by = delivery_by
        item.feedback_given = feedback_given

        item.save()
        send_mail('Feedback Form','Click on the link to give feedback' , settings.EMAIL_HOST_USER, [customer_email_id])

        return redirect('/repair_product/'+str(item.id))



    return render(request,'forms/rep_mod_form.html',)


def repair_product(request,id):
    repair_id = Repairing_after_sales_service.objects.get(id=id).id

    if request.method=='POST':
        type_of_machine = request.POST.get('type_of_machine')
        model = request.POST.get('model')
        sub_model = request.POST.get('sub_model')
        problem_in_scale = request.POST.get('problem_in_scale')
        components_replaced_in_warranty = request.POST.get('components_replaced_in_warranty')
        components_replaced = request.POST.get('components_replaced')
        replaced_scale_given = request.POST.get('replaced_scale_given')
        Replaced_scale_serial_no = request.POST.get('Replaced_scale_serial_no')
        deposite_taken_for_replaced_scale = request.POST.get('deposite_taken_for_replaced_scale')
        cost = request.POST.get('cost')

        item=Repairing_Product()

        item.type_of_machine = type_of_machine
        item.model = model
        item.sub_model = sub_model
        item.problem_in_scale = problem_in_scale
        item.components_replaced_in_warranty = components_replaced_in_warranty
        item.components_replaced = components_replaced
        item.replaced_scale_given = replaced_scale_given
        item.Replaced_scale_serial_no = Replaced_scale_serial_no
        item.deposite_taken_for_replaced_scale = deposite_taken_for_replaced_scale
        item.repairing_id_id = repair_id
        item.cost = cost

        item.save()

        return redirect('/update_repairing_details/'+str(id))
    context = {
        'repair_id': repair_id,
    }
    return render(request,'dashboardnew/repair_product.html',context)

def update_repairing_details(request,id):
    repair_id = Repairing_after_sales_service.objects.get(id=id)

    repair_list = Repairing_Product.objects.filter(repairing_id=id)
    print(repair_list)
    context={
        'repair_list': repair_list,
        'repair_id': repair_id,

    }
    return render(request,'update_forms/update_rep_mod_form.html',context)



def repairing_module_home(request):
    if request.method == 'POST':
        if'submit1' in request.POST:
            start_date = request.POST.get('date1')
            end_date = request.POST.get('date2')
            repair_list = Repairing_after_sales_service.objects.filter(entry_timedate__range=[start_date, end_date])
            context = {
                'repair_list': repair_list,
            }
            return render(request, 'dashboardnew/repairing_module_home.html', context)
        elif 'submit2' in request.POST:
            contact = request.POST.get('contact')
            repair_list = Repairing_after_sales_service.objects.filter(phone_no=contact)
            context = {
                'repair_list': repair_list,
            }
            return render(request, 'dashboardnew/repairing_module_home.html', context)

        elif 'submit3' in request.POST:
            email = request.POST.get('email')
            repair_list = Repairing_after_sales_service.objects.filter(customer_email_id=email)
            context = {
                'repair_list': repair_list,
            }
            return render(request, 'dashboardnew/repairing_module_home.html', context)
        elif 'submit4' in request.POST:
            customer = request.POST.get('customer')
            repair_list = Repairing_after_sales_service.objects.filter(name=customer)
            context = {
                'repair_list': repair_list,
            }
            return render(request, 'dashboardnew/repairing_module_home.html', context)

        elif  'submit5' in request.POST:
            company = request.POST.get('company')
            repair_list = Repairing_after_sales_service.objects.filter(company_name=company)
            context = {
                'repair_list': repair_list,
            }
            return render(request, 'dashboardnew/repairing_module_home.html', context)
        elif request.method=='POST' and 'submit6' in request.POST:
            crm = request.POST.get('crm')
            repair_list = Repairing_after_sales_service.objects.filter(crn_number=crm)
            context = {
                'repair_list': repair_list,
            }
            return render(request, 'dashboardnew/repairing_module_home.html', context)
    else:
        repair_list = Repairing_after_sales_service.objects.all()


        context = {
            'repair_list': repair_list,
        }
        return render(request, 'dashboardnew/repairing_module_home.html', context)

def manager_repairing_module_home(request):
    repair_employee_list = SiteUser.objects.all()
    context={
        'repair_employee_list':repair_employee_list,
    }
    return render(request,'dashboardnew/manager_repairing_module_home.html',context)

def repairing_report_module(request):
    if request.method == 'POST' or None:
        selected_list = request.POST.getlist('checks[]')
        repair_start_date = request.POST.get('date1')
        repair_end_date = request.POST.get('date2')
        repair_string = ','.join(selected_list)
        request.session['start_date'] = repair_start_date
        request.session['repair_end_date'] = repair_end_date
        request.session['repair_string'] = repair_string
        request.session['selected_list'] = selected_list
        return redirect('/final_repairing_report_module/')
    return render(request,'report/report_rep_mod_form.html',)

def final_repairing_report_module(request):
    repair_start_date = str(request.session.get('repair_start_date'))
    repair_end_date = str(request.session.get('repair_end_date'))
    repair_string = request.session.get('repair_string')
    selected_list = request.session.get('selected_list')
    print(repair_string)
    print(repair_start_date)
    print(repair_start_date)
    print(repair_start_date)
    print(repair_start_date)

    print(repair_start_date)
    print(repair_end_date)
    print(selected_list)
    with connection.cursor() as cursor:
        cursor.execute("SELECT "+repair_string+" from repairing_app_repairing_after_sales_service where today_date between '"+repair_start_date+"' and '"+repair_end_date+"';")
        row = cursor.fetchall()
        print(row)
        final_row = [list(x) for x in row]
        repairing_data = []
        for i in row:
            repairing_data.append(list(i))
    context = {
        'final_row': final_row,
        'selected_list': selected_list,
    }
    return render(request,'report/final_report_rep_mod_form.html',context)

def feedback_repairing(request):
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
        item.save()

        return HttpResponse('Feedback Submitted!!!')
    context = {
        'feedback_form': feedback_form,
    }
    return render(request,'feedback/feedback_repairing.html',context)

def edit_product(request,id):
    product_id = Repairing_Product.objects.get(id=id)
    print(product_id)
    context = {
            'product_id': product_id,
    }


    return render(request,'edit_product/edit_product_repair.html',context)


def load_reparing_stages_list(request,):

    selected = request.GET.get('loc_id')
    locc_id = request.GET.get('strUser')
    print(selected)
    print(locc_id)
    print(locc_id)
    if selected == 'All':
        repair_list = Repairing_after_sales_service.objects.filter(current_stage=locc_id)
        print("True")
        print(repair_list)
    else:
        date= datetime.date.today()-datetime.timedelta(int(selected))
        repair_list = Repairing_after_sales_service.objects.filter(entry_timedate__range=[date,datetime.date.today()],current_stage=locc_id)
        print("False")
        print(date)
        print(datetime.date.today())
        print(repair_list)

    context = {
        'repair_list': repair_list,
    }
    context.update(context)
    return render(request, 'AJAX/load_reparing_stage.html', context)





