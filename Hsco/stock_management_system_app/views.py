from django.db.models import Q, F
from django.shortcuts import render, redirect

from customer_app.models import type_purchase
from .forms import GodownForm
from .models import Godown, GodownProduct, RequestedProducts, GoodsRequest, Product, AGProducts, AcceptGoods
from user_app.models import SiteUser


def stock_godown_list(request):
    if request.user.role == 'Admin':
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
    assign_users = SiteUser.objects.filter(modules_assigned__icontains= 'Stock', admin__contains= request.user.profile_name)

    godown_initial_data = {
        'name_of_godown': godown.name_of_godown,
        'goddown_assign_to': godown.goddown_assign_to,
        'location': godown.location,
        'contact_no': godown.contact_no,
    }
    form = GodownForm(initial=godown_initial_data)
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
            return redirect('/update_godown/'+str(godown_id))
        if 'submit2' in request.POST:
            product_id = request.POST.get('product_id')
            GodownProduct.objects.get(id=product_id).delete()
            return redirect('/update_godown/'+str(godown_id))


    context={
        'godown': godown,
        'form': form,
        'godown_products': godown_products,
        'assign_users': assign_users,
    }
    return render(request, 'stock_management_system/update_godown.html',context)

def add_product_godown(request, godown_id):
    godown = Godown.objects.get(id=godown_id)
    type_of_purchase_list =type_purchase.objects.all() #1
    context = {
        'godown': godown,
        'type_of_purchase_list': type_of_purchase_list,

    }
    if request.method == 'POST' or request.method == 'FILES':
        carton_count = request.POST.get('carton_count')
        quantity = request.POST.get('quantity')
        is_last_product_yes = request.POST.get('is_last_product_yes')
        # model_of_purchase = request.POST.get('model_of_purchase')
        type_of_scale = request.POST.get('scale_type')
        main_category = request.POST.get('main_category')
        sub_category = request.POST.get('sub_category')
        sub_sub_category = request.POST.get('sub_sub_category')    #product code or sub_sub_category

        item = GodownProduct()
        if sub_sub_category != '':
            item.product_id = Product.objects.get(scale_type=type_of_scale, main_category=main_category,
                                                  sub_category=sub_category, sub_sub_category=sub_sub_category)
        item.godown_id = Godown.objects.get(id=godown_id)
        item.added_by_id = SiteUser.objects.get(id=request.user.id)
        item.quantity = quantity
        item.carton_count = carton_count
        item.log_entered_by = request.user.name
        item.save()

        if is_last_product_yes == 'yes':
            return redirect('/update_godown/' + str(godown_id))
        elif is_last_product_yes == 'no':
            return redirect('/add_product_godown/' + str(godown_id))

    return render(request, 'stock_management_system/add_product_godown.html',context)


def stock_godown(request,id):
    godown_id = Godown.objects.get(id=id)
    godown_products = GodownProduct.objects.filter(godown_id=id)

    if GoodsRequest.objects.all().count() == 0:
        new_good_request_id = 1
    else:
        new_good_request_id = GoodsRequest.objects.latest('id').id + 1



    context={
     'godown_id':godown_id,
     'new_good_request_id':new_good_request_id,
     'godown_products':godown_products,
    }
    return render(request,'stock_management_system/stock_godown.html',context)

def stock_godown_images(request):
    return render(request,'stock_management_system/stock_godown_images.html')

def stock_good_request(request,godown_id, request_id):
    # good_request = GoodsRequest.objects.get(id=request_id)
    godowns = Godown.objects.all()
    godown_goods = GodownProduct.objects.filter(godown_id=godown_id)
    requested_goods = RequestedProducts.objects.filter(godown_id=godown_id,goods_req_id =request_id)
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
            else:
                item2.req_to_godown = Godown.objects.get(id=req_to_godown)
            item2.log_entered_by = request.user.name
            item2.entered_by = SiteUser.objects.get(id=request.user.id)
            item2.status = 'Pending From Target'
            item2.save(update_fields=['req_from_godown','is_all_req','req_to_godown','log_entered_by','entered_by','status',])
            return redirect('/stock_godown/'+str(godown_id))

        elif 'submit3' in request.POST:
            request_id = request.POST.get('request_id')
            RequestedProducts.objects.get(id=request_id).delete()


    context={
        'godown_goods':godown_goods,
        'requested_goods':requested_goods,
        'godowns':godowns,
    }
    return render(request,'stock_management_system/stock_good_request.html',context)

def stock_pending_request(request,godown_id):
    godown = Godown.objects.get(id=godown_id)
    admin = request.user.admin

    pending_list = GoodsRequest.objects.filter(~Q(status='Confirms the transformation')&~Q(status=None)&Q(req_to_godown__goddown_assign_to__admin=admin)).order_by('-id')    | \
                   GoodsRequest.objects.filter(~Q(status='Confirms the transformation')&~Q(status=None)&Q(req_from_godown__goddown_assign_to__admin=admin)).order_by('-id') | \
                   GoodsRequest.objects.filter(Q(is_all_req=True)&~Q(status='Confirms the transformation')&~Q(status=None)&Q(req_to_godown__goddown_assign_to__admin=None)).order_by('-id')
    context = {
        'godown_id': godown,
        'pending_list': pending_list,
    }
    return render(request,'stock_management_system/stock_pending_request.html',context)

def stock_transaction_status(request,from_godown_id, trans_id):
    good_request = GoodsRequest.objects.get(id=trans_id)
    godown = Godown.objects.get(id=from_godown_id)
    requested_goods = RequestedProducts.objects.filter(godown_id=from_godown_id,goods_req_id =good_request)
    if request.method == 'POST' or request.method == 'FILES':
        if 'submit1' in request.POST:
            number = request.POST.get('number')
            req_type = request.POST.get('req_type')
            product_id = request.POST.get('product_id')
            faulty = request.POST.get('faulty')

            item2 = RequestedProducts.objects.get(id=product_id)
            if req_type == 'Individual':
                if good_request.status == 'Pending From Target':
                    if number != '0':
                        item2.sent_quantity = float(number)
                        item2.log_entered_by = request.user.name
                elif good_request.status == 'Confirmation of goods transformation':
                    if number != '0' :
                        item2.received_quantity = float(number)
                        item2.log_entered_by = request.user.name
                    if faulty != '0':
                        item2.faulty_quantity = float(faulty)
                        item2.log_entered_by = request.user.name

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
                                      'faulty_carton','faulty_quantity'])
            return redirect('/stock_transaction_status/'+str(from_godown_id)+'/'+str(trans_id))

        if 'submit2' in request.POST:
            status = request.POST.get('status')
            good_request = GoodsRequest.objects.get(id=trans_id)
            admin = request.user.admin
            if status == 'Confirmation of goods transformation':
                if good_request.req_to_godown == '' or 'None':
                    good_request.req_to_godown = Godown.objects.filter(goddown_assign_to__name=admin).first()
                    good_request.save(update_fields=['req_to_godown'])
                if good_request.goods_sent == False:
                    for good in requested_goods:
                        if GodownProduct.objects.filter(godown_id=good_request.req_to_godown.id,
                                                        product_id=good.godown_product_id.product_id):
                            # subtracting  the products quantity from sent godown
                            # sub_godown_product = GodownProduct.objects.get(godown_id=good_request.req_to_godown.id,
                            #                                                product_id=good.godown_product_id.product_id)
                            # sub_godown_product.quantity = float(sub_godown_product.quantity) - float(good.sent_quantity)
                            # sub_godown_product.carton_count = float(sub_godown_product.carton_count) - float(
                            #     good.sent_carton_count)
                            GodownProduct.objects.filter(godown_id=good_request.req_to_godown.id,
                                                         product_id=good.godown_product_id.product_id).update(
                                quantity=F("quantity") - good.sent_quantity)
                            GodownProduct.objects.filter(godown_id=good_request.req_to_godown.id,
                                                         product_id=good.godown_product_id.product_id).update(
                                carton_count=F("carton_count") - good.sent_carton_count)


                            good_request.goods_sent = True
                            good_request.save(update_fields=['goods_sent',])
            if status == 'Confirms the transformation':
                if good_request.goods_received == False:

                    for good in requested_goods:
                        if GodownProduct.objects.filter(godown_id=from_godown_id, product_id=good.godown_product_id.product_id):
                            GodownProduct.objects.filter(godown_id=from_godown_id,
                                                         product_id=good.godown_product_id.product_id).update(
                                quantity=F("quantity") + good.received_quantity)
                            GodownProduct.objects.filter(godown_id=from_godown_id,
                                                         product_id=good.godown_product_id.product_id).update(
                                carton_count=F("carton_count") + good.received_carton_count)
                            good_request.goods_received = True
                            good_request.save(update_fields=['goods_received',])
            good_request.status = status
            good_request.save(update_fields=['status',])
            return redirect('/stock_pending_request/'+str(from_godown_id))
    context = {
        'good_request': good_request,
        'godown': godown,
        'requested_goods': requested_goods,

    }
    return render(request,'stock_management_system/stock_transaction_status.html',context)

def stock_accpet_goods(request, godown_id, accept_id):
    godown_goods = GodownProduct.objects.filter(godown_id=godown_id)
    accepted_goods = AGProducts.objects.filter(godown_id_id=godown_id,accept_product_id_id =accept_id)
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
                item2.carton_count = number
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
                    godown_product.carton_count = float(godown_product.carton_count) + float(good.carton_count)
                    godown_product.log_entered_by = request.user.name
                    godown_product.save(update_fields=['quantity','carton_count','log_entered_by'])
                else:
                    godown_product = GodownProduct()
                    godown_product.godown_id = Godown.objects.get(id=good.godown_id.id)
                    godown_product.product_id = Product.objects.get(id=good.godown_product_id.product_id.id)
                    godown_product.added_by_id = SiteUser.objects.get(id=request.user.id)
                    godown_product.quantity = good.quantity
                    godown_product.carton_count = good.carton_count
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