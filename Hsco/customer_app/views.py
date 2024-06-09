from django.db.models import CharField, Value, F, Exists, OuterRef
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, F
import re

from lead_management.models import Lead
from django.db.models import OuterRef, Subquery, Exists

from .models import Customer_Details
from .models import type_purchase, main_model, sub_model, sub_sub_model
from .models import DynamicDropdown
from purchase_app.models import Purchase_Details, Product_Details
from lead_management.models import Pi_product, Lead_Customer_Details
from utils.common import paginate_data

DEFAULT_PAGE_NUMBER = 1
DEFAULT_PAGE_SIZE = 10
gst_pattern = r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$'


@login_required(login_url='/')
def update_customer_information(request, id, customer_type):
    if customer_type == "lead_customer":
        customer_qs = Lead_Customer_Details.objects.filter(id=id)
    else:
        customer_qs = Customer_Details.objects.annotate(
            purchase_exists=Exists(
                Purchase_Details.objects.filter(crm_no=OuterRef('pk'))
            )
        ).filter(id=id)
        print('customer qa', customer_qs, Customer_Details.objects.filter(id=id))

    try:
        customer = customer_qs.get()
    except (Customer_Details.DoesNotExist, Lead_Customer_Details.DoesNotExist):
        return None

    customer_qs = Customer_Details.objects.annotate(
        purchase_exists=Exists(
            Purchase_Details.objects.filter(crm_no=OuterRef('pk'))
        )
    ).filter(id=id)

    if request.method == 'POST':
        customer.customer_name = request.POST.get('customer_name')
        customer.company_name = request.POST.get('company_name')
        customer.address = request.POST.get('customer_address')

        customer.contact_no = request.POST.get('contact_no')
        customer.customer_email_id = request.POST.get('customer_email_id')
        customer.customer_gst_no = request.POST.get('customer_gst_no')
        # Validate GST number format using regular expression
        if not re.match(gst_pattern, customer.customer_gst_no) and customer.customer_gst_no != "NA":
            messages.error(request, "Invalid GST number format!")
            return redirect('/update_customer_information/{0}/{1}'.format(id, customer_type))
        customer.customer_industry = request.POST.get('industry')

        if customer_type != "lead_customer":
            customer.channel_of_marketing = request.POST.get(
                'channel_of_marketing')
            customer.city = request.POST.get('city')
            customer.state = request.POST.get('state')
            customer.pincode = request.POST.get('pincode')
            customer.channel_of_sales = request.POST.get('channel_of_sales')
            customer.channel_of_dispatch = request.POST.get(
                'channel_of_dispatch')
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
        return redirect('/update_customer_information/{0}/{1}'.format(id, customer_type))

    # channel_sales = DynamicDropdown.objects.filter(
    #     type="CHANNEL OF SALES", is_enabled=True)
    # channel_marketing = DynamicDropdown.objects.filter(
    #     type="CHANNEL OF MARKETING", is_enabled=True)
    # channel_dispatch = DynamicDropdown.objects.filter(
    #     type="CHANNEL OF DISPATCH", is_enabled=True)
    # industry_list = DynamicDropdown.objects.filter(
    #     type="INDUSTRY", is_enabled=True)

    context = {
        'customer_id': customer,
        'customer_type': customer_type,
        'channel_sales': DynamicDropdown.objects.filter(type="CHANNEL OF SALES", is_enabled=True),
        'channel_marketing': DynamicDropdown.objects.filter(type="CHANNEL OF MARKETING", is_enabled=True),
        'channel_dispatch': DynamicDropdown.objects.filter(type="CHANNEL OF DISPATCH", is_enabled=True),
        'industry_list': DynamicDropdown.objects.filter(type="INDUSTRY", is_enabled=True),
        'sales_list': [],
        'product_details_customer': [],
        'product_details_lead': [],
        'leads': []
    }

    if customer_type == "lead_customer":
        # fetch leads sent to the customer
        context['leads'] = Lead.objects.filter(customer_id=id)
    else:
        # fetch products purchased by customer
        context['sales_list'] = Purchase_Details.objects.filter(
            crm_no_id=customer)
        context['product_details_customer'] = Product_Details.objects.select_related('purchase_id', 'product_dispatch_id') \
            .filter(purchase_id__crm_no__id=customer)

        # fetch leads sent to the customer
        lead_customer_id = Lead_Customer_Details.get_leads_customer_id(id)
        context['leads'] = Lead.objects.filter(customer_id=lead_customer_id)
        # pi_product_details_lead = []
        # if lead_customer_id:
        #     context['product_details_lead'] = Pi_product.objects.filter(
        #         lead_id__customer_id=lead_customer_id)
        #     print('pi product details ---->', pi_product_details_lead)

    return render(request, 'informational_master/update_customer_information.html', context=context)


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
        if not re.match(gst_pattern, customer_gst_no) and customer_gst_no != "NA":
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
                customer_industry=industry,
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


@login_required(login_url='/')
def view_customer_information(request):

    # Initial queries with necessary fields
    customers = Customer_Details.objects.values(
        'id', 'entry_timedate', 'customer_name', 'company_name', 'address',
        'contact_no', 'customer_gst_no', 'customer_industry', 'city', 'state', 'pincode',
        'channel_of_marketing', 'channel_of_dispatch', 'channel_of_sales'
    ).annotate(
        existing_customer=Value(True, output_field=CharField()),
        customer_type=Value('', output_field=CharField()),
        lead_id=Value('', output_field=CharField()),
        purchase_exists=Exists(
            Purchase_Details.objects.filter(crm_no=OuterRef('id'))
        )
    )

    lead_customers = Lead_Customer_Details.objects.values(
        'id', 'entry_timedate', 'customer_name', 'company_name', 'address',
        'contact_no', 'customer_gst_no', 'customer_industry'
    ).annotate(
        city=Value('', output_field=CharField()),
        state=Value('', output_field=CharField()),
        pincode=Value('', output_field=CharField()),
        channel_of_marketing=Value('', output_field=CharField()),
        channel_of_dispatch=Value('', output_field=CharField()),
        channel_of_sales=Value('', output_field=CharField()),
        existing_customer=Value(False, output_field=CharField()),
        customer_type=Value('lead_customer', output_field=CharField()),
        lead_id=Subquery(
            Lead.objects.filter(customer_id=OuterRef('pk')).values('id')[:1]
        ),
        purchase_exists=Exists(
            Lead.objects.filter(customer_id=OuterRef(
                'id'), current_stage="Dispatch Done - Closed")
        )

    )
    # customers = customers.union(lead_customers).order_by('-id')
    # Apply filters based on the search type and query
    if request.method == 'POST':
        if 'submit1' in request.POST:

            # Search by Customer Number (d1)
            customer_number = request.POST.get('customer_number')
            customers = customers.filter(id__icontains=customer_number)
            lead_customers = lead_customers.filter(
                id__icontains=customer_number)

            # customers = Customer_Details.objects.filter(
            #     id__icontains=customer_number)
        elif 'submit2' in request.POST:
            # Search by Customer Name (d2)
            customer_name = request.POST.get('customer_name')
            customers = customers.filter(
                customer_name__icontains=customer_name)
            lead_customers = lead_customers.filter(
                customer_name__icontains=customer_name)
            print('lead customers -->', lead_customers)
            # customers = Customer_Details.objects.filter(
            #     customer_name__icontains=customer_name)
        elif 'submit3' in request.POST:
            # Search by Company Address (d3)
            company_address = request.POST.get('company_address')
            customers = customers.filter(address__icontains=company_address)
            lead_customers = lead_customers.filter(
                address__icontains=company_address)
            # cstomers = Customer_Details.objects.filter(
            #     address__icontains=company_address)
        elif 'submit4' in request.POST:
            # Search by Mobile Number (d4)
            mobile_number = request.POST.get('mobile_number')
            customers = customers.filter(contact_no__icontains=mobile_number)
            lead_customers = lead_customers.filter(
                contact_no__icontains=mobile_number)
            # customers = Customer_Details.objects.filter(
            #     contact_no__icontains=mobile_number)
        elif 'submit5' in request.POST:
            # Search by GST Number (d5)
            gst_number = request.POST.get('gst_number')
            customers = customers.filter(customer_gst_no__icontains=gst_number)
            lead_customers = lead_customers.filter(
                customer_gst_no__icontains=gst_number)
            # customers = Customer_Details.objects.filter(
            #     customer_gst_no__icontains=gst_number)
        elif 'submit6' in request.POST:
            # Search by Industry (d6)
            industry = request.POST.get('industry')
            customers = customers.filter(customer_industry__icontains=industry)
            lead_customers = lead_customers.filter(
                customer_industry__icontains=industry)
            # customers = Customer_Details.objects.filter(
            #     customer_industry__icontains=industry)
        elif 'submit7' in request.POST:
            # Search by City (d7)
            city = request.POST.get('city')
            customers = customers.filter(city__icontains=city)
            lead_customers = lead_customers.filter(
                city__icontains=city)
            # customers = Customer_Details.objects.filter(city__icontains=city)
        elif 'submit8' in request.POST:
            # Search by State (d8)
            state = request.POST.get('state')
            customers = customers.filter(state__icontains=state)
            lead_customers = lead_customers.filter(
                state__icontains=state)
            # customers = Customer_Details.objects.filter(state__icontains=state)
        elif 'submit9' in request.POST:
            # Search by Pincode (d9)
            pincode = request.POST.get('pincode')
            customers = customers.filter(pincode__icontains=pincode)
            lead_customers = lead_customers.filter(
                pincode__icontains=pincode)
            # customers = Customer_Details.objects.filter(
            #     pincode__icontains=pincode)
        elif 'submit10' in request.POST:
            # Search by company name (d10)
            company_name = request.POST.get('company_name')
            customers = customers.filter(company_name__icontains=company_name)
            lead_customers = lead_customers.filter(
                company_name__icontains=company_name)
            # customers = Customer_Details.objects.filter(
            #     company_name__icontains=company_name)
        elif 'submit11' in request.POST:
            # Search by date range (d11)
            start_date = request.POST.get('start_date')
            end_date = request.POST.get('end_date')
            if start_date and end_date:
                customers = customers.filter(
                    entry_timedate__range=[start_date, end_date])
                lead_customers = lead_customers.filter(
                    entry_timedate__range=[start_date, end_date])
            # if start_date and end_date:
            #     customers = Customer_Details.objects.filter(
            #         entry_timedate__range=[start_date, end_date])
        customers = customers.union(lead_customers).order_by('-entry_timedate')
    print(len(customers))
    page_number = request.GET.get('page', 1)
    # paginated_data = paginate_data(customers, page_number)
    # customers = customers.annotate(purchase_exists=Exists(
    #     Purchase_Details.objects.filter(crm_no=OuterRef('pk'))))

    paginator = Paginator(customers, 100)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'customer_list': page_obj,
    }
    return render(request, 'informational_master/view_customer_information.html', context=context)


@login_required(login_url='/')
def customer_reports(request):
    # Initial queries with necessary fields
    customers = Customer_Details.objects.values(
        'id', 'entry_timedate', 'customer_name', 'company_name', 'address',
        'contact_no', 'customer_gst_no', 'customer_industry', 'city', 'state', 'pincode',
        'channel_of_marketing', 'channel_of_dispatch', 'channel_of_sales'
    ).annotate(
        existing_customer=Value(True, output_field=CharField()),
        customer_type=Value('', output_field=CharField()),
        lead_id=Value('', output_field=CharField()),
        purchase_exists=Exists(
            Purchase_Details.objects.filter(crm_no=OuterRef('id'))
        )
    )

    lead_customers = Lead_Customer_Details.objects.values(
        'id', 'entry_timedate', 'customer_name', 'company_name', 'address',
        'contact_no', 'customer_gst_no', 'customer_industry'
    ).annotate(
        city=Value('', output_field=CharField()),
        state=Value('', output_field=CharField()),
        pincode=Value('', output_field=CharField()),
        channel_of_marketing=Value('', output_field=CharField()),
        channel_of_dispatch=Value('', output_field=CharField()),
        channel_of_sales=Value('', output_field=CharField()),
        existing_customer=Value(False, output_field=CharField()),
        customer_type=Value('lead_customer', output_field=CharField()),
        lead_id=Subquery(
            Lead.objects.filter(customer_id=OuterRef('pk')).values('id')[:1]
        ),
        purchase_exists=Exists(
            Lead.objects.filter(customer_id=OuterRef(
                'id'), current_stage="Dispatch Done - Closed")
        )

    )

    # Combine both queries

    combined_customers = []
    # Pagination
    # Show 100 customers per page
    # paginator = Paginator(combined_customers, 100)
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)

    # Prepare context
    channel_sales = DynamicDropdown.objects.filter(
        type="CHANNEL OF SALES", is_enabled=True)
    channel_marketing = DynamicDropdown.objects.filter(
        type="CHANNEL OF MARKETING", is_enabled=True)
    channel_dispatch = DynamicDropdown.objects.filter(
        type="CHANNEL OF DISPATCH", is_enabled=True)
    industry_list = DynamicDropdown.objects.filter(
        type="INDUSTRY", is_enabled=True)

    print('industry-list', industry_list)

    # Apply filters
    if request.method == "GET":
        customer_industry = request.GET.get('industry')
        channel_of_marketing = request.GET.get('channel_of_marketing')
        channel_of_sales = request.GET.get('channel_of_sales')
        channel_of_dispatch = request.GET.get('channel_of_dispatch')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        purchase_query = request.GET.get('purchase_query')

        if customer_industry:
            customers = customers.filter(customer_industry=customer_industry)
            lead_customers = lead_customers.filter(
                customer_industry=customer_industry)
        if channel_of_marketing:
            customers = customers.filter(
                channel_of_marketing=channel_of_marketing)
            lead_customers = lead_customers.filter(
                channel_of_marketing=channel_of_marketing)
        if channel_of_sales:
            customers = customers.filter(
                channel_of_sales=channel_of_sales)
            lead_customers = lead_customers.filter(
                channel_of_sales=channel_of_sales)
        if channel_of_dispatch:
            customers = customers.filter(
                channel_of_dispatch=channel_of_dispatch)
            lead_customers = lead_customers.filter(
                channel_of_dispatch=channel_of_dispatch)
        if purchase_query:
            if purchase_query == 'purchased':
                customers = customers.filter(
                    purchase_exists=True)
                lead_customers = lead_customers.filter(
                    purchase_exists=True)

            elif purchase_query == 'not_purchased':
                customers = customers.filter(
                    purchase_exists=False)
                lead_customers = lead_customers.filter(
                    purchase_exists=False)

        if start_date and end_date:
            customers = customers.filter(
                entry_timedate__range=[start_date, end_date])
            lead_customers = lead_customers.filter(
                entry_timedate__range=[start_date, end_date])
            # combined_customers = combined_customers.filter(
            #     entry_timedate__range=[start_date, end_date])
        combined_customers = customers.union(
            lead_customers).order_by('-entry_timedate')
        print('count combined customers --->', combined_customers.count())

    # Pagination
    # paginator = Paginator(combined_customers, 100)
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)

    context = {
        'channel_sales': channel_sales,
        'channel_marketing': channel_marketing,
        'channel_dispatch': channel_dispatch,
        'industry_list': industry_list,
        'customer_list': combined_customers[:2000],
        'channel_of_marketing': channel_of_marketing,
        'channel_of_sales': channel_of_sales,
        'channel_of_dispatch': channel_of_dispatch,
        'industry': customer_industry,
        'start_date': start_date,
        'end_date': end_date,
        'purchase_query': purchase_query,
    }
    return render(request, 'informational_master/customer_reports.html', context=context)
# @login_required(login_url='/')
# def customer_reports(request):

#     customers = Customer_Details.objects.all().order_by('-id')
#     customers = Customer_Details.objects.all().order_by('-id').values(
#         'id', 'customer_name', 'contact_no', 'channel_of_marketing',
#         'channel_of_sales', 'channel_of_dispatch', 'industry', 'entry_timedate'
#     )
#     lead_customers = Lead_Customer_Details.objects.all().order_by('-id').values(
#         'id', 'customer_name', 'contact_no', 'channel_of_marketing',
#         'channel_of_sales', 'channel_of_dispatch', 'customer_industry', 'entry_timedate'
#     ).annotate(industry=F('customer_industry'))

#     combined_customers = customers.union(lead_customers)

#     # Apply filters based on the search type and query
#     channel_of_marketing = request.GET.get('channel_of_marketing')
#     channel_of_sales = request.GET.get('channel_of_sales')
#     channel_of_dispatch = request.GET.get('channel_of_dispatch')
#     industry = request.GET.get('industry')
#     start_date = request.GET.get('start_date')
#     end_date = request.GET.get('end_date')
#     purchase_query = request.GET.get('purchase_query')

#     # print('start_date->', start_date)
#     # print('purchase_query->', purchase_query)
#     if channel_of_marketing != '' and channel_of_marketing != None:
#         customers = Customer_Details.objects.filter(
#             channel_of_marketing=channel_of_marketing)
#         print('channel_of_marketing->', channel_of_marketing)
#     if channel_of_sales != '' and channel_of_sales != None:
#         customers = Customer_Details.objects.filter(
#             channel_of_sales=channel_of_sales)
#         print('channel_of_sales->', channel_of_sales)
#     if channel_of_dispatch != '' and channel_of_dispatch != None:
#         customers = Customer_Details.objects.filter(
#             channel_of_dispatch=channel_of_dispatch)
#         print('channel_of_dispatch->', channel_of_dispatch)
#     if industry != '' and industry != None:
#         customers = Customer_Details.objects.filter(industry=industry)
#         print('industry->', industry)
#     if start_date and end_date:
#         print('------> start end', start_date, end_date)
#         customers = Customer_Details.objects.filter(
#             entry_timedate__range=[start_date, end_date])
#     customers = customers.annotate(purchase_exists=Exists(
#         Purchase_Details.objects.filter(crm_no=OuterRef('pk'))))
#     # Filter by purchase status
#     if purchase_query != '':

#         if purchase_query == 'purchased':
#             customers = customers.filter(purchase_exists=True)
#         elif purchase_query == 'not_purchased':
#             customers = customers.filter(purchase_exists=False)

#     messages.success(request, f"Total customers found: {len(customers)}")
#     # page_number = request.GET.get('page', 1)
#     # paginated_data = paginate_data(customers, page_number)
#     channel_sales = DynamicDropdown.objects.filter(
#         type="CHANNEL OF SALES", is_enabled=True)
#     channel_marketing = DynamicDropdown.objects.filter(
#         type="CHANNEL OF MARKETING", is_enabled=True)
#     channel_dispatch = DynamicDropdown.objects.filter(
#         type="CHANNEL OF DISPATCH", is_enabled=True)
#     industry_list = DynamicDropdown.objects.filter(
#         type="INDUSTRY", is_enabled=True)
#     context = {
#         'channel_sales': channel_sales,
#         'channel_marketing': channel_marketing,
#         'channel_dispatch': channel_dispatch,
#         'industry_list': industry_list,
#         'customer_list': customers[:1000],
#         'channel_of_marketing': channel_of_marketing,
#         'channel_of_sales': channel_of_sales,
#         'channel_of_dispatch': channel_of_dispatch,
#         'industry': industry,
#         'start_date': start_date,
#         'end_date': end_date,
#         'purchase_query': purchase_query,
#     }
#     return render(request, 'informational_master/customer_reports.html', context=context)


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
