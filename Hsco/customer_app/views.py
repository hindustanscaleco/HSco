from django.db import connection
from django.db.models import Avg
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from user_app.models import SiteUser
from dispatch_app.models import Dispatch
from dispatch_app.models import Product_Details_Dispatch
from ess_app.models import Employee_Analysis
from .forms import Customer_Details_Form, Feedback_Form
from .models import Customer_Details, Feedback
from .forms import Product_Details_Form
from .models import Product_Details
from datetime import datetime

def add_customer_details(request):
    form = Customer_Details_Form(request.POST or None, request.FILES or None)
    if request.method == 'POST' or request.method=='FILES':
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





        dispatch = Dispatch()


        dispatch.customer_no = item.pk
        dispatch.customer_email = customer_email_id
        dispatch.customer_name = customer_name
        dispatch.company_name = company_name
        dispatch.customer_address = address

        dispatch.save()


        dispatch2 = Dispatch.objects.get(id=dispatch.pk)
        dispatch2.dispatch_id = str(dispatch.pk + 00000)
        dispatch2.save(update_fields=['dispatch_id'])

        customer_id = Customer_Details.objects.get(id=item.pk)
        customer_id.dispatch_id_assigned = Dispatch.objects.get(id=dispatch.pk) #str(dispatch.pk + 00000)
        customer_id.save(update_fields=['dispatch_id_assigned'])

        return redirect('/add_product_details/'+str(item.id))

    context = {
        'form': form,
    }
    return render(request,'forms/cust_mod_form.html',context)


def view_customer_details(request):

    if request.method == 'POST':
        if'submit1' in request.POST:
            start_date = request.POST.get('date1')
            end_date = request.POST.get('date2')
            cust_list = Customer_Details.objects.filter(entry_timedate__range=[start_date, end_date])
            context = {
                'customer_list': cust_list,
            }
            return render(request, 'dashboardnew/cm.html', context)
        elif 'submit2' in request.POST:
            contact = request.POST.get('contact')
            cust_list = Customer_Details.objects.filter(contact_no=contact)
            context = {
                'customer_list': cust_list,
            }
            return render(request, 'dashboardnew/cm.html', context)

        elif 'submit3' in request.POST:
            email = request.POST.get('email')
            cust_list = Customer_Details.objects.filter(customer_email_id=email)
            context = {
                'customer_list': cust_list,
            }
            return render(request, 'dashboardnew/cm.html', context)
        elif 'submit4' in request.POST:
            customer = request.POST.get('customer')
            cust_list = Customer_Details.objects.filter(customer_name=customer)
            context = {
                'customer_list': cust_list,
            }
            return render(request, 'dashboardnew/cm.html', context)

        elif  'submit5' in request.POST:
            company = request.POST.get('company')
            cust_list = Customer_Details.objects.filter(company_name=company)
            context = {
                'customer_list': cust_list,
            }
            return render(request, 'dashboardnew/cm.html', context)
        elif request.method=='POST' and 'submit6' in request.POST:
            crm = request.POST.get('crm')
            cust_list = Customer_Details.objects.filter(crn_number=crm)
            context = {
                'customer_list': cust_list,
            }
            return render(request, 'dashboardnew/cm.html', context)
    else:
        cust_list=Customer_Details.objects.all().order_by('-id')

        # with connection.cursor() as cursor:
        #     cursor.execute(
        #         "SELECT  dispatch_id_assigned_id,company_name from customer_app_customer_details  ;")
        #     row = cursor.fetchall()
        #
        #     customer_list = [list(x) for x in row]
        #     print(customer_list)
        #     list2 = []
        #     list3 = []
        #     for item in customer_list:
        #         list2.append(item[0])
        #         list3.append(item[1])
        #
        #     final_list = zip(list2,list3)

        context = {
            'customer_list': cust_list,
        }
        return render(request,'dashboardnew/cm.html',context )


def update_customer_details(request,id):
    product_list = Product_Details.objects.filter(customer_id=id)
    print(product_list)
    customer_id = Customer_Details.objects.get(id=id)

    context={
        'cust_id':customer_id,
        'product_list':product_list,
    }

    return render(request,'update_forms/update_cust_mod_form.html',context)


def add_product_details(request,id):
    customer = Customer_Details.objects.get(id=id)
    customer_id = customer.id
    dispatch_id_assigned = str(customer.dispatch_id_assigned)
    form = Product_Details_Form(request.POST or None)
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        quantity = request.POST.get('quantity')
        model_of_purchase = request.POST.get('model_of_purchase')
        type_of_scale = request.POST.get('type_of_scale')
        sub_model = request.POST.get('sub_model')
        sub_sub_model = request.POST.get('sub_sub_model')
        serial_no_scale = request.POST.get('serial_no_scale')
        brand = request.POST.get('brand')
        capacity = request.POST.get('capacity')
        unit = request.POST.get('unit')
        sales_person = request.POST.get('sales_person')
        purchase_type = request.POST.get('purchase_type')

        item = Product_Details()

        item.product_name = product_name
        item.quantity = quantity
        item.type_of_scale = type_of_scale
        item.model_of_purchase = model_of_purchase
        item.sub_model = sub_model
        item.sub_sub_model = sub_sub_model
        item.serial_no_scale = serial_no_scale
        item.brand = brand
        item.capacity = capacity
        item.unit = unit
        item.customer_id_id = customer_id
        item.sales_person = sales_person
        item.purchase_type = purchase_type
        item.save()


        print("dispatch_id_assigned")
        print("dispatch_id_assigned")
        print("dispatch_id_assigned")
        print(dispatch_id_assigned)
        print(dispatch_id_assigned)
        print(dispatch_id_assigned)
        dispatch_id=Dispatch.objects.get(id=dispatch_id_assigned)
        dispatch_pro = Product_Details_Dispatch()

        dispatch_pro.product_name = product_name
        dispatch_pro.quantity = quantity
        dispatch_pro.type_of_scale = type_of_scale
        dispatch_pro.model_of_purchase = model_of_purchase
        dispatch_pro.sub_model = sub_model
        dispatch_pro.sub_sub_model = sub_sub_model
        dispatch_pro.serial_no_scale = serial_no_scale
        dispatch_pro.brand = brand
        dispatch_pro.capacity = capacity
        dispatch_pro.unit = unit
        dispatch_pro.dispatch_id = dispatch_id
        dispatch_pro.sales_person = sales_person
        dispatch_pro.purchase_type = purchase_type
        dispatch_pro.save()






        return redirect('/update_customer_details/'+str(id))


    context = {
        'form': form,
        'customer_id': customer_id,
    }
    return render(request,'dashboardnew/add_product.html',context)



def report(request):
    if request.method =='POST':
        selected_list = request.POST.getlist('checks[]')
        start_date = request.POST.get('date1')
        end_date = request.POST.get('date2')
        string = ','.join(selected_list)
        print(selected_list)
        request.session['start_date'] = start_date
        request.session['end_date'] = end_date
        request.session['string'] = string
        request.session['selected_list'] = selected_list
        return redirect('/final_report/')
    return render(request,"report/report_cust_mod_form.html",)


def final_report(request):
    start_date = request.session.get('start_date')
    end_date = request.session.get('end_date')
    string = request.session.get('string')
    selected_list = request.session.get('selected_list')
    with connection.cursor() as cursor:
        cursor.execute("SELECT  "+string+" from customer_app_customer_details where date_of_purchase between '"+start_date+"' and '"+end_date+"';")
        row = cursor.fetchall()


        final_row= [list(x) for x in row]
        list3=[]
        for i in row:
            list3.append(list(i))


    context={
        'final_row':final_row,
        'selected_list':selected_list,
    }
    return render(request,"dashboardnew/final_report.html",context)


def manager_report(request):
    employee_list = SiteUser.objects.all()
    context={
        'employee_list':employee_list,
    }
    return render(request, 'dashboardnew/manager_report.html',context)


def feedbacka(request):
    return render(request, 'feedback/feedbacka.html')

def employee_sales_graph(request):
    user_id=request.user.pk
    currentMonth = datetime.now().month
    currentYear = datetime.now().year
    list_sales=Employee_Analysis.objects.filter(year=currentYear,user_id=user_id).values_list('month')
    list_sales_month=Employee_Analysis.objects.filter(year=currentYear,user_id=user_id).values_list('total_sales_done')
    # list_sales=Employee_Analysis.objects.filter(year=currentYear,user_id=user_id).values_list('total_sales_done')
    print(list(list_sales_month))
    print(list(list_sales))
    final_list=[]
    final_list2=[]
    for item in list_sales:
        final_list.append(item[0])

    for item in list_sales_month:
        final_list2.append(item[0])

    print(final_list)
    print(final_list2)
    context={
        'final_list':final_list,
        'final_list2':final_list2
    }
    return render(request,"graphs/sales_graph.html",context)


def feedback_customer(request):
    feedback_form = Feedback_Form(request.POST or None, request.FILES or None)
    if request.method == 'POST' :
        knowledge_of_person = request.POST.get('knowledge_of_person')
        timeliness_of_person = request.POST.get('timeliness_of_person')
        price_of_product = request.POST.get('price_of_product')
        overall_interaction = request.POST.get('overall_interaction')
        about_hsco = request.POST.get('about_hsco')
        any_suggestion = request.POST.get('any_suggestion')

        item = Feedback()
        item.knowledge_of_person = knowledge_of_person
        item.timeliness_of_person = timeliness_of_person
        item.price_of_product = price_of_product
        item.overall_interaction = overall_interaction
        item.about_hsco = about_hsco
        item.any_suggestion = any_suggestion
        item.save()

        return HttpResponse('Feedback Submitted!!!')
    context={
        'feedback_form': feedback_form,
    }
    return render(request,"feedback/feedback_customer.html",context)






