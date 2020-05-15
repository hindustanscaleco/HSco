import calendar
from datetime import datetime
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from user_app.models import SiteUser
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required

from Hsco import settings
import requests
import json
from purchase_app.views import check_admin_roles
from onsitevisit_app.models import Onsite_Feedback
from .models import Employee_Leave, Defects_Warning, Employee_Analysis_month
from purchase_app.models import Feedback
from repairing_app.models import Repairing_Feedback
from amc_visit_app.models import AMC_Feedback

def add_ess_details(request):
    if request.method == 'POST' or  request.method=='FILES':
        employee_name = request.POST.get('employee_name')
        details = request.POST.get('details')
        contact_no = request.POST.get('contact_no')
        email_id = request.POST.get('email_id')
        photo = request.POST.get('photo')
        pancard = request.POST.get('pancard')
        aadhar_card = request.POST.get('aadhar_card')
        bank_details = request.POST.get('bank_details')
        photo_of_cancelled_cheque = request.POST.get('photo_of_cancelled_cheque')
        calendar = request.POST.get('calendar')
        target_of_month = request.POST.get('target_of_month')
        target_achived_till_now = request.POST.get('target_achived_till_now')
        month_on_month_sale_achived = request.POST.get('month_on_month_sale_achived')
        defect_given = request.POST.get('defect_given')
        warnings_given = request.POST.get('warnings_given')

        item = SiteUser()

        item.employee_name = employee_name
        item.details = details
        item.contact_no = contact_no
        item.email_id = email_id
        item.photo = photo
        item.pancard = pancard
        item.aadhar_card = aadhar_card
        item.photo_of_cancelled_cheque = photo_of_cancelled_cheque
        item.target_of_month = target_of_month
        item.target_achived_till_now = target_achived_till_now
        item.bank_details = bank_details
        item.contact_no = contact_no
        item.pancard = pancard
        item.aadhar_card = aadhar_card
        item.bank_details = bank_details
        item.photo_of_cancelled_cheque = photo_of_cancelled_cheque
        item.calendar = calendar
        item.target_of_month = target_of_month
        item.target_achived_till_now = target_achived_till_now
        item.month_on_month_sale_achived = month_on_month_sale_achived
        item.defect_given = defect_given
        item.warnings_given = warnings_given

        item.save()
        send_mail('Feedback Form','Click on the link to give feedback' , settings.EMAIL_HOST_USER, [email_id])

        message = 'txt'


        url = "http://smshorizon.co.in/api/sendsms.php?user=" + settings.user + "&apikey=" + settings.api + "&mobile=" + contact_no + "&message=" + message + "&senderid=" + settings.senderid + "&type=txt"
        payload = ""
        headers = {'content-type': 'application/x-www-form-urlencoded'}

        response = requests.request("GET", url, data=json.dumps(payload), headers=headers)
        x = response.text

        return redirect('/')




    return render(request,'forms/ess_form.html',)



def ess_home(request):
    context={}
    print(request.user.role)
    if request.user.role == 'Super Admin':
        leave_req_list = Employee_Leave.objects.filter(user_id__is_deleted=False,).order_by('-id')
        context2={
            'leave_req_list': leave_req_list
        }
        context.update(context2)
    elif request.user.role == 'Manager' or request.user.role == 'Admin':
        leave_req_list = Employee_Leave.objects.filter(user_id__group__icontains=request.user.name, user_id__is_deleted=False)
        context22 = {
            'leave_req_list': leave_req_list
        }
        context.update(context22)
    if request.user.role != 'Super Admin':
        leave_list = Employee_Leave.objects.filter(user_id=request.user.id)
        context25={
            'leave_list':leave_list,
        }
        context.update(context25)
    if request.method == 'POST' and 'list[]' in request.POST:
        user_id = request.POST.get('user_id')
        list = request.POST.getlist('list[]')



        item2 = Employee_Leave.objects.get(id=user_id)
        if 'yes' in list:
            item2.is_approved = True
            item2.save(update_fields=['is_approved'])

        elif 'no' in list:
            item2.is_approved = False
            item2.in_process = False
            item2.save(update_fields=['is_approved'])
            item2.save(update_fields=['in_process'])
        return redirect('/ess_home/')

    if request.method == 'POST'and 'from' in request.POST:
        from_date = request.POST.get('from')
        to = request.POST.get('to')
        reason = request.POST.get('reason')

        item = Employee_Leave()

        item.user_id = SiteUser.objects.get(id=request.user.pk)
        item.requested_leave_date_from = from_date
        item.requested_leave_date_to = to
        item.reason = reason
        item.save()
        context25={
            'success':True,
        }
        context.update(context25)

        return render(request,'dashboardnew/ess_home.html',context)

    return render(request,'dashboardnew/ess_home.html',context)


def load_deletd_users(request):
    selected = request.GET.get('loc_id')

    if selected == 'true':
        list = SiteUser.objects.filter(is_deleted=True).order_by('-id')
        if request.user.role == 'Super Admin':
            list = SiteUser.objects.filter(is_deleted=True, )
        elif request.user.role == 'Admin':
            list = SiteUser.objects.filter(is_deleted=True, admin__icontains=request.user.name, )
        elif request.user.role == 'Manager':
            list = SiteUser.objects.filter(is_deleted=True, manager__icontains=request.user.name, )

        context = {
            'list': list,
            'deleted': True,
        }
    else:
        list = SiteUser.objects.filter(group__icontains=request.user.name,is_deleted=False )
        if request.user.role == 'Super Admin':
            list = SiteUser.objects.filter(is_deleted=False, )
        elif request.user.role == 'Admin':
            list = SiteUser.objects.filter(is_deleted=False, admin__icontains=request.user.name, )
        elif request.user.role == 'Manager':
            list = SiteUser.objects.filter(is_deleted=False, manager__icontains=request.user.name, )

        context = {
            'list': list

        }


    return render(request, 'AJAX/load_deleted.html', context)

def load_deletd_employee(request):
    selected = request.GET.get('loc_id')

    if selected == 'true':

        if request.user.role == 'Super Admin':
            employee_list = SiteUser.objects.filter(role='Employee', group__icontains=request.user.name,
                                                    is_deleted=True)
        elif request.user.role == 'Admin':
            employee_list = SiteUser.objects.filter(role='Employee', admin__icontains=request.user.name,
                                                    is_deleted=True)
        elif request.user.role == 'Manager':
            employee_list = SiteUser.objects.filter(role='Employee', manager__icontains=request.user.name,
                                                    is_deleted=True)


        # list = SiteUser.objects.filter(role='Employee',group__icontains=request.user.name,is_deleted=True).order_by('-id')


        context = {
            'employee_list': employee_list,
            'deleted': True,
        }
    else:
        if request.user.role == 'Super Admin':
            employee_list = SiteUser.objects.filter(role='Employee', group__icontains=request.user.name,
                                                    is_deleted=False)
        elif request.user.role == 'Admin':
            employee_list = SiteUser.objects.filter(role='Employee', admin__icontains=request.user.name,
                                                    is_deleted=False)
        elif request.user.role == 'Manager':
            employee_list = SiteUser.objects.filter(role='Employee', manager__icontains=request.user.name,
                                                    is_deleted=False)

        context = {
            'employee_list': employee_list

        }


    return render(request, 'AJAX/load_deleted_employee.html', context)


def load_deletd_admin(request):
    selected = request.GET.get('loc_id')

    if selected == 'true':
        list = SiteUser.objects.filter(role='Admin', is_deleted=True).order_by('-id')

        context = {
            'admin_list': list,
            'deleted': True,
        }
    else:
        list = SiteUser.objects.filter(role='Admin', is_deleted=False)

        context = {
            'admin_list': list

        }

    return render(request, 'AJAX/load_deleted_admin.html', context)

def load_deletd_manager(request):
    selected = request.GET.get('loc_id')

    if selected == 'true':

        if request.user.role == 'Super Admin':
            list = SiteUser.objects.filter(role='Manager', group__icontains=request.user.name, is_deleted=True).order_by('-id')
        else:
            list = SiteUser.objects.filter(role='Manager', admin__icontains=request.user.name, is_deleted=True).order_by('-id')



        # list = SiteUser.objects.filter(group__icontains=request.user.name,role='Manager', is_deleted=True).order_by('-id')

        context = {
            'manager_list': list,
            'deleted': True,
        }
    else:
        if request.user.role == 'Super Admin':
            list = SiteUser.objects.filter(role='Manager', group__icontains=request.user.name, is_deleted=False).order_by('-id')
        else:
            list = SiteUser.objects.filter(role='Manager', admin__icontains=request.user.name, is_deleted=False).order_by('-id')
        # list = SiteUser.objects.filter(group__icontains=request.user.name,role='Manager', is_deleted=False)

        context = {
            'manager_list': list

        }

    return render(request, 'AJAX/load_deleted_manager.html', context)



def ess_all_user(request):
    list = SiteUser.objects.all()
    if request.user.role=='Super Admin':
        list = SiteUser.objects.filter(is_deleted=False,)
    elif request.user.role == 'Admin':
        list = SiteUser.objects.filter(is_deleted=False,admin__icontains=request.user.name,)
    elif request.user.role == 'Manager':
        list = SiteUser.objects.filter(is_deleted=False,manager__icontains=request.user.name,)


    context={
        'list': list,

    }
    return render(request,'dashboardnew/ess_all_user.html',context)

def employee_profile(request,id):
    valid_user=False
    valid_Manager=False
    user_id = SiteUser.objects.get(id=id)
    valid_group = user_id.group



    if user_id.manager == SiteUser.objects.get(id=request.user.pk).name:
        valid_Manager = True
    if user_id.admin == SiteUser.objects.get(id=request.user.pk).name:
        valid_user = True

    # for item in x:
    #     name = SiteUser.objects.filter(name=item)
    #     for i in name:
    #         if i.role == 'Admin':
    #             valid_user=True
    # for item in x:
    #     name = SiteUser.objects.filter(name=item)
    #     for i in name:
    #         if i.role == 'Manager':
    #             valid_Manager = True



    leave_list = Employee_Leave.objects.filter(user_id=id)
    context={}
    mon = datetime.now().month

    feeback = Feedback.objects.filter(user_id=user_id)

    rep_feedback = Repairing_Feedback.objects.filter(user_id=user_id)
    onsite_rep_feedback = Onsite_Feedback.objects.filter(user_id=user_id)

    amc_feedback = AMC_Feedback.objects.filter(user_id=user_id)

    context3={
        'feeback': feeback,
        'rep_feedback': rep_feedback,
        'onsite_rep_feedback': onsite_rep_feedback,
        'amc_feedback': amc_feedback,
    }
    context.update(context3)

    if Employee_Analysis_month.objects.filter(user_id=id,entry_date__month=mon).count()>0:
        this_month_target = Employee_Analysis_month.objects.get(user_id=id,entry_date__month=mon)

        context4 = {
            'user_id': user_id,
            'leave_list': leave_list,
            'this_month_target': this_month_target,
            'valid_user': valid_user,
            'valid_Manager': valid_Manager,
        }
        context.update(context4)
        emp_of_month_list = Employee_Analysis_month.objects.filter(Q(user_id=SiteUser.objects.get(id=request.user.pk)))
        context2 = {
            'user_id': user_id,
            'leave_list': leave_list,
            'emp_of_month_list': emp_of_month_list,

        }
        context.update(context2)
    else:
        context = {
            'user_id': user_id,
            'leave_list': leave_list,
            'valid_user': valid_user,
            'valid_Manager': valid_Manager,
        }
        emp_of_month_list = Employee_Analysis_month.objects.filter(Q(user_id=SiteUser.objects.get(id=request.user.pk)))
        context2 = {
            'user_id': user_id,
            'leave_list': leave_list,
            'emp_of_month_list': emp_of_month_list,

        }
        context.update(context2)
    if request.method == 'POST' and 'submit2' in request.POST:
        salary_date = request.POST.get('salary_date')
        salary_date = datetime.strptime(salary_date, "%Y-%m-%d")
        salary_date = salary_date.month
        salary_date2 = calendar.month_name[salary_date]

        if Employee_Analysis_month.objects.filter(user_id=id,entry_date__month=salary_date).count()>0:
            salary_slip = Employee_Analysis_month.objects.get(user_id=id,entry_date__month=salary_date).salary_slip
            context2 = {
                'user_id': user_id,
                'leave_list': leave_list,
                'salary_slip': salary_slip,
                'salary_date': salary_date2,
            }
            context.update(context2)
        else:
            pass


    elif request.method == 'POST'  and 'submit1' in request.POST:
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        name = request.POST.get('name')
        bank_name = request.POST.get('bank_name')
        account_no = request.POST.get('account_no')
        branch_name = request.POST.get('branch_name')
        ifsc_code = request.POST.get('ifsc_code')
        photo = request.FILES.get('photo')

        item = user_id

        item.mobile = mobile
        item.email = email
        item.profile_name = name
        item.bank_name = bank_name
        item.account_number = account_no
        item.branch_name = branch_name
        item.ifsc_code = ifsc_code
        item.photo = photo

        item.save(update_fields=['mobile','email', 'profile_name','bank_name','account_number','branch_name','ifsc_code','photo'])
        return redirect('/employee_profile/' + str(id))

    elif request.method == 'POST' and 'submit3'  in request.POST:
        type = request.POST.get('type')
        content = request.POST.get('content')

        item = Defects_Warning()

        item.user_id = user_id
        item.type = type
        item.content = content
        item.save()
        return redirect('/employee_profile/' + str(id))


    elif request.method == 'POST' and 'submit4'  in request.POST:
        if Employee_Analysis_month.objects.filter(Q(entry_date__month=datetime.now().month),
                                                  Q(user_id=id)).count() > 0:
            sales_target_given = request.POST.get('sales_target_given')
            reparing_target_given = request.POST.get('reparing_target_given')
            onsitereparing_target_given = request.POST.get('onsitereparing_target_given')
            restamping_target_given = request.POST.get('restamping_target_given')

            item3 = Employee_Analysis_month.objects.get(user_id=id, entry_date__month=datetime.now().month)

            item3.sales_target_given = float(sales_target_given)
            item3.reparing_target_given = reparing_target_given
            item3.onsitereparing_target_given = onsitereparing_target_given
            item3.restamping_target_given = restamping_target_given
            item3.save(update_fields=['sales_target_given', 'reparing_target_given','onsitereparing_target_given','restamping_target_given'])
        else:

            sales_target_given = request.POST.get('sales_target_given')
            reparing_target_given = request.POST.get('reparing_target_given')
            onsitereparing_target_given = request.POST.get('onsitereparing_target_given')
            restamping_target_given = request.POST.get('restamping_target_given')

            item3 = Employee_Analysis_month()

            item3.user_id = user_id
            item3.sales_target_given = sales_target_given
            item3.reparing_target_given = reparing_target_given
            item3.onsitereparing_target_given = onsitereparing_target_given
            item3.restamping_target_given = restamping_target_given

            item3.save()
        return redirect('/employee_profile/' + str(id))



    elif request.method == 'POST' and 'submit5' in request.POST:
        selected_list = request.POST.getlist('checks[]')
        if Employee_Analysis_month.objects.filter(Q(entry_date__month=datetime.now().month),
                                                  Q(user_id=id)).count() > 0:
            employee_analysis_id = Employee_Analysis_month.objects.get(user_id=id,
                                                                       entry_date__month=datetime.now().month)
            item2 = employee_analysis_id
            item2.is_employee_of_month = True

            item2.save(update_fields=['is_employee_of_month', ])
        else:
            item2 = Employee_Analysis_month()
            item2.user_id = user_id
            item2.is_employee_of_month = True

            item2.save()

        emp_of_month_list =  Employee_Analysis_month.objects.filter(Q(user_id=SiteUser.objects.get(id=request.user.pk)))
        context2 = {
            'user_id': user_id,
            'leave_list': leave_list,
            'emp_of_month_list': emp_of_month_list,

        }
        context.update(context2)


    elif request.method == 'POST' or request.method =='FILES' and 'submit6' in request.POST:
        upload_slip = request.FILES.get('upload_slip')
        salary_date = request.POST.get('salary_date')
        salary_date = datetime.strptime(salary_date, "%Y-%m-%d")
        salary_date = salary_date.month
        if Employee_Analysis_month.objects.filter(user_id=id, entry_date__month=salary_date).count() > 0:

            slip = Employee_Analysis_month.objects.get(user_id=id,entry_date__month=salary_date)

            slip.salary_slip = upload_slip
            slip.save(update_fields=['salary_slip',])
            return HttpResponse('Salary Slip Updated!!!')
        else:
            new_slip= Employee_Analysis_month()
            new_slip.salary_slip = upload_slip
            new_slip.save()
            return HttpResponse('Salary Slip Uploaded!!!')


    return render(request,'dashboardnew/employee_profile.html',context)

