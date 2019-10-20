from django.shortcuts import render

# Create your views here.
from ess_app.models import Employee_Leave,Defects_Warning


def notif_decl_home(request):
    leave_req_list = Employee_Leave.objects.all()
    warn_def_list = Defects_Warning.objects.all()
    context = {
        'leave_req_list': leave_req_list,
        'warn_def_list': warn_def_list
    }
    return render(request,'dashboardnew/notif_decl_home.html',context)
