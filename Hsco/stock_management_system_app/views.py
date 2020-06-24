import calendar

from django.contrib import messages
from django.db.models import Q, F, Sum
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from customer_app.models import type_purchase
from .forms import GodownForm
from .models import Godown, GodownProduct, RequestedProducts, GoodsRequest, Product, AGProducts, AcceptGoods, \
    GodownTransactions, DailyStock
from user_app.models import SiteUser
from customer_app.models import sub_model, main_model, sub_sub_model, type_purchase
from purchase_app.models import Product_Details

from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver

# @receiver(post_save, sender=GodownProduct)
# def purchase_handler(sender, instance, update_fields=None, **kwargs):
#     try:
#         if instance.id == None or instance.id == '' or instance.id == 'None' :
#             #########for insert action##########
#             new_instance = instance
#             log = GodownTransactions()
#
#             log.entered_by = new_instance.log_entered_by
#             log.module_name = 'Purchase Module'
#             log.action_type = 'Insert'
#             log.table_name = 'Purchase_Details'
#
#             log.reference = 'Purchase No: ' + str(new_instance.purchase_no)
#
#             # log.action = old_list
#             log.save()
#         elif instance.id != None or instance.id !='' or instance.id !='None':
#
#             #########for update action##########
#             old_instance = instance
#             new_instance = Purchase_Details.objects.get(id=instance.id)
#
#             track = instance.tracker.changed()
#             if 'log_entered_by' in track :
#                 del track['log_entered_by']
#             # string = ''
#             # new_list = []
#             # for key in track:
#             #     new_list.append(key)
#             #     string = string+str(key)+','
#             #     print('New value:'+str(key) + old_instance.key)
#
#
#             # with connection.cursor() as cursor:
#                 # if new_string != '' :
#                 #     print('something 1')
#                 #     new = Repairing_after_sales_service.objects.filter(id=instance.id).values(new_list)
#                 #     cursor.execute("SELECT " + (
#                 #                 new_string ) + " from  repairing_app_repairing_after_sales_service "
#                 #                                                                " where repairing_app_repairing_after_sales_service.repairing_no = '"+new_instance.repairing_no+"' ;")
#             if  track:
#                 old_list = []
#                 for key, value in track.items():
#                     if value != '' and str(value) != getattr(instance,key):
#                         old_list.append(key +':Old value= '+str(value) + ', New value='+getattr(instance,key) )
#                 log = Log()
#                 log.entered_by = instance.log_entered_by
#                 log.module_name = 'Purchase Module'
#                 log.action_type = 'Update'
#                 log.table_name = 'Purchase_Details'
#
#                 log.reference = 'Purchase No: '+str(new_instance.purchase_no)
#
#                 log.action = old_list
#                 if old_list != []:
#                     log.save()
#
#     except:
#         pass

@login_required(login_url='/')
def product_master_list(request):
    context={}
    product_list = Product.objects.all().order_by('-id')
    if request.method == 'GET' and 'success' in request.GET:
        if request.GET['success']== 'true':
            context22={
                'added_product':True,
            }
            context.update(context22)
        elif request.GET['success']== 'false':
            if 'msg' in request.GET:
                context22 = {
                    'not_added_product': True,
                    'msg': request.GET['msg'],
                }
                context.update(context22)
            else:
                context22={
                    'not_added_product':True,
                }
                context.update(context22)

    context25={
        'product_list': product_list,
    }
    context.update(context25)
    return render(request, 'stock_management_system/product_master_list.html',context)

@login_required(login_url='/')
def update_product_master(request,update_id):
    product_obj = Product.objects.get(id=update_id)
    type_of_purchase_list = type_purchase.objects.all()
    if request.method == 'POST':
        scale_type = request.POST.get('scale_type')
        main_category = request.POST.get('main_category')
        sub_category = request.POST.get('sub_category')
        sub_sub_category = request.POST.get('sub_sub_category')
        hsn_code = request.POST.get('hsn_code')
        max_capacity = request.POST.get('max_capacity')
        accuracy = request.POST.get('accuracy')
        platform_size = request.POST.get('platform_size')
        product_desc = request.POST.get('product_desc')
        cost_price = request.POST.get('cost_price')
        selling_price = request.POST.get('selling_price')
        carton_size = request.POST.get('carton_size')
        product_image = request.FILES.get('product_image')
        product_brochure = request.FILES.get('product_brochure')
        product_document = request.FILES.get('product_document')

        fol_pro = product_obj
        # fol_pro.scale_type = type_purchase.objects.get(id=scale_type)
        # fol_pro.main_category = main_model.objects.get(id=main_category)
        # fol_pro.sub_category = sub_model.objects.get(id=sub_category)
        # fol_pro.sub_sub_category = sub_sub_model.objects.get(id=sub_sub_category)
        fol_pro.hsn_code = hsn_code
        fol_pro.max_capacity = max_capacity
        fol_pro.accuracy = accuracy
        fol_pro.platform_size = platform_size
        fol_pro.product_desc = product_desc
        fol_pro.cost_price = cost_price
        fol_pro.selling_price = selling_price
        fol_pro.carton_size = carton_size
        if product_image != None and product_image != '':
            fol_pro.product_image = product_image
            fol_pro.save(update_fields=['product_image',])
        if product_brochure != None and product_brochure != '':
            fol_pro.product_brochure = product_brochure
            fol_pro.save(update_fields=['product_brochure', ])
        if product_document != None and product_document != '':
            fol_pro.product_document = product_document
            fol_pro.save(update_fields=['product_document', ])

        fol_pro.save(update_fields=['hsn_code','max_capacity','accuracy','platform_size',
                                    # 'product_desc','cost_price','selling_price','carton_size',])
                                    'product_desc','cost_price','selling_price','carton_size',])

        return redirect('/product_master_list/')
    context={
        'product_obj':product_obj,
        'type_purchase': type_of_purchase_list,
    }
    return render(request, 'stock_management_system/update_product_master.html',context)

@login_required(login_url='/')
def add_product_master(request):
    type_of_purchase_list = type_purchase.objects.all()
    context = {}

    if request.method == 'POST' or request.method == 'FILES' :
        if 'scale_type' in request.POST and 'send_submit' not in request.POST:

            is_last_product_yes = request.POST.get('is_last_product_yes')
            scale_type = request.POST.get('scale_type')
            main_category = request.POST.get('main_category')
            sub_category = request.POST.get('sub_category')
            sub_sub_category = request.POST.get('sub_sub_category')
            hsn_code = request.POST.get('hsn_code')
            max_capacity = request.POST.get('max_capacity')
            accuracy = request.POST.get('accuracy')
            platform_size = request.POST.get('platform_size')
            product_desc = request.POST.get('product_desc')
            cost_price = request.POST.get('cost_price')
            selling_price = request.POST.get('selling_price')
            carton_size = request.POST.get('carton_size')
            product_image = request.FILES.get('product_image')
            product_brochure = request.FILES.get('product_brochure')
            product_document = request.FILES.get('product_document')

            if request.POST.get('sub_sub_category') != None and request.POST.get('sub_sub_category') !='' and len(sub_sub_category) > 0:

                if Product.objects.filter(scale_type__id=request.POST.get('scale_type'), main_category__id=request.POST.get('main_category'),
                                             sub_category__id=request.POST.get('sub_category'), sub_sub_category__id=request.POST.get('sub_sub_category')).count()>0:
                    context2={
                        'product_already_exist':True
                    }
                    context.update(context2)
                else:

                    fol_pro = Product()
                    fol_pro.scale_type = type_purchase.objects.get(id=scale_type)
                    fol_pro.main_category = main_model.objects.get(id=main_category)
                    fol_pro.sub_category = sub_model.objects.get(id=sub_category)
                    fol_pro.sub_sub_category = sub_sub_model.objects.get(id=sub_sub_category)
                    fol_pro.hsn_code = hsn_code
                    fol_pro.max_capacity = max_capacity
                    fol_pro.accuracy = accuracy
                    fol_pro.platform_size = platform_size
                    fol_pro.product_desc = product_desc
                    fol_pro.cost_price = cost_price
                    fol_pro.selling_price = selling_price
                    fol_pro.carton_size = carton_size
                    fol_pro.product_image = product_image
                    fol_pro.product_brochure = product_brochure
                    fol_pro.product_document = product_document
                    fol_pro.log_entered_by = request.user.name

                    try:
                        fol_pro.save()
                        if is_last_product_yes == 'yes':
                            return redirect('/product_master_list/?success=true')
                    except Exception as e:
                        if is_last_product_yes == 'yes':
                            return redirect('/product_master_list/?success=false&?msg='+str(e))
                    # elif is_last_product_yes == 'no':
                    #     return redirect('/add_product_master/')

            if request.POST.get('sub_sub_category') == None or request.POST.get('sub_sub_category') ==''  or len(sub_sub_category) < 1:

                if Product.objects.filter(scale_type__id=request.POST.get('scale_type'), main_category__id=request.POST.get('main_category'),
                                             sub_category__id=request.POST.get('sub_category')).count()>0:
                    context2={
                        'product_already_exist':True
                    }
                    context.update(context2)

                else:

                    fol_pro=Product()
                    fol_pro.scale_type = type_purchase.objects.get(id=scale_type)
                    fol_pro.main_category = main_model.objects.get(id=main_category)
                    fol_pro.sub_category = sub_model.objects.get(id=sub_category)
                    # fol_pro.sub_sub_category = sub_sub_model.objects.get(id=sub_sub_category)
                    fol_pro.hsn_code = hsn_code
                    fol_pro.max_capacity = max_capacity
                    fol_pro.accuracy = accuracy
                    fol_pro.platform_size = platform_size
                    fol_pro.product_desc = product_desc
                    fol_pro.cost_price = cost_price
                    fol_pro.selling_price = selling_price
                    fol_pro.carton_size = carton_size
                    fol_pro.product_image = product_image
                    fol_pro.product_brochure = product_brochure
                    fol_pro.product_document = product_document
                    fol_pro.log_entered_by = request.user.name
                    try:
                        fol_pro.save()
                        if is_last_product_yes == 'yes':
                            return redirect('/product_master_list/?success=true')
                    except Exception as e:
                        if is_last_product_yes == 'yes':
                            return redirect('/product_master_list/?success=false&?msg='+str(e))


                    # elif is_last_product_yes == 'no':
                    #     return redirect('/add_product_master/')


        if 'send_submit' in request.POST:
            scale_type = request.POST.get('scale_type')
            scale_type_d = request.POST.get('scale_type_d')
            main_category = request.POST.get('main_category')
            main_category_d = request.POST.get('main_category_d')
            sub_category = request.POST.get('sub_category')
            sub_category_d = request.POST.get('sub_category_d')
            sub_sub_category = request.POST.get('sub_sub_category')

            scale_type = scale_type if len(scale_type)>1 else scale_type_d
            main_category = main_category if len(main_category)>1 else main_category_d if main_category_d!=None and main_category_d !='' else None
            sub_category = sub_category if len(sub_category)>1 else sub_category_d if sub_category_d!=None and sub_category_d !='' else None
            sub_sub_category = sub_sub_category if len(sub_sub_category)>1 and sub_sub_category != None else None


            try:
                type=type_purchase.objects.filter(Q(id = scale_type))
            except:
                type=type_purchase.objects.filter(Q(name=scale_type))

            if type.count()>0:
                try:
                    item=type_purchase.objects.get(Q(id = scale_type))
                except:
                    item = type_purchase.objects.get(Q(name=scale_type))
                # context22 = {
                #     'already_exist': True,
                #     'already_exist_msg': 'Scale Type: '+scale_type + 'Already Exist!!!' ,
                # }
                # context.update(context22)
            else:
                item = type_purchase()
                item.name = scale_type
                item.save()
                context22={
                    'already_dont_exist': True,
                    'scale_type' : item
                }
                context.update(context22)

            if main_category != None:
                try:
                    main = main_model.objects.filter(Q(id=main_category))
                except:
                    main = main_model.objects.filter(Q(name=main_category))

                if main.count() > 0:
                    try:
                        item2 = main_model.objects.get(Q(id = main_category))
                    except:
                        item2 = main_model.objects.get(Q(name = main_category))

                    # context22 = {
                    #     'already_exist': True,
                    #     'already_exist_msg': 'Main Category: ' + main_category + 'Already Exist!!!',
                    # }
                    # context.update(context22)
                else:
                    item2 = main_model()
                    item2.name = main_category
                    item2.type_purchase = item
                    item2.save()
                    context22 = {
                        'already_dont_exist_main': True,
                        'main_category': item2
                    }
                    context.update(context22)

            if sub_category != None:
                try:
                    sub = sub_model.objects.filter(Q(id=sub_category))
                except:
                    sub = sub_model.objects.filter(Q(name = sub_category))

                if sub.count() > 0:
                    try:
                        item3 = sub_model.objects.get(Q(id = sub_category))
                    except:
                        item3 = sub_model.objects.get(Q(name=sub_category))


                    # context22 = {
                    #     'already_exist': True,
                    #     'already_exist_msg': 'Sub Category: ' + sub_category + 'Already Exist!!!',
                    # }
                    # context.update(context22)
                else:
                    item3 = sub_model()
                    item3.name = sub_category
                    item3.main_model = item2
                    item3.save()
                    context22 = {
                        'already_dont_exist_sub': True,
                        'sub_category': item3
                    }
                    context.update(context22)

            if sub_sub_category != None and sub_sub_category != 'None':
                sub_sub= sub_sub_model.objects.filter(name=sub_sub_category)
                if (sub_sub_category!= None or sub_sub_category!= '') and sub_sub.count() > 0 :
                    context22 = {
                        'already_exist': True,
                        'already_exist_msg': 'Sub Sub Category: ' + sub_sub_category + 'Already Exist!!!',
                    }
                    context.update(context22)

                else:
                    item4 = sub_sub_model()
                    item4.name = sub_sub_category
                    item4.sub_model = item3
                    item4.save()
                    context22 = {
                        'already_dont_exist_sub_sub': True,
                        'sub_sub_category': item4
                    }
                    context.update(context22)

    context22={
        'type_purchase':type_of_purchase_list,

    }
    context.update(context22)
    return render(request,'stock_management_system/add_product_master.html',context)

@login_required(login_url='/')
def stock_godown_list(request):
    if request.user.role == 'Super Admin':
        godown_list = Godown.objects.all().order_by('-id')
    elif request.user.role == 'Admin':
        godown_list = Godown.objects.filter(godown_admin__id=request.user.id).order_by('-id')
    else:
        godown_list = Godown.objects.filter(goddown_assign_to__id=request.user.id).order_by('-id') | \
                    Godown.objects.filter(godown_admin__profile_name=request.user.admin).order_by('-id')

    request_admin_indication = GoodsRequest.objects.filter(Q(req_from_godown__godown_admin__id=request.user.id) &
     Q(request_admin=True) & Q(request_admin_id=None)) | \
     GoodsRequest.objects.filter(~Q(req_from_godown__godown_admin__id=request.user.id) &Q(request_admin=True)
                                 & ~Q(request_admin_id = None)& Q(req_to_godown = None))

    context = {
        'godown_list':godown_list,
        'request_admin_indication':request_admin_indication,
    }
    return render(request,'stock_management_system/stock_godown_list.html',context)

@login_required(login_url='/')
def add_godown(request):
    products = Product.objects.all()

    if request.user.role == 'Super Admin':
        assign_users = SiteUser.objects.all()
    elif request.user.role == 'Admin':
        assign_users = SiteUser.objects.filter(modules_assigned__icontains= 'Stock', admin__contains= request.user.profile_name)| \
                       SiteUser.objects.filter(modules_assigned__icontains='Stock', id = request.user.id)

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
        messages.success(request, "Godown Created Please Add Products")

        return redirect('/update_godown/'+str(item.id))

    context = {
        'form':form,
        'products':products,
        'assign_users':assign_users,
    }
    return render(request, 'stock_management_system/add_godown.html',context)

@login_required(login_url='/')
def update_godown(request,godown_id):
    godown = Godown.objects.get(id=godown_id)
    godown_products = GodownProduct.objects.filter(godown_id=godown_id)
    if request.user.role == 'Super Admin':
        assign_users = SiteUser.objects.filter(~Q(id=godown.goddown_assign_to.id))
    else:
        assign_users = SiteUser.objects.filter(Q(modules_assigned__icontains= 'Stock')&Q(admin__contains= request.user.profile_name)
                                               )| \
                       SiteUser.objects.filter(Q(modules_assigned__icontains='Stock')&Q(id=request.user.id))

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

            GodownProduct.objects.get(godown_id=godown_id,id=product_id).delete()
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
        if 'update_stock' in request.POST:
            quantity = request.POST.get('quantity')
            individual_faulty = request.POST.get('individual_faulty')
            carton_count = request.POST.get('carton_count')
            product_id = request.POST.get('product_id')
            product_master_id = request.POST.get('product_master_id')

            faulty_type = request.POST.get('faulty_type')
            convert_faulty_quantity = request.POST.get('convert_faulty_quantity')


            if faulty_type != None and convert_faulty_quantity != None and convert_faulty_quantity != '0':
                if faulty_type == 'Repaired':
                    GodownProduct.objects.filter(godown_id=godown_id, id=product_id).update(
                        individual_faulty=float(individual_faulty) - float(convert_faulty_quantity))
                    GodownProduct.objects.filter(godown_id=godown_id, id=product_id).update(
                        quantity=float(quantity) + float(convert_faulty_quantity))

                    messages.success(request, convert_faulty_quantity+ " Product shifted from Faulty to Repaired!!! ")
                    #save transaction
                    new_transaction = GodownTransactions()
                    new_transaction.godown_product_id = GodownProduct.objects.get(id=product_id)
                    new_transaction.adjustment_quantity = convert_faulty_quantity
                    new_transaction.notes = 'Adjustment - Faulty to Repaired by id:'+request.user.employee_number+', Name:'+request.user.profile_name+', Contact:'+request.user.mobile
                    new_transaction.save()

                    return redirect('/update_godown/'+str(godown_id))
                elif faulty_type == 'Scrap':
                    GodownProduct.objects.filter(godown_id=godown_id, id=product_id).update(
                        individual_faulty=float(individual_faulty) - float(convert_faulty_quantity) )
                    messages.success(request, convert_faulty_quantity+ " Product shifted from Faulty to Scrap!!! ")
                    # save transaction
                    new_transaction = GodownTransactions()
                    new_transaction.godown_product_id = GodownProduct.objects.get(id=product_id)
                    new_transaction.loss_quantity = convert_faulty_quantity
                    new_transaction.notes = 'Loss - Faulty to Scrap by id:'+request.user.employee_number+', Name:'+request.user.profile_name+', Contact:'+request.user.mobile
                    new_transaction.save()
                    return redirect('/update_godown/'+str(godown_id))
            product_carton_count = GodownProduct.objects.get(godown_id=godown_id, id=product_id).carton_count
            product_quantity = GodownProduct.objects.get(godown_id=godown_id, id=product_id).quantity
            format_carton_count ="{:.2f}".format(float(product_carton_count))
            if float(format_carton_count) !=  float(carton_count):

                product = Product.objects.get(id=product_master_id)
                individual_quantity = (float(product.carton_size) * float(carton_count))

                GodownProduct.objects.filter(godown_id=godown_id, id=product_id).update(
                    quantity=individual_quantity)
                new_transaction = GodownTransactions()
                new_transaction.godown_product_id = GodownProduct.objects.get(id=product_id)
                new_transaction.adjustment_quantity = float(carton_count) - float(product_carton_count)
                new_transaction.notes = 'Adjustment in stock by id:' + request.user.employee_number + ', Name:' + request.user.profile_name + ', Contact:' + request.user.mobile+'\nOld Carton Count: '+str(product_carton_count)+', New Carton Count: '+str(carton_count)
                new_transaction.save()
                messages.success(request, "Product updated !!! Carton Quantity:- "+carton_count )

            elif float(product_quantity) != float(quantity):
                GodownProduct.objects.filter(godown_id=godown_id, id=product_id).update(
                    quantity=quantity)
                new_transaction = GodownTransactions()
                new_transaction.godown_product_id = GodownProduct.objects.get(id=product_id)
                new_transaction.adjustment_quantity = float(quantity) - float(product_quantity)
                new_transaction.notes = 'Adjustment in stock by id:' + request.user.employee_number + ', Name:' + request.user.profile_name + ', Contact:' + request.user.mobile + '\nOld Carton Count: '+str(product_quantity)+', New Carton Count: '+str(quantity)
                new_transaction.save()
                messages.success(request, "Product updated!!! Individual Quantity:- "+quantity)
            return redirect('/update_godown/' + str(godown_id))

    return render(request, 'stock_management_system/update_godown.html',context)

@login_required(login_url='/')
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
                Godown_product_filter = GodownProduct.objects.filter(godown_id=godown_id,product_id__scale_type=type_of_scale,product_id__main_category=main_category,
                product_id__sub_category=sub_category,product_id__sub_sub_category=sub_sub_category)
                if Godown_product_filter.count() > 0:
                    if req_type == 'Individual':
                        Godown_product_filter.update(
                        quantity=F("quantity") + quantity)
                        if critical_limit != '0' and critical_limit != '' and critical_limit != 'None':
                            Godown_product_filter.update(
                                critical_limit= critical_limit)
                    elif req_type == 'Carton':
                        product = Product.objects.get(scale_type=type_of_scale, main_category=main_category,
                                                      sub_category=sub_category, sub_sub_category=sub_sub_category)
                        individual_quantity = (float(product.carton_size) * float(quantity))

                        Godown_product_filter.update(
                        quantity=F("quantity") + individual_quantity)
                        if critical_limit != '0' and critical_limit != '' and critical_limit != 'None':
                            individual_critical_limit = (float(product.carton_size) * float(critical_limit))
                            Godown_product_filter.update(
                                critical_limit=individual_critical_limit)

                else:

                    item.product_id = Product.objects.get(scale_type__id=type_of_scale, main_category__id=main_category,
                                                          sub_category__id=sub_category, sub_sub_category__id=sub_sub_category)

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
            elif sub_category != '':
                Godown_product_filter = GodownProduct.objects.filter(godown_id=godown_id,
                                                                     product_id__scale_type=type_of_scale,
                                                                     product_id__main_category=main_category,
                                                                     product_id__sub_category=sub_category,
                                                                     product_id__sub_sub_category=None)
                if Godown_product_filter.count() > 0:
                    if req_type == 'Individual':
                        Godown_product_filter.update(
                            quantity=F("quantity") + quantity)
                        if critical_limit != '0' and critical_limit != '' and critical_limit != 'None':
                            Godown_product_filter.update(
                                critical_limit=critical_limit)
                    elif req_type == 'Carton':
                        product = Product.objects.get(scale_type=type_of_scale, main_category=main_category,
                                                      sub_category=sub_category, sub_sub_category=None)
                        individual_quantity = (float(product.carton_size) * float(quantity))

                        Godown_product_filter.update(
                            quantity=F("quantity") + individual_quantity)
                        if critical_limit != '0' and critical_limit != '' and critical_limit != 'None':
                            individual_critical_limit = (float(product.carton_size) * float(critical_limit))
                            Godown_product_filter.update(
                                critical_limit=individual_critical_limit)

                else:

                    item.product_id = Product.objects.get(scale_type__id=type_of_scale, main_category__id=main_category,
                                                          sub_category__id=sub_category,
                                                          sub_sub_category__id=None)

                    item.godown_id = Godown.objects.get(id=godown_id)
                    item.added_by_id = SiteUser.objects.get(id=request.user.id)
                    if req_type == 'Individual':
                        if quantity != '' and 'None':
                            item.quantity = quantity
                        if critical_limit != '' and 'None':
                            item.critical_limit = critical_limit
                    elif req_type == 'Carton':
                        product = Product.objects.get(scale_type=type_of_scale, main_category=main_category,
                                                      sub_category=sub_category, sub_sub_category=None)
                        individual_quantity = (float(product.carton_size) * float(quantity))
                        individual_critical_limit = (float(product.carton_size) * float(critical_limit))
                        if quantity != '' and 'None':
                            item.quantity = individual_quantity
                        if critical_limit != '' and 'None':
                            item.critical_limit = individual_critical_limit
                    else:
                        item.quantity = 0.0

                    item.log_entered_by = request.user.name
                    item.save()

            if is_last_product_yes == 'yes':
                messages.success(request, "Product Added Successfully")
                return redirect('/update_godown/' + str(godown_id))
            elif is_last_product_yes == 'no':
                messages.success(request, "Product Added Successfully, Add Another")
                return redirect('/add_product_godown/' + str(godown_id))
        except Exception as e:
            print(e)
            msg = "Selected Product does not exist in Main Product Database Table!!!"
            context1={
                'msg':msg,
            }
            context.update(context1)

    return render(request, 'stock_management_system/add_product_godown.html',context)


@login_required(login_url='/')
def stock_godown(request,id):
    type_of_purchase_list =type_purchase.objects.all() #1
    products = Product.objects.all()
    godown_id = Godown.objects.get(id=id)
    godown_products = GodownProduct.objects.filter(godown_id=id)

    if GoodsRequest.objects.all().count() == 0:
        new_good_request_id = 1
    else:
        new_good_request_id = GoodsRequest.objects.latest('id').id + 1

    pending_req_indication = GoodsRequest.objects.filter(~Q(status='Confirms the transformation')&~Q(status=None)&Q(req_to_godown__goddown_assign_to__id=request.user.id)&Q(req_to_godown__id=id)& Q(goods_sent=False)) | \
    GoodsRequest.objects.filter(Q(status='Confirmation of goods transformation') & ~Q(status=None) & Q(req_from_godown__goddown_assign_to__id=request.user.id) & Q(req_to_godown__id=id) ) | \
    GoodsRequest.objects.filter(~Q(status='Confirms the transformation') & ~Q(status=None) & Q(req_to_godown__godown_admin__id=request.user.id) & Q(req_to_godown__id=id) & Q(goods_sent=False)) | \
    GoodsRequest.objects.filter(Q(status='Confirmation of goods transformation') & ~Q(status=None) & Q(req_from_godown__godown_admin__id=request.user.id) & Q(req_from_godown__id=id)) | \
    GoodsRequest.objects.filter(~Q(status='Confirms the transformation') & ~Q(status=None) & Q(req_to_godown__godown_admin__profile_name=request.user.admin) & Q( req_to_godown__id=id)& Q(goods_sent=False))| \
    GoodsRequest.objects.filter(Q(status='Confirmation of goods transformation') & ~Q(status=None) & Q(req_from_godown__godown_admin__profile_name=request.user.admin) & Q( req_from_godown__id=id))| \
    GoodsRequest.objects.filter(~Q(status='Confirms the transformation') & ~Q(status=None)& ~Q(req_from_godown__id=id) & Q(req_to_godown=None) & Q(is_all_req=True)& Q(goods_sent=False))
    print(pending_req_indication)
    context={
        'godown_id': godown_id,
        'new_good_request_id': new_good_request_id,
        'type_of_purchase_list': type_of_purchase_list,
        'products': products,
        'godown_products': godown_products,
        'pending_req_indication': pending_req_indication,

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

@login_required(login_url='/')
def stock_godown_images(request):
    return render(request,'stock_management_system/stock_godown_images.html')

@login_required(login_url='/')
def stock_good_request(request,godown_id, request_id):
    # good_request = GoodsRequest.objects.get(id=request_id)
    godowns = Godown.objects.filter(Q(goddown_assign_to__name=request.user.admin)& ~Q(id=godown_id))| \
              Godown.objects.filter(Q(godown_admin__id=request.user.id)& ~Q(id=godown_id)) | \
              Godown.objects.filter(Q(godown_admin__profile_name=request.user.admin) & ~Q(id=godown_id))
    godowns_superadmin = Godown.objects.filter(~Q(id=godown_id))
    godown_goods = GodownProduct.objects.filter(godown_id=godown_id)
    requested_goods = RequestedProducts.objects.filter(godown_id=godown_id,goods_req_id =request_id)
    type_of_purchase_list = type_purchase.objects.all()  # 1
    products = Product.objects.all()
    context = {
        'godown_goods': godown_goods,
        'requested_goods': requested_goods,
        'godowns': godowns,
        'godowns_superadmin': godowns_superadmin,
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
            messages.success(request, "Product Added In Request List!")
            return redirect('/stock_good_request/'+str(godown_id)+'/'+str(request_id))
        elif 'submit2' in request.POST:
            req_to_godown = request.POST.get('req_to_godown')

            item2 = GoodsRequest.objects.get(id=request_id)

            item2.req_from_godown = Godown.objects.get(id=godown_id)
            if req_to_godown == '':
                item2.is_all_req = True
            elif req_to_godown == 'admin':
                item2.request_admin = True
                item2.outside_workstation = True
            else:
                item2.req_to_godown = Godown.objects.get(id=req_to_godown)
            item2.log_entered_by = request.user.name
            item2.entered_by = SiteUser.objects.get(id=request.user.id)
            item2.status = 'Pending From Target'
            item2.save(update_fields=['req_from_godown','is_all_req','req_to_godown','log_entered_by','entered_by','status','request_admin','outside_workstation'])
            messages.success(request, "Request Sent Successfully")
            return redirect('/stock_pending_request/'+str(godown_id))

        elif 'submit3' in request.POST:
            request_id = request.POST.get('request_id')
            RequestedProducts.objects.get(id=request_id).delete()
            messages.success(request, "Product Removed From Request List!")

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

@login_required(login_url='/')
def stock_pending_request(request,godown_id):
    godown = Godown.objects.get(id=godown_id)
    if request.user.role == 'Super Admin':
        pending_list = GoodsRequest.objects.filter(~Q(status='Confirms the transformation')&~Q(status=None)).order_by('-id')
    else:
        pending_list = GoodsRequest.objects.filter(~Q(status='Confirms the transformation')&~Q(status=None)&Q(req_to_godown__goddown_assign_to__id=request.user.id)&Q(req_to_godown__id=godown_id)).order_by('-id')    | \
                       GoodsRequest.objects.filter(~Q(status='Confirms the transformation')&~Q(status=None)&Q(req_from_godown__goddown_assign_to__id=request.user.id)&Q(req_from_godown__id=godown_id)).order_by('-id') | \
                       GoodsRequest.objects.filter(~Q(status='Confirms the transformation')&~Q(status=None)&Q(req_to_godown__godown_admin__id=request.user.id)&Q(req_to_godown__id=godown_id)).order_by('-id') | \
                       GoodsRequest.objects.filter(~Q(status='Confirms the transformation')&~Q(status=None)&Q(req_from_godown__godown_admin__id=request.user.id)&Q(req_from_godown__id=godown_id)).order_by('-id') | \
                       GoodsRequest.objects.filter(~Q(status='Confirms the transformation')&~Q(status=None)&Q(req_from_godown__godown_admin__profile_name=request.user.admin)&Q(req_from_godown__id=godown_id)).order_by('-id') | \
                       GoodsRequest.objects.filter(~Q(status='Confirms the transformation')&~Q(status=None)&Q(req_to_godown__godown_admin__profile_name=request.user.admin)&Q(req_to_godown__id=godown_id)).order_by('-id') | \
                       GoodsRequest.objects.filter(Q(is_all_req=True)&~Q(status='Confirms the transformation')&~Q(status=None)&(Q(req_from_godown__godown_admin__profile_name=request.user.profile_name)|Q(req_from_godown__goddown_assign_to__admin=request.user.admin))&Q(req_to_godown__goddown_assign_to__admin=None)).order_by('-id')
    context = {
        'godown_id': godown,
        'pending_list': pending_list,
    }
    return render(request,'stock_management_system/stock_pending_request.html',context)

@login_required(login_url='/')
def stock_transaction_status(request,from_godown_id, trans_id):
    good_request = GoodsRequest.objects.get(id=trans_id)
    godown = Godown.objects.get(id=from_godown_id)
    requested_goods = RequestedProducts.objects.filter(godown_id=from_godown_id,goods_req_id =good_request)
    godown_assign_employee = Godown.objects.filter(Q(goddown_assign_to__id=request.user.id)&~Q(id=good_request.req_from_godown.id))
    godown_assign_admin = Godown.objects.filter(Q(godown_admin__id=request.user.id)&~Q(id=good_request.req_from_godown.id))
    godown_assign_superadmin = Godown.objects.filter(~Q(id=good_request.req_from_godown.id))

    if request.method == 'POST' or request.method == 'FILES':
        if 'submit1' in request.POST:
            number = request.POST.get('number')
            req_type = request.POST.get('req_type')
            product_id = request.POST.get('product_id')
            faulty = request.POST.get('faulty')
            req_to_godown = request.POST.get('req_to_godown')
            item2 = RequestedProducts.objects.get(id=product_id)

            if good_request.req_to_godown == 'None' or good_request.req_to_godown == None :
                good_request.req_to_godown = Godown.objects.get(id=req_to_godown)

            if req_type == 'Individual':
                if good_request.status == 'Pending From Target':
                    if good_request.req_to_godown == 'None' or good_request.req_to_godown ==  None :
                        good_request.req_to_godown = Godown.objects.get(id=req_to_godown)
                    if number != '0':
                        item2.sent_quantity = float(number)
                        item2.log_entered_by = request.user.name
                elif good_request.status == 'Confirmation of goods transformation' or good_request.status == 'Mismatch occured':
                    if number != '0':
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
                elif good_request.status == 'Confirmation of goods transformation' or good_request.status == 'Mismatch occured':
                    if number != '0' :
                        item2.received_carton_count = float(number)
                        item2.log_entered_by = request.user.name
                    if  faulty != '0':
                        item2.faulty_carton = float(faulty)
                        item2.log_entered_by = request.user.name


            item2.save(update_fields=['sent_quantity','received_quantity','sent_carton_count','received_carton_count','log_entered_by',
                                      'faulty_carton','faulty_quantity'])
            good_request.save(update_fields=['req_to_godown','status'])
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

                        if good_request.req_to_godown:
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

            if status == 'Confirms the transformation' :

                if good_request.goods_received == False:

                    for good in requested_goods:

                        if GodownProduct.objects.filter(godown_id=from_godown_id, product_id=good.godown_product_id.product_id):
                            if good.req_type == 'Individual':
                                #for mismatch

                                if good.sent_quantity != (good.faulty_quantity + good.received_quantity):
                                    messages.success(request, 'Mismatch Occured')
                                    print('something')
                                    good_request.status = 'Mismatch occured'
                                    good_request.notify = True
                                    print('something23')
                                    good_request.save(update_fields=['status','notify'])
                                    print('something2')

                                    return redirect('/stock_transaction_status/' + str(from_godown_id) + '/' + str(trans_id))
                                elif good.sent_quantity == (good.faulty_quantity + good.received_quantity):
                                    good_request.status = 'Confirms the transformation'
                                GodownProduct.objects.filter(godown_id=from_godown_id,
                                                             product_id=good.godown_product_id.product_id).update(
                                    quantity=F("quantity") + good.received_quantity)
                                GodownProduct.objects.filter(godown_id=from_godown_id,
                                                             product_id=good.godown_product_id.product_id).update(
                                    individual_faulty=F("individual_faulty") + good.faulty_quantity)

                            elif good.req_type == 'Carton':
                                #for mismatch
                                if good.sent_carton_count != (good.faulty_carton + good.received_carton_count):
                                    good_request.status = 'Mismatch occured'
                                    good_request.notify = True
                                    good_request.save(update_fields=['status', 'notify'])
                                    messages.success(request, 'Mismatch Occured')
                                    return redirect('/stock_transaction_status/' + str(from_godown_id) + '/' + str(trans_id))
                                elif good.sent_carton_count == (good.faulty_carton + good.received_carton_count):
                                    good_request.status = 'Confirms the transformation'
                                #converting carton quantity to individual quantity
                                product = Product.objects.get(id=good.godown_product_id.product_id)
                                individual_quantity = (float(product.carton_size) * float(good.received_carton_count))

                                GodownProduct.objects.filter(godown_id=from_godown_id,
                                                             product_id=good.godown_product_id.product_id).update(
                                    quantity=F("quantity") + individual_quantity)

                                #converting faulty carton to individual faulty
                                individual_faulty = (float(product.carton_size) * float(good.faulty_carton))
                                GodownProduct.objects.filter(godown_id=from_godown_id,
                                                             product_id=good.godown_product_id.product_id).update(
                                    individual_faulty=F("individual_faulty") + individual_faulty)
                            good_request.goods_received = True

                            good_request.status = status
                            good_request.goods_received = True
                            good_request.save(update_fields=['status','req_to_godown','goods_received'])
                            # save transaction
                            new_transaction = GodownTransactions()
                            new_transaction.goods_req_id = good_request
                            new_transaction.save()
            return redirect('/stock_pending_request/'+str(from_godown_id))
    context = {
        'good_request': good_request,
        'godown': godown,
        'requested_goods': requested_goods,
        'godown_assign_admin': godown_assign_admin,
        'godown_assign_employee': godown_assign_employee,
        'godown_assign_superadmin': godown_assign_superadmin,

    }
    return render(request,'stock_management_system/stock_transaction_status.html',context)

@login_required(login_url='/')
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

                item2.carton_count = number
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
            # save transaction
            new_transaction = GodownTransactions()
            new_transaction.accept_goods_id = item2
            new_transaction.save()
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

@login_required(login_url='/')
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

@login_required(login_url='/')
def stock_transaction_history_list(request, godown_id):
    trans_history = GodownTransactions.objects.filter(goods_req_id__req_from_godown=godown_id, goods_req_id__status='Confirms the transformation').order_by('-id') | \
                    GodownTransactions.objects.filter(goods_req_id__req_to_godown=godown_id,goods_req_id__status='Confirms the transformation').order_by('-id') | \
                    GodownTransactions.objects.filter(accept_goods_id__from_godown=godown_id).order_by('-id') | \
                    GodownTransactions.objects.filter(godown_product_id__godown_id=godown_id).order_by('-id') | \
                    GodownTransactions.objects.filter(purchase_product_id__godown_id=godown_id).order_by('-id')


    context={
        'trans_history': trans_history,
    }
    return render(request,'stock_management_system/stock_transaction_history_list.html', context)

@login_required(login_url='/')
def stock_transaction_history(request, from_godown_id, trans_id):
    godown_id = Godown.objects.get(id=from_godown_id)
    godown_transaction = GodownTransactions.objects.get(id=trans_id)

    if godown_transaction.goods_req_id :
        requested_goods = RequestedProducts.objects.filter(godown_id=godown_id.id,goods_req_id =godown_transaction.goods_req_id.id)
    elif godown_transaction.accept_goods_id :
        requested_goods = AGProducts.objects.filter(godown_id=godown_id.id,accept_product_id =godown_transaction.accept_goods_id.id)
    context = {
        'godown_transaction': godown_transaction,
        'requested_goods': requested_goods,
    }

    if godown_transaction.goods_req_id :
        from_godown_initial_data = {
            'name_of_godown': godown_transaction.goods_req_id.req_from_godown.name_of_godown,
            'goddown_assign_to': godown_transaction.goods_req_id.req_from_godown.goddown_assign_to.profile_name,
            'location': godown_transaction.goods_req_id.req_from_godown.location,
            'contact_no': godown_transaction.goods_req_id.req_from_godown.contact_no,
        }
        to_godown_initial_data= {
            'name_of_godown': godown_transaction.goods_req_id.req_to_godown.name_of_godown,
            'goddown_assign_to': godown_transaction.goods_req_id.req_to_godown.goddown_assign_to.profile_name,
            'location': godown_transaction.goods_req_id.req_to_godown.location,
            'contact_no': godown_transaction.goods_req_id.req_to_godown.contact_no,
        }
        from_godown_form = GodownForm(initial=from_godown_initial_data)
        to_godown_form = GodownForm(initial=to_godown_initial_data)
        context1={
            'from_godown_form':from_godown_form,
            'to_godown_form':to_godown_form,
            'godown_transaction':godown_transaction,
            'requested_goods':requested_goods,
        }
        context.update(context1)
    return render(request, 'stock_management_system/stock_transaction_history.html',context)


@login_required(login_url='/')
def request_admin(request):
    request_admin_list= GoodsRequest.objects.filter(Q(request_admin=True)& Q(req_from_godown__godown_admin__id=request.user.id)).order_by('-id') | \
                        GoodsRequest.objects.filter(Q(request_admin=True) & Q(request_admin_id__id=request.user.id)).order_by('-id')
    try:
        outside_workarea_admins = Godown.objects.filter(~Q(godown_admin__id=request.user.id)&~Q(godown_admin__id__in=[x.request_admin_id.id for x in request_admin_list])).values_list('godown_admin__id','godown_admin__name').distinct()
    except:
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
            messages.success(request, 'Request Accepted to the Godown ('+Godown.objects.get(id=accept_to_godown).name_of_godown+')')
            return redirect('/request_admin')

        elif 'request_send' in request.POST:
            good_req = request.POST.get('good_req')
            outside_admin_id = request.POST.get('outside_admin')
            good_request = GoodsRequest.objects.get(id=good_req)
            good_request.request_admin_id = SiteUser.objects.get(id=outside_admin_id)
            good_request.save(update_fields=['request_admin_id'])
            messages.success(request, 'Request Send to Admin ('+SiteUser.objects.get(id=outside_admin_id).profile_name+')')
            return redirect('/request_admin')


    return render(request,'stock_management_system/request_admin_page.html',context)


@login_required(login_url='/')
def stock_godown_report(request,godown_id):
    context={}
    from . import cron_job_daily

    godown = Godown.objects.get(id=godown_id)
    godown_products = GodownProduct.objects.filter(godown_id=godown_id)

    if request.method == 'POST' or request.method == 'FILES':
        select_type = request.POST.get('select_type')
        from_month = request.POST.get('from_month')
        to_month = request.POST.get('to_month')
        from_month2 = datetime.strptime(from_month, "%Y-%m")
        to_month2 = datetime.strptime(to_month, "%Y-%m")
        from_month = from_month2.month
        to_month = to_month2.month
        from_year = from_month2.year
        to_year = to_month2.year
        opening_stock_date_first = DailyStock.objects.first().entry_timedate  # removeaftermonth
        opening_stock_date = calendar.monthrange(from_year, from_month-1 if from_month > 1 else 12)[1]
        opening_stock_date = datetime.strptime(str(from_year)+"-"+str(from_month-1 if from_month > 1 else 12 )+"-"+str(opening_stock_date), "%Y-%m-%d")
        if select_type == 'Day':
            products_list = GodownProduct.objects.filter(godown_id=godown_id).order_by('-product_id__sub_sub_category').order_by('product_id__sub_category')
            for godown_product in products_list:
                gt_list = DailyStock.objects.filter(
                    Q(entry_timedate__month__gte=from_month, entry_timedate__year=from_year) &
                    Q(entry_timedate__month__lte=to_month, entry_timedate__year=to_year) &
                    Q(godown_products__id=godown_product.pk)).values('entry_timedate')\
                    .annotate(sales_quantity=Sum('sales_quantity'))\
                    .annotate(goods_request_quantity=Sum('goods_request_quantity'))\
                    .annotate(accept_goods_quantity=Sum('accept_goods_quantity'))\
                    .annotate(closing_stock=Sum('closing_stock'))
                godown_product.gt_list = gt_list
                try:
                    opening_stock = DailyStock.objects.get(
                        Q(entry_timedate=opening_stock_date)&
                        Q(godown_products__product_id__id=godown_product.pk)).closing_stock

                except:
                    try:
                        opening_stock = DailyStock.objects.get(
                            Q(entry_timedate=opening_stock_date_first) &
                            Q(godown_products__product_id__id=godown_product.pk)).closing_stock
                    except:
                        opening_stock = 0
                godown_product.opening_stock = opening_stock
        else:
            products_list = GodownProduct.objects.filter(godown_id=godown_id).order_by('-product_id__sub_sub_category').order_by('product_id__sub_category')

            for godown_product in products_list:
                gt_list = DailyStock.objects.filter(
                    Q(entry_timedate__month__gte=from_month, entry_timedate__year=from_year) &
                    Q(entry_timedate__month__lte=to_month, entry_timedate__year=to_year) &
                    Q(godown_products__id=godown_product.pk)).values('godown_products')\
                    .annotate(faulty_quantity_sum=Sum('faulty_quantity'))\
                    .annotate(adjustment_quantity_sum=Sum('adjustment_quantity'))\
                    .annotate(loss_quantity_sum=Sum('loss_quantity'))\
                    .annotate(sales_quantity_sum=Sum('sales_quantity'))\
                    .annotate(goods_request_quantity_sum=Sum('goods_request_quantity'))\
                    .annotate(accept_goods_quantity_sum=Sum('accept_goods_quantity'))\
                    .annotate(closing_stock_sum=Sum('closing_stock'))
                try:
                    opening_stock = DailyStock.objects.get(
                        Q(entry_timedate=opening_stock_date)&
                        Q(godown_products__product_id__id=godown_product.pk)).closing_stock

                except:
                    try:
                        opening_stock = DailyStock.objects.get(
                            Q(entry_timedate=opening_stock_date_first) &
                            Q(godown_products__product_id__id=godown_product.pk)).closing_stock
                    except:
                        opening_stock = 0

                try:
                    godown_product.faulty_quantity_sum = gt_list[0]['faulty_quantity_sum']
                    godown_product.adjustment_quantity_sum = gt_list[0]['adjustment_quantity_sum']
                    godown_product.loss_quantity_sum = gt_list[0]['loss_quantity_sum']
                    godown_product.sales_quantity_sum = gt_list[0]['sales_quantity_sum']
                    godown_product.goods_request_quantity_sum = gt_list[0]['goods_request_quantity_sum']
                    godown_product.accept_goods_quantity_sum = gt_list[0]['accept_goods_quantity_sum']
                    godown_product.closing_stock_sum = gt_list[0]['closing_stock_sum']
                except:
                    print('no transaction of this product'+str(godown_product))
                    pass

                godown_product.opening_stock = opening_stock


        context={
            'godown': godown,
            # 'gt_list': gt_list,
            'pro_list': products_list,
            'godown_products': godown_products,
            'select_type': select_type,
        }
    return render(request,'stock_management_system/stock_godown_report.html',context)

from datetime import datetime
@login_required(login_url='/')
def stock_report(request):
    context={}
    from . import cron_job_daily
    if request.method == 'POST' or request.method == 'FILES':
        select_type = request.POST.get('select_type')
        from_month_str = request.POST.get('from_month')
        to_month_str = request.POST.get('to_month')
        from_month2 = datetime.strptime(from_month_str, "%Y-%m")
        to_month2 = datetime.strptime(to_month_str, "%Y-%m")

        from_month = from_month2.month
        to_month = to_month2.month
        from_year = from_month2.year
        to_year = to_month2.year
        opening_stock_date_first = DailyStock.objects.first().entry_timedate  #removeaftermonth

        opening_stock_date = calendar.monthrange(from_year, from_month-1 if from_month > 1 else 12)[1]
        opening_stock_date = datetime.strptime(str(from_year)+"-"+str(from_month-1 if from_month > 1 else 12 )+"-"+str(opening_stock_date), "%Y-%m-%d")


        if select_type == 'Day':
            products_list = Product.objects.all().order_by('-sub_sub_category').order_by('sub_category')
            for product in products_list:
                gt_list = DailyStock.objects.filter(
                    Q(entry_timedate__month__gte=from_month, entry_timedate__year=from_year) &
                    Q(entry_timedate__month__lte=to_month, entry_timedate__year=to_year) &
                    Q(godown_products__product_id__id=product.pk)).values('entry_timedate')\
                    .annotate(sales_quantity=Sum('sales_quantity'))\
                    .annotate(goods_request_quantity=Sum('goods_request_quantity'))\
                    .annotate(accept_goods_quantity=Sum('accept_goods_quantity'))\
                    .annotate(closing_stock=Sum('closing_stock'))
                try:
                    opening_stock = DailyStock.objects.filter(
                        Q(entry_timedate=opening_stock_date)&
                        Q(godown_products__product_id__id=product.pk)).values('godown_products__product_id').annotate(closing_stock_sum=Sum('closing_stock'))

                    opening_stock=opening_stock[0]['closing_stock_sum']
                except:
                    try:
                        opening_stock = DailyStock.objects.filter(
                            Q(entry_timedate=opening_stock_date_first) &
                            Q(godown_products__product_id__id=product.pk)).values('godown_products__product_id').annotate(
                            closing_stock_sum=Sum('closing_stock'))

                        opening_stock = opening_stock[0]['closing_stock_sum']
                    except:
                        opening_stock=0
                product.gt_list = gt_list
                product.opening_stock = opening_stock
            context22 = {
                'pro_list': products_list,
                'select_type': select_type,
                'loading': True,
            }
            context.update(context22)
        else:
            products_list = Product.objects.all().order_by('-sub_sub_category').order_by('sub_category')

            for product in products_list:
                gt_list = DailyStock.objects.filter(
                     Q(entry_timedate__month__gte=from_month, entry_timedate__year=from_year) &
                    Q(entry_timedate__month__lte=to_month, entry_timedate__year=to_year) &
                    Q(godown_products__product_id__id=product.pk)).values('godown_products__product_id')\
                    .annotate(faulty_quantity_sum=Sum('faulty_quantity'))\
                    .annotate(adjustment_quantity_sum=Sum('adjustment_quantity'))\
                    .annotate(loss_quantity_sum=Sum('loss_quantity'))\
                    .annotate(sales_quantity_sum=Sum('sales_quantity'))\
                    .annotate(goods_request_quantity_sum=Sum('goods_request_quantity'))\
                    .annotate(accept_goods_quantity_sum=Sum('accept_goods_quantity'))\
                    .annotate(closing_stock_sum=Sum('closing_stock'))

                try:
                    opening_stock = DailyStock.objects.filter(
                        Q(entry_timedate=opening_stock_date)&
                        Q(godown_products__product_id__id=product.pk)).values('godown_products__product_id').annotate(closing_stock_sum=Sum('closing_stock'))

                    opening_stock=opening_stock[0]['closing_stock_sum']
                except:
                    try:
                        opening_stock = DailyStock.objects.filter(
                            Q(entry_timedate=opening_stock_date_first) &
                            Q(godown_products__product_id__id=product.pk)).values('godown_products__product_id').annotate(
                            closing_stock_sum=Sum('closing_stock'))

                        opening_stock = opening_stock[0]['closing_stock_sum']
                    except:
                        opening_stock=0

                try:
                    product.faulty_quantity_sum = gt_list[0]['faulty_quantity_sum']
                    product.adjustment_quantity_sum = gt_list[0]['adjustment_quantity_sum']
                    product.loss_quantity_sum = gt_list[0]['loss_quantity_sum']
                    product.sales_quantity_sum = gt_list[0]['sales_quantity_sum']
                    product.goods_request_quantity_sum = gt_list[0]['goods_request_quantity_sum']
                    product.accept_goods_quantity_sum = gt_list[0]['accept_goods_quantity_sum']
                    product.closing_stock_sum = gt_list[0]['closing_stock_sum']
                except:
                    print('no transaction of this product'+str(product))



                product.opening_stock = opening_stock
            context22 = {
                'pro_list': products_list,
                'select_type': select_type,
                'loading': True,
            }
            context.update(context22)

    return render(request,'stock_management_system/stock_system_report.html',context)

def load_popup_details(request):
    date2 = datetime.strptime(request.GET.get('date2'), "%B %d, %Y").strftime('%Y-%m-%d')
    item = request.GET.get('item')
    type = request.GET.get('type')


    if type == 'sales':
        sales_list = DailyStock.objects.filter(
                            Q(entry_timedate=date2) &
                            Q(godown_products__product_id__id=item)).values('sales_ids')
        item_list=''
        for item in sales_list:
            if item['sales_ids'] != '' and len(item['sales_ids'])>1:
                item_list=item_list+item['sales_ids']
        sales_list = item_list.replace("'", "").replace("\"", "").split(', ')
        sales_list=[x for x in sales_list if x]
        pro_id = Product_Details.objects.filter(pk__in=sales_list)

        context={
            'pro_id':pro_id,
            'type':type,
        }
    if type == 'purchase':
        sales_list = DailyStock.objects.filter(
                            Q(entry_timedate=date2) &
                            Q(godown_products__product_id__id=item)).values('accept_goods_ids')
        item_list=''
        for item in sales_list:
            if item['sales_ids'] != '' and len(item['sales_ids'])>1:
                item_list=item_list+item['sales_ids']
        sales_list = item_list.replace("'", "").replace("\"", "").split(', ')
        sales_list=[x for x in sales_list if x]
        pro_id = AGProducts.objects.filter(pk__in=sales_list)

        context={
            'pro_id':pro_id,
            'type':type,
        }
    if type == 'transfer':
        sales_list = DailyStock.objects.filter(
                            Q(entry_timedate=date2) &
                            Q(godown_products__product_id__id=item)).values('goods_request_ids')
        item_list=''
        for item in sales_list:
            if item['sales_ids'] != '' and len(item['sales_ids'])>1:
                item_list=item_list+item['sales_ids']
        sales_list = item_list.replace("'", "").replace("\"", "").split(', ')
        sales_list=[x for x in sales_list if x]
        pro_id = GoodsRequest.objects.filter(pk__in=sales_list)

        context={
            'pro_id':pro_id,
            'type':type,
        }

    return render(request,"stock_management_system/load_popup_details.html",context)