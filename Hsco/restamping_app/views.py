from django.shortcuts import render, redirect


from .models import Restamping_after_sales_service


def restamping_after_sales_service(request):
    # form = Customer_Details_Form(request.POST or None, request.FILES or None)
    if request.method == 'POST' or request.method=='FILES':
        customer_no = request.POST.get('customer_no')
        company_name = request.POST.get('company_name')
        address = request.POST.get('address')
        today_date = request.POST.get('today_date')
        mobile_no = request.POST.get('mobile_no')
        customer_email_id = request.POST.get('customer_email_id')
        product_to_stampped = request.POST.get('product_to_stampped')
        scale_type = request.POST.get('scale_type')
        sub_model = request.POST.get('sub_model')
        capacity = request.POST.get('capacity')
        old_serial_no = request.POST.get('old_serial_no')
        old_brand = request.POST.get('old_brand')
        amount = request.POST.get('amount')
        new_serial_no = request.POST.get('new_serial_no')
        brand = request.POST.get('brand')
        scale_delivery_date = request.POST.get('scale_delivery_date')

        item = Restamping_after_sales_service()

        item.customer_no = customer_no
        item.company_name = company_name
        item.address = address
        item.today_date = today_date
        item.company_name = company_name
        item.mobile_no = mobile_no
        item.customer_email_id = customer_email_id
        item.product_to_stampped = product_to_stampped
        item.scale_type = scale_type
        item.sub_model = sub_model
        item.capacity = capacity
        item.old_serial_no = old_serial_no
        item.old_brand = old_brand
        item.amount = amount
        item.new_serial_no = new_serial_no
        item.brand = brand
        item.scale_delivery_date = scale_delivery_date


        item.save()


        return redirect('/')

    return render(request,'forms/restamping_form.html',)
