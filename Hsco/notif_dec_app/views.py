from django.shortcuts import render

# Create your views here.


def notif_decl_home(request):
    return render(request,'dashboardnew/notif_decl_home.html',)
