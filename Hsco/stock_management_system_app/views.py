from django.shortcuts import render, redirect
from .forms import GodownForm
from .models import Godown
from user_app.models import SiteUser


def stock_godown_list(request):
    godown_list = Godown.objects.all()
    context = {
        'godown_list':godown_list,
    }
    return render(request,'stock_management_system/stock_godown_list.html',context)

def add_godown(request):
    form = GodownForm()   
    if request.method == 'POST' or request.method=='FILES':
        name_of_godown = request.POST.get('name_of_godown')
        goddown_assign_to = request.POST.get('goddown_assign_to')
        location = request.POST.get('location')
        contact_no = request.POST.get('contact_no')

        item=Godown()
        item.name_of_godown=name_of_godown
        item.goddown_assign_to=SiteUser.objects.filter(profile_name=goddown_assign_to).first()
        item.location=location
        item.contact_no=contact_no
        item.save()

        return redirect('/stock_godown_list/')

    context = {
        'form':form
    }
    return render(request, 'stock_management_system/add_godown.html',context)

def stock_godown(request,id):
    godown_id = Godown.objects.get(id=id)
    context={
             godown_id:'godown_id'
    }
    return render(request,'stock_management_system/stock_godown.html',context)

def stock_godown_images(request):
    return render(request,'stock_management_system/stock_godown_images.html')

def stock_good_request(request):
    return render(request,'stock_management_system/stock_good_request.html')

def stock_pending_request(request):
    return render(request,'stock_management_system/stock_pending_request.html')

def stock_transaction_status(request):
    return render(request,'stock_management_system/stock_transaction_status.html')

def stock_accpet_goods(request):
    return render(request,'stock_management_system/stock_accpet_goods.html')

def stock_accpet_goods_list(request):
    return render(request,'stock_management_system/stock_accpet_goods_list.html')

def stock_transaction_history_list(request):
    return render(request,'stock_management_system/stock_transaction_history_list.html')

def stock_transaction_history(request):
    form = GodownForm()
    context={
        'form':form
    }
    return render(request, 'stock_management_system/stock_transaction_history.html',context)