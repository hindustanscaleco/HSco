from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Customer_Details
from .models import type_purchase, main_model, sub_model, sub_sub_model
from .models import DynamicDropdown

from utils.common import paginate_data

DEFAULT_PAGE_NUMBER = 1
DEFAULT_PAGE_SIZE = 10
# @login_required(login_url='/')
# def add_customer_details(request):
#     if request.method == 'POST' or request.method == 'FILES':
#         customer_name = request.POST.get('customer_name')
#         company_name = request.POST.get('company_name')
#         address = request.POST.get('address')
#         contact_no = request.POST.get('contact_no')
#         customer_email_id = request.POST.get('customer_email_id')

#         item = Customer_Details()

#         item.customer_name = customer_name
#         item.company_name = company_name
#         item.address = address
#         item.contact_no = contact_no
#         item.customer_email_id = customer_email_id

#         item.save()

#     return render(request, 'informational_master/add_customer.html',)


@login_required(login_url='/')
def update_customer_information(request, id):
    customer_id = Customer_Details.objects.get(id=id)
    channel_sales = DynamicDropdown.objects.filter(
        type="CHANNEL OF SALES", is_enabled=True)
    channel_marketing = DynamicDropdown.objects.filter(
        type="CHANNEL OF MARKETING", is_enabled=True)
    channel_dispatch = DynamicDropdown.objects.filter(
        type="CHANNEL OF DISPATCH", is_enabled=True)
    industry_list = DynamicDropdown.objects.filter(
        type="INDUSTRY", is_enabled=True)
    context = {
        'customer_id': customer_id,
        'channel_sales': channel_sales,
        'channel_marketing': channel_marketing,
        'channel_dispatch': channel_dispatch,
        'industry_list': industry_list,
    }
    return render(request, 'informational_master/update_customer_information.html', context=context)


@login_required(login_url='/')
def view_customer_information(request):
    customer_list = Customer_Details.objects.all().order_by(
        '-id')[:100]
    print(len(customer_list))
    page_number = request.GET.get('page', 1)
    paginated_data = paginate_data(customer_list, page_number)
    print(paginated_data)
    print(len(paginated_data))
    context = {
        'customer_list': customer_list,
    }
    return render(request, 'informational_master/view_customer_information.html', context=context)


@login_required(login_url='/')
def add_customer_details(request):
    if request.method == 'POST':
        customer_name = request.POST.get('customer_name')
        company_name = request.POST.get('company_name')
        customer_address = request.POST.get('customer_address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        contact_no = request.POST.get('contact_no')
        customer_email_id = request.POST.get('customer_email_id')
        customer_gst_no = request.POST.get('customer_gst_no')
        new_repeat_purchase = request.POST.get('new_repeat_purchase')
        # bill_no = request.POST.get('bill_no')
        channel_of_marketing = request.POST.get('channel_of_marketing')
        industry = request.POST.get('industry')
        channel_of_sales = request.POST.get('channel_of_sales')
        channel_of_dispatch = request.POST.get('channel_of_dispatch')
        notes = request.POST.get('notes')
        bill_address = request.POST.get('bill_address')
        shipping_address = request.POST.get('shipping_address')
        bill_notes = request.POST.get('bill_notes')
        marketing_whatsapp = request.POST.get(
            'marketing_whatsapp', False) == 'on'
        lead_whatsapp = request.POST.get('lead_whatsapp', False) == 'on'
        sales_whatsapp = request.POST.get('sales_whatsapp', False) == 'on'
        repairing_whatsapp = request.POST.get(
            'repairing_whatsapp', False) == 'on'

        if Customer_Details.objects.filter(customer_name=customer_name, contact_no=contact_no, customer_gst_no=customer_gst_no).exists():
            messages.error(
                request, "This customer has already been added !!!")
            return redirect("/add_customer_details/")

        else:
            item = Customer_Details(
                customer_name=customer_name,
                company_name=company_name,
                address=customer_address,
                city=city,
                state=state,
                pincode=pincode,
                contact_no=contact_no,
                customer_email_id=customer_email_id,
                customer_gst_no=customer_gst_no,
                new_repeat_purchase=new_repeat_purchase,
                # bill_no=bill_no,
                channel_of_marketing=channel_of_marketing,
                industry=industry,
                channel_of_sales=channel_of_sales,
                channel_of_dispatch=channel_of_dispatch,
                notes=notes,
                bill_address=bill_address,
                shipping_address=shipping_address,
                bill_notes=bill_notes,
                marketing_whatsapp=marketing_whatsapp,
                lead_whatsapp=lead_whatsapp,
                sales_whatsapp=sales_whatsapp,
                repairing_whatsapp=repairing_whatsapp,
                # sales_channel_of_sales_id=DynamicDropdown.objects.get(
                #     id=channel_of_sales),
                # sales_industry_id=DynamicDropdown.objects.get(id=industry),
                # sales_channel_of_dispatch_id=DynamicDropdown.objects.get(
                #     id=channel_of_dispatch),
                # sales_channel_of_marketing_id=DynamicDropdown.objects.get(
                #     id=channel_of_marketing)
            )

            item.save()
            messages.success(request, "Customer Added Successfully!")

            return redirect('/view_customer_information/')

    channel_sales = DynamicDropdown.objects.filter(
        type="CHANNEL OF SALES", is_enabled=True)
    channel_marketing = DynamicDropdown.objects.filter(
        type="CHANNEL OF MARKETING", is_enabled=True)
    channel_dispatch = DynamicDropdown.objects.filter(
        type="CHANNEL OF DISPATCH", is_enabled=True)
    indutry = DynamicDropdown.objects.filter(type="INDUSTRY", is_enabled=True)

    context = {
        'channel_sales': channel_sales,
        'channel_marketing': channel_marketing,
        'channel_dispatch': channel_dispatch,
        'indutry': indutry,
    }
    return render(request, 'informational_master/add_customer.html', context)


@ login_required(login_url='/')
def load_models(request):
    category_id = request.GET.get('item_id')
    subcat = main_model.objects.filter(type_purchase=category_id)
    subcat_count = main_model.objects.filter(type_purchase=category_id).count()
    return render(request, 'AJAX_dropdowns/subcat-dropdown.html', {'subcat': subcat, 'subcat_count': subcat_count})


@ login_required(login_url='/')
def load_sub_models(request):
    category_id = request.GET.get('item_id')

    subcat = sub_model.objects.filter(main_model=category_id)

    return render(request, 'AJAX_dropdowns/subcat-dropdown.html', {'subcat': subcat, })


@ login_required(login_url='/')
def load_sub_sub_models(request):
    category_id = request.GET.get('item_id')
    subcat = sub_sub_model.objects.filter(sub_model=category_id)
    return render(request, 'AJAX_dropdowns/subcat-dropdown.html', {'subcat': subcat})
