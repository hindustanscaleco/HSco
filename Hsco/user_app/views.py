import json

import requests
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail, get_connection, EmailMessage
from django.db import connection
from django.db.models import F, Sum, Avg
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
from django.contrib import messages

from lead_management.models import Auto_followup_details, Lead

from lead_management.utils import send_html_mail,send_text_mail

from lead_management.email_content import user

from purchase_app.models import Purchase_Details, Feedback

host_file = 'webmail.hindustanscale.com'

class LoginView(FormView):

    form_class = LoginForm
    template_name = 'auth/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            next = request.GET.get('next', '/dashboard/')

            if next!= None:

                if not is_safe_url(next, allowed_hosts=None):
                    next = '/dashboard/'
                return redirect(next)
            else:
                return redirect('/dashboard/')
        else:
            request = self.request
            form = LoginForm(request.POST or None)
            if request.session.has_key('registered_mobile'):

                mobile = request.session['registered_mobile']
                password = request.session['user_password']
                latitude = request.session['latitude']
                longitude = request.session['longitude']
                user = authenticate(request, employee_number=mobile, password=password)
                if user is not None and user.role !="Super Admin" and user.is_active and not user.is_deleted:
                    login(request, user)
                    request.session['registered_mobile'] = mobile
                    request.session['user_password'] = password

                    dev_fam = request.user_agent.device.family
                    os_fam = request.user_agent.os.family
                    browser_fam = request.user_agent.browser.family
                    is_mobile = request.user_agent.is_mobile


                    msg = '''New System User is Login to HSCo System User ID - ''' + str(
                        mobile) + ', Name - ' + str(request.user.profile_name) + '''\n
                                        User login via Mobile: ''' + str(is_mobile) + '''\n
                                        OS Used : ''' + str(os_fam) + '''\n
                                        Browser Used : ''' + str(browser_fam) + '''\n
                                        Device Used : ''' + str(dev_fam) + '''\n
                                        Location of the User : ''' + str(latitude) + ''' , ''' + str(longitude) + '''\n
                                                '''

                    url = "http://smshorizon.co.in/api/sendsms.php?user=" + settings.user + "&apikey=" + settings.api + "&mobile=" + SiteUser.objects.get(
                        role='Super Admin').login_sms_number + "&message=" + msg + "&senderid=" + settings.senderid + "&type=txt&tid=1207162079781332773"
                    payload = ""
                    headers = {'content-type': 'application/x-www-form-urlencoded'}

                    try:
                        response = requests.request("GET", url, data=json.dumps(payload), headers=headers)
                        x = response.text
                        print(x)
                        print('login sms send!!45')
                    except Exception as e:
                        print('login sms not send')
                        print(e)

                    return redirect('/dashboard/')
                elif user is not None and user.role =="Super Admin":
                    login(request, user)
                    request.session['registered_mobile'] = mobile
                    request.session['user_password'] = password

                    dev_fam = request.user_agent.device.family
                    os_fam = request.user_agent.os.family
                    browser_fam = request.user_agent.browser.family
                    is_mobile = request.user_agent.is_mobile



                    msg = '''New System User is Login to HSCo System User ID - ''' + str(
                        mobile) + ', Name - ' + str(request.user.profile_name) + '''\n
                                                            User login via Mobile: ''' + str(is_mobile) + '''\n
                                                            OS Used : ''' + str(os_fam) + '''\n
                                                            Browser Used : ''' + str(browser_fam) + '''\n
                                                            Device Used : ''' + str(dev_fam) + '''\n
                                                            Location of the User : ''' + str(
                        latitude) + ''' , ''' + str(longitude) + '''\n
                                                                    '''

                    url = "http://smshorizon.co.in/api/sendsms.php?user=" + settings.user + "&apikey=" + settings.api + "&mobile=" + SiteUser.objects.get(
                        role='Super Admin').login_sms_number + "&message=" + msg + "&senderid=" + settings.senderid + "&type=txt&tid=1207162079781332773"
                    payload = ""
                    headers = {'content-type': 'application/x-www-form-urlencoded'}

                    try:
                        response = requests.request("GET", url, data=json.dumps(payload), headers=headers)
                        x = response.text
                        print(x)
                        print('login sms send!!88')
                    except Exception as e:
                        print('login sms not send')
                        print(e)
                    return redirect('/dashboard/')

            return render(request, self.template_name, {'form': form})

    def form_valid(self, form):
        request = self.request

        if request.session.has_key('registered_mobile'):
            mobile = request.session['registered_mobile']
            password = request.session['user_password']
            latitude = request.session['latitude']
            longitude = request.session['longitude']

            user = authenticate(request, employee_number=mobile, password=password)
            if user is not None and user.role !="Super Admin" and user.is_active and not user.is_deleted:
                login(request, user)
                request.session['registered_mobile'] = mobile
                request.session['user_password'] = password

                next = request.GET.get('next', '/dashboard/')

                if not is_safe_url(next,allowed_hosts=None):
                    dev_fam = request.user_agent.device.family
                    os_fam = request.user_agent.os.family
                    browser_fam = request.user_agent.browser.family
                    is_mobile = request.user_agent.is_mobile



                    msg = '''New System User is Login to HSCo System User ID - ''' + str(
                        mobile) + ', Name - ' + str(request.user.profile_name) + '''\n
                                                                                User login via Mobile: ''' + str(
                        is_mobile) + '''\n
                                                                                OS Used : ''' + str(os_fam) + '''\n
                                                                                Browser Used : ''' + str(browser_fam) + '''\n
                                                                                Device Used : ''' + str(dev_fam) + '''\n
                                                                                Location of the User : ''' + str(
                        latitude) + ''' , ''' + str(longitude) + '''\n
                                                                                        '''

                    url = "http://smshorizon.co.in/api/sendsms.php?user=" + settings.user + "&apikey=" + settings.api + "&mobile=" + SiteUser.objects.get(
                        role='Super Admin').login_sms_number + "&message=" + msg + "&senderid=" + settings.senderid + "&type=txt&tid=1207162079781332773"
                    payload = ""
                    headers = {'content-type': 'application/x-www-form-urlencoded'}

                    try:
                        response = requests.request("GET", url, data=json.dumps(payload), headers=headers)
                        x = response.text
                        print(x)
                        print('login sms send!!78')
                    except Exception as e:
                        print('login sms not send')
                        print(e)
                    next = '/dashboard/'
                return redirect(next)
            elif user is not None and user.role =="Super Admin":
                login(request, user)
                request.session['registered_mobile'] = mobile
                request.session['user_password'] = password

                next = request.GET.get('next', '/dashboard/')

                if not is_safe_url(next, allowed_hosts=None):
                    dev_fam = request.user_agent.device.family
                    os_fam = request.user_agent.os.family
                    browser_fam = request.user_agent.browser.family
                    is_mobile = request.user_agent.is_mobile


                    msg = '''New System User is Login to HSCo System User ID - ''' + str(
                        mobile) + ', Name - ' + str(request.user.profile_name) + '''\n
                                                                                User login via Mobile: ''' + str(
                        is_mobile) + '''\n
                                                                                OS Used : ''' + str(os_fam) + '''\n
                                                                                Browser Used : ''' + str(browser_fam) + '''\n
                                                                                Device Used : ''' + str(dev_fam) + '''\n
                                                                                Location of the User : ''' + str(
                        latitude) + ''' , ''' + str(longitude) + '''\n
                                                                                        '''

                    url = "http://smshorizon.co.in/api/sendsms.php?user=" + settings.user + "&apikey=" + settings.api + "&mobile=" + SiteUser.objects.get(
                        role='Super Admin').login_sms_number + "&message=" + msg + "&senderid=" + settings.senderid + "&type=txt&tid=1207162079781332773"
                    payload = ""
                    headers = {'content-type': 'application/x-www-form-urlencoded'}

                    try:
                        response = requests.request("GET", url, data=json.dumps(payload), headers=headers)
                        x = response.text
                        print(x)
                        print('login sms send!!555')
                    except Exception as e:
                        print('login sms not send')
                        print(e)
                    next = '/dashboard/'
                return redirect(next)

        else:
            employee_number = form.cleaned_data.get('mobile')
            password = form.cleaned_data.get('password')
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            
            user = authenticate(request, employee_number=employee_number, password=password)
            if user is not None and user.role !="Super Admin" and user.is_active and not user.is_deleted:
                login(request, user)
                request.session['registered_mobile'] = employee_number
                request.session['user_password'] = password
                request.session['latitude'] = latitude
                request.session['longitude'] = longitude
                registered_mobile = request.session['registered_mobile']
                print(request.session['user_password'])
                next = request.GET.get('next', '/dashboard/')
                if is_safe_url(next, allowed_hosts=None):
                    dev_fam = request.user_agent.device.family
                    os_fam = request.user_agent.os.family
                    browser_fam = request.user_agent.browser.family
                    is_mobile = 'No' if request.user_agent.is_mobile == False else 'Yes'

                    msg = '''New System User is Login to HSCo System User ID - ''' + str(
                        employee_number) + ', Name - ' + str(request.user.profile_name) + '''\n
                    User login via Mobile: ''' + str(is_mobile) + '''\n
                    OS Used : ''' + str(os_fam) + '''\n
                    Browser Used : ''' + str(browser_fam) + '''\n
                    Device Used : ''' + str(dev_fam) + '''\n
                    Location of the User : ''' + str(latitude) + ''' , ''' + str(longitude) + '''\n
                            '''

                    url = "http://smshorizon.co.in/api/sendsms.php?user=" + settings.user + "&apikey=" + settings.api + "&mobile="+SiteUser.objects.get(role='Super Admin').login_sms_number+"&message=" + msg + "&senderid=" + settings.senderid + "&type=txt&tid=1207162079781332773"
                    payload = ""
                    headers = {'content-type': 'application/x-www-form-urlencoded'}
                    print(SiteUser.objects.get(id=request.user.id).is_deleted)
                    if SiteUser.objects.get(id=request.user.id).is_deleted == True:
                        messages.error(request,"Deleted user cannot be logged in !")
                        return redirect('/logout/')
                    try:
                        response = requests.request("GET", url, data=json.dumps(payload), headers=headers)
                        x = response.text
                        print(x)
                        print('login sms send!!787878')
                    except Exception as e:
                        print('login sms not send')
                        print(e)
                    next = '/dashboard/'
                return redirect(next)

                # return redirect('/dashboard/')
            elif user is not None and user.role =="Super Admin":
                login(request, user)
                request.session['registered_mobile'] = employee_number
                request.session['user_password'] = password
                request.session['latitude'] = latitude
                request.session['longitude'] = longitude
                registered_mobile = request.session['registered_mobile']
                print(request.session['user_password'])
                next = request.GET.get('next', '/dashboard/')
                if is_safe_url(next, allowed_hosts=None):
                    dev_fam = request.user_agent.device.family
                    os_fam = request.user_agent.os.family
                    browser_fam = request.user_agent.browser.family
                    is_mobile = 'No' if request.user_agent.is_mobile == False else 'Yes'

                    msg = '''New System User is Login to HSCo System User ID - ''' + str(employee_number) + ', Name - ' + str(request.user.profile_name) + '''\n
User login via Mobile: ''' + str(is_mobile) + '''\n
OS Used : ''' + str(os_fam) + '''\n
Browser Used : ''' + str(browser_fam) + '''\n
Device Used : ''' + str(dev_fam) + '''\n
Location of the User : ''' + str(latitude) + ''' , ''' + str(longitude) + '''\n
                                            '''

                    url = "http://smshorizon.co.in/api/sendsms.php?user=" + settings.user + "&apikey=" + settings.api + "&mobile=" + SiteUser.objects.get(
                        role='Super Admin').login_sms_number + "&message=" + msg + "&senderid=" + settings.senderid + "&type=txt&tid=1207162079781332773"
                    payload = ""
                    headers = {'content-type': 'application/x-www-form-urlencoded'}
                    print(SiteUser.objects.get(id=request.user.id).is_deleted)
                    if SiteUser.objects.get(id=request.user.id).is_deleted == True:
                        messages.error(request, "Deleted user cannot be logged in !")
                        return redirect('/logout/')
                    try:
                        response = requests.request("GET", url, data=json.dumps(payload), headers=headers)
                        x = response.text
                        print(x)
                        print('login sms send!!sdsd')
                    except Exception as e:
                        print('login sms not send')
                        print(e)
                    next = '/dashboard/'
                return redirect(next)

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

        aadhar_card = request.POST.get('aadhar_card')
        pancard = request.POST.get('pancard')
        professional_email = request.POST.get('professional_email')
        professional_email_password = request.POST.get('professional_email_password')
        product_master = request.POST.get('product_master')

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
        item.aadhar_card = aadhar_card
        item.pancard = pancard
        item.salary_slip = salary_slip
        item.upload_pancard = upload_pancard
        item.upload_aadhar_card = upload_aadhar_card
        item.professional_email_password = professional_email_password
        item.professional_email = professional_email
        if product_master == 'True':
            item.product_master_access = True
        elif product_master == None:
            item.product_master_access = False
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
        aadhar_card = request.POST.get('aadhar_card')
        pancard = request.POST.get('pancard')
        professional_email = request.POST.get('professional_email')
        professional_email_password = request.POST.get('professional_email_password')
        product_master = request.POST.get('product_master')
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
        item.aadhar_card = aadhar_card
        item.pancard = pancard
        item.salary_slip = salary_slip
        item.password_text = request.POST.get('password')
        item.super_admin = SiteUser.objects.get(role='Super Admin').name
        # if admin != '---------':
        #     item.admin = admin
        item.upload_pancard = upload_pancard
        item.upload_aadhar_card = upload_aadhar_card
        item.professional_email_password = professional_email_password
        item.professional_email = professional_email

        item.set_password(request.POST.get('password'))
        if product_master == 'True':
            item.product_master_access = True
        elif product_master == None:
            item.product_master_access = False

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

        aadhar_card = request.POST.get('aadhar_card')
        pancard = request.POST.get('pancard')
        professional_email = request.POST.get('professional_email')
        professional_email_password = request.POST.get('professional_email_password')
        product_master = request.POST.get('product_master')

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
        item.aadhar_card = aadhar_card
        item.pancard = pancard
        item.salary_slip = salary_slip
        item.super_admin = SiteUser.objects.get(role='Super Admin').name
        item.admin = admin
        item.upload_pancard = upload_pancard
        item.upload_aadhar_card = upload_aadhar_card
        item.professional_email_password = professional_email_password
        item.professional_email = professional_email
        if is_admin:

            if manager == '' or manager == None or manager == '---------':
                item.group = group
            else:
                item.group = group+ "'" + manager + "'"
                item.manager = manager
        else:
            item.group = group
            item.manager = manager
        if product_master == 'True':
            item.product_master_access = True
        elif product_master == None:
            item.product_master_access = False
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


@login_required(login_url='/')
def dashboard(request):
    todays_date = datetime.now().date()


    afd=Auto_followup_details.objects.filter(followup_date=todays_date)
    if afd.count()>0:
        try:
            for item in afd:

                if (item.follow_up_history.is_email):
                        if (item.follow_up_history.html_content != None and item.follow_up_history.html_content != '' and len(item.follow_up_history.html_content)>5):
                            # with get_connection(
                            #         host=host_file,
                            #         port=587,
                            #         username=item.follow_up_history.follow_up_section.lead_id.owner_of_opportunity.professional_email,
                            #         password=item.follow_up_history.follow_up_section.lead_id.owner_of_opportunity.professional_email_password,
                            #         use_tls=True
                            # ) as connection:
                            #     email_send = EmailMessage(item.follow_up_history.email_subject,
                            #                               item.follow_up_history.html_content,
                            #                               item.follow_up_history.follow_up_section.lead_id.owner_of_opportunity.professional_email
                            #                               , [item.follow_up_history.follow_up_section.lead_id.customer_id.customer_email_id, ],
                            #                               connection=connection)
                            #     # part1 = MIMEText(text, 'plain')
                            #     # part2 = MIMEText(user(request), 'html')
                            #     # email_send.attach(part1)
                            #     email_send.content_subtype = 'html'
                            #     email_send.send()
                            send_html_mail(item.follow_up_history.email_subject, item.follow_up_history.html_content, settings.EMAIL_HOST_USER, [item.follow_up_history.follow_up_section.lead_id.customer_id.customer_email_id, ],cc=[request.user.professional_email])
                        else:
                            send_text_mail(item.follow_up_history.email_subject, item.follow_up_history.email_msg,
                                           settings.EMAIL_HOST_USER, [
                                               item.follow_up_history.follow_up_section.lead_id.customer_id.customer_email_id, ],cc=[request.user.professional_email])

                            # with get_connection(
                            #         host=host_file,
                            #         port=587,
                            #         username=item.follow_up_history.follow_up_section.lead_id.owner_of_opportunity.professional_email,
                            #         password=item.follow_up_history.follow_up_section.lead_id.owner_of_opportunity.professional_email_password,
                            #         use_tls=True
                            # ) as connection:
                            #     email_send = EmailMessage(item.follow_up_history.email_subject,
                            #                               user(request, item.follow_up_history.email_msg),
                            #                               item.follow_up_history.follow_up_section.lead_id.owner_of_opportunity.professional_email,
                            #                               [item.follow_up_history.follow_up_section.lead_id.customer_id.customer_email_id, ],
                            #                               connection=connection)
                            #
                            #     email_send.content_subtype = 'html'
                            #     email_send.send()



                if (item.follow_up_history.is_sms):

                    url = "http://smshorizon.co.in/api/sendsms.php?user=" + settings.user + "&apikey=" + settings.api + "&mobile=" + item.follow_up_history.follow_up_section.lead_id.customer_id.contact_no + "&message=" + item.follow_up_history.sms_msg+'\n'+item.follow_up_history.sms_con + "&senderid=" + settings.senderid + "&type=txt"
                    payload = ""
                    headers = {'content-type': 'application/x-www-form-urlencoded'}
                    response = requests.request("GET", url, data=json.dumps(payload), headers=headers)

                end_date = todays_date + timedelta(days=2)
                Auto_followup_details.objects.filter(id=item.id).update(followup_date=end_date,no_of_times_fdone=F('no_of_times_fdone')+1)
                Lead.objects.filter(id=item.follow_up_history.follow_up_section.lead_id).update(no_of_times_followup_done=F('no_of_times_followup_done')+1)
        except Exception as e:
            messages.error(request, str(e))
    user_id = request.user.id
    feeback = Feedback.objects.filter(user_id=user_id)
    # this month sales
    knowledge_of_person = Feedback.objects.filter(user_id=user_id).aggregate(Avg('knowledge_of_person'))
    timeliness_of_person = Feedback.objects.filter(user_id=user_id).aggregate(Avg('timeliness_of_person'))
    price_of_product = Feedback.objects.filter(user_id=user_id).aggregate(Avg('price_of_product'))
    overall_interaction = Feedback.objects.filter(user_id=user_id).aggregate(Avg('overall_interaction'))

    mon = datetime.now().month

    # this_month = Employee_Analysis_date.objects.filter(user_id=user_id,entry_date__month=mon).values('entry_date',
    #                                                                                                      'total_sales_done_today').order_by('entry_date')
    if request.user.role == "Super Admin":
        this_month = Purchase_Details.objects.filter(
                                                     date_of_purchase__month=datetime.now().month,date_of_purchase__year=datetime.now().year).order_by('date_of_purchase')\
            .values('date_of_purchase').annotate(data_sum=Sum('value_of_goods'))
    else:
        this_month = Purchase_Details.objects.filter(sales_person=SiteUser.objects.get(id=request.user.id).profile_name,
            date_of_purchase__month=datetime.now().month, date_of_purchase__year=datetime.now().year).order_by('date_of_purchase')\
            .values('date_of_purchase').annotate(data_sum=Sum('value_of_goods'))
    this_lis_date = []
    this_lis_sum = []
    for i in this_month:
        x = i
        this_lis_date.append(x['date_of_purchase'].strftime('%Y-%m-%d'))
        this_lis_sum.append(x['data_sum'])

    # previous month sales
    mon = (datetime.now().month)
    if mon == 1:
        previous_mon = 12
    else:
        previous_mon = (datetime.now().month) - 1
    if request.user.role == "Super Admin":
        previous_month = Purchase_Details.objects.filter(
                                                         date_of_purchase__month=previous_mon,date_of_purchase__year=datetime.now().year).order_by('date_of_purchase')\
            .values('date_of_purchase').annotate(data_sum=Sum('value_of_goods'))
    else:
        previous_month = Purchase_Details.objects.filter(
            sales_person=SiteUser.objects.get(id=request.user.id).profile_name,
            date_of_purchase__month=previous_mon, date_of_purchase__year=datetime.now().year).order_by('date_of_purchase')\
            .values('date_of_purchase').annotate(data_sum=Sum('value_of_goods'))

    previous_lis_date = []
    previous_lis_sum = []
    for i in previous_month:
        x = i
        previous_lis_date.append(x['date_of_purchase'].strftime('%Y-%m-%d'))
        previous_lis_sum.append(x['data_sum'])

    if request.user.role == "Super Admin":
        qs = Purchase_Details.objects.filter(
                                             date_of_purchase__year=datetime.now().year).order_by('date_of_purchase').values('date_of_purchase').annotate(data_sum=Sum('value_of_goods'))
    else:
        qs = Purchase_Details.objects.filter(sales_person = SiteUser.objects.get(id=request.user.id).profile_name,
             date_of_purchase__year=datetime.now().year).order_by('date_of_purchase').values('date_of_purchase').annotate(data_sum=Sum('value_of_goods'))
    lis_date = []
    lis_sum = []
    for i in qs:
        x = i
        lis_date.append(x['date_of_purchase'].strftime('%B-%Y'))
        lis_sum.append(x['data_sum'])
    print(lis_date)
    print(lis_sum)


    if request.user.role == "Super Admin":
        smly_qs = Purchase_Details.objects.filter(
            date_of_purchase__month=datetime.now().month, date_of_purchase__year=datetime.now().year-1).order_by(
            'date_of_purchase').values('date_of_purchase').annotate(data_sum=Sum('value_of_goods'))
    else:
        smly_qs = Purchase_Details.objects.filter(sales_person=SiteUser.objects.get(id=request.user.id).profile_name,
                                             date_of_purchase__month=datetime.now().month,
                                             date_of_purchase__year=datetime.now().year-1).order_by(
            'date_of_purchase').values('date_of_purchase').annotate(data_sum=Sum('value_of_goods'))
    smly_lis_date = []
    smly_lis_sum = []
    for i in smly_qs:
        x = i
        smly_lis_date.append(x['date_of_purchase'].strftime('%Y-%m-%d'))
        smly_lis_sum.append(x['data_sum'])
    print(smly_lis_date)
    print(smly_lis_sum)
    context = {
        'final_list': lis_date,
        'final_list2': lis_sum,
        'smly_lis_date': smly_lis_date,
        'smly_lis_sum': smly_lis_sum,
        'previous_lis_date': previous_lis_date,
        'previous_lis_sum': previous_lis_sum,
        'this_lis_date': this_lis_date,
        'this_lis_sum': this_lis_sum,
        'feeback': feeback,
        'graph_name': str(datetime.now().strftime("%B"))+" "+str(datetime.now().year-1)

    }
    return render(request,"dashboardnew/dashboard.html",context)

def graph(request):
    return render(request,"graphs/sales_graph.html",)

@login_required(login_url='/')
def update_admin(request,id):
    admin_id = SiteUser.objects.get(id=id)
    form = SiteUser_Form(request.POST or None)
    if request.method == 'POST' or request.method == 'FILES':
        # if 'test_submit' in request.POST:
        #     test_professional_email = request.POST.get('test_professional_email')
        #     test_professional_email_password = request.POST.get('test_professional_email_password')
        #     test_to = request.POST.get('test_to')
        #     try:
        #         with get_connection(
        #                 host=host_file,
        #                 port=587,
        #                 username=test_professional_email,
        #                 password=test_professional_email_password,
        #                 use_tls=True
        #         ) as connection:
        #             email_send = EmailMessage('Testing Email Credentials',
        #                                       "Testing Email Credentials",
        #                                       test_professional_email,
        #                                       [test_to, ],
        #                                       connection=connection)
        #
        #             # email_send.content_subtype = 'html'
        #             email_send.send()
        #         messages.success(request,"Email Sent!!!")
        #         return redirect('/update_admin/'+str(id))
        #     except Exception as e:
        #         messages.error(request, str(e))
        #         return redirect('/update_admin/' + str(id))

        if 'mobile' in request.POST or request.method == 'FILES':
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
            aadhar_card = request.POST.get('aadhar_card')
            pancard = request.POST.get('pancard')
            professional_email = request.POST.get('professional_email')
            professional_email_password = request.POST.get('professional_email_password')

            upload_pancard = request.FILES.get('upload_pancard')
            upload_aadhar_card = request.FILES.get('upload_aadhar_card')
            product_master = request.POST.get('product_master')

            if is_deleted == 'on':
                is_deleted = True
            else:
                is_deleted = False
            item = admin_id
            # if item.professional_email_password != professional_email_password:
            #     try:
            #         with get_connection(
            #                 host=host_file,
            #                 port=587,
            #                 username=professional_email,
            #                 password=professional_email_password,
            #                 use_tls=True
            #         ) as connection:
            #             email_send = EmailMessage('Password Updated',
            #                                       "New Password :"+str(professional_email_password),
            #                                       professional_email,
            #                                       [professional_email, ],
            #                                       connection=connection)
            #
            #             # email_send.content_subtype = 'html'
            #             email_send.send()
            #         messages.success(request, "Updated Password Sent To Email: "+professional_email)
            #
            #     except Exception as e:
            #         messages.error(request, str(e))


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
            item.aadhar_card = aadhar_card
            item.pancard = pancard
            item.salary_slip = salary_slip
            item.professional_email_password = professional_email_password
            item.professional_email = professional_email
            item.password_text = request.POST.get('password')
            if product_master == 'True':
                item.product_master_access = True
            elif product_master == None:
                item.product_master_access = False
            if photo != None and photo != "":
                item.photo = photo
                item.save(update_fields=['photo', ])
            if upload_aadhar_card != None and upload_aadhar_card != "":
                item.upload_aadhar_card = upload_aadhar_card
                item.save(update_fields=['upload_aadhar_card', ])
            if upload_pancard != None and upload_pancard != "":
                item.upload_pancard = upload_pancard
                item.save(update_fields=['upload_pancard', ])

            item.set_password(request.POST.get('password'))

            item.save(update_fields=['password_text','professional_email','professional_email_password',
                                     'employee_number','mobile','email', 'profile_name','role','group','is_deleted',
                                     'modules_assigned','bank_name','account_number','branch_name','ifsc_code','password','aadhar_card','pancard','product_master_access'])
            return redirect('/admin_list/')
    context = {
        'form': form,
        'admin_id': admin_id,
    }
    return render(request,"update_forms/update_admin.html",context)

@login_required(login_url='/')
def update_manager(request,id):
    manager_id = SiteUser.objects.get(id=id)
    admin = SiteUser.objects.get(id=id).admin
    admin_id = SiteUser.objects.get(name=admin)
    form = SiteUser_Form(request.POST or None)
    if request.method == 'POST' or request.method == 'FILES':
        # if 'test_submit' in request.POST:
        #     test_professional_email = request.POST.get('test_professional_email')
        #     test_professional_email_password = request.POST.get('test_professional_email_password')
        #     test_to = request.POST.get('test_to')
        #     print(test_professional_email)
        #     print(test_professional_email_password)
        #     try:
        #         with get_connection(
        #                 host=host_file,
        #                 port=587,
        #                 username=test_professional_email,
        #                 password=test_professional_email_password,
        #                 use_tls=True
        #         ) as connection:
        #             email_send = EmailMessage('Testing Email Credentials',
        #                                       "Testing Email Credentials",
        #                                       test_professional_email,
        #                                       [test_to, ],
        #                                       connection=connection)
        #
        #             # email_send.content_subtype = 'html'
        #             email_send.send()
        #         messages.success(request, "Email Sent!!!")
        #         return redirect('/update_manager/' + str(id))
        #     except Exception as e:
        #         messages.error(request, str(e))
        #         return redirect('/update_manager/' + str(id))
        if 'mobile' in request.POST or request.method == 'FILES':
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
            aadhar_card = request.POST.get('aadhar_card')
            pancard = request.POST.get('pancard')
            professional_email = request.POST.get('professional_email')
            professional_email_password = request.POST.get('professional_email_password')
            product_master = request.POST.get('product_master')
            if is_deleted == 'on':
                is_deleted = True
            else:
                is_deleted = False
            item = manager_id
            # if item.professional_email_password != professional_email_password:
            #     try:
            #         with get_connection(
            #                 host=host_file,
            #                 port=587,
            #                 username=professional_email,
            #                 password=professional_email_password,
            #                 use_tls=True
            #         ) as connection:
            #             email_send = EmailMessage('Password Updated',
            #                                       "New Password :" + str(professional_email_password),
            #                                       professional_email,
            #                                       [professional_email, ],
            #                                       connection=connection)
            #
            #             # email_send.content_subtype = 'html'
            #             email_send.send()
            #         messages.success(request, "Updated Password Sent To Email: " + professional_email)
            #
            #     except Exception as e:
            #         messages.error(request, str(e))
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
            item.salary_slip = salary_slip
            item.pancard = pancard
            item.aadhar_card = aadhar_card
            item.professional_email_password = professional_email_password
            item.professional_email = professional_email
            item.password_text = request.POST.get('password')
            item.set_password(request.POST.get('password'))
            if photo != None and photo != "":
                item.photo = photo
                item.save(update_fields=['photo', ])
            if upload_aadhar_card != None and upload_aadhar_card != "":
                item.upload_aadhar_card = upload_aadhar_card
                item.save(update_fields=['upload_aadhar_card', ])
            if upload_pancard != None and upload_pancard != "":
                item.upload_pancard = upload_pancard
                item.save(update_fields=['upload_pancard', ])
            if product_master == 'True':
                item.product_master_access = True
            elif product_master == None:
                item.product_master_access = False
            item.save(update_fields=['product_master_access','professional_email_password','professional_email','pancard','aadhar_card','password_text','employee_number','mobile','email', 'profile_name','role','group','is_deleted','modules_assigned','bank_name','account_number','branch_name','ifsc_code','password'])
            return redirect('/manager_list/')
    context = {
        'form': form,
        'manager_id': manager_id,
        'admin_id': admin_id,
    }
    return render(request,"update_forms/update_manager_add.html",context)

@login_required(login_url='/')
def update_employee(request,id):
    employee_id = SiteUser.objects.get(id=id)
    manager = SiteUser.objects.get(id=id).manager
    manager_id = SiteUser.objects.get(name=manager)
    form = SiteUser_Form(request.POST or None)
    if request.method == 'POST' or request.method == 'FILES':
        # if 'test_submit' in request.POST:
        #     test_professional_email = request.POST.get('test_professional_email')
        #     test_professional_email_password = request.POST.get('test_professional_email_password')
        #     test_to = request.POST.get('test_to')
        #     try:
        #         with get_connection(
        #                 host=host_file,
        #                 port=587,
        #                 username=test_professional_email,
        #                 password=test_professional_email_password,
        #                 use_tls=True
        #         ) as connection:
        #             email_send = EmailMessage('Testing Email Credentials',
        #                                       "Testing Email Credentials",
        #                                       test_professional_email,
        #                                       [test_to, ],
        #                                       connection=connection)
        #
        #             # email_send.content_subtype = 'html'
        #             email_send.send()
        #         messages.success(request, "Email Sent!!!")
        #         return redirect('/update_employee/' + str(id))
        #     except Exception as e:
        #         messages.error(request, str(e))
        #         return redirect('/update_employee/' + str(id))

        if 'mobile' in request.POST or request.method == 'FILES':
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
            aadhar_card = request.POST.get('aadhar_card')
            pancard = request.POST.get('pancard')
            professional_email_password = request.POST.get('professional_email_password')
            professional_email = request.POST.get('professional_email')
            product_master = request.POST.get('product_master')
            if is_deleted == 'on':
                is_deleted = True
            else:
                is_deleted = False
            item = employee_id
            # if item.professional_email_password != professional_email_password:
            #     try:
            #         with get_connection(
            #                 host=host_file,
            #                 port=587,
            #                 username=professional_email,
            #                 password=professional_email_password,
            #                 use_tls=True
            #         ) as connection:
            #             email_send = EmailMessage('Password Updated',
            #                                       "New Password :" + str(professional_email_password),
            #                                       professional_email,
            #                                       [professional_email, ],
            #                                       connection=connection)
            #
            #             # email_send.content_subtype = 'html'
            #             email_send.send()
            #         messages.success(request, "Updated Password Sent To Email: " + professional_email)
            #
            #     except Exception as e:
            #         messages.error(request, str(e))
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
            item.salary_slip = salary_slip
            item.pancard = pancard
            item.aadhar_card = aadhar_card
            item.professional_email_password = professional_email_password
            item.professional_email = professional_email
            item.password_text = request.POST.get('password')
            item.set_password(request.POST.get('password'))
            if product_master == 'True':
                item.product_master_access = True
            elif product_master == None:
                item.product_master_access = False
            if photo != None and photo != "":
                item.photo = photo
                item.save(update_fields=['photo', ])
            if upload_aadhar_card != None and upload_aadhar_card != "":
                item.upload_aadhar_card = upload_aadhar_card
                item.save(update_fields=['upload_aadhar_card', ])
            if upload_pancard != None and upload_pancard != "":
                item.upload_pancard = upload_pancard
                item.save(update_fields=['upload_pancard', ])
            item.save(update_fields=['professional_email_password','product_master_access','professional_email','pancard','aadhar_card','password_text','mobile','email','employee_number', 'profile_name','role','group','is_deleted','modules_assigned','bank_name','account_number','branch_name','ifsc_code','password'])
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



































