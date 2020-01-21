from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
from ess_app.models import Employee_Leave,Defects_Warning


def notif_decl_home(request):
    if request.user.role == 'Super Admin':
        leave_req_list = Employee_Leave.objects.filter(user_id__group__icontains=request.user.name, user_id__is_deleted=False)
        warn_def_list = Defects_Warning.objects.filter(user_id__group__icontains=request.user.name, user_id__is_deleted=False)
    else:
        leave_req_list = Employee_Leave.objects.filter(user_id__pk=request.user.pk,)
        warn_def_list = Defects_Warning.objects.filter(user_id__pk=request.user.pk,)

    context = {
        'leave_req_list': leave_req_list,
        'warn_def_list': warn_def_list
    }
    return render(request,'dashboardnew/notif_decl_home.html',context)
