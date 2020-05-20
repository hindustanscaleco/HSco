from django.contrib import admin

from .models import Product,Godown,GodownProduct,GoodsRequest,RequestedProducts,AcceptGoods,AGProducts,GodownTransactions
class Product_Admin(admin.ModelAdmin):

    list_display = ('scale_type','main_category','sub_category','sub_sub_category')

    search_fields = ('scale_type','main_category','sub_category','sub_sub_category')

admin.site.register(Product, Product_Admin)
admin.site.register(Godown)
admin.site.register(GodownProduct)
admin.site.register(GoodsRequest)
admin.site.register(RequestedProducts)
admin.site.register(AcceptGoods)
admin.site.register(AGProducts)
admin.site.register(GodownTransactions)
