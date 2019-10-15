from django.db import connection
from django.shortcuts import render, redirect


from .models import Restamping_after_sales_service, Restamping_Product

def restamping_manager(request):
    restamp_list= Restamping_after_sales_service.objects.all()
    context={
        'restamp_list':restamp_list,
    }
    return render(request, "manager/restamping_manager.html",context)

def restamping_after_sales_service(request):
    # form = Customer_Details_Form(request.POST or None, request.FILES or None)
    if request.method == 'POST' or request.method=='FILES':
        restampingno = request.POST.get('restampingno')
        customer_no = request.POST.get('customer_no')
        company_name = request.POST.get('company_name')
        address = request.POST.get('address')
        today_date = request.POST.get('today_date')
        mobile_no = request.POST.get('mobile_no')

        new_serial_no = request.POST.get('new_serial_no')
        brand = request.POST.get('brand')
        scale_delivery_date = request.POST.get('scale_delivery_date')

        item = Restamping_after_sales_service()

        item.restampingno = restampingno
        item.customer_no = customer_no
        item.company_name = company_name
        item.address = address
        item.today_date = today_date
        item.company_name = company_name
        item.mobile_no = mobile_no

        item.new_serial_no = new_serial_no
        item.brand = brand
        item.scale_delivery_date = scale_delivery_date


        item.save()


        return redirect('/restamping_product/'+str(item.id))

    return render(request, 'forms/restamping_form.html',)

def restamping_product(request,id):
    restamping_id = Restamping_after_sales_service.objects.get(id=id).id

    if request.method=='POST':
        customer_email_id = request.POST.get('customer_email_id')
        product_to_stampped = request.POST.get('product_to_stampped')
        scale_type = request.POST.get('scale_type')
        sub_model = request.POST.get('sub_model')
        capacity = request.POST.get('capacity')
        old_serial_no = request.POST.get('old_serial_no')
        old_brand = request.POST.get('old_brand')
        amount = request.POST.get('amount')

        item=Restamping_Product()

        item.customer_email_id = customer_email_id
        item.product_to_stampped = product_to_stampped
        item.scale_type = scale_type
        item.sub_model = sub_model
        item.capacity = capacity
        item.old_serial_no = old_serial_no
        item.old_brand = old_brand
        item.amount = amount
        item.restamping_id_id = restamping_id

        item.save()

        return redirect('/update_restamping_details/'+str(id))
    context = {
        'restamping_id': restamping_id,
    }
    return render(request,'dashboardnew/restamping_product.html',context)

def update_restamping_details(request,id):
    restamp_product_list = Restamping_Product.objects.filter(restamping_id=id)
    print(restamp_product_list)
    restamp_id = Restamping_after_sales_service.objects.get(id=id)

    context={
        'restamp_product_list':restamp_product_list,
        'restamp_id':restamp_id,
    }

    return render(request,'update_forms/update_restamping_form.html',context)

def report_restamping(request):
    if request.method == 'POST' or None:
        selected_list = request.POST.getlist('checks[]')
        repair_start_date = request.POST.get('date1')
        repair_end_date = request.POST.get('date2')
        repair_string = ','.join(selected_list)

        request.session['start_date'] = repair_start_date
        request.session['repair_end_date'] = repair_end_date
        request.session['repair_string'] = repair_string
        request.session['selected_list'] = selected_list
        return redirect('/final_report_restamping/')
    return render(request, "report/report_restamping_form.html",)

def final_report_restamping(request):
    restamp_start_date = str(request.session.get('repair_start_date'))
    restamp_end_date = str(request.session.get('repair_end_date'))
    restamp_string = request.session.get('repair_string')
    selected_list = request.session.get('selected_list')
    print(restamp_string )
    print(restamp_string )
    print(restamp_string )
    print(restamp_string )
    print(restamp_string )
    print(restamp_string )
    print(restamp_string )
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT " + restamp_string + " from restamping_app_restamping_after_sales_service where today_date between '" + restamp_start_date + "' and '" + restamp_end_date + "';")
        row = cursor.fetchall()
        print(row)
        final_row = [list(x) for x in row]
        repairing_data = []
        for i in row:
            repairing_data.append(list(i))
    context = {
        'final_row': final_row,
        'selected_list': selected_list,
    }
    return render(request,"report/final_report_restamp_mod_form.html",context)


