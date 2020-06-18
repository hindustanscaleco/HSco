from .models import *
import datetime
todays_date = datetime.datetime.today()

all_godown_products = GodownProduct.objects.all()
daily_count = DailyStock.objects.filter(entry_timedate=todays_date).count()
if daily_count == 0:
    for product in all_godown_products:
        item = DailyStock()
        item.godown_products = product
        item.closing_stock = product.quantity
        item.save()

    godown_trans = GodownTransactions.objects.filter(entry_timedate=todays_date)

    for transaction in godown_trans:
        item = DailyStock.objects.filter(entry_timedate=todays_date,
                                         godown_products=transaction.purchase_product_id.product_master_obj)
        req_pro = RequestedProducts.objects.filter(goods_req_id=transaction.goods_req_id).received_quantity


        item = DailyStock.objects.filter(entry_timedate=todays_date,godown_products=transaction.purchase_product_id.product_master_obj).update(
            sales_quantity= transaction.purchase_product_id.quantity,sales_ids= transaction.purchase_product_id.pk+', '
        )
        item.godown_products = product
        item.closing_stock = product.quantity
        item.sales_quantity = godown_trans.purchase_quantity
        item.faulty_quantity = product.individual_faulty
        item.save()