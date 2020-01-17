from django.shortcuts import render
from django.views import View
from .models import Stock_System
from .forms import StockRegisterForm
from django.contrib.auth.decorators import login_required


# def stock_system_form(request):
#     stock_form = StockRegisterForm(request.POST or None)
#     if request.method =='POST':
#         type_of_scale =request.POST.get('type_of_scale')
#         hsn_code =request.POST.get('hsn_code')
#         product_code =request.POST.get('product_code')
#         product_sub_code =request.POST.get('product_sub_code')
#         product_sub_sub_code =request.POST.get('product_sub_sub_code')
#         photo =request.POST.get('photo')
#         description =request.POST.get('description')
#         plate_size =request.POST.get('plate_size')
#
#         item = Stock_System()
#         item.type_of_scale = type_of_scale
#         item.hsn_code = hsn_code
#         item.product_code = product_code
#         item.product_sub_code = product_sub_code
#         item.product_sub_sub_code = product_sub_sub_code
#         item.photo = photo
#         item.description = description
#         item.plate_size = plate_size
#         item.save()
#
#     context = {
#         'form':stock_form
#     }
#
#     return render(request,'stock_system/stock_system_input.html',context)


class Stock_System_View(View):
    def get(self,request):
        stock_form = StockRegisterForm()
        context = {
            'form': stock_form
        }
        return render(request,'stock_system/stock_system_input.html',context)


    def post(self,request):
        stock_system = Stock_System()
        form = StockRegisterForm(request.POST,instance=stock_system)
        if form.is_valid():
            form.save()


        context = {
            'form': form
        }
        return render(request,'stock_system/stock_system_input.html',context)

