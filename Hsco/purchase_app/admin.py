from django.contrib import admin

# Register your models here.
from .models import Purchase_Details, Product_Details, Feedback

class Purchase_DetailsAdmin(admin.ModelAdmin):

    list_display = ('purchase_no','id','date_of_purchase')

    search_fields = ('purchase_no','id','date_of_purchase')

class Product_DetailsAdmin(admin.ModelAdmin):

    list_display = ('purchase_id','id')

    search_fields = ('purchase_id','id')


admin.site.register(Purchase_Details , Purchase_DetailsAdmin)
admin.site.register(Product_Details, Product_DetailsAdmin)
admin.site.register(Feedback)
