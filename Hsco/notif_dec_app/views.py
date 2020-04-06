from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
# Create your views here.
from ess_app.models import Employee_Leave,Defects_Warning

from .models import Chat_model
from user_app.models import SiteUser


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

def chat_details(request,from_id,to_id):
    todays_date = timezone.now
    # chat_bot = Student.objects.get(id=higher_authority_id)
    msg_list1 = Chat_model.objects.filter(
        (Q(message_from_id=SiteUser.objects.get(id=to_id).id) &
         Q(message_to=SiteUser.objects.get(id=from_id).id))|
        (Q(message_from_id=SiteUser.objects.get(id=from_id).id)&
         Q(message_to=SiteUser.objects.get(id=to_id).id)))

    msg_list2 = Chat_model.objects.filter()

    if request.method == 'POST' or request.method=='FILES':
        message = request.POST.get('message')

        item = Chat_model()

        item.message_from_id = request.user.id
        item.message = message

        item.is_superadmin = True if request.user.role == 'Super Admin' else False
        item.is_admin = True if request.user.role == 'Admin' else False
        item.is_manager = True if request.user.role == 'Manager' else False
        item.is_employee = True if request.user.role == 'Employee' else False




        item.message_to_id = SiteUser.objects.get(id=to_id).id




        item.save()

        return redirect('/chat_details/'+str(from_id)+'/'+str(to_id))
    context={
        'chat_bot':'',
        'msg_list1':msg_list1,
        'todays_date':todays_date,
    }
    return render(request,'Chat/chat_details.html',context)


def chat_with_user(request):

    if request.user.role == 'Employee':
        all_users_list = SiteUser.objects.filter(name = SiteUser.objects.get(id=request.user.id).manager)
    elif request.user.role == 'Manager':
        all_users_list = SiteUser.objects.filter(name = SiteUser.objects.get(id=request.user.id).admin)
    elif request.user.role == 'Admin':
        all_users_list = SiteUser.objects.filter(Q(admin = request.user.name) & Q(role = 'Manager') | Q(role = 'Super Admin'))
    elif request.user.role == 'Super Admin':
        all_users_list = SiteUser.objects.filter(role = 'Admin')
    context={
        'all_users_list':all_users_list,
    }
    return render(request,"Chat/users_list.html",context)
