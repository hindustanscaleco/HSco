from django.shortcuts import render, redirect
from django.views import View
from .models import Stock_System
from .forms import StockRegisterForm
from django.contrib.auth.decorators import login_required
from customer_app.models import type_purchase
from .models import Lead_Product
from customer_app.models import sub_model, main_model, sub_sub_model

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

# def add_lead_product(request,id):
#     type_of_purchase_list =type_purchase.objects.all() #1
#
#     if request.method == 'POST' or request.method=='FILES':
#         scale_type = request.POST.get('scale_type')
#         main_category = request.POST.get('main_category')
#         sub_category = request.POST.get('sub_category')
#         sub_sub_category = request.POST.get('sub_sub_category')
#         hsn_code = request.POST.get('hsn_code')
#         product_image = request.POST.get('product_image')
#         max_capacity = request.POST.get('max_capacity')
#         accuracy = request.POST.get('accuracy')
#         platform_size = request.POST.get('platform_size')
#         product_desc = request.POST.get('product_desc')
#         product_brochure = request.POST.get('product_brochure')
#         product_document = request.POST.get('product_document')
#         cost_price = request.POST.get('cost_price')
#         selling_price = request.POST.get('selling_price')
#         carton_size = request.POST.get('carton_size')
#         is_last_product_yes = request.POST.get('is_last_product_yes')
#
#         item = Lead_Product()
#
#         item.lead_id = Lead.objects.get(id=id)
#         item.scale_type = type_purchase.objects.get(id=scale_type).name
#         item.main_category = main_model.objects.get(id=main_category).name
#         item.sub_category = sub_model.objects.get(id=sub_category).name
#         item.sub_sub_category = sub_sub_model.objects.get(id=sub_sub_category).name
#         item.hsn_code = hsn_code
#         item.product_image = product_image
#         item.max_capacity = max_capacity
#         item.accuracy = accuracy
#         item.platform_size = platform_size
#         item.product_desc = product_desc
#         item.product_brochure = product_brochure
#         item.product_document = product_document
#         item.cost_price = cost_price
#         item.selling_price = selling_price
#         item.carton_size = carton_size
#
#         item.save()
#         if is_last_product_yes == 'yes':
#             return redirect('/update_view_lead/'+str(id))
#         elif is_last_product_yes == 'no':
#             return redirect('/add_lead_product/'+str(id))
#     context={
#         'type_purchase': type_of_purchase_list,  # 2
#
#     }
#     return render(request,'lead_management/add_lead_product.html',context)
