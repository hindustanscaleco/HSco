from django.shortcuts import render

def home(request):
    return render(request,"dashboardnew/dash.html",)


def cust_mod_form(request):
    return render(request,"forms/cust_mod_form.html",)

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

