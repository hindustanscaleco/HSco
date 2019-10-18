from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render, redirect


from .forms import Onsite_Repairing_Feedback_Form
from .models import Onsite_aftersales_service, Onsite_Products, Onsite_Feedback


def onsite_views(request):
    if request.method=='POST' :
        if'submit1' in request.POST:
            start_date = request.POST.get('date1')
            end_date = request.POST.get('date2')
            onsite_list = Onsite_aftersales_service.objects.filter(entry_timedate__range=[start_date, end_date])
            context = {
                'onsite_list': onsite_list,
            }
            return render(request, "manager/onsite_reparing.html", context)
        elif 'submit2' in request.POST:
            contact = request.POST.get('contact')
            onsite_list = Onsite_aftersales_service.objects.filter(phone_no=contact)
            context = {
                'onsite_list': onsite_list,
            }
            return render(request, "manager/onsite_reparing.html", context)

        elif 'submit3' in request.POST:
            email = request.POST.get('email')
            onsite_list = Onsite_aftersales_service.objects.filter(customer_email_id=email)
            context = {
                'onsite_list': onsite_list,
            }
            return render(request, "manager/onsite_reparing.html", context)
        elif 'submit4' in request.POST:
            customer = request.POST.get('customer')
            onsite_list = Onsite_aftersales_service.objects.filter(customer_name=customer)
            context = {
                'onsite_list': onsite_list,
            }
            return render(request, "manager/onsite_reparing.html", context)

        elif  'submit5' in request.POST:
            company = request.POST.get('company')
            onsite_list = Onsite_aftersales_service.objects.filter(company_name=company)
            context = {
                'onsite_list': onsite_list,
            }
            return render(request, "manager/onsite_reparing.html", context)
        elif request.method=='POST' and 'submit6' in request.POST:
            crm = request.POST.get('crm')
            onsite_list = Onsite_aftersales_service.objects.filter(crn_number=crm)
            context = {
                'onsite_list': onsite_list,
            }
            return render(request, "manager/onsite_reparing.html", context)
    else:
        onsite_list = Onsite_aftersales_service.objects.all()

        context = {
            'onsite_list': onsite_list,
        }
        return render(request, "manager/onsite_reparing.html", context)


def add_onsite_aftersales_service(request):
    form = add_Onsite_aftersales_service_form(request.POST or None, request.FILES or None)
    if request.method == 'POST' or request.method == 'FILES':
        repairingno = request.POST.get('repairingno')
        customer_name = request.POST.get('customer_name')
        company_name = request.POST.get('company_name')
        customer_no = request.POST.get('customer_no')
        previous_repairing_number = request.POST.get('previous_repairing_number')
        in_warranty = request.POST.get('in_warranty')
        phone_no = request.POST.get('phone_no')
        customer_email_id = request.POST.get('customer_email_id')
        date_of_complaint_received = request.POST.get('date_of_complaint_received')
        customer_address = request.POST.get('customer_address')
        complaint_received_by = request.POST.get('complaint_received_by')
        nearest_railwaystation = request.POST.get('nearest_railwaystation')
        train_line = request.POST.get('train_line')
        products_to_be_repaired = request.POST.get('products_to_be_repaired')

        visiting_charges_told_customer = request.POST.get('visiting_charges_told_customer')
        total_cost = request.POST.get('components_replaced_in_warranty')
        complaint_assigned_to = request.POST.get('complaint_assigned_to')
        complaint_assigned_on = request.POST.get('complaint_assigned_on')
        time_taken_destination_return_office_min = request.POST.get('time_taken_destination_return_office_min')
        notes = request.POST.get('notes')
        feedback_given = request.POST.get('feedback_given')


        item=Onsite_aftersales_service()


        item.repairingno = repairingno
        item.customer_name = customer_name
        item.company_name = company_name
        item.customer_name = customer_name
        item.company_name = company_name
        item.customer_no = customer_no
        item.previous_repairing_number = previous_repairing_number
        item.in_warranty = in_warranty
        item.phone_no = phone_no
        item.customer_email_id = customer_email_id
        item.date_of_complaint_received = date_of_complaint_received
        item.customer_address = customer_address
        item.complaint_received_by = complaint_received_by
        item.nearest_railwaystation = nearest_railwaystation
        item.train_line = train_line
        item.products_to_be_repaired = products_to_be_repaired

        item.visiting_charges_told_customer = visiting_charges_told_customer
        item.total_cost = total_cost
        item.complaint_assigned_to = complaint_assigned_to
        item.complaint_assigned_on = complaint_assigned_on
        item.time_taken_destination_return_office_min = time_taken_destination_return_office_min
        item.notes = notes
        item.feedback_given = feedback_given

        item.save()
        return redirect('/add_onsite_product/'+str(item.id))
    context={
        'form':form,
    }

    return render(request, 'forms/onsite_rep_form.html',context)

def add_onsite_product(request,id):
    onsite_id = Onsite_aftersales_service.objects.get(id=id).id
    print(onsite_id)
    if request.method == 'POST' or request.method == 'FILES':
        type_of_machine = request.POST.get('type_of_machine')
        model = request.POST.get('model')
        sub_model = request.POST.get('sub_model')
        capacity = request.POST.get('capacity')
        problem_in_scale = request.POST.get('problem_in_scale')
        components_replaced_in_warranty = request.POST.get('components_replaced_in_warranty')
        components_replaced = request.POST.get('components_replaced')
        cost = request.POST.get('cost')

        item = Onsite_Products()

        item.onsite_repairing_id_id = onsite_id
        item.type_of_machine = type_of_machine
        item.model = model
        item.sub_model = sub_model
        item.capacity = capacity
        item.problem_in_scale = problem_in_scale
        item.components_replaced_in_warranty = components_replaced_in_warranty
        item.components_replaced = components_replaced
        item.cost = cost

        item.save()
        return redirect('/update_onsite_details/'+str(id))
    context = {
        'onsite_id': onsite_id,
    }
    return render(request,"forms/onsite_product.html",context)

def update_onsite_details(request,id):
    onsite_product_list = Onsite_Products.objects.filter(onsite_repairing_id=id)
    print(onsite_product_list)
    onsite_id = Onsite_aftersales_service.objects.get(id=id)

    context={
        'onsite_product_list':onsite_product_list,
        'onsite_id':onsite_id,
    }

    return render(request,'update_forms/update_onsite_rep_form.html',context)

def report_onsite(request):
    if request.method == 'POST' or None:
        selected_list = request.POST.getlist('checks[]')
        onsite_start_date = request.POST.get('date1')
        onsite_end_date = request.POST.get('date2')
        onsite_string = ','.join(selected_list)

        request.session['start_date'] = onsite_start_date
        request.session['repair_end_date'] = onsite_end_date
        request.session['repair_string'] = onsite_string
        request.session['selected_list'] = selected_list
        return redirect('/final_report_onsite/')
    return render(request,"report/report_onsite_rep_form.html",)

def final_report_onsite(request):
    repair_start_date = str(request.session.get('repair_start_date'))
    repair_end_date = str(request.session.get('repair_end_date'))
    repair_string = request.session.get('repair_string')
    selected_list = request.session.get('selected_list')
    print(repair_string)
    print(repair_start_date)


    print(repair_start_date)
    print(repair_end_date)
    print(selected_list)
    with connection.cursor() as cursor:
        cursor.execute("SELECT "+repair_string+" from onsitevisit_app_onsite_aftersales_service where auto_timedate between '"+repair_start_date+"' and '"+repair_end_date+"';")
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
    return render(request,'report/final_onsite_report.html',context)

def feedback_onrepairing(request):
    feedback_form = Onsite_Repairing_Feedback_Form(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        backend_team = request.POST.get('backend_team')
        onsite_worker = request.POST.get('onsite_worker')
        speed_of_performance = request.POST.get('speed_of_performance')
        price_of_reparing = request.POST.get('price_of_reparing')
        overall_interaction = request.POST.get('overall_interaction')
        about_hsco = request.POST.get('about_hsco')
        any_suggestion = request.POST.get('any_suggestion')

        item = Onsite_Feedback()
        item.backend_team = backend_team
        item.onsite_worker = onsite_worker
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
    return render(request,"feedback/feedback_onrepairing.html",context)