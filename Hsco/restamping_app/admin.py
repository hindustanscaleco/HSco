from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

# Register your models here.
from .models import Restamping_after_sales_service, Restamping_Product

class Restamping_after_sales_serviceAdmin(SimpleHistoryAdmin):

    list_display = ('restamping_no','id')

    search_fields = ('restamping_no','id')

class Restamping_ProductAdmin(SimpleHistoryAdmin):

    list_display = ('restamping_id','id')

    search_fields = ('restamping_id','id')


admin.site.register(Restamping_after_sales_service, Restamping_after_sales_serviceAdmin)
admin.site.register(Restamping_Product, Restamping_ProductAdmin)