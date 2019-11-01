from datetime import datetime

from django.db.models import Sum, Min
from django.shortcuts import render, redirect
from django.db import connection
# Create your views here.
from user_app.models import SiteUser

from customer_app.models import Customer_Details

from purchase_app.views import check_admin_roles
from .models import Dispatch, Product_Details_Dispatch
from django.core.mail import send_mail
from Hsco import settings
import requests
import json
from ess_app.models import Employee_Analysis_month
from ess_app.models import Employee_Analysis_date



def add_dispatch_details(request):
    # form = Customer_Details_Form(request.POST or None, request.FILES or None)
    cust_sugg=Customer_Details.objects.all()

    if request.method == 'POST' or request.method=='FILES':
        customer_name = request.POST.get('customer_name')
        company_name = request.POST.get('company_name')
        address = request.POST.get('customer_address')
        contact_no = request.POST.get('contact_no')
        customer_email_id = request.POST.get('customer_email_id')

        item = Customer_Details()

        item.customer_name = customer_name
        item.company_name = company_name
        item.address = address
        item.contact_no = contact_no
        item.customer_email_id = customer_email_id

        item.save()


        dispatch_id = request.POST.get('dispatch_id')
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

        item2 = Dispatch()
        item2.user_id = SiteUser.objects.get(id=request.user.pk)
        item2.crm_no_id = item.pk
        item2.dispatch_id = dispatch_id
        item2.date_of_dispatch = date_of_dispatch
        item2.dispatch_by = dispatch_by
        item2.packed_by = packed_by
        item2.hamal_name = hamal_name
        item2.no_bundles = no_bundles
        item2.transport_name = transport_name
        item2.lr_no = lr_no
        item2.photo_lr_no = photo_lr_no
        item2.channel_of_dispatch = channel_of_dispatch
        item2.notes = notes

        item2.save()
        
        send_mail('Feedback Form','Click on the link to give feedback http://vikka.pythonanywhere.com/'+str(request.user.pk)+'/'+str(item.id)+'/'+str(item2.id) , settings.EMAIL_HOST_USER, [customer_email_id])

        message = 'Click on the link to give feedback http://vikka.pythonanywhere.com/'+str(request.user.pk)+'/'+str(item.id)+'/'+str(item2.id)


        url = "http://smshorizon.co.in/api/sendsms.php?user=" + settings.user + "&apikey=" + settings.api + "&mobile=" + contact_no + "&message=" + message + "&senderid=" + settings.senderid + "&type=txt"
        payload = ""
        headers = {'content-type': 'application/x-www-form-urlencoded'}

        response = requests.request("GET", url, data=json.dumps(payload), headers=headers)
        x = response.text


        return redirect('/dispatch_view')

    context = {
        'cust_sugg': cust_sugg
    }
    return render(request,'forms/dis_mod_form.html',context)

def report_dis_mod(request):
    if request.method =='POST':
        selected_list = request.POST.getlist('checks[]')
        start_date = request.POST.get('date1')
        end_date = request.POST.get('date2')
        string = ','.join(selected_list)
        print(selected_list)
        request.session['start_date']= start_date
        request.session['end_date']= end_date
        request.session['string']= string
        request.session['selected_list']= selected_list
        return redirect('/final_report_dis_mod/')
    return render(request,"report/report_dis_mod_form.html",)

def final_report_dis_mod(request):
    start_date = request.session.get('start_date')
    end_date = request.session.get('end_date')
    string = request.session.get('string')
    selected_list = request.session.get('selected_list')

    try:
        del request.session['start_date']
        del request.session['end_date']
        del request.session['string']
        del request.session['selected_list']
    except:
        pass
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT  " + string + " from dispatch_app_dispatch , customer_app_customer_details"
                                  "  where dispatch_app_dispatch.crm_no_id = customer_app_customer_details.id and entry_timedate between '" + start_date + "' and '" + end_date + "';")
        row = cursor.fetchall()
        final_row = [list(x) for x in row]
        list3 = []
        for i in row:
            list3.append(list(i))
    try:
        del request.session['start_date']
        del request.session['end_date']
        del request.session['string']
        del request.session['selected_list']
    except:
        pass

    context = {
        'final_row': final_row,
        'selected_list': selected_list,
    }

    return render(request,"report/final_report_dis_mod.html",context)

def dispatch_view(request):
    if request.method=='POST' :
        if'submit1' in request.POST:
            start_date = request.POST.get('date1')
            end_date = request.POST.get('date2')
            if check_admin_roles(request):  # For ADMIN
                dispatch_list = Dispatch.objects.filter(user_id__group__icontains=request.user.group,
                                                        user_id__is_deleted=False,entry_timedate__range=[start_date, end_date]).order_by('-id')
            else:  # For EMPLOYEE
                dispatch_list = Dispatch.objects.filter(user_id=request.user.pk,entry_timedate__range=[start_date, end_date]).order_by('-id')
            # dispatch_list = Dispatch.objects.filter()
            context = {
                'dispatch_list': dispatch_list,
            }
            return render(request, "manager/dispatch_view.html", context)
        elif 'submit2' in request.POST:
            contact = request.POST.get('contact')
            if check_admin_roles(request):  # For ADMIN
                dispatch_list = Dispatch.objects.filter(user_id__group__icontains=request.user.group,
                                                        user_id__is_deleted=False,crm_no__contact_no=contact).order_by('-id')
            else:  # For EMPLOYEE
                dispatch_list = Dispatch.objects.filter(user_id=request.user.pk,crm_no__contact_no=contact).order_by('-id')
            # dispatch_list = Dispatch.objects.filter(customer_no=contact)
            context = {
                'dispatch_list': dispatch_list,
            }
            return render(request, "manager/dispatch_view.html", context)

        elif 'submit3' in request.POST:
            email = request.POST.get('email')
            if check_admin_roles(request):  # For ADMIN
                dispatch_list = Dispatch.objects.filter(user_id__group__icontains=request.user.group,
                                                        user_id__is_deleted=False,crm_no__customer_email_id=email).order_by('-id')
            else:  # For EMPLOYEE
                dispatch_list = Dispatch.objects.filter(user_id=request.user.pk,crm_no__customer_email_id=email).order_by('-id')
            # dispatch_list = Dispatch.objects.filter(customer_email=email)
            context = {
                'dispatch_list': dispatch_list,
            }
            return render(request, "manager/dispatch_view.html", context)
        elif 'submit4' in request.POST:
            customer = request.POST.get('customer')
            if check_admin_roles(request):  # For ADMIN
                dispatch_list = Dispatch.objects.filter(user_id__group__icontains=request.user.group,
                                                        user_id__is_deleted=False,crm_no__customer_name=customer).order_by('-id')
            else:  # For EMPLOYEE
                dispatch_list = Dispatch.objects.filter(user_id=request.user.pk,crm_no__customer_name=customer).order_by('-id')
            # dispatch_list = Dispatch.objects.filter(customer_name=customer)
            context = {
                'dispatch_list': dispatch_list,
            }
            return render(request, "manager/dispatch_view.html", context)

        elif  'submit5' in request.POST:
            company = request.POST.get('company')
            if check_admin_roles(request):  # For ADMIN
                dispatch_list = Dispatch.objects.filter(user_id__group__icontains=request.user.group,
                                                        user_id__is_deleted=False,crm_no__company_name=company).order_by('-id')
            else:  # For EMPLOYEE
                dispatch_list = Dispatch.objects.filter(user_id=request.user.pk,crm_no__company_name=company).order_by('-id')
            # dispatch_list = Dispatch.objects.filter(company_name=company)
            context = {
                'dispatch_list': dispatch_list,
            }
            return render(request, "manager/dispatch_view.html", context)
        elif request.method=='POST' and 'submit6' in request.POST:
            crm = request.POST.get('crm')
            if check_admin_roles(request):  # For ADMIN
                dispatch_list = Dispatch.objects.filter(user_id__group__icontains=request.user.group,
                                                        user_id__is_deleted=False,crm_no__pk=crm).order_by('-id')
            else:  # For EMPLOYEE
                dispatch_list = Dispatch.objects.filter(user_id=request.user.pk,crm_no__pk=crm).order_by('-id')
            # dispatch_list = Dispatch.objects.filter(crn_number=crm)
            context = {
                'dispatch_list': dispatch_list,
            }
            return render(request, "manager/dispatch_view.html", context)
    else:
        if check_admin_roles(request):     #For ADMIN
            dispatch_list = Dispatch.objects.filter(user_id__group__icontains=request.user.group,user_id__is_deleted=False).order_by('-id')
        else:  #For EMPLOYEE
            dispatch_list = Dispatch.objects.filter(user_id=request.user.pk).order_by('-id')
        # dispatch_list = Dispatch.objects.all()

        context = {
            'dispatch_list': dispatch_list,
        }
        return render(request, "manager/dispatch_view.html", context)

def update_dispatch_details(request,update_id):
    dispatch_item=Dispatch.objects.get(id=update_id)
    product_list = Product_Details_Dispatch.objects.filter(dispatch_id=update_id)
    customer_id = Dispatch.objects.get(id=update_id).crm_no

    customer_id = Customer_Details.objects.get(id=customer_id)

    if request.method == 'POST' or request.method=='FILES':
        contact_no = request.POST.get('contact_no')
        customer_email = request.POST.get('customer_email_id')
        customer_name = request.POST.get('customer_name')
        company_name = request.POST.get('company_name')
        customer_address = request.POST.get('customer_address')

        item2 = customer_id

        item2.customer_name = customer_name
        item2.company_name = company_name
        item2.address = customer_address
        item2.contact_no = contact_no
        item2.customer_email_id = customer_email

        item2.save(update_fields=['contact_no', ]),
        item2.save(update_fields=['customer_email_id', ]),
        item2.save(update_fields=['customer_name', ]),
        item2.save(update_fields=['company_name', ]),
        item2.save(update_fields=['address', ]),


        dispatch_id = request.POST.get('dispatch_id')

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

        item = Dispatch.objects.get(id=update_id)

        item.dispatch_id = dispatch_id

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

        item.save(update_fields=['dispatch_id', ]),

        item.save(update_fields=['date_of_dispatch', ]),
        item.save(update_fields=['dispatch_by', ]),
        item.save(update_fields=['packed_by', ]),
        item.save(update_fields=['hamal_name', ]),
        item.save(update_fields=['no_bundles', ]),
        item.save(update_fields=['transport_name', ]),
        item.save(update_fields=['lr_no', ]),
        item.save(update_fields=['photo_lr_no', ]),
        item.save(update_fields=['channel_of_dispatch', ]),
        item.save(update_fields=['notes', ]),
        dispatch_item = Dispatch.objects.get(id=update_id)
        product_list = Product_Details_Dispatch.objects.filter(dispatch_id=update_id)

        context = {
            'dispatch_item': dispatch_item,
            'product_list': product_list,
        }
        return render(request, "update_forms/update_dis_mod_form.html", context)

    context = {
            'dispatch_item': dispatch_item,
            'product_list': product_list,
        }
    return render(request, "update_forms/update_dis_mod_form.html", context)
       # item.save(update_fields=[''])


        #return redirect('/dispatch_view')

    # context={
    #     'dispatch_item':dispatch_item,
    #     'product_list':product_list,
    # }
    # return render(request, "update_forms/update_dis_mod_form.html",context)

def dispatch_logs(request):
    return render(request,"logs/dispatch_logs.html",)

def dispatch_analytics(request):
    mon = datetime.now().month
    this_month = Employee_Analysis_month.objects.all().values('entry_date').annotate(data_sum=Sum('total_dispatch_done'))
    this_lis_date = []
    this_lis_sum = []
    for i in this_month:
        x = i
        this_lis_date.append(x['entry_date'].strftime("%B-%Y"))
        this_lis_sum.append(x['data_sum'])

    from django.db.models import Max
    # Generates a "SELECT MAX..." query
    value = Employee_Analysis_month.objects.aggregate(Max('total_dispatch_done'))
    print(value['total_dispatch_done__max'])
    try:
        value = Employee_Analysis_month.objects.get(total_sales_done=value['total_dispatch_done__max'])
    except:
        pass

    value_low = Employee_Analysis_month.objects.aggregate(Min('total_dispatch_done'))
    print(value_low['total_dispatch_done__min'])
    try:
        value_low = Employee_Analysis_month.objects.filter(total_sales_done=value_low['total_dispatch_done__min']).order_by('id').first()
    except:
        pass
    context = {

        'this_lis_date': this_lis_date,
        'this_lis_sum': this_lis_sum,
        'value': value,
        'value_low': value_low,

    }
    return render(request,"analytics/dispatch_analytics.html",)

def dispatch_employee_graph(request,user_id):
    from django.db.models import Sum

    user_id = request.user.pk

    # current month
    mon = datetime.now().month
    this_month = Employee_Analysis_date.objects.filter(user_id=user_id,entry_date__month=mon).values('entry_date',
                                                                                                         'total_dispatch_done_today')
    this_lis_date = []
    this_lis_sum = []
    for i in this_month:
        x = i
        this_lis_date.append(x['entry_date'].strftime('%Y-%m-%d'))
        this_lis_sum.append(x['total_dispatch_done_today'])

    # previous month sales
    mon = (datetime.now().month) - 1
    previous_month = Employee_Analysis_date.objects.filter(user_id=user_id,entry_date__month=mon).values('entry_date',
                                                                                                         'total_dispatch_done_today')
    previous_lis_date = []
    previous_lis_sum = []
    for i in previous_month:
        x = i
        previous_lis_date.append(x['entry_date'].strftime('%Y-%m-%d'))
        previous_lis_sum.append(x['total_dispatch_done_today'])

    if request.method == 'POST':
        start_date = request.POST.get('date1')
        end_date = request.POST.get('date2')
        qs = Employee_Analysis_date.objects.filter(user_id=user_id,entry_date__range=(start_date, end_date)).values(
            'entry_date','total_dispatch_done_today')
        lis_date = []
        lis_sum = []
        for i in qs:
            x = i
            lis_date.append(x['entry_date'].strftime('%Y-%m-%d'))
            lis_sum.append(x['total_dispatch_done_today'])

        context = {
            'final_list': lis_date,
            'final_list2': lis_sum,
            'previous_lis_date': previous_lis_date,
            'previous_lis_sum': previous_lis_sum,
            'this_lis_date': this_lis_date,
            'this_lis_sum': this_lis_sum,
            # 'rep_feedback': rep_feedback,
        }
        return render(request, "graphs/dispatch_employee_graph.html", context)
    else:

        qs = Employee_Analysis_date.objects.filter(user_id=user_id,entry_date__month=datetime.now().month).values(
            'entry_date','total_dispatch_done_today')
        lis_date = []
        lis_sum = []
        for i in qs:
            x = i
            lis_date.append(x['entry_date'].strftime('%Y-%m-%d'))
            lis_sum.append(x['total_dispatch_done_today'])
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
            # 'rep_feedback': rep_feedback,
            # 'feeback': feeback,
        }
        return render(request,"graphs/dispatch_employee_graph.html",context)



def load_dispatch_done(request,):
    selected = request.GET.get('loc_id')
    if selected=='true':
        dispatch_list = Dispatch.objects.filter(~Q(dispatch_by=None))

    else:
        dispatch_list = Dispatch.objects.filter(dispatch_by=None)
    context = {
        'dispatch_list': dispatch_list,
    }

    return render(request, 'AJAX/load_dispatch_done.html', context)

def load_dispatch_done_manager(request,):
    selected = request.GET.get('loc_id')

    if selected=='true':
        dispatch_list = Employee_Analysis_month.objects.filter(manager_id=request.user.name)
        # dispatch_list = Employee_Analysis_month.objects.filter(user_id__group=str(request.user.name))
        print("dispatch_list22")
        print(dispatch_list)
        context = {
            'dispatch_list2': dispatch_list,
            'manager': True,
        }

        return render(request, 'AJAX/load_dispatch_done_manager.html', context)
    else:
        dispatch_list = Dispatch.objects.all()
        print("dispatch_list")
        print(dispatch_list)
        context = {
            'dispatch_list': dispatch_list,
            'manager': False,
        }

        return render(request, 'AJAX/load_dispatch_done_manager.html', context)




