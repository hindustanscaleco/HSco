from django.shortcuts import render
from .forms import GodownForm

def stock_godown_list(request):
    return render(request,'stock_management_system/stock_godown_list.html')

def add_godown(request):
    form = GodownForm()
    context = {
        'form':form
    }
    return render(request, 'stock_management_system/add_godown.html',context)

def stock_godown(request):
    return render(request,'stock_management_system/stock_godown.html')

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