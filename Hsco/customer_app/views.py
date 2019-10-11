from django.shortcuts import render, redirect

from .forms import Customer_Details_Form
from .models import Customer_Details
from .forms import Product_Details_Form
from .models import Product_Details

def add_customer_details(request):
    form = Customer_Details_Form(request.POST or None, request.FILES or None)
    if request.method == 'POST' or  request.method=='FILES':
        customer_name = request.POST.get('customer_name')
        company_name = request.POST.get('company_name')
        address = request.POST.get('address')
        contact_no = request.POST.get('contact_no')
        customer_email_id = request.POST.get('customer_email_id')
        date_of_purchase = request.POST.get('date_of_purchase')
        product_purchase_date = request.POST.get('product_purchase_date')
        bill_no = request.POST.get('bill_no')
        upload_op_file = request.POST.get('upload_op_file')
        po_number = request.POST.get('po_number')
        photo_lr_no = request.POST.get('photo_lr_no')
        channel_of_sales = request.POST.get('channel_of_sales')
        industry = request.POST.get('industry')
        value_of_goods = request.POST.get('value_of_goods')
        channel_of_dispatch = request.POST.get('channel_of_dispatch')
        notes = request.POST.get('notes')
        feedback_form_filled = request.POST.get('feedback_form_filled')

        item = Customer_Details()

        item.customer_name = customer_name
        item.company_name = company_name
        item.date = address
        item.company_name = company_name
        item.address = address
        item.contact_no = contact_no
        item.customer_email_id = customer_email_id
        item.date_of_purchase = date_of_purchase
        item.product_purchase_date = product_purchase_date
        item.bill_no = bill_no
        item.upload_op_file = upload_op_file
        item.photo_lr_no = photo_lr_no
        item.po_number = po_number
        item.channel_of_sales = channel_of_sales
        item.industry = industry
        item.value_of_goods = value_of_goods
        item.channel_of_dispatch = channel_of_dispatch
        item.notes = notes
        item.feedback_form_filled = feedback_form_filled

        item.save()


        return redirect('/')

    context = {
        'form': form,
    }
    return render(request,'forms/cust_mod_form.html',context)



def add_product_details(request):
    form = Product_Details_Form(request.POST or None)
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        quantity = request.POST.get('quantity')
        type_of_scale = request.POST.get('type_of_scale')
        sub_model = request.POST.get('sub_model')
        sub_sub_model = request.POST.get('sub_sub_model')
        serial_no_scale = request.POST.get('serial_no_scale')
        brand = request.POST.get('brand')
        unit = request.POST.get('unit')

        item = Product_Details()

        item.product_name = product_name
        item.quantity = quantity
        item.type_of_scale = type_of_scale
        item.sub_model = sub_model
        item.sub_sub_model = sub_sub_model
        item.serial_no_scale = serial_no_scale
        item.brand = brand
        item.unit = unit

        item.save()

    return redirect('//')


    context = {
        'form': form,
    }
    return render(request,'',context)

def view_customer_details(request):
    customer_list = Customer_Details.objects.all()
    context={
        customer_list:'customer_list',
    }
    return render(request,'dashboardnew/cm.html',context )



def manager_report(request):
    return render(request, 'dashboardnew/manager_report.html',)
