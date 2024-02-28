from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from simple_history.admin import SimpleHistoryAdmin

from .models import Product, Godown, GodownProduct, GoodsRequest, RequestedProducts, AcceptGoods, AGProducts, \
    GodownTransactions, DailyStock

class Product_Admin(SimpleHistoryAdmin):

    list_display = ('id','scale_type','main_category','sub_category','sub_sub_category')

    search_fields = ('id','scale_type__name','main_category__name','sub_category__name','sub_sub_category__name')

class GodownProduct_Admin(SimpleHistoryAdmin):

    list_display = ('id', 'product_id','entry_timedate')

    search_fields = ('product_id__id','product_id__scale_type__name','product_id__main_category__name','product_id__sub_category__name','product_id__sub_sub_category__name')

class GodownTransactions_Admin(SimpleHistoryAdmin):
    def godown_product(self, obj):
        return obj.godown_product_id

    list_display = ('id','godown_product','purchase_product_id','purchase_quantity','adjustment_quantity','loss_quantity', 'type','entry_timedate')

    search_fields = ('adjustment_quantity','loss_quantity','goods_req_id__id','accept_goods__id','purchase_id__id','loss_quantity','adjustment_quantity','godown_product_id__id')

    list_filter = ('adjustment_quantity', 'godown_product_id__product_id__sub_sub_category',)

class DailyStock_Admin(ImportExportModelAdmin):
    def godown_product(self, obj):
        return obj.godown_products.product_id.sub_sub_category
    list_display = ('id', 'godown_product','adjustment_quantity','loss_quantity', 'closing_stock', 'sales_quantity', 'entry_timedate')
    search_fields = ('godown_products__product_id__sub_sub_category__name',)
    list_filter = ('adjustment_quantity', 'loss_quantity','godown_products__product_id__sub_sub_category','godown_products__product_id__sub_category',)

admin.site.register(Product, Product_Admin)
admin.site.register(Godown)
admin.site.register(GodownProduct, GodownProduct_Admin)
admin.site.register(GoodsRequest)
admin.site.register(RequestedProducts)
admin.site.register(AcceptGoods)
admin.site.register(AGProducts)
admin.site.register(GodownTransactions, GodownTransactions_Admin)
admin.site.register(DailyStock,DailyStock_Admin)
