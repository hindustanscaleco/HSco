from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import type_purchase,main_model,sub_model,sub_sub_model, Log,DynamicDropdown

# Register your models here.
from .models import Customer_Details,Lead_Customer_Details

class CustomerDetailsAdmin(admin.ModelAdmin):
    list_display = ('id','customer_name','company_name','contact_no','customer_gst_no')
    search_fields = ('id','customer_name','contact_no','company_name','customer_gst_no')

admin.site.register(Customer_Details, CustomerDetailsAdmin)

class LeadCustomerDetailsAdmin(admin.ModelAdmin):
    list_display = ('id','customer_name','company_name','contact_no','customer_gst_no')
    search_fields = ('id','customer_name','contact_no','company_name','customer_gst_no')

admin.site.register(Lead_Customer_Details, LeadCustomerDetailsAdmin)

class DDAdmin(ImportExportModelAdmin):
    list_display = ('name', 'type', 'is_enabled','entry_timedate',)
    list_filter = ( 'type','is_enabled',)
    search_fields = ('name',)

#admin.site.register(Customer_Details)
admin.site.register(Lead_Customer_Details)
admin.site.register(type_purchase)
admin.site.register(main_model)
admin.site.register(sub_model)
admin.site.register(sub_sub_model)
admin.site.register(Log)
admin.site.register(DynamicDropdown,DDAdmin)

