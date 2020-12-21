from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Product, Godown, GodownProduct, GoodsRequest, RequestedProducts, AcceptGoods, AGProducts, \
    GodownTransactions, DailyStock

class Product_Admin(admin.ModelAdmin):

    list_display = ('scale_type','main_category','sub_category','sub_sub_category')

    search_fields = ('scale_type__name','main_category__name','sub_category__name','sub_sub_category__name')

class GodownProduct_Admin(admin.ModelAdmin):

    list_display = ('id', 'product_id','entry_timedate')

    search_fields = ('product_id__id','product_id__scale_type__name','product_id__main_category__name','product_id__sub_category__name','product_id__sub_sub_category__name')

class GodownTransactions_Admin(admin.ModelAdmin):

    list_display = ('id','adjustment_quantity','loss_quantity', 'type','entry_timedate')

    search_fields = ('adjustment_quantity','loss_quantity','goods_req_id__id','accept_goods__id','purchase_id__id','loss_quantity','adjustment_quantity','godown_product_id__id')

    list_filter = ('adjustment_quantity', )

class DailyStock_Admin(ImportExportModelAdmin):
    list_display = ('id', 'godown_products','adjustment_quantity','loss_quantity', 'closing_stock', 'sales_quantity', 'entry_timedate')
    search_fields = ('godown_products__product_id__sub_sub_category__name',)
    list_filter = ('adjustment_quantity', 'loss_quantity',)

admin.site.register(Product, Product_Admin)
admin.site.register(Godown)
admin.site.register(GodownProduct, GodownProduct_Admin)
admin.site.register(GoodsRequest)
admin.site.register(RequestedProducts)
admin.site.register(AcceptGoods)
admin.site.register(AGProducts)
admin.site.register(GodownTransactions, GodownTransactions_Admin)
admin.site.register(DailyStock,DailyStock_Admin)
