from django.shortcuts import render, redirect
from django.db import connection
# Create your views here.
from .models import Dispatch, Product_Details_Dispatch


def add_dispatch_details(request):
    # form = Customer_Details_Form(request.POST or None, request.FILES or None)
    if request.method == 'POST' or request.method=='FILES':
        dispatch_id = request.POST.get('dispatch_id')
        customer_no = request.POST.get('customer_no')
        customer_email = request.POST.get('customer_email')
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

        item = Dispatch()

        item.dispatch_id = dispatch_id
        item.customer_no = customer_no
        item.customer_email = customer_email
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


        return redirect('/dispatch_view')

    context = {
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
            "SELECT  " + string + " from dispatch_app_dispatch where entry_timedate between '" + start_date + "' and '" + end_date + "';")
        row = cursor.fetchall()

        final_row = [list(x) for x in row]
        list3 = []
        for i in row:
            list3.append(list(i))

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
            dispatch_list = Dispatch.objects.filter(entry_timedate__range=[start_date, end_date])
            context = {
                'dispatch_list': dispatch_list,
            }
            return render(request, "manager/dispatch_view.html", context)
        elif 'submit2' in request.POST:
            contact = request.POST.get('contact')
            dispatch_list = Dispatch.objects.filter(customer_no=contact)
            context = {
                'dispatch_list': dispatch_list,
            }
            return render(request, "manager/dispatch_view.html", context)

        elif 'submit3' in request.POST:
            email = request.POST.get('email')
            dispatch_list = Dispatch.objects.filter(customer_email=email)
            context = {
                'dispatch_list': dispatch_list,
            }
            return render(request, "manager/dispatch_view.html", context)
        elif 'submit4' in request.POST:
            customer = request.POST.get('customer')
            dispatch_list = Dispatch.objects.filter(customer_name=customer)
            context = {
                'dispatch_list': dispatch_list,
            }
            return render(request, "manager/dispatch_view.html", context)

        elif  'submit5' in request.POST:
            company = request.POST.get('company')
            dispatch_list = Dispatch.objects.filter(company_name=company)
            context = {
                'dispatch_list': dispatch_list,
            }
            return render(request, "manager/dispatch_view.html", context)
        elif request.method=='POST' and 'submit6' in request.POST:
            crm = request.POST.get('crm')
            dispatch_list = Dispatch.objects.filter(crn_number=crm)
            context = {
                'dispatch_list': dispatch_list,
            }
            return render(request, "manager/dispatch_view.html", context)
    else:
        dispatch_list = Dispatch.objects.all()

        context = {
            'dispatch_list': dispatch_list,
        }
        return render(request, "manager/dispatch_view.html", context)


def update_dispatch_details(request,update_id):
    dispatch_item=Dispatch.objects.get(id=update_id)
    product_list = Product_Details_Dispatch.objects.filter(dispatch_id=update_id)
    if request.method == 'POST' or request.method=='FILES':
        dispatch_id = request.POST.get('dispatch_id')
        customer_no = request.POST.get('customer_no')
        customer_email = request.POST.get('customer_email')
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

        item = Dispatch.objects.get(id=update_id)

        item.dispatch_id = dispatch_id
        item.customer_no = customer_no
        item.customer_email = customer_email
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


        item.save(update_fields=[''])


        return redirect('/dispatch_view')

    context={
        'dispatch_item':dispatch_item,
        'product_list':product_list,
    }
    return render(request, "update_forms/update_dis_mod_form.html",context)

def dispatch_logs(request):
    return render(request,"logs/dispatch_logs.html",)


