from django.db import connection
from django.shortcuts import render, redirect

from .forms import SiteUser_Form
from .models import SiteUser

def admin_list(request):
    admin_list = SiteUser.objects.filter(role='Admin')
    context={
        'admin_list':admin_list,
    }
    return render(request,"auth/admin_list.html",context)

def create_admin(request):
    form = SiteUser_Form(request.POST or None)
    if request.method == 'POST' or request.method == 'FILES':
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        name = request.POST.get('name')
        group = request.POST.get('group')
        is_deleted = request.POST.get('is_deleted')
        modules_assigned = request.POST.get('modules_assigned')
        date_of_joining = request.POST.get('date_of_joining')
        bank_name = request.POST.get('bank_name')
        account_no = request.POST.get('account_no')
        branch_name = request.POST.get('branch_name')
        ifsc_code = request.POST.get('ifsc_code')
        photo = request.POST.get('photo')



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
        item.account_no = account_no
        item.branch_name = branch_name
        item.ifsc_code = ifsc_code
        item.photo = photo

        item.save()
        return redirect('/admin_list/')
    context={
        'form':form,
    }
    return render(request,"auth/create_admin.html",context)

def manager_list(request):
    manager_list = SiteUser.objects.filter(role='Manager')
    context={
        'manager_list':manager_list,
    }
    return render(request,"auth/manager_list.html",context)

def create_manager(request):
    form = SiteUser_Form(request.POST or None)
    if request.method == 'POST' or request.method == 'FILES':
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        name = request.POST.get('name')
        group = request.POST.get('group')
        is_deleted = request.POST.get('is_deleted')
        modules_assigned = request.POST.get('modules_assigned')
        date_of_joining = request.POST.get('date_of_joining')
        bank_name = request.POST.get('bank_name')
        account_no = request.POST.get('account_no')
        branch_name = request.POST.get('branch_name')
        ifsc_code = request.POST.get('ifsc_code')
        photo = request.POST.get('photo')

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
        item.account_no = account_no
        item.branch_name = branch_name
        item.ifsc_code = ifsc_code
        item.photo = photo

        item.save()
        return redirect('/manager_list/')
    context = {
        'form': form,
    }
    return render(request, "auth/create_manager.html", context)

def employee_list(request):
    employee_list = SiteUser.objects.filter(role='Employee')
    context = {
        'employee_list': employee_list,
    }
    return render(request,"auth/employee_list.html",context)

def create_employee(request):
    form = SiteUser_Form(request.POST or None)
    if request.method == 'POST' or request.method == 'FILES':
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        name = request.POST.get('name')
        group = request.POST.get('group')
        is_deleted = request.POST.get('is_deleted')
        modules_assigned = request.POST.get('modules_assigned')
        date_of_joining = request.POST.get('date_of_joining')
        bank_name = request.POST.get('bank_name')
        account_no = request.POST.get('account_no')
        branch_name = request.POST.get('branch_name')
        ifsc_code = request.POST.get('ifsc_code')
        photo = request.POST.get('photo')

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
        item.account_no = account_no
        item.branch_name = branch_name
        item.ifsc_code = ifsc_code
        item.photo = photo

        item.save()
        return redirect('/employee_list/')
    context = {
        'form': form,
    }
    return render(request,"auth/create_employee.html",context)

def assign_man_to_admin(request):
    admin_list = SiteUser.objects.filter(role='Admin').all()
    manager_list = SiteUser.objects.filter(role='Manager')
    if request.method=='POST':
        group = request.POST.get('group')
        manager_id = request.POST.get('manager_id')

        item = SiteUser.objects.get(id=manager_id)

        item.group = group

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

        item.group = group

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

def login(request):
    return render(request,"auth/login.html",)

def dashboard(request):
    return render(request,"dashboardnew/dashboard.html",)

def graph(request):
    return render(request,"dashboardnew/graph.html",)



