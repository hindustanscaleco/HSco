from django.db import connection
from django.shortcuts import render, redirect


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


def report(request):
    if request.method =='POST':
        selected_list = request.POST.getlist('checks[]')
        start_date = request.POST.get('date1')
        end_date = request.POST.get('date2')
        string = ','.join(selected_list)

        request.session['start_date']= start_date
        request.session['end_date']= end_date
        request.session['string']= string
        return redirect('/final_report/')
    return render(request,"dashboardnew/report.html",)


def final_report(request):
    start_date = request.session.get('start_date')
    end_date = request.session.get('end_date')
    string = request.session.get('string')
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT " + string + " from customer_app_customer_details where date_of_purchase between '"+start_date+"' and '"+end_date+"';")
        row = cursor.fetchall()
    print(string)
    print(start_date)
    print(end_date)
    print(row)
    return render(request,"dashboardnew/final_report.html")
