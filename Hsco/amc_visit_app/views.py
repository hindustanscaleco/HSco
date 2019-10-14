from django.shortcuts import render, redirect
from .models import Amc_After_Sales



def add_amc_after_sales(request):
    form = (request.POST or None, request.FILES or None)
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

        return redirect('/')


    context = {
        'form': form,
    }
    return render(request,'forms/amc_form.html', context)

def report_amc(request):
    return render(request, "report/report_amc_form.html",)