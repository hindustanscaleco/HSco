from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.views.generic import FormView

from Hsco import settings
from .forms import SiteUser_Form, LoginForm, Password_reset_Form
from .models import SiteUser
import secrets
import string

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
            mobile = form.cleaned_data.get('mobile')
            password = form.cleaned_data.get('password')
            print("NormalOGIN" + str(mobile))
            print("NormalOGIN" + str(password))
            user = authenticate(request, mobile=mobile, password=password)
            # print("NormalOGIN"+str(user))
            if user is not None:
                login(request, user)
                request.session['registered_mobile'] = mobile
                request.session['user_password'] = password
                registered_mobile = request.session['registered_mobile']
                print(request.session['user_password'])

                return redirect('/dashboard/')

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

    admin_list = SiteUser.objects.filter(role='Admin')
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
        group = request.POST.get('group')
        is_deleted = request.POST.get('is_deleted')
        modules_assigned = request.POST.getlist('checks[]')
        date_of_joining = request.POST.get('date_of_joining')
        bank_name = request.POST.get('bank_name')
        account_no = request.POST.get('account_no')
        branch_name = request.POST.get('branch_name')
        ifsc_code = request.POST.get('ifsc_code')
        photo = request.FILES.get('photo')
        salary_slip = request.FILES.get('salary_slip')



        item=SiteUser()


        item.mobile = mobile
        item.email = email
        item.name = name
        item.role = 'Admin'
        item.group = group
        item.is_deleted = is_deleted
        item.modules_assigned = modules_assigned
        item.date_of_joining = date_of_joining
        item.bank_name = bank_name
        item.account_number = account_no
        item.branch_name = branch_name
        item.ifsc_code = ifsc_code
        item.photo = photo
        item.salary_slip = salary_slip
        item.set_password(request.POST.get('password'))

        item.save()
        return redirect('/admin_list/')
    context={
        'form':form,
        'group': "'" + group + "'," + group2,
    }
    return render(request,"auth/create_admin.html",context)

def manager_list(request):
    manager_list = SiteUser.objects.filter(role='Manager')
    context={
        'manager_list':manager_list,
    }
    return render(request,"auth/manager_list.html",context)

def create_manager(request):
    form = SiteUser_Form(request.POST or None, request.FILES or None)
    group = SiteUser.objects.get(id=request.user.pk).name
    group2 = SiteUser.objects.get(id=request.user.pk).group
    if request.method == 'POST' or request.method == 'FILES':
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        name = request.POST.get('name')
        group = request.POST.get('group')
        is_deleted = request.POST.get('is_deleted')
        modules_assigned = request.POST.getlist('checks[]')
        date_of_joining = request.POST.get('date_of_joining')
        bank_name = request.POST.get('bank_name')
        account_no = request.POST.get('account_no')
        branch_name = request.POST.get('branch_name')
        ifsc_code = request.POST.get('ifsc_code')
        photo = request.FILES.get('photo')
        salary_slip = request.FILES.get('salary_slip')

        item = SiteUser()

        item.mobile = mobile
        item.email = email
        item.name = name
        item.role = 'Manager'
        item.group = group
        item.is_deleted = is_deleted
        item.modules_assigned = modules_assigned
        item.date_of_joining = date_of_joining
        item.bank_name = bank_name
        item.account_number = account_no
        item.branch_name = branch_name
        item.ifsc_code = ifsc_code
        item.photo = photo
        item.salary_slip = salary_slip
        item.set_password(request.POST.get('password'))

        item.save()
        return redirect('/manager_list/')

    print(group)
    print(group2)
    print(group2)
    context = {
        'form': form,
        'group': "'"+group+"',"+group2,
    }
    return render(request, "auth/create_manager.html", context)

def employee_list(request):
    employee_list = SiteUser.objects.filter(role='Employee')
    context = {
        'employee_list': employee_list,
    }
    return render(request,"auth/employee_list.html",context)

def create_employee(request):
    form = SiteUser_Form(request.POST or None, request.FILES or None)
    group = SiteUser.objects.get(id=request.user.pk).name
    group2 = SiteUser.objects.get(id=request.user.pk).group
    if request.method == 'POST' or request.method == 'FILES':
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        name = request.POST.get('name')
        group = request.POST.get('group')
        is_deleted = request.POST.get('is_deleted')
        modules_assigned = request.POST.getlist('checks[]')
        date_of_joining = request.POST.get('date_of_joining')
        bank_name = request.POST.get('bank_name')
        account_no = request.POST.get('account_no')
        branch_name = request.POST.get('branch_name')
        ifsc_code = request.POST.get('ifsc_code')
        photo = request.FILES.get('photo')
        salary_slip = request.FILES.get('salary_slip')

        item = SiteUser()

        item.mobile = mobile
        item.email = email
        item.name = name
        item.role = 'Employee'
        item.group = group
        item.is_deleted = is_deleted
        item.modules_assigned = modules_assigned
        item.date_of_joining = date_of_joining
        item.bank_name = bank_name
        item.account_number = account_no
        item.branch_name = branch_name
        item.ifsc_code = ifsc_code
        item.photo = photo
        item.salary_slip = salary_slip
        item.set_password(request.POST.get('password'))

        item.save()
        return redirect('/employee_list/')
    context = {
        'form': form,
        'group': "'" + group + "'," + group2,
    }
    return render(request,"auth/create_employee.html",context)

def assign_man_to_admin(request):
    admin_list = SiteUser.objects.filter(role='Admin').all()
    manager_list = SiteUser.objects.filter(role='Manager')
    if request.method=='POST':
        group = request.POST.get('group')
        manager_id = request.POST.get('manager_id')

        item = SiteUser.objects.get(id=manager_id)
        # old_group=item.group
        # item.group = "'"+group+"'"+old_group
        item.group=group

        item.save(update_fields=['group',])
    print(admin_list)
    context = {
        'admin_list': admin_list,
        'manager_list': manager_list,
    }
    return render(request,"auth/assign_man_to_admin.html",context)

def assign_emp_to_manager(request):
    employee_list = SiteUser.objects.filter(role='Employee').all()
    manager_list = SiteUser.objects.filter(role='Manager')

    if request.method=='POST':
        group = request.POST.get('group')
        employee_id = request.POST.get('employee_id')

        item = SiteUser.objects.get(id=employee_id)
        item.group=group
        # old_group = item.group
        # item.group = group + old_group
        item.save(update_fields=['group',])
    context = {
        'employee_list': employee_list,
        'manager_list': manager_list,
    }
    return render(request,"auth/assign_emp_to_manager.html",context)

def assign_module_to_emp(request):
    employee_list = SiteUser.objects.filter(role='Employee')
    if request.method=='POST':
        employee_id = request.POST.get('employee_id')
        selected_list = request.POST.getlist('checks[]')

        item = SiteUser.objects.get(id=employee_id)

        print(selected_list)
        print(employee_id)
        print(employee_id)
        print(employee_id)
        print(employee_id)
        print(employee_id)
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
        bank_name = request.POST.get('bank_name')
        account_no = request.POST.get('account_no')
        branch_name = request.POST.get('branch_name')
        ifsc_code = request.POST.get('ifsc_code')
        photo = request.FILES.get('photo')
        salary_slip = request.FILES.get('salary_slip')
        if is_deleted == 'on':
            is_deleted = True
        else:
            is_deleted = False
        item = admin_id

        item.mobile = mobile
        item.email = email
        item.name = name
        item.role = 'Admin'
        item.group = group
        item.is_deleted = is_deleted
        item.modules_assigned = modules_assigned
        item.bank_name = bank_name
        item.account_number = account_no
        item.branch_name = branch_name
        item.ifsc_code = ifsc_code
        item.photo = photo
        item.salary_slip = salary_slip

        item.set_password(request.POST.get('password'))

        item.save(update_fields=['mobile','email', 'name','role','group','is_deleted','modules_assigned','bank_name','account_number','branch_name','ifsc_code','photo','password'])
        return redirect('/update_admin/'+str(item.id))
    context = {
        'form': form,
        'admin_id': admin_id,
    }
    return render(request,"update_forms/update_admin.html",context)

def update_manager(request,id):
    manager_id = SiteUser.objects.get(id=id)
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
        ifsc_code = request.POST.get('ifsc_code')
        photo = request.FILES.get('photo')
        salary_slip = request.FILES.get('salary_slip')
        if is_deleted == 'on':
            is_deleted = True
        else:
            is_deleted = False
        item = manager_id

        item.mobile = mobile
        item.email = email
        item.name = name
        item.role = 'Manager'
        item.group = group
        item.is_deleted = is_deleted
        item.modules_assigned = modules_assigned
        item.bank_name = bank_name
        item.account_number = account_no
        item.branch_name = branch_name
        item.ifsc_code = ifsc_code
        item.photo = photo
        item.salary_slip = salary_slip
        item.set_password(request.POST.get('password'))

        item.save(update_fields=['mobile','email', 'name','role','group','is_deleted','modules_assigned','bank_name','account_number','branch_name','ifsc_code','photo','password'])
        return redirect('/update_manager/' + str(item.id))
    context = {
        'form': form,
        'manager_id': manager_id,
    }
    return render(request,"update_forms/update_manager_add.html",context)

def update_employee(request,id):
    employee_id = SiteUser.objects.get(id=id)
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
        ifsc_code = request.POST.get('ifsc_code')
        photo = request.POST.get('photo')
        salary_slip = request.FILES.get('salary_slip')
        if is_deleted == 'on':
            is_deleted = True
        else:
            is_deleted = False
        item = employee_id

        item.mobile = mobile
        item.email = email
        item.name = name
        item.role = 'Employee'
        item.group = group
        item.is_deleted = is_deleted
        item.modules_assigned = modules_assigned
        item.bank_name = bank_name
        item.account_number = account_no
        item.branch_name = branch_name
        item.ifsc_code = ifsc_code
        item.photo = photo
        item.salary_slip = salary_slip
        item.set_password(request.POST.get('password'))

        item.save(update_fields=['mobile','email', 'name','role','group','is_deleted','modules_assigned','bank_name','account_number','branch_name','ifsc_code','photo','password'])
        return redirect('/update_employee/' + str(item.id))
    context = {
        'form': form,
        'employee_id': employee_id,
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

