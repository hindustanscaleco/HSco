from django.db.models import F

from .models import *
import datetime
todays_date = datetime.datetime.today()

# all_godown_products = GodownProduct.objects.all()
all_godown_products = GodownProduct.objects.filter(product_id__sub_sub_category__name='MSS001')
daily_count = DailyStock.objects.filter(entry_timedate=todays_date).count()
if daily_count == 0:
    for product in all_godown_products:
        item = DailyStock()
        item.godown_products = product
        item.closing_stock = product.quantity
        item.save()

    godown_trans = GodownTransactions.objects.filter(entry_timedate=todays_date)

    for transaction in godown_trans:
        val = transaction.purchase_product_id

        if val.sub_sub_model != None and val.sub_sub_model != "" and val.sub_sub_model != 'None':
            product = Product.objects.get(scale_type__name=val.type_of_scale,
                                         main_category__name=val.model_of_purchase,
                                         sub_category__name=val.sub_model,
                                         sub_sub_category__name=val.sub_sub_model)
        else:
            product = Product.objects.get(scale_type__name=val.type_of_scale,
                                                                             main_category__name=val.model_of_purchase,
                                                                             sub_category__name=val.sub_model)
        godown_pro = GodownProduct.objects.filter(godown_id=val.godown_id,product_id=product)
        godown_pro = godown_pro[0] if godown_pro.count() > 0 else None



        item = DailyStock.objects.filter(entry_timedate=todays_date,godown_products=godown_pro)
        for id in item:
            old_ids=id.sales_ids

        item.update(sales_quantity= F("sales_quantity") + transaction.purchase_product_id.quantity, sales_ids= str(old_ids) + str(transaction.purchase_product_id.pk)+', ' )

        req_pro = RequestedProducts.objects.filter(goods_req_id=transaction.goods_req_id)
        for obj in req_pro:
            DailyStock.objects.filter(entry_timedate=todays_date,
                                      godown_products=obj.godown_product_id).update(goods_request_quantity = F("goods_request_quantity")+obj.received_quantity,
                                                                                    faulty_quantity = F("faulty_quantity")+obj.faulty_quantity,
                                                                                    goods_request_ids= F("goods_request_ids") + obj.goods_req_id.pk+', ')

        accp_goods = AGProducts.objects.filter(accept_product_id=transaction.accept_goods_id)
        for obj in accp_goods:
            DailyStock.objects.filter(entry_timedate=todays_date,
                                      godown_products=obj.godown_product_id).update(
                accept_goods_quantity=F("accept_goods_quantity") + obj.quantity,
                accept_goods_ids=F("accept_goods_ids") + obj.accept_product_id.pk + ', ')

        item = DailyStock.objects.filter(entry_timedate=todays_date,
                                         godown_products=transaction.godown_product_id)
        item.update(loss_quantity= F("loss_quantity") +transaction.loss_quantity)
        item.update(adjustment_quantity= F("adjustment_quantity") +transaction.adjustment_quantity)
