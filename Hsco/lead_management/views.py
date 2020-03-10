from django.shortcuts import render
from .forms import Deal_detailForm,Customer_detailForm
from .form2 import Customer_detail_disabledForm
from customer_app.models import Customer_Details
from .models import Deal_details_section

# Create your views here.

def lead_home(request):
    lead_list = Customer_Details.objects.all()

    context={
        'lead_list':lead_list,
    }
    return render(request,'lead_management/lead_home.html',context)

def view_lead(request):
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
        upload_requirement_file = request.POST.get('upload_requirement_file')
        owner_of_opportunity = request.POST.get('owner_of_opportunity')



        item = Customer_Details()
        item2 = Deal_details_section()

        item.customer_name = customer_name
        item.company_name = company_name
        item.address = address
        item.contact_no = contact_no
        item.customer_industry = customer_industry
        item.customer_email_id = customer_email_id
        item.customer_gst_no = customer_gst_no

        item2.current_stage = current_stage
        item2.new_existing_customer = new_existing_customer
        item2.date_of_initiation = date_of_initiation
        item2.channel = channel
        item2.requirement = requirement
        item2.upload_requirement_file = upload_requirement_file
        item2.owner_of_opportunity = owner_of_opportunity

        item.save()
    context={
        'form':form,
        'form2':form2,
    }
    return render(request, 'lead_management/view_lead.html',context)

def update_view_lead(request,id):
    lead_id = Customer_Details.objects.get(id=id)
    initial_data = {
        'customer_name': lead_id.customer_name,
        'company_name': lead_id.company_name,
        'contact_no': lead_id.contact_no,
        'customer_email_id': lead_id.customer_email_id,
        'address': lead_id.address,
        'customer_industry': lead_id.customer_industry,
        'customer_gst_no': lead_id.customer_gst_no,
    }
    form = Customer_detail_disabledForm(initial=initial_data)
    context={
        'form':form
    }

    return render(request, 'lead_management/update_view_lead.html',context)




def lead_report(request):
    return render(request,'lead_management/report_lead.html')

def lead_manager_view(request):
    return render(request,'lead_management/lead_manager.html')

def lead_follow_up_histroy(request):
    return render(request,'lead_management/lead_history.html')

def lead_delete_product(request):
    return render(request,'lead_management/lead_delete_product.html')

def lead_analytics(request):
    return render(request,'lead_management/analytics.html')

def lead_employee_graph(request):
    return render(request,'lead_management/lead_employee_graph.html')