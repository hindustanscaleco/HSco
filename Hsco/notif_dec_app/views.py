from django.db.models import Q, F
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
# Create your views here.
from ess_app.models import Employee_Leave,Defects_Warning

from .models import Chat_model
from user_app.models import SiteUser

from lead_management.models import Lead

from stock_management_system_app.models import GodownProduct, RequestedProducts, GoodsRequest
from datetime import timedelta



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
    dont_show = False

    to_role=SiteUser.objects.get(id=to_id).role
    to_id_id=SiteUser.objects.get(id=to_id)
    from_role=SiteUser.objects.get(id=from_id).role
    if request.user.role == 'Super Admin':
        can_reply_to_sa=SiteUser.objects.get(id=to_id).can_reply_to_sa
    else:
        can_reply_to_sa = SiteUser.objects.get(id=from_id).can_reply_to_sa

    if(to_role=='Admin' and from_role=='Manager'):
        dont_show = True
    elif (to_role == 'Super Admin' and from_role == 'Admin'):
        dont_show = True
    elif (to_role == 'Super Admin' and from_role == 'Manager'):
        dont_show = True



    msg_list1 = Chat_model.objects.filter(
        (Q(message_from_id=SiteUser.objects.get(id=to_id).id) &
         Q(message_to=SiteUser.objects.get(id=from_id).id))|
        (Q(message_from_id=SiteUser.objects.get(id=from_id).id)&
         Q(message_to=SiteUser.objects.get(id=to_id).id)))

    Chat_model.objects.filter(Q(message_to=SiteUser.objects.get(id=from_id).id) & Q(is_viewed=False)).update(is_viewed=True)

    msg_list2 = Chat_model.objects.filter()

    if request.method == 'POST' or request.method=='FILES':
        message = request.POST.get('message')
        defectnwarn = request.POST.get('defectnwarn')


        item = Chat_model()

        item.message_from_id = request.user.id
        item.message = message

        item.is_defect = True if defectnwarn == 'defect' else False
        item.is_warning = True if defectnwarn == 'warning' else False

        item.is_superadmin = True if request.user.role == 'Super Admin' else False
        item.is_admin = True if request.user.role == 'Admin' else False
        item.is_manager = True if request.user.role == 'Manager' else False
        item.is_employee = True if request.user.role == 'Employee' else False




        item.message_to_id = SiteUser.objects.get(id=to_id).id




        item.save()

        return redirect('/chat_details/'+str(from_id)+'/'+str(to_id))
    context={
        'can_reply_to_sa':can_reply_to_sa,
        'msg_list1':msg_list1,
        'todays_date':todays_date,
        'dont_show':dont_show,
        'to_id_id':to_id_id.id,
        'to_id_name':to_id_id.profile_name,
    }
    return render(request,'Chat/chat_details.html',context)


def chat_with_user(request):

    if request.user.role == 'Employee':
        # all_users_list = SiteUser.objects.filter(Q(name = SiteUser.objects.get(id=request.user.id).manager) | Q(name = SiteUser.objects.get(id=request.user.id).admin) | Q(role = 'Super Admin'))
        all_users_list = SiteUser.objects.filter(Q(name = SiteUser.objects.get(id=request.user.id).manager) | Q(role = 'Super Admin'))
    elif request.user.role == 'Manager':
        all_users_list = SiteUser.objects.filter(Q(name = SiteUser.objects.get(id=request.user.id).admin) | Q(manager = request.user.name) | Q(role = 'Super Admin'))
    elif request.user.role == 'Admin':
        all_users_list = SiteUser.objects.filter(Q(admin = request.user.name) & Q(role = 'Manager') | Q(role = 'Super Admin'))
    elif request.user.role == 'Super Admin':
        all_users_list = SiteUser.objects.all()
    context={
        'all_users_list': all_users_list,
    }
    return render(request,"Chat/users_list.html",context)

def change_replying_status_ajax(request,user_id):
    selected = request.GET.get('loc_id')
    name = SiteUser.objects.get(id=user_id).profile_name
    if(selected=='true'):
        SiteUser.objects.filter(id=user_id).update(can_reply_to_sa=True)
        context={
            'status_changed':'true',
            'msg':'Now "'+name+'" Can Reply to Your Messages!!'
        }
    else:
        SiteUser.objects.filter(id=user_id).update(can_reply_to_sa=False)
        context = {
            'status_changed': 'true',
            'msg':'Now "' + name + '" Cannot Reply to Your Messages!!'
        }

    return JsonResponse(context)

import datetime
def notification_context(request):
    if request.user.is_authenticated:


        message = Chat_model.objects.filter(message_to=request.user.id, is_viewed=False,is_warning=False,is_defect=False)
        alert = Chat_model.objects.filter((Q(message_to=request.user.id) &Q(is_viewed=False))&(Q(is_warning=True)|Q(is_defect=True)))
        postponed_alert = Lead.objects.filter(Q(current_stage='Postponed') & Q(postpond_time_date__gte=datetime.date.today()) & Q(owner_of_opportunity__id=request.user.pk))
        # next_date = datetime.date.today() + timedelta(days=1)



        critical_limit_notif = GodownProduct.objects.filter(critical_limit__gte=F('quantity'),godown_id__goddown_assign_to=request.user)
        request_admin_list = GoodsRequest.objects.filter(Q(request_admin=True) & Q(req_from_godown__godown_admin__id=request.user.id)) | \
                             GoodsRequest.objects.filter(Q(request_admin=True) & Q(request_admin_id__id=request.user.id))
        # req_product_mismatch_notif = RequestedProducts.objects.filter((Q(sent_quantity__gte=0.0)|Q(sent_carton_count__gte=0.0))|~Q(sent_quantity=F('received_quantity')))
        if request.user.role == 'Super Admin':
            req_product_mismatch_notif = RequestedProducts.objects.filter(Q(goods_req_id__notify=True)&(~Q(sent_quantity=F('received_quantity') + F('faulty_quantity')) | ~Q(
                    sent_carton_count=F('received_carton_count') + F('received_carton_count')))).order_by('-id')
        else:
            req_product_mismatch_notif = RequestedProducts.objects.filter(
                (Q(goods_req_id__notify=True)&~Q(sent_quantity=(F('received_quantity')+F('faulty_quantity')))|~Q(sent_carton_count=(F('received_carton_count')+F('received_carton_count'))))& Q(godown_id__godown_admin=request.user)
            ).order_by('-id')


        if postponed_alert.count() > 0:
            post_alert = True
        else:
            post_alert = False
        return {
            'notification_count': message.count(),
            'alert_count': alert.count()+postponed_alert.count()+critical_limit_notif.count()+request_admin_list.count()+req_product_mismatch_notif.count(),
            'notif_message': message,
            'notif_alert': alert,
            'is_post_alert': post_alert,
            'postponed_alert': postponed_alert,
            'critical_limit_alert': critical_limit_notif,
            'request_admin_notif': request_admin_list,
            'req_product_mismatch_notif': req_product_mismatch_notif,
        }
    else:
        return {}