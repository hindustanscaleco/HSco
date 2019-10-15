from django.db import connection
from django.shortcuts import render, redirect

from user_app.models import SiteUser
from .models import Repairing_after_sales_service, Repairing_Product


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

        return redirect('/repair_product/'+str(item.id))



    return render(request,'forms/rep_mod_form.html',    )


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
    repair_list = Repairing_after_sales_service.objects.all()
    context = {
        'repair_list': repair_list,
    }
    return render(request,'dashboardnew/repairing_module_home.html',context)

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





