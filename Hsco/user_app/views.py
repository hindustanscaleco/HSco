import json

import requests
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.db import connection
from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.views.generic import FormView
from Hsco import settings
from django.contrib.auth.decorators import login_required

from .forms import SiteUser_Form, LoginForm, Password_reset_Form
from .models import SiteUser
import secrets
import string
from datetime import datetime, timedelta

from lead_management.models import Auto_followup_details, Lead

from lead_management.utils import send_html_mail



class LoginView(FormView):

    form_class = LoginForm
    template_name = 'auth/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('/dashboard/')
        else:
            request = self.request
            form = LoginForm(request.POST or None)
            if request.session.has_key('registered_mobile'):
                print('fdsjk')
                print('fdsjk')
                print('fdsjk')
                mobile = request.session['registered_mobile']
                password = request.session['user_password']

                user = authenticate(request, mobile=mobile, password=password)
                if user is not None:
                    login(request, user)
                    request.session['registered_mobile'] = mobile
                    request.session['user_password'] = password

                    return redirect('/dashboard/')
            return render(request, self.template_name, {'form': form})

    def form_valid(self, form):
        request = self.request

        if request.session.has_key('registered_mobile'):
            mobile = request.session['registered_mobile']
            password = request.session['user_password']
            user = authenticate(request, mobile=mobile, password=password)
            if user is not None:
                login(request, user)
                request.session['registered_mobile'] = mobile
                request.session['user_password'] = password
                next = request.GET.get('next', '/dashboard/')

                if not is_safe_url(next,allowed_hosts=None):
                    next = '/dashboard/'
                return redirect(next)
        else:
            employee_number = form.cleaned_data.get('mobile')
            password = form.cleaned_data.get('password')
            # try:
            #     mobile=SiteUser.objects.get(employee_number=employee_number).mobile
            #     user = authenticate(request, mobile=mobile, password=password)
            #     if user is not None:
            #         login(request, user)
            #         request.session['registered_mobile'] = mobile
            #         request.session['user_password'] = password
            #         registered_mobile = request.session['registered_mobile']
            #         print(request.session['user_password'])
            #
            #         return redirect('/dashboard/')
            #
            # except:
            #     pass

            # mobile = SiteUser.objects.get(employee_number=employee_number).mobile
            user = authenticate(request, mobile=employee_number, password=password)
            if user is not None:
                login(request, user)
                request.session['registered_mobile'] = employee_number
                request.session['user_password'] = password
                registered_mobile = request.session['registered_mobile']
                print(request.session['user_password'])

                return redirect('/dashboard/')

            # print("NormalOGIN"+str(user))


        return super(LoginView, self).form_invalid(form)

def logout_page(request):
    logout(request)
    try:
        del request.session['registered_mobile']
        del request.session['user_password']
    except:
        pass
    return redirect('/')


def admin_list(request):

    admin_list = SiteUser.objects.filter(role='Admin',is_deleted=False)
    context={
        'admin_list':admin_list,
    }
    return render(request,"auth/admin_list.html",context)

def create_admin(request):
    form = SiteUser_Form(request.POST or None, request.FILES or None)
    group = SiteUser.objects.get(id=request.user.pk).name
    group2 = SiteUser.objects.get(id=request.user.pk).group
    if request.method == 'POST' or request.method == 'FILES':
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        name = request.POST.get('name')
        # group = request.POST.get('group')
        is_deleted = False
        modules_assigned = request.POST.getlist('checks[]')
        date_of_joining = request.POST.get('date_of_joining')
        bank_name = request.POST.get('bank_name')
        account_no = request.POST.get('account_no')
        branch_name = request.POST.get('branch_name')
        ifsc_code = request.POST.get('ifsc_code')
        employee_number = request.POST.get('employee_number')
        photo = request.FILES.get('photo')
        upload_pancard = request.FILES.get('upload_pancard')
        upload_aadhar_card = request.FILES.get('upload_aadhar_card')
        salary_slip = request.FILES.get('salary_slip')

        item=SiteUser()


        item.mobile = mobile
        item.email = email
        item.name = name
        item.profile_name = name
        item.role = 'Admin'
        item.group = "'" + group + "'," + group2
        item.is_deleted = is_deleted
        item.modules_assigned = modules_assigned
        item.date_of_joining = date_of_joining
        item.bank_name = bank_name
        item.account_number = account_no
        item.employee_number = employee_number
        item.branch_name = branch_name
        item.ifsc_code = ifsc_code
        item.photo = photo
        item.salary_slip = salary_slip
        item.upload_pancard = upload_pancard
        item.upload_aadhar_card = upload_aadhar_card
        item.password_text = request.POST.get('password')
        item.super_admin = SiteUser.objects.get(role='Super Admin').name
        item.set_password(request.POST.get('password'))


        item.save()
        return redirect('/admin_list/')
    context={
        'form':form,
        'group': "'" + group + "'," + group2,
    }
    return render(request,"auth/create_admin.html",context)


def manager_list(request):
    if request.user.role=='Super Admin':
        manager_list = SiteUser.objects.filter(role='Manager',group__icontains=request.user.name,is_deleted=False)
    else:
        manager_list = SiteUser.objects.filter(role='Manager', admin__icontains=request.user.name, is_deleted=False)
    context={
        'manager_list':manager_list,
    }
    return render(request,"auth/manager_list.html",context)


def create_manager(request):
    form = SiteUser_Form(request.POST or None, request.FILES or None)
    if request.user.role == 'Manager' or request.user.role == 'Admin':
        group = SiteUser.objects.get(id=request.user.pk).name
    else:
        group=''
    group2 = SiteUser.objects.get(id=request.user.pk).group[:-1]
    admin_list = SiteUser.objects.filter(role='Admin', is_deleted=False)
    if request.method == 'POST' or request.method == 'FILES':
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        name = request.POST.get('name')
        # group = request.POST.get('group')
        admin = request.POST.get('admin')
        is_deleted = False
        modules_assigned = request.POST.getlist('checks[]')
        date_of_joining = request.POST.get('date_of_joining')
        bank_name = request.POST.get('bank_name')
        account_no = request.POST.get('account_no')
        employee_number = request.POST.get('employee_number')
        branch_name = request.POST.get('branch_name')
        ifsc_code = request.POST.get('ifsc_code')
        photo = request.FILES.get('photo')
        salary_slip = request.FILES.get('salary_slip')
        upload_pancard = request.FILES.get('upload_pancard')
        upload_aadhar_card = request.FILES.get('upload_aadhar_card')
        item = SiteUser()

        item.mobile = mobile
        item.email = email
        item.name = name
        item.profile_name = name
        item.role = 'Manager'

        if request.user.role == 'Super Admin':
            if admin == '' or admin == None or admin =='---------':
                item.group = "'" + group + "'," + group2
            else:
                item.group = "'"+group+"',"+group2+",'"+admin+"'"
                item.admin = admin
        elif request.user.role == 'Admin':
            item.group = "'" + group + "'," + group2
            item.admin = admin

        item.is_deleted = is_deleted
        item.modules_assigned = modules_assigned
        if date_of_joining != '' and date_of_joining != None:
            item.date_of_joining = date_of_joining
        item.bank_name = bank_name
        item.account_number = account_no
        item.branch_name = branch_name
        item.ifsc_code = ifsc_code
        item.employee_number = employee_number
        item.photo = photo
        item.salary_slip = salary_slip
        item.password_text = request.POST.get('password')
        item.super_admin = SiteUser.objects.get(role='Super Admin').name
        # if admin != '---------':
        #     item.admin = admin
        item.upload_pancard = upload_pancard
        item.upload_aadhar_card = upload_aadhar_card

        item.set_password(request.POST.get('password'))


        item.save()
        return redirect('/manager_list/')


    context = {
        'form': form,
        'admin_list': admin_list,
        'group': "'"+group+"',"+group2,
    }
    return render(request, "auth/create_manager.html", context)


def employee_list(request):
    if request.user.role == 'Super Admin':
        employee_list = SiteUser.objects.filter(role='Employee',group__icontains=request.user.name,is_deleted=False)
    elif request.user.role == 'Admin':
        employee_list = SiteUser.objects.filter(role='Employee', admin__icontains=request.user.name, is_deleted=False)
    elif request.user.role == 'Manager':
        employee_list = SiteUser.objects.filter(role='Employee', manager__icontains=request.user.name, is_deleted=False)
    context = {
        'employee_list': employee_list,
    }
    return render(request,"auth/employee_list.html",context)


def create_employee(request):
    form = SiteUser_Form(request.POST or None, request.FILES or None)
    group = SiteUser.objects.get(id=request.user.pk).name
    group2 = SiteUser.objects.get(id=request.user.pk).group
    is_admin = False

    admin_logged = None
    manager_logged = None
    manager_list=None
    if SiteUser.objects.get(id=request.user.pk).role =='Admin':
        admin_logged = SiteUser.objects.get(id=request.user.pk).name
        manager_list = SiteUser.objects.filter(role='Manager', admin__icontains=request.user.name, is_deleted=False)
        is_admin = True

    elif SiteUser.objects.get(id=request.user.pk).role =='Manager':
        manager_logged = SiteUser.objects.get(id=request.user.pk).name
        admin_logged = SiteUser.objects.get(id=request.user.pk, is_deleted=False).admin
        is_admin = False


    if request.method == 'POST' or request.method == 'FILES':
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        name = request.POST.get('name')
        group = request.POST.get('group')
        admin = request.POST.get('admin')
        manager = request.POST.get('manager')
        is_deleted = False
        modules_assigned = request.POST.getlist('checks[]')
        date_of_joining = request.POST.get('date_of_joining')
        employee_number = request.POST.get('employee_number')
        bank_name = request.POST.get('bank_name')
        account_no = request.POST.get('account_no')
        branch_name = request.POST.get('branch_name')
        ifsc_code = request.POST.get('ifsc_code')
        photo = request.FILES.get('photo')
        salary_slip = request.FILES.get('salary_slip')
        upload_pancard = request.FILES.get('upload_pancard')
        upload_aadhar_card = request.FILES.get('upload_aadhar_card')
        item = SiteUser()

        item.mobile = mobile
        item.email = email
        item.name = name
        item.profile_name = name
        item.role = 'Employee'
        # item.group = group
        item.is_deleted = is_deleted
        item.modules_assigned = modules_assigned
        if date_of_joining != '':
            item.date_of_joining = date_of_joining
        item.bank_name = bank_name
        item.account_number = account_no
        item.branch_name = branch_name
        item.employee_number = employee_number
        item.ifsc_code = ifsc_code
        item.photo = photo
        item.salary_slip = salary_slip
        item.super_admin = SiteUser.objects.get(role='Super Admin').name
        item.admin = admin
        item.upload_pancard = upload_pancard
        item.upload_aadhar_card = upload_aadhar_card
        if is_admin:

            if manager == '' or manager == None or manager == '---------':
                item.group = group
            else:
                item.group = group+ "'" + manager + "'"
                item.manager = manager
        else:
            item.group = group
            item.manager = manager

        item.password_text = request.POST.get('password')
        item.set_password(request.POST.get('password'))

        item.save()
        return redirect('/employee_list/')
    context = {
        'admin_logged': admin_logged,
        'manager_logged': manager_logged,
        'form': form,
        'manager_list': manager_list,
        'group': "'" + group + "'," + group2,
    }
    return render(request,"auth/create_employee.html",context)



def assign_man_to_admin(request):
    admin_list = SiteUser.objects.filter(role='Admin',is_deleted=False)
    manager_list = SiteUser.objects.filter(role='Manager',is_deleted=False)
    if request.method=='POST':
        group = request.POST.get('group')
        manager_id = request.POST.get('manager_id')

        item = SiteUser.objects.get(id=manager_id)
        # old_group=item.group
        # item.group = "'"+group+"'"+old_group
        item.group=group+SiteUser.objects.get(role='Super Admin')

        item.save(update_fields=['group',])
    print(admin_list)
    context = {
        'admin_list': admin_list,
        'manager_list': manager_list,
    }
    return render(request,"auth/assign_man_to_admin.html",context)


def assign_emp_to_manager(request):
    employee_list = SiteUser.objects.filter(role='Employee',is_deleted=False)
    manager_list = None
    if request.user.role == 'Admin':
        manager_list = SiteUser.objects.filter(role='Manager',admin__icontains=request.user.name,is_deleted=False)
    # elif request.user.role == 'Manager':
    #     manager_list = SiteUser.objects.filter(pk='Manager', is_deleted=False)

    if request.method=='POST':
        group = request.POST.get('group')
        employee_id = request.POST.get('employee_id')

        item = SiteUser.objects.get(id=employee_id)
        item.group=group+SiteUser.objects.get(role='Super Admin')
        # old_group = item.group
        # item.group = group + old_group
        item.save(update_fields=['group',])
    context = {
        'employee_list': employee_list,
        'manager_list': manager_list,
    }
    return render(request,"auth/assign_emp_to_manager.html",context)



def assign_module_to_emp(request):

    employee_list = SiteUser.objects.filter(role='Employee',manager__icontains=request.user.name,is_deleted=False)
    if request.method=='POST':
        employee_id = request.POST.get('employee_id')
        selected_list = request.POST.getlist('checks[]')

        item = SiteUser.objects.get(id=employee_id)

        print(selected_list)

        item.modules_assigned = selected_list
        item.save(update_fields=['modules_assigned',])

    context={
        'employee_list':employee_list,
    }
    return render(request,"auth/assign_module_to_emp.html",context)

def home(request):
    return render(request,"dashboardnew/dash.html",)

def user_profile(request):

    return render(request,"dashboardnew/userprofile.html",)

def user_logs(request):
    return render(request,"dashboardnew/logs.html")


def amc_form(request):
    return render(request,"forms/amc_form.html",)

def dis_mod_form(request):
    return render(request,"forms/dis_mod_form.html",)

def ess_form(request):
    return render(request,"forms/ess_form.html",)

def onsite_rep_form(request):
    return render(request,"forms/onsite_rep_form.html",)

def rep_mod_form(request):
    return render(request,"forms/rep_mod_form.html",)

def restamping_form(request):
    return render(request,"forms/restamping_form.html",)

def sidebar(request):
    return render(request,"base_templates/sidebar.html",)

def navbar(request):
    return render(request,"base_templates/navbar_for_dashboard.html",)



def dashboard(request):
    todays_date = datetime.now().date()


    afd=Auto_followup_details.objects.filter(followup_date=todays_date)

    for item in afd:

        if (item.follow_up_history.is_email):

            send_html_mail(item.follow_up_history.email_subject, item.follow_up_history.html_content, settings.EMAIL_HOST_USER, [item.follow_up_history.follow_up_section.lead_id.customer_id.customer_email_id, ])


        if (item.follow_up_history.is_sms):

            url = "http://smshorizon.co.in/api/sendsms.php?user=" + settings.user + "&apikey=" + settings.api + "&mobile=" + item.follow_up_history.follow_up_section.lead_id.customer_id.contact_no + "&message=" + item.follow_up_history.sms_msg + "&senderid=" + settings.senderid + "&type=txt"
            payload = ""
            headers = {'content-type': 'application/x-www-form-urlencoded'}
            response = requests.request("GET", url, data=json.dumps(payload), headers=headers)

        end_date = todays_date + timedelta(days=2)
        Auto_followup_details.objects.filter(id=item.id).update(followup_date=end_date,no_of_times_fdone=F('no_of_times_fdone')+1)
        Lead.objects.filter(id=item.follow_up_history.follow_up_section.lead_id).update(no_of_times_followup_done=F('no_of_times_followup_done')+1)






    return render(request,"dashboardnew/dashboard.html",)

def graph(request):
    return render(request,"graphs/sales_graph.html",)


def update_admin(request,id):
    admin_id = SiteUser.objects.get(id=id)
    form = SiteUser_Form(request.POST or None)
    if request.method == 'POST' or request.method == 'FILES':
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        name = request.POST.get('name')
        group = request.POST.get('group')
        is_deleted = request.POST.get('is_deleted')
        modules_assigned = request.POST.getlist('checks[]')
        employee_number = request.POST.get('employee_number')
        bank_name = request.POST.get('bank_name')
        account_no = request.POST.get('account_no')
        branch_name = request.POST.get('branch_name')
        ifsc_code = request.POST.get('ifsc_code')
        photo = request.FILES.get('photo')
        salary_slip = request.FILES.get('salary_slip')
        upload_pancard = request.FILES.get('upload_pancard')
        upload_aadhar_card = request.FILES.get('upload_aadhar_card')
        if is_deleted == 'on':
            is_deleted = True
        else:
            is_deleted = False
        item = admin_id

        item.mobile = mobile
        item.email = email
        item.profile_name = name
        item.role = 'Admin'
        item.group = group
        item.is_deleted = is_deleted
        item.modules_assigned = modules_assigned
        item.bank_name = bank_name
        item.account_number = account_no
        item.employee_number = employee_number
        item.branch_name = branch_name
        item.ifsc_code = ifsc_code
        item.photo = photo
        item.salary_slip = salary_slip
        item.password_text = request.POST.get('password')
        item.upload_pancard = upload_pancard
        item.upload_aadhar_card = upload_aadhar_card
        item.set_password(request.POST.get('password'))

        item.save(update_fields=['upload_pancard','upload_aadhar_card','password_text','employee_number','mobile','email', 'profile_name','role','group','is_deleted','modules_assigned','bank_name','account_number','branch_name','ifsc_code','photo','password'])
        return redirect('/admin_list/')
    context = {
        'form': form,
        'admin_id': admin_id,
    }
    return render(request,"update_forms/update_admin.html",context)


def update_manager(request,id):
    manager_id = SiteUser.objects.get(id=id)
    admin = SiteUser.objects.get(id=id).admin
    admin_id = SiteUser.objects.get(name=admin)
    form = SiteUser_Form(request.POST or None)
    if request.method == 'POST' or request.method == 'FILES':
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        name = request.POST.get('name')
        group = request.POST.get('group')
        is_deleted = request.POST.get('is_deleted')
        employee_number = request.POST.get('employee_number')
        modules_assigned = request.POST.getlist('checks[]')
        bank_name = request.POST.get('bank_name')
        account_no = request.POST.get('account_no')
        branch_name = request.POST.get('branch_name')
        ifsc_code = request.POST.get('ifsc_code')
        photo = request.FILES.get('photo')
        salary_slip = request.FILES.get('salary_slip')
        upload_pancard = request.FILES.get('upload_pancard')
        upload_aadhar_card = request.FILES.get('upload_aadhar_card')
        if is_deleted == 'on':
            is_deleted = True
        else:
            is_deleted = False
        item = manager_id

        item.mobile = mobile
        item.email = email
        item.profile_name = name
        item.role = 'Manager'
        item.group = group
        item.employee_number = employee_number
        item.is_deleted = is_deleted
        item.modules_assigned = modules_assigned
        item.bank_name = bank_name
        item.account_number = account_no
        item.branch_name = branch_name
        item.ifsc_code = ifsc_code
        item.photo = photo
        item.salary_slip = salary_slip
        item.password_text = request.POST.get('password')
        item.set_password(request.POST.get('password'))
        item.upload_pancard = upload_pancard
        item.upload_aadhar_card = upload_aadhar_card
        item.save(update_fields=['upload_pancard','upload_aadhar_card','password_text','employee_number','mobile','email', 'profile_name','role','group','is_deleted','modules_assigned','bank_name','account_number','branch_name','ifsc_code','photo','password'])
        return redirect('/manager_list/')
    context = {
        'form': form,
        'manager_id': manager_id,
        'admin_id': admin_id,
    }
    return render(request,"update_forms/update_manager_add.html",context)

def update_employee(request,id):
    employee_id = SiteUser.objects.get(id=id)
    manager = SiteUser.objects.get(id=id).manager
    manager_id = SiteUser.objects.get(name=manager)
    form = SiteUser_Form(request.POST or None)
    if request.method == 'POST' or request.method == 'FILES':
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        name = request.POST.get('name')
        group = request.POST.get('group')
        is_deleted = request.POST.get('is_deleted')
        modules_assigned = request.POST.getlist('checks[]')
        bank_name = request.POST.get('bank_name')
        account_no = request.POST.get('account_no')
        branch_name = request.POST.get('branch_name')
        employee_number = request.POST.get('employee_number')
        ifsc_code = request.POST.get('ifsc_code')
        photo = request.POST.get('photo')
        salary_slip = request.FILES.get('salary_slip')
        upload_pancard = request.FILES.get('upload_pancard')
        upload_aadhar_card = request.FILES.get('upload_aadhar_card')
        if is_deleted == 'on':
            is_deleted = True
        else:
            is_deleted = False
        item = employee_id

        item.mobile = mobile
        item.email = email
        item.profile_name = name
        item.role = 'Employee'
        item.group = group
        item.employee_number = employee_number
        item.is_deleted = is_deleted
        item.modules_assigned = modules_assigned
        item.bank_name = bank_name
        item.account_number = account_no
        item.branch_name = branch_name
        item.ifsc_code = ifsc_code
        item.photo = photo
        item.salary_slip = salary_slip
        item.password_text = request.POST.get('password')
        item.set_password(request.POST.get('password'))
        item.upload_pancard = upload_pancard
        item.upload_aadhar_card = upload_aadhar_card
        item.save(update_fields=['upload_pancard','upload_aadhar_card','password_text','mobile','email','employee_number', 'profile_name','role','group','is_deleted','modules_assigned','bank_name','account_number','branch_name','ifsc_code','photo','password'])
        return redirect('/employee_list/')
    context = {
        'form': form,
        'employee_id': employee_id,
        'manager_id': manager_id,
    }
    return render(request,"update_forms/update_employee.html",context)


def forgotpassword(request):
    form = Password_reset_Form(request.POST or None)

    if request.method == 'POST':
        email = request.POST.get('email')


        alphabet = string.ascii_letters + string.digits
        password = ''.join(secrets.choice(alphabet) for i in range(8))


        user = SiteUser.objects.get(email=email)
        user.set_password(password)
        user.save(update_fields=['password'])

        send_mail('HSCO: Your Password has been reset successfully!!!','New Password: '+password  , settings.EMAIL_HOST_USER,[email])
        return HttpResponse('Password has been reset successfully!!!')

    context = {
        'form': form
    }
    return render(request, 'auth/forgot_password.html', context)


def load_modules(request):
    item_name=request.GET.get('item_name')
    print(item_name)
    reparing_true = False

    valid_modules = SiteUser.objects.get(name=item_name)
    valid_modules_list = SiteUser.objects.get(name=item_name).modules_assigned
    print(valid_modules_list)

    valid_modules_list = valid_modules_list.strip('][').split(',')
    for item in valid_modules_list:

        if item == "'Repairing Module'":
            reparing_true=True


    context={
        'valid_modules':valid_modules,
        'reparing_true':reparing_true
    }
    return render(request, 'AJAX/load_modules.html', context)



































