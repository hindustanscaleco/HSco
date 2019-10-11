from django.shortcuts import render, redirect

from onsitevisit_app.forms import add_Onsite_aftersales_service_form
from .models import Onsite_aftersales_service


def add_Onsite_aftersales_service(request):
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
        type_of_machine = request.POST.get('type_of_machine')
        model = request.POST.get('model')
        sub_model = request.POST.get('sub_model')
        capacity = request.POST.get('capacity')
        problem_in_scale = request.POST.get('problem_in_scale')
        components_replaced_in_warranty = request.POST.get('components_replaced_in_warranty')
        components_replaced = request.POST.get('components_replaced')
        cost = request.POST.get('cost')
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
        item.type_of_machine = type_of_machine
        item.model = model
        item.sub_model = sub_model
        item.capacity = capacity
        item.problem_in_scale = problem_in_scale
        item.components_replaced_in_warranty = components_replaced_in_warranty
        item.components_replaced = components_replaced
        item.cost = cost
        item.visiting_charges_told_customer = visiting_charges_told_customer
        item.total_cost = total_cost
        item.complaint_assigned_to = complaint_assigned_to
        item.complaint_assigned_on = complaint_assigned_on
        item.time_taken_destination_return_office_min = time_taken_destination_return_office_min
        item.notes = notes
        item.feedback_given = feedback_given

        item.save()
        return redirect('/')
    context={
        'form':form,
    }

    return render(request, 'forms/onsite_rep_form.html',context )