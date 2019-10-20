from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render, redirect

from customer_app.models import Customer_Details

from user_app.models import SiteUser
from .forms import add_Onsite_aftersales_service_form
import datetime

from .forms import Onsite_Repairing_Feedback_Form
from .models import Onsite_aftersales_service, Onsite_Products, Onsite_Feedback
from django.core.mail import send_mail
from Hsco import settings
from ess_app.models import Employee_Analysis_month
from ess_app.models import Employee_Analysis_date

def onsite_views(request):

    if request.method=='POST' :
        if'submit1' in request.POST:
            start_date = request.POST.get('date1')
            end_date = request.POST.get('date2')
            onsite_list = Onsite_aftersales_service.objects.filter(entry_timedate__range=[start_date, end_date])
            context = {
                'onsite_list': onsite_list,
            }
            return render(request, "manager/onsite_reparing.html", context)
        elif 'submit2' in request.POST:
            contact = request.POST.get('contact')
            onsite_list = Onsite_aftersales_service.objects.filter(phone_no=contact)
            context = {
                'onsite_list': onsite_list,
            }
            return render(request, "manager/onsite_reparing.html", context)

        elif 'submit3' in request.POST:
            email = request.POST.get('email')
            onsite_list = Onsite_aftersales_service.objects.filter(customer_email_id=email)
            context = {
                'onsite_list': onsite_list,
            }
            return render(request, "manager/onsite_reparing.html", context)
        elif 'submit4' in request.POST:
            customer = request.POST.get('customer')
            onsite_list = Onsite_aftersales_service.objects.filter(customer_name=customer)
            context = {
                'onsite_list': onsite_list,
            }
            return render(request, "manager/onsite_reparing.html", context)

        elif  'submit5' in request.POST:
            company = request.POST.get('company')
            onsite_list = Onsite_aftersales_service.objects.filter(company_name=company)
            context = {
                'onsite_list': onsite_list,
            }
            return render(request, "manager/onsite_reparing.html", context)
        elif request.method=='POST' and 'submit6' in request.POST:
            crm = request.POST.get('crm')
            onsite_list = Onsite_aftersales_service.objects.filter(crn_number=crm)
            context = {
                'onsite_list': onsite_list,
            }
            return render(request, "manager/onsite_reparing.html", context)
    else:
        onsite_list = Onsite_aftersales_service.objects.all()

        context = {
            'onsite_list': onsite_list,
        }
        return render(request, "manager/onsite_reparing.html", context)


def add_onsite_aftersales_service(request):
    # form = add_Onsite_aftersales_service_form(request.POST or None, request.FILES or None)
    if request.method == 'POST' or request.method == 'FILES':
        customer_name = request.POST.get('customer_name')
        company_name = request.POST.get('company_name')
        address = request.POST.get('customer_address')
        contact_no = request.POST.get('phone_no')
        customer_email_id = request.POST.get('customer_email_id')

        item = Customer_Details()

        item.customer_name = customer_name
        item.company_name = company_name
        item.address = address
        item.contact_no = contact_no
        item.customer_email_id = customer_email_id

        item.save()

        repairingno = request.POST.get('repairingno')
        previous_repairing_number = request.POST.get('previous_repairing_number')
        in_warranty = request.POST.get('in_warranty')
        date_of_complaint_received = request.POST.get('date_of_complaint_received')
        complaint_received_by = request.POST.get('complaint_received_by')
        nearest_railwaystation = request.POST.get('nearest_railwaystation')
        train_line = request.POST.get('tr   ain_line')
        products_to_be_repaired = request.POST.get('products_to_be_repaired')

        visiting_charges_told_customer = request.POST.get('visiting_charges_told_customer')
        total_cost = request.POST.get('components_replaced_in_warranty')
        complaint_assigned_to = request.POST.get('complaint_assigned_to')
        complaint_assigned_on = request.POST.get('complaint_assigned_on')
        time_taken_destination_return_office_min = request.POST.get('time_taken_destination_return_office_min')
        notes = request.POST.get('notes')
        feedback_given = request.POST.get('feedback_given')

        item2 = Onsite_aftersales_service()

        item2.crm_no_id = item.pk
        item2.repairingno = repairingno
        item2.previous_repairing_number = previous_repairing_number
        item2.in_warranty = in_warranty
        item2.date_of_complaint_received = date_of_complaint_received
        item2.complaint_received_by = complaint_received_by
        item2.nearest_railwaystation = nearest_railwaystation
        item2.train_line = train_line
        item2.products_to_be_repaired = products_to_be_repaired

        item2.visiting_charges_told_customer = visiting_charges_told_customer
        item2.total_cost = total_cost
        item2.complaint_assigned_to = complaint_assigned_to
        item2.complaint_assigned_on = complaint_assigned_on
        item2.time_taken_destination_return_office_min = time_taken_destination_return_office_min
        item2.notes = notes
        item2.feedback_given = feedback_given

        item2.save()
        send_mail('Feedback Form','Click on the link to give feedback' , settings.EMAIL_HOST_USER, [customer_email_id])

        return redirect('/add_onsite_product/'+str(item2.id))
    context={
        # 'form':form,
       
    }

    return render(request, 'forms/onsite_rep_form.html',context)

def add_onsite_product(request,id):
    onsite_id = Onsite_aftersales_service.objects.get(id=id).id
    print(onsite_id)
    if request.method == 'POST' or request.method == 'FILES':
        type_of_machine = request.POST.get('type_of_machine')
        model = request.POST.get('model')
        sub_model = request.POST.get('sub_model')
        capacity = request.POST.get('capacity')
        problem_in_scale = request.POST.get('problem_in_scale')
        components_replaced_in_warranty = request.POST.get('components_replaced_in_warranty')
        components_replaced = request.POST.get('components_replaced')
        cost = request.POST.get('cost')

        item = Onsite_Products()

        item.onsite_repairing_id_id = onsite_id
        item.type_of_machine = type_of_machine
        item.model = model
        item.sub_model = sub_model
        item.capacity = capacity
        item.problem_in_scale = problem_in_scale
        item.components_replaced_in_warranty = components_replaced_in_warranty
        item.components_replaced = components_replaced
        item.cost = cost
        item.save()



        return redirect('/update_onsite_details/'+str(id))
    context = {
        'onsite_id': onsite_id,
    }
    return render(request,"forms/onsite_product.html",context)

def update_onsite_details(request,id):
    onsite_id = Onsite_aftersales_service.objects.get(id=id)
    onsite_product_list = Onsite_Products.objects.filter(onsite_repairing_id=id)
    employee_list = SiteUser.objects.filter(role='Employee')

    print(onsite_product_list)
    if request.method == 'POST' or request.method == 'FILES':
        repairingno = request.POST.get('repairingno')
        customer_name = request.POST.get('customer_name')
        company_name = request.POST.get('company_name')
        customer_no = request.POST.get('customer_no')
        previous_repairing_number = request.POST.get('previous_repairing_number')
        in_warranty = request.POST.get('in_warranty')
        phone_no = request.POST.get('phone_no')
        customer_email_id = request.POST.get('customer_email_id')
        date_of_complaint_received = request.POST.get('date_of_complaint_received')
        customer_address = request.POST.get('customer_address')
        complaint_received_by = request.POST.get('complaint_received_by')
        nearest_railwaystation = request.POST.get('nearest_railwaystation')
        train_line = request.POST.get('train_line')
        products_to_be_repaired = request.POST.get('products_to_be_repaired')

        visiting_charges_told_customer = request.POST.get('visiting_charges_told_customer')
        total_cost = request.POST.get('components_replaced_in_warranty')
        complaint_assigned_to = request.POST.get('complaint_assigned_to')
        complaint_assigned_on = request.POST.get('complaint_assigned_on')
        time_taken_destination_return_office_min = request.POST.get('time_taken_destination_return_office_min')
        notes = request.POST.get('notes')
        feedback_given = request.POST.get('feedback_given')
        assigned_to = request.POST.get('assigned_to')


        item = onsite_id

        item.repairingno = repairingno
        item.customer_name = customer_name
        item.company_name = company_name
        item.customer_no = customer_no
        item.previous_repairing_number = previous_repairing_number
        item.in_warranty = in_warranty
        item.phone_no = phone_no
        item.customer_email_id = customer_email_id
        item.date_of_complaint_received = date_of_complaint_received
        item.customer_address = customer_address
        item.complaint_received_by = complaint_received_by
        item.nearest_railwaystation = nearest_railwaystation
        item.train_line = train_line
        item.products_to_be_repaired = products_to_be_repaired
        item.visiting_charges_told_customer = visiting_charges_told_customer
        item.total_cost = total_cost
        item.complaint_assigned_to = complaint_assigned_to
        item.complaint_assigned_on = complaint_assigned_on
        item.time_taken_destination_return_office_min = time_taken_destination_return_office_min
        item.notes = notes
        item.feedback_given = feedback_given
        item.assigned_to = assigned_to

        #item.save(update_fields=['onsite_repairing_id_id', ]),
        item.save(update_fields=['assigned_to', ]),
        item.save(update_fields=['repairingno', ]),
        item.save(update_fields=['customer_name', ]),
        item.save(update_fields=['company_name', ]),
        item.save(update_fields=['customer_no', ]),
        item.save(update_fields=['previous_repairing_number', ]),
        item.save(update_fields=['in_warranty', ]),
        item.save(update_fields=['phone_no', ]),
        item.save(update_fields=['customer_email_id', ]),
        item.save(update_fields=['date_of_complaint_received', ]),
        item.save(update_fields=['customer_address', ]),
        item.save(update_fields=['complaint_received_by', ]),
        item.save(update_fields=['nearest_railwaystation', ]),
        item.save(update_fields=['train_line', ]),
        item.save(update_fields=['products_to_be_repaired', ]),
        item.save(update_fields=['visiting_charges_told_customer', ]),
        item.save(update_fields=['total_cost', ]),
        item.save(update_fields=['complaint_assigned_to', ]),
        item.save(update_fields=['complaint_assigned_on', ]),
        item.save(update_fields=['time_taken_destination_return_office_min', ]),
        item.save(update_fields=['notes', ]),
        item.save(update_fields=['feedback_given', ]),
        onsite_id = Onsite_aftersales_service.objects.get(id=id)

        context = {
            'onsite_id': onsite_id,
            'onsite_product_list': onsite_product_list,
        }

        return render(request, 'update_forms/update_onsite_rep_form.html', context)


    context={
        'onsite_id':onsite_id,
        'onsite_product_list':onsite_product_list,
        'employee_list':employee_list,
    }

    return render(request,'update_forms/update_onsite_rep_form.html',context)

def report_onsite(request):
    if request.method == 'POST' or None:
        selected_list = request.POST.getlist('checks[]')
        onsite_start_date = request.POST.get('date1')
        onsite_end_date = request.POST.get('date2')
        onsite_string = ','.join(selected_list)

        request.session['start_date'] = onsite_start_date
        request.session['repair_end_date'] = onsite_end_date
        request.session['repair_string'] = onsite_string
        request.session['selected_list'] = selected_list
        return redirect('/final_report_onsite/')
    return render(request,"report/report_onsite_rep_form.html",)

def final_report_onsite(request):
    repair_start_date = str(request.session.get('repair_start_date'))
    repair_end_date = str(request.session.get('repair_end_date'))
    repair_string = request.session.get('repair_string')
    selected_list = request.session.get('selected_list')
    print(repair_string)
    print(repair_start_date)


    print(repair_start_date)
    print(repair_end_date)
    print(selected_list)
    with connection.cursor() as cursor:
        cursor.execute("SELECT "+repair_string+" from onsitevisit_app_onsite_aftersales_service where auto_timedate between '"+repair_start_date+"' and '"+repair_end_date+"';")
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
    return render(request,'report/final_onsite_report.html',context)

def feedback_onrepairing(request):
    feedback_form = Onsite_Repairing_Feedback_Form(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        backend_team = request.POST.get('backend_team')
        onsite_worker = request.POST.get('onsite_worker')
        speed_of_performance = request.POST.get('speed_of_performance')
        price_of_reparing = request.POST.get('price_of_reparing')
        overall_interaction = request.POST.get('overall_interaction')
        about_hsco = request.POST.get('about_hsco')
        any_suggestion = request.POST.get('any_suggestion')

        item = Onsite_Feedback()
        item.backend_team = backend_team
        item.onsite_worker = onsite_worker
        item.speed_of_performance = speed_of_performance
        item.price_of_reparing = price_of_reparing
        item.overall_interaction = overall_interaction
        item.about_hsco = about_hsco
        item.any_suggestion = any_suggestion
        item.save()

        return HttpResponse('Feedback Submitted!!!')
    context = {
        'feedback_form': feedback_form,
    }
    return render(request,"feedback/feedback_onrepairing.html",context)


def load_onsite_reparing_stages_list(request,):
    selected = request.GET.get('loc_id')
    onsite_list = Onsite_aftersales_service.objects.filter(current_stage=selected)
    context = {
        'onsite_list': onsite_list,
    }

    return render(request, 'AJAX/load_onsite_reparing_stage.html', context)

def onsitevisit_app_graph(request):
    from django.db.models import Sum

    user_id = request.user.pk
    rep_feedback = Onsite_Feedback.objects.all()

    print(user_id)
    obj = Employee_Analysis_month.objects.get(user_id=user_id)
    obj.onsitereparing_target_achived_till_now = (obj.total_reparing_done_onsite / obj.onsitereparing_target_given) * 100
    obj.save()
    # current month
    target_achieved = obj.sales_target_achived_till_now
    # current month
    mon = datetime.now().month
    this_month = Employee_Analysis_date.objects.filter(entry_date__month=mon).values('entry_date').annotate(
        data_sum=Sum('total_reparing_done_onsite_today'))
    this_lis_date = []
    this_lis_sum = []
    for i in this_month:
        x = i
        this_lis_date.append(x['entry_date'].strftime('%Y-%m-%d'))
        this_lis_sum.append(x['data_sum'])

    # previous month sales
    mon = (datetime.now().month) - 1
    previous_month = Employee_Analysis_date.objects.filter(entry_date__month=mon).values('entry_date').annotate(
        data_sum=Sum('total_reparing_done_onsite_today'))
    previous_lis_date = []
    previous_lis_sum = []
    for i in previous_month:
        x = i
        previous_lis_date.append(x['entry_date'].strftime('%Y-%m-%d'))
        previous_lis_sum.append(x['data_sum'])

    if request.method == 'POST':
        start_date = request.POST.get('date1')
        end_date = request.POST.get('date2')
        qs = Employee_Analysis_date.objects.filter(entry_date__range=(start_date, end_date)).values(
            'entry_date').annotate(data_sum=Sum('total_reparing_done_onsite_today'))
        lis_date = []
        lis_sum = []
        for i in qs:
            x = i
            lis_date.append(x['entry_date'].strftime('%Y-%m-%d'))
            lis_sum.append(x['data_sum'])

        context = {
            'final_list': lis_date,
            'final_list2': lis_sum,
            'previous_lis_date': previous_lis_date,
            'previous_lis_sum': previous_lis_sum,
            'this_lis_date': this_lis_date,
            'this_lis_sum': this_lis_sum,
            'target_achieved': target_achieved,
            # 'rep_feedback': rep_feedback,
        }
        return render(request, "graphs/onsitevisit_app_graph.html", context)
    else:

        qs = Employee_Analysis_date.objects.filter(entry_date__month=datetime.now().month).values(
            'entry_date').annotate(data_sum=Sum('total_reparing_done_onsite_today'))
        lis_date = []
        lis_sum = []
        for i in qs:
            x = i
            lis_date.append(x['entry_date'].strftime('%Y-%m-%d'))
            lis_sum.append(x['data_sum'])
        print(lis_date)
        print(lis_sum)

        # user_id=request.user.pk
        # currentMonth = datetime.now().month
        # currentYear = datetime.now().year
        # list_sales=Employee_Analysis_month.objects.filter(year=currentYear,user_id=user_id).values_list('month')
        # list_sales_month=Employee_Analysis_month.objects.filter(year=currentYear,user_id=user_id).values_list('total_sales_done')
        # # list_sales=Employee_Analysis.objects.filter(year=currentYear,user_id=user_id).values_list('total_sales_done')
        # print(list(list_sales_month))
        # print(list(list_sales))
        # final_list=[]
        # final_list2=[]
        # for item in list_sales:
        #     final_list.append(item[0])
        #
        # for item in list_sales_month:
        #     final_list2.append(item[0])
        #
        # print(final_list)
        # print(final_list2)
        context = {
            'final_list': lis_date,
            'final_list2': lis_sum,
            'previous_lis_date': previous_lis_date,
            'previous_lis_sum': previous_lis_sum,
            'this_lis_date': this_lis_date,
            'this_lis_sum': this_lis_sum,
            'target_achieved': target_achieved,
            # 'feeback': feeback,
        }
        return render(request,"graphs/onsitevisit_app_graph.html",context)

