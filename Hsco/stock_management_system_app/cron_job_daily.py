from .models import GodownProduct, DailyStock, GodownTransactions, Product, RequestedProducts, AGProducts


def main():
    from django.db.models import F

    import datetime
    todays_date = datetime.datetime.today()

    # all_godown_products = GodownProduct.objects.all()
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


            if transaction.purchase_product_id:
                try:
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
                    godown_pro = GodownProduct.objects.filter(godown_id=val.godown_id, product_id=product)
                    godown_pro = godown_pro[0] if godown_pro.count() > 0 else None

                    item = DailyStock.objects.filter(entry_timedate=todays_date, godown_products=godown_pro)

                    old_ids = ''
                    for daily_stock in item:
                        old_ids = daily_stock.sales_ids


                    sales_ids= str(old_ids) + str(transaction.pk)+', '
                    item.update(sales_quantity= F("sales_quantity") + transaction.purchase_quantity, sales_ids= sales_ids.replace('None','') )
                except:
                    print('Not sales')

            elif transaction.goods_req_id:
                try:
                    trans = transaction.goods_req_id
                    req_pro = RequestedProducts.objects.filter(goods_req_id=transaction.goods_req_id)
                    # goods_request_old_ids = ''
                    # item = DailyStock.objects.filter(entry_timedate=todays_date, godown_products=godown_pro)
                    # for id in item:
                    #     goods_request_old_ids=id.goods_request_ids
                    for obj in req_pro:
                        daily_req_id = DailyStock.objects.get(entry_timedate=todays_date,godown_products=obj.godown_product_id).goods_request_ids
                        DailyStock.objects.filter(entry_timedate=todays_date,
                                                  godown_products=obj.godown_product_id).update(goods_request_quantity = F("goods_request_quantity")+obj.received_quantity,
                                                                                                faulty_quantity = F("faulty_quantity")+obj.faulty_quantity,
                                                                                                goods_request_ids = str(daily_req_id).replace('None','') + str(transaction.pk) + ', ')
                except:
                    print('Not Transfer')

            elif transaction.accept_goods_id:
                try:
                    trans = transaction.accept_goods_id
                    accp_goods = AGProducts.objects.filter(accept_product_id=transaction.accept_goods_id)
                    # accept_goods_old_ids = ''
                    # for id in item:
                    #     accept_goods_old_ids = id.accept_goods_ids
                    for obj in accp_goods:
                        daily_accept_id = DailyStock.objects.get(entry_timedate=todays_date,godown_products=obj.godown_product_id).accept_goods_ids
                        DailyStock.objects.filter(entry_timedate=todays_date,
                                                  godown_products=obj.godown_product_id).update(
                            accept_goods_quantity=F("accept_goods_quantity") + obj.quantity,
                            accept_goods_ids=str(daily_accept_id).replace('None','') + str(transaction.pk) + ', ')
                except:
                    print('Not Purchase')

            else:
                try:
                    item = DailyStock.objects.filter(entry_timedate=todays_date,
                                                     godown_products=transaction.godown_product_id)
                    item.update(loss_quantity= F("loss_quantity") +transaction.loss_quantity)
                    item.update(adjustment_quantity= F("adjustment_quantity") +transaction.adjustment_quantity)
                except:
                    print('Not adjustment or loss')

if __name__ == "__main__":
    main()

def hello():
    print("crontab")
    print("crontab")
    print("crontab")
    print("crontab")
