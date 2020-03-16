from django.shortcuts import render, redirect

from customer_app.models import type_purchase

from customer_app.models import sub_model, main_model, sub_sub_model
from .forms import Deal_detailForm, Customer_detailForm, Pi_sectionForm
from .form2 import Customer_detail_disabledForm
from customer_app.models import Customer_Details
from .models import Lead, Lead_Product, Pi_section


# Create your views here.

def lead_home(request):
    lead_list = Lead.objects.all()
    if Lead.objects.all().count() == 0:
        latest_lead_id = 1
    else:
        latest_lead_id = Lead.objects.latest('id').id + 1
    context={
        'lead_list':lead_list,
        'latest_lead_id':latest_lead_id,
    }
    return render(request,'lead_management/lead_home.html',context)


def add_lead_product(request,id):
    type_of_purchase_list =type_purchase.objects.all() #1

    if request.method == 'POST' or request.method=='FILES':
        scale_type = request.POST.get('scale_type')
        main_category = request.POST.get('main_category')
        sub_category = request.POST.get('sub_category')
        sub_sub_category = request.POST.get('sub_sub_category')
        hsn_code = request.POST.get('hsn_code')
        product_image = request.POST.get('product_image')
        max_capacity = request.POST.get('max_capacity')
        accuracy = request.POST.get('accuracy')
        platform_size = request.POST.get('platform_size')
        product_desc = request.POST.get('product_desc')
        product_brochure = request.POST.get('product_brochure')
        product_document = request.POST.get('product_document')
        cost_price = request.POST.get('cost_price')
        selling_price = request.POST.get('selling_price')
        carton_size = request.POST.get('carton_size')
        is_last_product_yes = request.POST.get('is_last_product_yes')

        item = Lead_Product()

        item.lead_id = Lead.objects.get(id=id)
        item.scale_type = type_purchase.objects.get(id=scale_type).name
        item.main_category = main_model.objects.get(id=main_category).name
        item.sub_category = sub_model.objects.get(id=sub_category).name
        item.sub_sub_category = sub_sub_model.objects.get(id=sub_sub_category).name
        item.hsn_code = hsn_code
        item.product_image = product_image
        item.max_capacity = max_capacity
        item.accuracy = accuracy
        item.platform_size = platform_size
        item.product_desc = product_desc
        item.product_brochure = product_brochure
        item.product_document = product_document
        item.cost_price = cost_price
        item.selling_price = selling_price
        item.carton_size = carton_size

        item.save()
        if is_last_product_yes == 'yes':
            return redirect('/update_view_lead/'+str(id))
        elif is_last_product_yes == 'no':
            return redirect('/add_lead_product/'+str(id))
    context={
        'type_purchase': type_of_purchase_list,  # 2

    }
    return render(request,'lead_management/add_lead_product.html',context)

def add_lead(request):
    if Lead.objects.all().count() == 0:
        latest_lead_id = 1
    else:
        latest_lead_id = Lead.objects.latest('id').id
    form = Customer_detailForm()
    form2 = Deal_detailForm()
    if request.method == 'POST' or request.method=='FILES':
        customer_name = request.POST.get('customer_name')
        company_name = request.POST.get('company_name')
        address = request.POST.get('address')
        contact_no = request.POST.get('contact_no')
        customer_industry = request.POST.get('customer_email_id')
        customer_email_id = request.POST.get('customer_email_id')
        customer_gst_no = request.POST.get('customer_gst_no')

        current_stage = request.POST.get('current_stage')
        new_existing_customer = request.POST.get('new_existing_customer')
        date_of_initiation = request.POST.get('date_of_initiation')
        channel = request.POST.get('channel')
        requirement = request.POST.get('requirement')
        upload_requirement_file = request.FILES.get('upload_requirement_file')
        owner_of_opportunity = request.POST.get('owner_of_opportunity')



        item2 = Lead()
        if Customer_Details.objects.filter(customer_name=customer_name,
                                           contact_no=contact_no).count() > 0:

            item2.customer_id = Customer_Details.objects.filter(contact_no=contact_no).first()

            item3 = Customer_Details.objects.filter(customer_name=customer_name,
                                                    contact_no=contact_no).first()
            if company_name != '' and company_name != None:
                item3.company_name = company_name
                item3.save(update_fields=['company_name'])
            if address != '' and address != None:
                item3.address = address
                item3.save(update_fields=['address'])
            if customer_email_id != '' and customer_email_id != None:
                item3.customer_email_id = customer_email_id
                item3.save(update_fields=['customer_email_id'])
            if customer_gst_no != '' and customer_gst_no != None:
                item3.customer_gst_no = customer_gst_no
                item3.save(update_fields=['customer_gst_no'])
            if customer_industry != '' and customer_industry != None:
                item3.customer_industry = customer_industry
                item3.save(update_fields=['customer_industry'])
        else:
            new_cust = Customer_Details()

            new_cust.customer_name = customer_name
            if company_name != '':
                new_cust.company_name = company_name
            if address != '':
                new_cust.address = address
            new_cust.contact_no = contact_no
            if customer_email_id != '':
                new_cust.customer_email_id = customer_email_id
            if customer_gst_no != '':
                new_cust.customer_gst_no = customer_gst_no
            if customer_industry != '':
                new_cust.customer_industry = customer_industry
            try:
                new_cust.save()
                item2.customer_id = Customer_Details.objects.get(id=new_cust.pk)
            except:
                pass


        item2.current_stage = current_stage
        item2.new_existing_customer = new_existing_customer
        item2.date_of_initiation = date_of_initiation
        item2.channel = channel
        item2.requirement = requirement
        item2.upload_requirement_file = upload_requirement_file
        item2.owner_of_opportunity = owner_of_opportunity
        item2.save()
        return redirect('/update_view_lead/'+str(item2.id))
        # item.save()
    context={
        'form':form,
        'form2':form2,
        'latest_lead_id':latest_lead_id,
    }
    return render(request, 'lead_management/add_lead.html',context)

def update_view_lead(request,id):
    lead_id = Lead.objects.get(id=id)

    lead_pi_products = Lead_Product.objects.filter(lead_id=id)
    customer_id = Customer_Details.objects.get(id=lead_id.customer_id)
    customer_initial_data = {
        'customer_name': customer_id.customer_name,
        'company_name': customer_id.company_name,
        'contact_no': customer_id.contact_no,
        'customer_email_id': customer_id.customer_email_id,
        'address': customer_id.address,
        'customer_industry': customer_id.customer_industry,
        'customer_gst_no': customer_id.customer_gst_no,
    }
    deal_details_initial_data = {
        'current_stage': lead_id.current_stage,
        'new_existing_customer': lead_id.new_existing_customer,
        'date_of_initiation': lead_id.date_of_initiation,
        'channel': lead_id.channel,
        'requirement': lead_id.requirement,
        'upload_requirement_file': lead_id.upload_requirement_file,
        'owner_of_opportunity': lead_id.owner_of_opportunity,
    }
    form = Customer_detailForm(initial=customer_initial_data)
    form2 = Deal_detailForm(initial=deal_details_initial_data)
    form3 = Pi_sectionForm()

    context = {
        'form': form,
        'form2': form2,
        'form3': form3,
        'lead_id': lead_id,
        'lead_pi_products': lead_pi_products,
    }
    if Pi_section.objects.filter(lead_id=id).count() > 0:
        pi_id = Pi_section.objects.get(lead_id=id)
        print(pi_id.call2)
        print(pi_id.call2)
        print(pi_id.call2)
        pi_initial_data = {
            'discount': pi_id.discount,
            'upload_pi_file': pi_id.upload_pi_file,
            'select_pi_template': pi_id.select_pi_template,
            'call': pi_id.call,
            'email': pi_id.email,
            'whatsapp': pi_id.whatsapp,
            'call2': pi_id.call2,
            'payment_channel': pi_id.payment_channel,
            'payment_receipt': pi_id.payment_receipt,
            'upload_po_file': pi_id.upload_po_file,
            'payment_received_date': pi_id.payment_received_date,
            'notes': pi_id.notes,
        }
        form3 = Pi_sectionForm(initial=pi_initial_data)
        context = {
            'form': form,
            'form2': form2,
            'form3': form3,
            'lead_id': lead_id,
            'lead_pi_products': lead_pi_products,
        }
        context.update(context)
    else:
        pass

    if request.method == 'POST' or request.method == 'FILES':
        if  'submit1' in request.POST:
            customer_name = request.POST.get('customer_name')
            company_name = request.POST.get('company_name')
            address = request.POST.get('address')
            contact_no = request.POST.get('contact_no')
            customer_industry = request.POST.get('customer_email_id')
            customer_email_id = request.POST.get('customer_email_id')
            customer_gst_no = request.POST.get('customer_gst_no')

            current_stage = request.POST.get('current_stage')
            new_existing_customer = request.POST.get('new_existing_customer')
            date_of_initiation = request.POST.get('date_of_initiation')
            channel = request.POST.get('channel')
            requirement = request.POST.get('requirement')
            upload_requirement_file = request.FILES.get('upload_requirement_file')
            owner_of_opportunity = request.POST.get('owner_of_opportunity')

            item2 = Lead.objects.get(id=id)



            item3 = Customer_Details.objects.get(id=lead_id.customer_id)

            if customer_name != '' and customer_name != None:
                item3.customer_name = customer_name
                item3.save(update_fields=['customer_name'])
            if contact_no != '' and contact_no != None:
                item3.contact_no = contact_no
                item3.save(update_fields=['contact_no'])
            if company_name != '' and company_name != None:
                item3.company_name = company_name
                item3.save(update_fields=['company_name'])
            if address != '' and address != None:
                item3.address = address
                item3.save(update_fields=['address'])
            if customer_email_id != '' and customer_email_id != None:
                item3.customer_email_id = customer_email_id
                item3.save(update_fields=['customer_email_id'])
            if customer_gst_no != '' and customer_gst_no != None:
                item3.customer_gst_no = customer_gst_no
                item3.save(update_fields=['customer_gst_no'])
            if customer_industry != '' and customer_industry != None:
                item3.customer_industry = customer_industry
                item3.save(update_fields=['customer_industry'])

            item2.current_stage = current_stage
            item2.new_existing_customer = new_existing_customer
            item2.date_of_initiation = date_of_initiation
            item2.channel = channel
            item2.requirement = requirement
            item2.upload_requirement_file = upload_requirement_file
            item2.owner_of_opportunity = owner_of_opportunity
            item2.save(update_fields=['current_stage','new_existing_customer','date_of_initiation','channel',
                                      'requirement','upload_requirement_file','owner_of_opportunity',])
            return redirect('/update_view_lead/'+str(id))

        elif 'submit2' in request.POST:
            discount = request.POST.get('discount')
            upload_pi_file = request.FILES.get('upload_pi_file')
            select_pi_template = request.FILES.get('select_pi_template')
            call = request.POST.get('call')
            email = request.POST.get('email')
            whatsapp = request.POST.get('whatsapp')
            call2 = request.POST.get('call2')
            if call2 == 'on':
                call2 = 'True'
            else:
                call2 = 'False'
            if email == 'on':
                email = 'True'
            else:
                email = 'False'
            if whatsapp == 'on':
                whatsapp = 'True'
            else:
                whatsapp = 'False'
            if Pi_section.objects.filter(lead_id=id).count() > 0:

                item2 = Pi_section.objects.filter(lead_id=id).first()

                item2.discount = discount
                item2.upload_pi_file = upload_pi_file
                item2.select_pi_template = select_pi_template
                item2.call = call
                item2.email = email
                item2.whatsapp = whatsapp
                item2.call2 = call2

                item2.save(update_fields=['discount', 'upload_pi_file', 'select_pi_template', 'call',
                                        'email', 'whatsapp','call2'  ])
            else :
                item2 = Pi_section()
                item2.discount = discount
                item2.upload_pi_file = upload_pi_file
                item2.select_pi_template = select_pi_template
                item2.call = call
                item2.email = email
                item2.whatsapp = whatsapp
                item2.call2 = call2
                item2.lead_id = Lead.objects.get(id=id)
                item2.save()
    return render(request, 'lead_management/update_view_lead.html',context)




def lead_report(request):
    return render(request,'lead_management/report_lead.html')

def lead_manager_view(request):
    return render(request,'lead_management/lead_manager.html')

def lead_follow_up_histroy(request):
    return render(request,'lead_management/lead_history.html')

def lead_delete_product(request,id):
    leads = Lead_Product.objects.filter(lead_id=id).order_by('-id')
    if request.method == 'POST' or request.method=='FILES':
        delete_id = request.POST.getlist('check[]')
        for i in delete_id:
            Lead_Product.objects.filter(id=i).delete()
    context={
        'leads':leads,
    }
    return render(request,'lead_management/lead_delete_product.html',context)

def lead_analytics(request):
    return render(request,'lead_management/analytics.html')

def lead_employee_graph(request):
    return render(request,'lead_management/lead_employee_graph.html')

def lead_pi_form(request):
    return render(request,'lead_management/lead_pi_form.html')