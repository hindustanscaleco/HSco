from datetime import datetime

from django.db import connection
from django.shortcuts import render, redirect

from django.core.mail import send_mail
from Hsco import settings
from .models import Restamping_after_sales_service, Restamping_Product
import requests
import json
from ess_app.models import Employee_Analysis

def restamping_manager(request):
    if request.method == 'POST':
        if 'submit1' in request.POST:
            start_date = request.POST.get('date1')
            end_date = request.POST.get('date2')
            restamp_list = Restamping_after_sales_service.objects.filter(entry_timedate__range=[start_date, end_date])
            context = {
                'restamp_list': restamp_list,
            }
            return render(request, "manager/restamping_manager.html", context)
        elif 'submit2' in request.POST:
            contact = request.POST.get('contact')
            restamp_list = Restamping_after_sales_service.objects.filter(mobile_no=contact)
            context = {
                'restamp_list': restamp_list,
            }
            return render(request, "manager/restamping_manager.html", context)

        elif 'submit3' in request.POST:
            email = request.POST.get('email')
            restamp_list = Restamping_after_sales_service.objects.filter(customer_email_id=email)
            context = {
                'restamp_list': restamp_list,
            }
            return render(request, "manager/restamping_manager.html", context)
        elif 'submit4' in request.POST:
            customer = request.POST.get('customer')
            restamp_list = Restamping_after_sales_service.objects.filter(name=customer)
            context = {
                'restamp_list': restamp_list,
            }
            return render(request, "manager/restamping_manager.html", context)

        elif 'submit5' in request.POST:
            company = request.POST.get('company')
            restamp_list = Restamping_after_sales_service.objects.filter(company_name=company)
            context = {
                'restamp_list': restamp_list,
            }
            return render(request, "manager/restamping_manager.html", context)
        elif request.method == 'POST' and 'submit6' in request.POST:
            crm = request.POST.get('crm')
            restamp_list = Restamping_after_sales_service.objects.filter(crn_number=crm)
            context = {
                'restamp_list': restamp_list,
            }
            return render(request, "manager/restamping_manager.html", context)
    else:
        restamp_list = Restamping_after_sales_service.objects.all()

        context = {
            'restamp_list': restamp_list,
        }
        return render(request, "manager/restamping_manager.html", context)


def restamping_after_sales_service(request):
    # form = Customer_Details_Form(request.POST or None, request.FILES or None)
    if request.method == 'POST' or request.method=='FILES':
        restampingno = request.POST.get('restampingno')
        customer_no = request.POST.get('customer_no')
        company_name = request.POST.get('company_name')
        address = request.POST.get('address')
        today_date = request.POST.get('today_date')
        mobile_no = request.POST.get('mobile_no')
        customer_email_id = request.POST.get('customer_email_id')

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
        item.customer_email_id = customer_email_id
        item.new_serial_no = new_serial_no
        item.brand = brand
        item.scale_delivery_date = scale_delivery_date


        item.save()
        send_mail('Feedback Form','Click on the link to give feedback' , settings.EMAIL_HOST_USER, [customer_email_id])

        # message = 'txt'
        #
        #
        # url = "http://smshorizon.co.in/api/sendsms.php?user=" + settings.user + "&apikey=" + settings.api + "&mobile=" + mobile_no + "&message=" + message + "&senderid=" + settings.senderid + "&type=txt"
        # payload = ""
        # headers = {'content-type': 'application/x-www-form-urlencoded'}
        #
        # response = requests.request("GET", url, data=json.dumps(payload), headers=headers)
        # x = response.text


        return redirect('/restamping_product/'+str(item.id))

    return render(request, 'forms/restamping_form.html',)

def restamping_product(request,id):
    restamping_id = Restamping_after_sales_service.objects.get(id=id).id

    if request.method=='POST':
        product_to_stampped = request.POST.get('product_to_stampped')
        scale_type = request.POST.get('scale_type')
        sub_model = request.POST.get('sub_model')
        capacity = request.POST.get('capacity')
        old_serial_no = request.POST.get('old_serial_no')
        old_brand = request.POST.get('old_brand')
        amount = request.POST.get('amount')

        item=Restamping_Product()

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
    personal_id = Restamping_after_sales_service.objects.get(id=id)
    if request.method == 'POST':
        restampingno = request.POST.get('restampingno')
        customer_no = request.POST.get('customer_no')
        company_name = request.POST.get('company_name')
        address = request.POST.get('address')
        today_date = request.POST.get('today_date')
        mobile_no = request.POST.get('mobile_no')
        new_serial_no = request.POST.get('new_serial_no')
        brand = request.POST.get('brand')
        scale_delivery_date = request.POST.get('scale_delivery_date')

        print(today_date)
        print(today_date)
        print(today_date)
        item = personal_id
        item.restampingno = restampingno
        item.customer_no = customer_no
        item.company_name = company_name
        item.address = address
        item.today_date = today_date
        item.mobile_no = mobile_no
        item.new_serial_no = new_serial_no
        item.brand = brand
        item.scale_delivery_date = scale_delivery_date

        item.save(update_fields=['restampingno', ]),
        item.save(update_fields=['customer_no', ]),
        item.save(update_fields=['company_name', ]),
        item.save(update_fields=['address', ]),
        item.save(update_fields=['today_date', ]),
        item.save(update_fields=['mobile_no', ]),
        item.save(update_fields=['new_serial_no', ]),
        item.save(update_fields=['brand', ]),
        item.save(update_fields=['scale_delivery_date', ]),
        personal_id = Restamping_after_sales_service.objects.get(id=id)

        context = {
            'personal_id': personal_id,
        }

        return render(request, 'update_forms/update_restamping_form.html', context)

    context = {
        'personal_id': personal_id,
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

def restamping_employee_graph(request):
    user_id=request.user.pk
    currentMonth = datetime.now().month
    currentYear = datetime.now().year
    list_sales=Employee_Analysis.objects.filter(year=currentYear,user_id=user_id).values_list('month')
    list_sales_month=Employee_Analysis.objects.filter(year=currentYear,user_id=user_id).values_list('total_restamping_done')
    # list_sales=Employee_Analysis.objects.filter(year=currentYear,user_id=user_id).values_list('total_sales_done')
    list_avg = Employee_Analysis.objects.filter(year=currentYear,user_id=user_id).values_list('avg_time_collect_to_dispatch_restamping')
    avg_time_est =Employee_Analysis.objects.filter(year=currentYear,user_id=user_id).values_list('total_reparing_done_onsite')

    print(list(list_sales_month))
    print(list(list_sales))
    final_list=[]
    final_list2=[]
    final_list3=[]
    final_list4=[]
    for item in list_sales:
        final_list.append(item[0])

    for item in list_sales_month:
        final_list2.append(item[0])

    for item in list_avg:
        final_list3.append(item[0])

    for item in avg_time_est:
        final_list4.append(item[0])

    context={
        'final_list':final_list,
        'final_list2':final_list2,
    }
    return render(request,"graphs/restamping_employee_graph.html",context)








