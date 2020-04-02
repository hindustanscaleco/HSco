from django.contrib import admin

from .models import Product,Godown,GodownProduct,GoodsRequest,RequestedProducts,AcceptGoods,AGProducts,GodownTransactions

admin.site.register(Product)
admin.site.register(Godown)
admin.site.register(GodownProduct)
admin.site.register(GoodsRequest)
admin.site.register(RequestedProducts)
admin.site.register(AcceptGoods)
admin.site.register(AGProducts)
admin.site.register(GodownTransactions)
