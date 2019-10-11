from django.shortcuts import render, redirect


# Create your views here.
from .models import Restamping_after_sales_service


def restamping_after_sales_service(request):
    # form = Customer_Details_Form(request.POST or None, request.FILES or None)
    if request.method == 'POST' or request.method=='FILES':
        customer_no = request.POST.get('customer_no')
        company_address = request.POST.get('company_address')
        address = request.POST.get('address')
        customer_name = request.POST.get('customer_name')
        company_name = request.POST.get('company_name')
        customer_address = request.POST.get('customer_address')
        date_of_dispatch = request.POST.get('date_of_dispatch')
        dispatch_by = request.POST.get('dispatch_by')
        packed_by = request.POST.get('packed_by')
        hamal_name = request.POST.get('hamal_name')
        no_bundles = request.POST.get('no_bundles')
        transport_name = request.POST.get('transport_name')
        lr_no = request.POST.get('lr_no')
        photo_lr_no = request.POST.get('photo_lr_no')
        channel_of_dispatch = request.POST.get('channel_of_dispatch')
        notes = request.POST.get('notes')

        item = Restamping_after_sales_service()

        item.customer_no = customer_no
        item.company_address = customer_no
        item.address = address
        item.customer_name = customer_name
        item.company_name = company_name
        item.customer_address = customer_address
        item.date_of_dispatch = date_of_dispatch
        item.dispatch_by = dispatch_by
        item.packed_by = packed_by
        item.hamal_name = hamal_name
        item.no_bundles = no_bundles
        item.transport_name = transport_name
        item.lr_no = lr_no
        item.photo_lr_no = photo_lr_no
        item.channel_of_dispatch = channel_of_dispatch
        item.notes = notes


        item.save()
        print('dsdsd')
        print(item)

        return redirect('/')

    context = {
    }
    return render(request,'forms/restamping_form.html',context)
