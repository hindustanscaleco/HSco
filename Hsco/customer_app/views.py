from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, F
import re

from lead_management.models import Lead

from .models import Customer_Details
from .models import type_purchase, main_model, sub_model, sub_sub_model
from .models import DynamicDropdown
from purchase_app.models import Purchase_Details, Product_Details
from utils.common import paginate_data

DEFAULT_PAGE_NUMBER = 1
DEFAULT_PAGE_SIZE = 10
# gst_pattern = r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[0-9A-Z]{1}[0-9]{1}$'
# gst_pattern = r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][0-9A-Z][0-9]$'
gst_pattern = r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$'
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
    customer = Customer_Details.objects.get(id=id)
    if request.method == 'POST':
        customer.customer_name = request.POST.get('customer_name')
        customer.company_name = request.POST.get('company_name')
        customer.address = request.POST.get('customer_address')
        customer.city = request.POST.get('city')
        customer.state = request.POST.get('state')
        customer.pincode = request.POST.get('pincode')
        customer.contact_no = request.POST.get('contact_no')
        customer.customer_email_id = request.POST.get('customer_email_id')
        customer.customer_gst_no = request.POST.get('customer_gst_no')
        # Validate GST number format using regular expression
        if not re.match(gst_pattern, customer.customer_gst_no):
            messages.error(request, "Invalid GST number format!")
            return redirect('/update_customer_information/{0}'.format(id))
        customer.new_repeat_purchase = request.POST.get('new_repeat_purchase')
        customer.channel_of_marketing = request.POST.get(
            'channel_of_marketing')
        customer.industry = request.POST.get('industry')
        customer.channel_of_sales = request.POST.get('channel_of_sales')
        customer.channel_of_dispatch = request.POST.get('channel_of_dispatch')
        customer.notes = request.POST.get('notes')
        customer.bill_address = request.POST.get('bill_address')
        customer.shipping_address = request.POST.get('shipping_address')
        customer.bill_notes = request.POST.get('bill_notes')
        customer.marketing_whatsapp = request.POST.get(
            'marketing_whatsapp', False) == 'on'
        customer.lead_whatsapp = request.POST.get(
            'lead_whatsapp', False) == 'on'
        customer.sales_whatsapp = request.POST.get(
            'sales_whatsapp', False) == 'on'
        customer.repairing_whatsapp = request.POST.get(
            'repairing_whatsapp', False) == 'on'
        customer.save()
        messages.success(request, "Customer details updated successfully!")
        return redirect('/view_customer_information/')
    sales_list = Purchase_Details.objects.filter(crm_no_id=customer)
    # sales_list = Lead.objects.filter(customer_id=customer_id)
    product_details_customer = Product_Details.objects.select_related('purchase_id', 'product_dispatch_id') \
        .filter(purchase_id__crm_no__id=customer)
    # customer_ids = Lead.objects.values_list(
    #     'customer_id', flat=True).distinct()

    # # Filter Product_Details based on customer IDs where count is greater than 0
    # product_details = Product_Details.objects.filter(
    #     purchase_id__lead__customer_id__in=customer_ids
    # ).annotate(
    #     customer_count=Count('purchase_id__lead__customer_id')
    # ).filter(
    #     customer_count__gt=0
    # ).values_list('purchase_id__lead__customer_id', flat=True)
    # print('product counts leads', product_details)
    product_details_lead = Product_Details.objects.filter(
        purchase_id__lead__customer_id=customer.id).annotate(
        lead_id=F('purchase_id__lead__id'),
        sales_person=F('purchase_id__sales_person'),
        date_of_purchase=F('purchase_id__date_of_purchase'),
        feedback_stars=F('purchase_id__feedback_stars')
    ).values()
    print('lead_count', product_details_lead.count())
    print(product_details_lead)
    # leads_purchase_ids = Lead.objects.filter(
    #     customer_id=customer_id).values_list('purchase_id__id', flat=True)
    # print(leads_purchase_ids)
    # product_details_lead_customer = Product_Details.objects.select_related('purchase_id', 'product_dispatch_id') \
    #     .filter(purchase_id__crm_no__id=customer_id)
    # print(product_details_customer.count())
    # print(product_details_customer.values())
    channel_sales = DynamicDropdown.objects.filter(
        type="CHANNEL OF SALES", is_enabled=True)
    channel_marketing = DynamicDropdown.objects.filter(
        type="CHANNEL OF MARKETING", is_enabled=True)
    channel_dispatch = DynamicDropdown.objects.filter(
        type="CHANNEL OF DISPATCH", is_enabled=True)
    industry_list = DynamicDropdown.objects.filter(
        type="INDUSTRY", is_enabled=True)
    context = {
        'customer_id': customer,
        'channel_sales': channel_sales,
        'channel_marketing': channel_marketing,
        'channel_dispatch': channel_dispatch,
        'industry_list': industry_list,
        'sales_list': sales_list,
        'product_details_customer': product_details_customer,
        'product_details_lead': product_details_lead,
    }
    return render(request, 'informational_master/update_customer_information.html', context=context)


@login_required(login_url='/')
def view_customer_information(request):
    # search_type = request.GET.get('search_type', None)
    # search_query = request.GET.get('search_query', None)
    # print('search -->', search_type, search_query)
    # Initialize the customer queryset with all customers
    # customer_queryset = Customer_Details.objects.all().order_by('-id')
    customers = Customer_Details.objects.all().order_by('-id')[:100]
    # Apply filters based on the search type and query
    if request.method == 'POST':
        if 'submit1' in request.POST:
            # Search by Customer Number (d1)
            customer_number = request.POST.get('customer_number')
            customers = Customer_Details.objects.filter(
                id__icontains=customer_number)
        elif 'submit2' in request.POST:
            # Search by Customer Name (d2)
            customer_name = request.POST.get('customer_name')
            customers = Customer_Details.objects.filter(
                customer_name__icontains=customer_name)
        elif 'submit3' in request.POST:
            # Search by Company Address (d3)
            company_address = request.POST.get('company_address')
            customers = Customer_Details.objects.filter(
                address__icontains=company_address)
        elif 'submit4' in request.POST:
            # Search by Mobile Number (d4)
            mobile_number = request.POST.get('mobile_number')
            customers = Customer_Details.objects.filter(
                contact_no__icontains=mobile_number)
        elif 'submit5' in request.POST:
            # Search by GST Number (d5)
            gst_number = request.POST.get('gst_number')
            customers = Customer_Details.objects.filter(
                customer_gst_no__icontains=gst_number)
        elif 'submit6' in request.POST:
            # Search by Industry (d6)
            industry = request.POST.get('industry')
            customers = Customer_Details.objects.filter(
                customer_industry__icontains=industry)
        elif 'submit7' in request.POST:
            # Search by City (d7)
            city = request.POST.get('city')
            customers = Customer_Details.objects.filter(city__icontains=city)
        elif 'submit8' in request.POST:
            # Search by State (d8)
            state = request.POST.get('state')
            customers = Customer_Details.objects.filter(state__icontains=state)
        elif 'submit9' in request.POST:
            # Search by Pincode (d9)
            pincode = request.POST.get('pincode')
            customers = Customer_Details.objects.filter(
                pincode__icontains=pincode)

    print(len(customers))
    page_number = request.GET.get('page', 1)
    paginated_data = paginate_data(customers, page_number)

    context = {
        'customer_list': customers,
    }
    return render(request, 'informational_master/view_customer_information.html', context=context)


@login_required(login_url='/')
def customer_reports(request):
    # search_type = request.GET.get('search_type', None)
    # search_query = request.GET.get('search_query', None)
    # print('search -->', search_type, search_query)
    # Initialize the customer queryset with all customers
    # customer_queryset = Customer_Details.objects.all().order_by('-id')
    customers = Customer_Details.objects.all().order_by('-id')[:100]
    # Apply filters based on the search type and query
    page_number = request.GET.get('page', 1)
    paginated_data = paginate_data(customers, page_number)

    context = {
        'customer_list': customers,
    }
    return render(request, 'informational_master/customer_reports.html', context=context)


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
        # gst validation
        if not re.match(gst_pattern, customer_gst_no):
            messages.error(request, "Invalid GST number format!")
            return redirect('/add_customer_details')
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
