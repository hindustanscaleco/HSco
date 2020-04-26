from django.contrib import messages
from django.db.models import Q, F
from django.shortcuts import render, redirect

from customer_app.models import type_purchase
from .forms import GodownForm
from .models import Godown, GodownProduct, RequestedProducts, GoodsRequest, Product, AGProducts, AcceptGoods
from user_app.models import SiteUser
from customer_app.models import sub_model, main_model, sub_sub_model


def stock_godown_list(request):
    if request.user.role == 'Super Admin':
        godown_list = Godown.objects.all().order_by('-id')
    elif request.user.role == 'Admin':
        godown_list = Godown.objects.filter(godown_admin__id=request.user.id).order_by('-id')
    else:
        godown_list = Godown.objects.filter(goddown_assign_to__id=request.user.id).order_by('-id')

    context = {
        'godown_list':godown_list,
    }
    return render(request,'stock_management_system/stock_godown_list.html',context)

def add_godown(request):
    products = Product.objects.all()
    assign_users = SiteUser.objects.filter(modules_assigned__icontains= 'Stock', admin__contains= request.user.profile_name)

    form = GodownForm()
    if request.method == 'POST' or request.method=='FILES':
        name_of_godown = request.POST.get('name_of_godown')
        goddown_assign_to = request.POST.get('goddown_assign_to')
        location = request.POST.get('location')
        contact_no = request.POST.get('contact_no')

        item=Godown()
        item.name_of_godown=name_of_godown
        item.goddown_assign_to=SiteUser.objects.filter(id=goddown_assign_to).first()
        item.godown_admin=SiteUser.objects.get(id=request.user.id)
        item.location=location
        item.contact_no=contact_no
        item.log_entered_by = request.user.name
        item.save()

        return redirect('/update_godown/'+str(item.id))

    context = {
        'form':form,
        'products':products,
        'assign_users':assign_users,
    }
    return render(request, 'stock_management_system/add_godown.html',context)

def update_godown(request,godown_id):
    godown = Godown.objects.get(id=godown_id)
    godown_products = GodownProduct.objects.filter(godown_id=godown_id)

    assign_users = SiteUser.objects.filter(Q(modules_assigned__icontains= 'Stock')&Q(admin__contains= request.user.profile_name)
                                           &~Q(id=godown.goddown_assign_to.id))
    type_of_purchase_list = type_purchase.objects.all()  # 1
    products = Product.objects.all()
    godown_initial_data = {
        'name_of_godown': godown.name_of_godown,
        'goddown_assign_to': godown.goddown_assign_to,
        'location': godown.location,
        'contact_no': godown.contact_no,
    }
    form = GodownForm(initial=godown_initial_data)
    context = {
        'godown_products': godown_products,
        'godown': godown,
        'form': form,
        'assign_users': assign_users,
        'type_of_purchase_list': type_of_purchase_list,
        'products': products,

    }
    if request.method == 'POST' or request.method=='FILES':
        if 'submit1' in request.POST:
            name_of_godown = request.POST.get('name_of_godown')
            goddown_assign_to = request.POST.get('goddown_assign_to')
            location = request.POST.get('location')
            contact_no = request.POST.get('contact_no')

            item = Godown.objects.get(id=godown_id)
            item.name_of_godown = name_of_godown
            item.goddown_assign_to = SiteUser.objects.filter(profile_name=goddown_assign_to).first()
            item.location = location
            item.contact_no = contact_no
            item.log_entered_by = request.user.name
            item.save(update_fields=['name_of_godown','goddown_assign_to','location','contact_no','log_entered_by'])
            context1={
                'godown_msg' : "Godown Updated Successfully!!!",
                'godown_products': godown_products,
                'godown': godown,
                'form': form,
                'assign_users': assign_users,
                'type_of_purchase_list': type_of_purchase_list,
                'products': products,
            }
            context.update(context1)
            return render(request, 'stock_management_system/update_godown.html', context)
        if 'submit2' in request.POST:
            product_id = request.POST.get('product_id')
            GodownProduct.objects.get(id=product_id).delete()
            context1 = {
                'product_deleted': "Product Removed From Godown Successfully!!!",
                'godown_products': godown_products,
                'godown': godown,
                'form': form,
                'assign_users': assign_users,
                'type_of_purchase_list': type_of_purchase_list,
                'products': products,
            }
            context.update(context1)
            return render(request, 'stock_management_system/update_godown.html', context)
        if 'submit3' in request.POST:
            type_of_scale = request.POST.get('scale_type')
            main_category = request.POST.get('main_category')
            sub_category = request.POST.get('sub_category')
            sub_sub_category = request.POST.get('sub_sub_category')

            if ((sub_sub_category != None and sub_sub_category != '') and (
                    sub_category != None and sub_category != '') and (
                    main_category != None and main_category != '') and (
                    type_of_scale != None and type_of_scale != '')):
                godown_products = GodownProduct.objects.filter(godown_id=godown_id,product_id__scale_type=type_of_scale,
                                                    product_id__main_category=main_category,
                                                    product_id__sub_category=sub_category,
                                                    product_id__sub_sub_category=sub_sub_category)

            elif ((sub_category != None and sub_category != '') and (
                    main_category != None and main_category != '') and (
                          type_of_scale != None and type_of_scale != '')):
                godown_products = GodownProduct.objects.filter(godown_id=godown_id,product_id__scale_type=type_of_scale,
                                                    product_id__main_category=main_category,
                                                    product_id__sub_category=sub_category)

            elif ((main_category != None and main_category != '') and (
                    type_of_scale != None and type_of_scale != '')):
                godown_products = GodownProduct.objects.filter(godown_id=godown_id,product_id__scale_type=type_of_scale,
                                                    product_id__main_category=main_category)

            elif (type_of_scale != None and type_of_scale != ''):
                godown_products = GodownProduct.objects.filter(godown_id=godown_id,product_id__scale_type=type_of_scale)
            context1 = {
                'godown_products': godown_products,
                'godown': godown,
                'form': form,
                'assign_users': assign_users,
                'type_of_purchase_list': type_of_purchase_list,
                'products': products,
            }
            context.update(context1)
            return render(request, 'stock_management_system/update_godown.html', context)


    return render(request, 'stock_management_system/update_godown.html',context)

def add_product_godown(request, godown_id):
    godown = Godown.objects.get(id=godown_id)
    type_of_purchase_list =type_purchase.objects.all() #1
    context = {
        'godown': godown,
        'type_of_purchase_list': type_of_purchase_list,

    }
    if request.method == 'POST' or request.method == 'FILES':
        quantity = request.POST.get('quantity')
        req_type = request.POST.get('req_type')
        is_last_product_yes = request.POST.get('is_last_product_yes')
        # model_of_purchase = request.POST.get('model_of_purchase')
        type_of_scale = request.POST.get('scale_type')
        main_category = request.POST.get('main_category')
        sub_category = request.POST.get('sub_category')
        critical_limit = request.POST.get('critical_limit')
        sub_sub_category = request.POST.get('sub_sub_category')    #product code or sub_sub_category


        item = GodownProduct()
        try:
            if sub_sub_category != '':
                if GodownProduct.objects.filter(godown_id=godown_id,product_id__scale_type=type_of_scale,product_id__main_category=main_category,
                product_id__sub_category=sub_category,product_id__sub_sub_category=sub_sub_category).count() > 0:
                    if req_type == 'Individual':
                        GodownProduct.objects.filter(godown_id=godown_id,product_id__scale_type=type_of_scale,product_id__main_category=main_category,
                        product_id__sub_category=sub_category,product_id__sub_sub_category=sub_sub_category).update(
                        quantity=F("quantity") + quantity)
                        if critical_limit != '0' and critical_limit != '' and critical_limit != 'None':
                            GodownProduct.objects.filter(godown_id=godown_id, product_id__scale_type=type_of_scale,
                                                         product_id__main_category=main_category,
                                                         product_id__sub_category=sub_category,
                                                         product_id__sub_sub_category=sub_sub_category).update(
                                critical_limit= critical_limit)
                    elif req_type == 'Carton':
                        product = Product.objects.get(scale_type=type_of_scale, main_category=main_category,
                                                      sub_category=sub_category, sub_sub_category=sub_sub_category)
                        individual_quantity = (float(product.carton_size) * float(quantity))

                        GodownProduct.objects.filter(godown_id=godown_id, product_id__scale_type=type_of_scale,product_id__main_category=main_category,
                        product_id__sub_category=sub_category,product_id__sub_sub_category=sub_sub_category).update(
                        quantity=F("quantity") + individual_quantity)
                        if critical_limit != '0' and critical_limit != '' and critical_limit != 'None':
                            individual_critical_limit = (float(product.carton_size) * float(critical_limit))
                            GodownProduct.objects.filter(godown_id=godown_id, product_id__scale_type=type_of_scale,
                                                         product_id__main_category=main_category,
                                                         product_id__sub_category=sub_category,
                                                         product_id__sub_sub_category=sub_sub_category).update(
                                critical_limit=individual_critical_limit)

                else:
                    item.product_id = Product.objects.get(scale_type=type_of_scale, main_category=main_category,
                                                          sub_category=sub_category, sub_sub_category=sub_sub_category)
                    item.godown_id = Godown.objects.get(id=godown_id)
                    item.added_by_id = SiteUser.objects.get(id=request.user.id)
                    if req_type == 'Individual':
                        if quantity !=  '' and 'None':
                            item.quantity = quantity
                        if critical_limit != '' and 'None':
                            item.critical_limit = critical_limit
                    elif req_type == 'Carton':
                        product = Product.objects.get(scale_type=type_of_scale, main_category=main_category,
                                                      sub_category=sub_category, sub_sub_category=sub_sub_category)
                        individual_quantity = (float(product.carton_size) * float(quantity))
                        individual_critical_limit = (float(product.carton_size) * float(critical_limit))
                        if quantity !=  '' and 'None':
                            item.quantity = individual_quantity
                        if critical_limit != '' and 'None':
                            item.critical_limit = individual_critical_limit
                    else:
                        item.quantity = 0.0

                    item.log_entered_by = request.user.name
                    item.save()

            if is_last_product_yes == 'yes':
                return redirect('/update_godown/' + str(godown_id))
            elif is_last_product_yes == 'no':
                return redirect('/add_product_godown/' + str(godown_id))
        except Exception as e:
            print(e)
            msg = "Selected Product does not exist in Main Product Database Table!!!"
            context1={
                'msg':msg,
            }
            context.update(context1)

    return render(request, 'stock_management_system/add_product_godown.html',context)


def stock_godown(request,id):
    type_of_purchase_list =type_purchase.objects.all() #1
    products = Product.objects.all()
    godown_id = Godown.objects.get(id=id)
    godown_products = GodownProduct.objects.filter(godown_id=id)

    if GoodsRequest.objects.all().count() == 0:
        new_good_request_id = 1
    else:
        new_good_request_id = GoodsRequest.objects.latest('id').id + 1
    context={
        'godown_id': godown_id,
        'new_good_request_id': new_good_request_id,
        'type_of_purchase_list': type_of_purchase_list,
        'products': products,
        'godown_products': godown_products,

    }
    if request.method == 'POST' or request.method == 'FILES':

        type_of_scale = request.POST.get('scale_type')
        main_category = request.POST.get('main_category')
        sub_category = request.POST.get('sub_category')
        sub_sub_category = request.POST.get('sub_sub_category')

        if ((sub_sub_category != None and sub_sub_category !='') and (sub_category != None and sub_category !='') and (main_category != None and main_category !='') and (type_of_scale != None and type_of_scale !='')):
            sort = GodownProduct.objects.filter(godown_id=id,product_id__scale_type=type_of_scale,
                                                  product_id__main_category=main_category,
                                                  product_id__sub_category=sub_category,
                                                  product_id__sub_sub_category=sub_sub_category)
            context1={
                'godown_products':sort,
                'godown_id': godown_id,
                'new_good_request_id': new_good_request_id,
                'type_of_purchase_list': type_of_purchase_list,
                'products': products,
            }
            context.update(context1)
            return render(request, 'stock_management_system/stock_godown.html', context)


        elif ( (sub_category != None and sub_category !='')and (main_category != None and main_category !='')  and (type_of_scale != None and type_of_scale !='')):
            sort = GodownProduct.objects.filter(godown_id=id,product_id__scale_type=type_of_scale,
                                                  product_id__main_category=main_category,
                                                  product_id__sub_category=sub_category)
            context1 = {
                'godown_products': sort,
                'godown_id': godown_id,
                'new_good_request_id': new_good_request_id,
                'type_of_purchase_list': type_of_purchase_list,
                'products': products,
            }
            context.update(context1)
            return render(request, 'stock_management_system/stock_godown.html', context)


        elif (  (main_category != None and main_category !='')  and (type_of_scale != None and type_of_scale !='')):
            sort = GodownProduct.objects.filter(godown_id=id,product_id__scale_type=type_of_scale,
                                                  product_id__main_category=main_category)
            context1 = {
                'godown_products': sort,
                'godown_id': godown_id,
                'new_good_request_id': new_good_request_id,
                'type_of_purchase_list': type_of_purchase_list,
                'products': products,
            }
            context.update(context1)
            return render(request, 'stock_management_system/stock_godown.html', context)


        elif (type_of_scale != None and type_of_scale !=''):
            sort = GodownProduct.objects.filter(godown_id=id,product_id__scale_type=type_of_scale)
            context1 = {
                'godown_products': sort,
                'godown_id': godown_id,
                'new_good_request_id': new_good_request_id,
                'type_of_purchase_list': type_of_purchase_list,
                'products': products,
            }
            context.update(context1)
            return render(request, 'stock_management_system/stock_godown.html', context)


    return render(request,'stock_management_system/stock_godown.html',context)

def stock_godown_images(request):
    return render(request,'stock_management_system/stock_godown_images.html')

def stock_good_request(request,godown_id, request_id):
    # good_request = GoodsRequest.objects.get(id=request_id)
    godowns = Godown.objects.filter(Q(goddown_assign_to__name=request.user.admin)& ~Q(id=godown_id))| \
              Godown.objects.filter(Q(godown_admin__id=request.user.id)& ~Q(id=godown_id))
    godown_goods = GodownProduct.objects.filter(godown_id=godown_id)
    requested_goods = RequestedProducts.objects.filter(godown_id=godown_id,goods_req_id =request_id)
    type_of_purchase_list = type_purchase.objects.all()  # 1
    products = Product.objects.all()
    context = {
        'godown_goods': godown_goods,
        'requested_goods': requested_goods,
        'godowns': godowns,
        'type_of_purchase_list': type_of_purchase_list,
        'products': products,
    }
    if request.method == 'POST' or request.method == 'FILES':
        if 'submit1' in request.POST:
            product_id = request.POST.get('product_id')

            req_type = request.POST.get('req_type')
            number = request.POST.get('number')

            item2 = RequestedProducts()

            item2.req_type = req_type
            if req_type == 'Individual':
                item2.req_quantity = number
            elif req_type == 'Carton':
                item2.req_carton_count = number

            item2.godown_id = Godown.objects.get(id=godown_id)
            item2.godown_product_id = GodownProduct.objects.get(product_id=product_id,godown_id=godown_id)
            item2.log_entered_by = request.user.name
            item2.save()
            if GoodsRequest.objects.filter(id=request_id).count() == 0:
                item3 = GoodsRequest()
                item3.save()
            else:
                item3 = GoodsRequest.objects.get(id=request_id)
            item2.goods_req_id = item3
            item2.save(update_fields=['goods_req_id',])
            return redirect('/stock_good_request/'+str(godown_id)+'/'+str(request_id))
        elif 'submit2' in request.POST:
            req_to_godown = request.POST.get('req_to_godown')

            item2 = GoodsRequest.objects.get(id=request_id)

            item2.req_from_godown = Godown.objects.get(id=godown_id)
            if req_to_godown == '':
                item2.is_all_req = True
            elif req_to_godown == 'admin':
                item2.request_admin = True
            else:
                item2.req_to_godown = Godown.objects.get(id=req_to_godown)
            item2.log_entered_by = request.user.name
            item2.entered_by = SiteUser.objects.get(id=request.user.id)
            item2.status = 'Pending From Target'
            item2.save(update_fields=['req_from_godown','is_all_req','req_to_godown','log_entered_by','entered_by','status','request_admin'])
            return redirect('/stock_godown/'+str(godown_id))

        elif 'submit3' in request.POST:
            request_id = request.POST.get('request_id')
            RequestedProducts.objects.get(id=request_id).delete()

        elif 'submit4' in request.POST:
            type_of_scale = request.POST.get('scale_type')
            main_category = request.POST.get('main_category')
            sub_category = request.POST.get('sub_category')
            sub_sub_category = request.POST.get('sub_sub_category')

            if ((sub_sub_category != None and sub_sub_category != '') and (
                    sub_category != None and sub_category != '') and (
                    main_category != None and main_category != '') and (
                    type_of_scale != None and type_of_scale != '')):
                sort = GodownProduct.objects.filter(godown_id=godown_id,product_id__scale_type=type_of_scale,
                                                    product_id__main_category=main_category,
                                                    product_id__sub_category=sub_category,
                                                    product_id__sub_sub_category=sub_sub_category)
                context1 = {
                    'godown_goods': sort,
                    'requested_goods': requested_goods,
                    'godowns': godowns,
                    'type_of_purchase_list': type_of_purchase_list,
                    'products': products,
                }
                context.update(context1)
                return render(request, 'stock_management_system/stock_good_request.html', context)


            elif ((sub_category != None and sub_category != '') and (
                    main_category != None and main_category != '') and (
                          type_of_scale != None and type_of_scale != '')):
                sort = GodownProduct.objects.filter(godown_id=godown_id,product_id__scale_type=type_of_scale,
                                                    product_id__main_category=main_category,
                                                    product_id__sub_category=sub_category)
                context1 = {
                    'godown_goods': sort,
                    'requested_goods': requested_goods,
                    'godowns': godowns,
                    'type_of_purchase_list': type_of_purchase_list,
                    'products': products,
                }
                context.update(context1)
                return render(request, 'stock_management_system/stock_good_request.html', context)


            elif ((main_category != None and main_category != '') and (
                    type_of_scale != None and type_of_scale != '')):
                sort = GodownProduct.objects.filter(godown_id=godown_id,product_id__scale_type=type_of_scale,
                                                    product_id__main_category=main_category)
                context1 = {
                    'godown_goods': sort,
                    'requested_goods': requested_goods,
                    'godowns': godowns,
                    'type_of_purchase_list': type_of_purchase_list,
                    'products': products,
                }
                context.update(context1)
                return render(request, 'stock_management_system/stock_good_request.html', context)


            elif (type_of_scale != None and type_of_scale != ''):
                sort = GodownProduct.objects.filter(godown_id=godown_id,product_id__scale_type=type_of_scale)
                context1 = {
                    'godown_goods': sort,
                    'requested_goods': requested_goods,
                    'godowns': godowns,
                    'type_of_purchase_list': type_of_purchase_list,
                    'products': products,
                }
                context.update(context1)
                return render(request, 'stock_management_system/stock_good_request.html', context)


    return render(request,'stock_management_system/stock_good_request.html',context)

def stock_pending_request(request,godown_id):
    godown = Godown.objects.get(id=godown_id)
    if request.user.role == 'Super Admin':
        pending_list = GoodsRequest.objects.filter(~Q(status=None)).order_by('-id')
    else:
        pending_list = GoodsRequest.objects.filter(~Q(status='Confirms the transformation')&~Q(status=None)&Q(req_to_godown__goddown_assign_to__id=request.user.id)).order_by('-id')    | \
                       GoodsRequest.objects.filter(~Q(status='Confirms the transformation')&~Q(status=None)&Q(req_from_godown__goddown_assign_to__id=request.user.id)).order_by('-id') | \
                       GoodsRequest.objects.filter(~Q(status='Confirms the transformation')&~Q(status=None)&Q(req_to_godown__godown_admin__id=request.user.id)).order_by('-id') | \
                       GoodsRequest.objects.filter(~Q(status='Confirms the transformation')&~Q(status=None)&Q(req_from_godown__godown_admin__id=request.user.id)).order_by('-id') | \
                       GoodsRequest.objects.filter(Q(is_all_req=True)&~Q(status='Confirms the transformation')&~Q(status=None)&(Q(req_from_godown__godown_admin__name=request.user.name)|Q(req_from_godown__goddown_assign_to__id=request.user.id))&Q(req_to_godown__goddown_assign_to__admin=None)).order_by('-id')
    context = {
        'godown_id': godown,
        'pending_list': pending_list,
    }
    return render(request,'stock_management_system/stock_pending_request.html',context)

def stock_transaction_status(request,from_godown_id, trans_id):
    good_request = GoodsRequest.objects.get(id=trans_id)
    godown = Godown.objects.get(id=from_godown_id)
    requested_goods = RequestedProducts.objects.filter(godown_id=from_godown_id,goods_req_id =good_request)
    godown_assign_employee = Godown.objects.filter(Q(goddown_assign_to__id=request.user.id)&~Q(id=good_request.req_from_godown.id))
    godown_assign_admin = Godown.objects.filter(Q(godown_admin__id=request.user.id)&~Q(id=good_request.req_from_godown.id))
    if request.method == 'POST' or request.method == 'FILES':
        if 'submit1' in request.POST:
            number = request.POST.get('number')
            req_type = request.POST.get('req_type')
            product_id = request.POST.get('product_id')
            faulty = request.POST.get('faulty')
            req_to_godown = request.POST.get('req_to_godown')
            item2 = RequestedProducts.objects.get(id=product_id)

            if req_type == 'Individual':
                if good_request.status == 'Pending From Target':
                    if good_request.req_to_godown == 'None' or good_request.req_to_godown ==  None :
                        good_request.req_to_godown = Godown.objects.get(id=req_to_godown)
                    if number != '0':
                        item2.sent_quantity = float(number)
                        item2.log_entered_by = request.user.name
                elif good_request.status == 'Confirmation of goods transformation':
                    if number != '0':
                        item2.received_quantity = float(number)
                        item2.log_entered_by = request.user.name
                    if faulty != '0':
                        item2.faulty_quantity = float(faulty)
                        item2.log_entered_by = request.user.name
                    if good_request.req_to_godown == 'None' or None or '':
                        good_request.req_to_godown = Godown.objects.get(id=req_to_godown)

            elif req_type == 'Carton':
                if good_request.status == 'Pending From Target':
                    if number != '0':
                        item2.sent_carton_count = float(number)
                        item2.log_entered_by = request.user.name
                elif good_request.status == 'Confirmation of goods transformation':
                    if number != '0' :
                        item2.received_carton_count = float(number)
                        item2.log_entered_by = request.user.name
                    if  faulty != '0':
                        item2.faulty_carton = float(faulty)
                        item2.log_entered_by = request.user.name

            item2.save(update_fields=['sent_quantity','received_quantity','sent_carton_count','received_carton_count','log_entered_by',
                                      'faulty_carton','faulty_quantity',])
            good_request.save(update_fields=['req_to_godown'])
            return redirect('/stock_transaction_status/'+str(from_godown_id)+'/'+str(trans_id))

        if 'submit2' in request.POST:
            status = request.POST.get('status')

            good_request = GoodsRequest.objects.get(id=trans_id)
            admin = request.user.admin
            if status == 'Confirmation of goods transformation':
                good_request.status = 'Confirmation of goods transformation'
                good_request.save(update_fields=['status'])
                if good_request.goods_sent == False:
                    for good in requested_goods:

                        if good_request.req_to_godown :
                            godown_product_sent = GodownProduct.objects.get(godown_id=good_request.req_to_godown.id,
                                                            product_id=good.godown_product_id.product_id)
                            if godown_product_sent.quantity < good.sent_quantity:

                                messages.success(request, 'Insufficient Stock to Transfer, Please Update Your Stock!!!')

                            elif GodownProduct.objects.filter(godown_id=good_request.req_to_godown.id,
                                                            product_id=good.godown_product_id.product_id):
                                if good.req_type == 'Individual':
                                    GodownProduct.objects.filter(godown_id=good_request.req_to_godown.id,
                                                                 product_id=good.godown_product_id.product_id).update(
                                        quantity=F("quantity") - good.sent_quantity)
                                elif good.req_type == 'Carton':
                                    product = Product.objects.get(id=good.godown_product_id.product_id)
                                    individual_quantity = (float(product.carton_size) * float(good.sent_carton_count))
                                    GodownProduct.objects.filter(godown_id=good_request.req_to_godown.id,
                                                                 product_id=good.godown_product_id.product_id).update(
                                        quantity=F("quantity") - individual_quantity)
                                good_request.goods_sent = True
                                good_request.save(update_fields=['goods_sent',])
                                messages.success(request, 'Stock Transferred!!!')

                        else:
                            if good.req_type == 'Individual':
                                GodownProduct.objects.filter(godown_id=Godown.objects.get(id=godown.id),
                                                             product_id=good.godown_product_id.product_id).update(
                                    quantity=F("quantity") - good.sent_quantity)
                            elif good.req_type == 'Carton':
                                product = Product.objects.get(id=good.godown_product_id.product_id)
                                individual_quantity = (float(product.carton_size) * float(good.sent_carton_count))
                                GodownProduct.objects.filter(godown_id=Godown.objects.get(id=godown.id),
                                                             product_id=good.godown_product_id.product_id).update(
                                    quantity=F("quantity") - individual_quantity)
                            good_request.req_to_godown = Godown.objects.get(id=godown.id)
                            good_request.goods_sent = True
                            good_request.req_to_godown = Godown.objects.get(id=godown.id)
                            good_request.save(update_fields=['goods_sent','req_to_godown'])
                            messages.success(request, 'Stock Transferred!!!')

                return redirect('/stock_transaction_status/' + str(from_godown_id) + '/' + str(trans_id))

            if status == 'Confirms the transformation':
                good_request.status = 'Confirms the transformation'
                good_request.save(update_fields=['status'])
                if good_request.goods_received == False:

                    for good in requested_goods:
                        if GodownProduct.objects.filter(godown_id=from_godown_id, product_id=good.godown_product_id.product_id):
                            if good.req_type == 'Individual':
                                GodownProduct.objects.filter(godown_id=from_godown_id,
                                                             product_id=good.godown_product_id.product_id).update(
                                    quantity=F("quantity") + good.received_quantity)

                            elif good.req_type == 'Carton':
                                product = Product.objects.get(id=good.godown_product_id.product_id)
                                individual_quantity = (float(product.carton_size) * float(good.received_carton_count))

                                GodownProduct.objects.filter(godown_id=from_godown_id,
                                                             product_id=good.godown_product_id.product_id).update(
                                    quantity=F("quantity") + individual_quantity)
                            good_request.goods_received = True
                            good_request.save(update_fields=['goods_received',])

                            good_request.status = status
                            good_request.goods_received = True
                            good_request.save(update_fields=['status','req_to_godown','goods_received'])
            return redirect('/stock_pending_request/'+str(from_godown_id))
    context = {
        'good_request': good_request,
        'godown': godown,
        'requested_goods': requested_goods,
        'godown_assign_admin': godown_assign_admin,
        'godown_assign_employee': godown_assign_employee,

    }
    return render(request,'stock_management_system/stock_transaction_status.html',context)

def stock_accpet_goods(request, godown_id, accept_id):
    godown_goods = GodownProduct.objects.filter(godown_id=godown_id)
    accepted_goods = AGProducts.objects.filter(godown_id_id=godown_id,accept_product_id_id =accept_id).order_by('-id')
    if request.method == 'POST' or request.method == 'FILES':
        if 'submit1' in request.POST:
            product_id = request.POST.get('product_id')

            req_type = request.POST.get('req_type')
            number = request.POST.get('number')

            item2 = AGProducts()

            item2.type = req_type
            if req_type == 'Individual':
                item2.quantity = number
            elif req_type == 'Carton':
                product = Product.objects.get(id=product_id)
                individual_quantity = (float(product.carton_size) * float(number))
                item2.quantity = individual_quantity

            item2.godown_id = Godown.objects.get(id=godown_id)
            item2.godown_product_id = GodownProduct.objects.filter(product_id=product_id, godown_id=godown_id).first()
            item2.log_entered_by = request.user.name
            item2.save()
            if AcceptGoods.objects.filter(id=accept_id).count() == 0:
                item3 = AcceptGoods()
                item3.save()
            else:
                item3 = AcceptGoods.objects.get(id=accept_id)
            item2.accept_product_id = item3
            item2.save(update_fields=['accept_product_id', ])
            return redirect('/stock_accpet_goods/' + str(godown_id) + '/' + str(accept_id))
        elif 'submit2' in request.POST:
            notes = request.POST.get('notes')

            item2 = AcceptGoods.objects.get(id=accept_id)

            item2.from_godown = Godown.objects.get(id=godown_id)
            item2.good_added = True

            item2.log_entered_by = request.user.name
            item2.notes = notes
            item2.save(update_fields=['notes', 'log_entered_by', 'from_godown','good_added'])
            accepted_goods = AGProducts.objects.filter(godown_id_id=godown_id,accept_product_id_id =accept_id)
            for good in accepted_goods:
                if GodownProduct.objects.filter(godown_id=godown_id,product_id=good.godown_product_id.product_id):
                    godown_product = GodownProduct.objects.get(godown_id=godown_id,product_id=good.godown_product_id.product_id)
                    godown_product.quantity = float(godown_product.quantity) + float(good.quantity)
                    godown_product.log_entered_by = request.user.name
                    godown_product.save(update_fields=['quantity','log_entered_by'])
                else:
                    godown_product = GodownProduct()
                    godown_product.godown_id = Godown.objects.get(id=good.godown_id.id)
                    godown_product.product_id = Product.objects.get(id=good.godown_product_id.product_id.id)
                    godown_product.added_by_id = SiteUser.objects.get(id=request.user.id)
                    godown_product.quantity = good.quantity
                    godown_product.log_entered_by = request.user.name
                    godown_product.save()
            return redirect('/stock_accpet_goods_list/' + str(godown_id))

        elif 'submit3' in request.POST:
            request_id = request.POST.get('request_id')
            AGProducts.objects.get(id=request_id).delete()
            return redirect('/stock_accpet_goods/' + str(godown_id) + '/' + str(accept_id))

    context={
        'godown_goods': godown_goods,
        'accepted_goods': accepted_goods,
    }
    return render(request,'stock_management_system/stock_accpet_goods.html',context)

def stock_accpet_goods_list(request, godown_id):
    godown = Godown.objects.get(id=godown_id)
    if AcceptGoods.objects.all().count() == 0:
        new_accept_request_id = 1
    else:
        new_accept_request_id = AcceptGoods.objects.latest('id').id + 1
    accept_good_list = AcceptGoods.objects.filter(from_godown_id=godown_id).order_by('-id')
    context={
        'godown':godown,
        'new_accept_request_id':new_accept_request_id,
        'accept_good_list':accept_good_list,
    }
    return render(request,'stock_management_system/stock_accpet_goods_list.html',context)

def stock_transaction_history_list(request, godown_id):
    trans_history = GoodsRequest.objects.filter(req_from_godown=godown_id, status='Confirms the transformation').order_by('-id') | \
                    GoodsRequest.objects.filter(req_from_godown=godown_id, status='Confirms the transformation').order_by('-id') | \
                    GoodsRequest.objects.filter(Q(is_all_req=True) & Q(status='Confirms the transformation')).order_by('-id')

    context={
        'trans_history': trans_history,
    }
    return render(request,'stock_management_system/stock_transaction_history_list.html', context)

def stock_transaction_history(request, from_godown_id, trans_id):
    godown_id = Godown.objects.get(id=from_godown_id)
    good_request = GoodsRequest.objects.get(id=trans_id)
    requested_goods = RequestedProducts.objects.filter(godown_id=godown_id.id,goods_req_id =trans_id)

    from_godown_initial_data = {
        'name_of_godown': good_request.req_from_godown.name_of_godown,
        'goddown_assign_to': good_request.req_from_godown.goddown_assign_to.profile_name,
        'location': good_request.req_from_godown.location,
        'contact_no': good_request.req_from_godown.contact_no,
    }
    to_godown_initial_data= {
        'name_of_godown': good_request.req_to_godown.name_of_godown,
        'goddown_assign_to': good_request.req_to_godown.goddown_assign_to.profile_name,
        'location': good_request.req_to_godown.location,
        'contact_no': good_request.req_to_godown.contact_no,
    }
    from_godown_form = GodownForm(initial=from_godown_initial_data)
    to_godown_form = GodownForm(initial=to_godown_initial_data)
    context={
        'from_godown_form':from_godown_form,
        'to_godown_form':to_godown_form,
        'good_request':good_request,
        'requested_goods':requested_goods,
    }
    return render(request, 'stock_management_system/stock_transaction_history.html',context)


def request_admin(request):
    request_admin_list= GoodsRequest.objects.filter(Q(request_admin=True)& Q(req_from_godown__godown_admin__id=request.user.id)).order_by('-id') | \
                        GoodsRequest.objects.filter(Q(request_admin=True) & Q(request_admin_id__id=request.user.id)).order_by('-id')
    outside_workarea_admins = Godown.objects.filter(~Q(godown_admin__id=request.user.id)).values_list('godown_admin__id','godown_admin__name').distinct()
    admin_godowns = Godown.objects.filter(Q(godown_admin__id=request.user.id)).values_list('id','name_of_godown').distinct()
    context = {
        'request_admin_list': request_admin_list,
        'outside_workarea_admins': outside_workarea_admins,
        'admin_godowns': admin_godowns,
    }
    if request.method == 'POST' or request.method == 'FILES':
        if 'request_accepted' in request.POST:
            good_req = request.POST.get('good_req')
            accept_to_godown = request.POST.get('accept_to_godown')
            good_request = GoodsRequest.objects.get(id=good_req)
            good_request.request_admin = False
            good_request.req_to_godown = Godown.objects.get(id=accept_to_godown)
            good_request.save(update_fields=['request_admin','req_to_godown'])
            messages.success(request, 'Request Accepted to the Selected Godown')

        elif 'request_send' in request.POST:
            good_req = request.POST.get('good_req')
            outside_admin_id = request.POST.get('outside_admin')
            good_request = GoodsRequest.objects.get(id=good_req)
            good_request.request_admin_id = SiteUser.objects.get(id=outside_admin_id)
            good_request.save(update_fields=['request_admin_id'])
            messages.success(request, 'Request Send to Admin')


    return render(request,'stock_management_system/request_admin_page.html',context)