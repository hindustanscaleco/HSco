from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required

from .models import Customer_Details
from .models import type_purchase,main_model,sub_model,sub_sub_model


@login_required(login_url='/')
def add_customer_details(request):
    if request.method == 'POST' or request.method=='FILES':
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


    return render(request,'forms/cust_details_form.html',)



@login_required(login_url='/')
def load_models(request):
    category_id = request.GET.get('item_id')
    subcat = main_model.objects.filter(type_purchase=category_id)
    subcat_count = main_model.objects.filter(type_purchase=category_id).count()
    return render(request, 'AJAX_dropdowns/subcat-dropdown.html', {'subcat': subcat,'subcat_count':subcat_count})

@login_required(login_url='/')
def load_sub_models(request):
    category_id = request.GET.get('item_id')

    subcat = sub_model.objects.filter(main_model=category_id)

    return render(request, 'AJAX_dropdowns/subcat-dropdown.html', {'subcat': subcat,})


@login_required(login_url='/')
def load_sub_sub_models(request):
    category_id = request.GET.get('item_id')
    subcat = sub_sub_model.objects.filter(sub_model=category_id)
    return render(request, 'AJAX_dropdowns/subcat-dropdown.html', {'subcat': subcat})




