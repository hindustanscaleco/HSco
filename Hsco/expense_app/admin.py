from django.contrib import admin
from .models import Bill, Expense_Type_Sub_Master, Expense_Type_Sub_Sub_Master, Vendor, Expense, Expense_Product
# Register your models here.
class ExpenseAdmin(admin.ModelAdmin):

    list_display = ('expense_type_sub_sub_master_id','id')

    search_fields = ('expense_type_sub_sub_master_id','id')

class Expense_Type_Sub_MasterAdmin(admin.ModelAdmin):

    list_display = ('expense_type_master','id')

    search_fields = ('expense_type_master','id')

class BillAdmin(admin.ModelAdmin):

    list_display = ('id','purchase_id','update_bill_no','entry_date')

    search_fields = ('id','purchase_id','update_bill_no','update_bill_no')

admin.site.register(Bill, BillAdmin)
admin.site.register(Expense_Type_Sub_Master, Expense_Type_Sub_MasterAdmin)
admin.site.register(Expense_Type_Sub_Sub_Master)
admin.site.register(Vendor)
admin.site.register(Expense,ExpenseAdmin)
admin.site.register(Expense_Product)
