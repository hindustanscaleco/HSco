from django.contrib.auth import authenticate, login, logout
from django.db import connection
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.views.generic import FormView

from .forms import SiteUser_Form, LoginForm
from .models import SiteUser

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
            print("NormalOGIN"+str(user))
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
        item.set_password(request.POST.get('password'))

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
        item.set_password(request.POST.get('password'))

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
        item.set_password(request.POST.get('password'))

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



def dashboard(request):
    return render(request,"dashboardnew/dashboard.html",)

def graph(request):
    return render(request,"graphs/sales_graph.html",)


def update_admin(request):
    if request.method =='POST' and 'performance' in request.POST:
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
    return render(request,"update_forms/update_admin.html",)



def update_manager_add(request):
    if request.method =='POST' and 'performance' in request.POST:
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

    return render(request,"update_forms/update_manager_add.html")

def update_employee(request):
    if request.method =='POST' and 'performance' in request.POST:
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

    return render(request,"update_forms/update_employee.html")

