from django.contrib import admin
from .models import Bill, Expense_Type_Sub_Master, Expense_Type_Sub_Sub_Master, Vendor, Expense, Expense_Product
# Register your models here.
class ExpenseAdmin(admin.ModelAdmin):

    list_display = ('expense_type_sub_sub_master_id','id')

    search_fields = ('expense_type_sub_sub_master_id','id')

class Expense_Type_Sub_MasterAdmin(admin.ModelAdmin):

    list_display = ('expense_type_master','id')

    search_fields = ('expense_type_master','id')

admin.site.register(Bill)
admin.site.register(Expense_Type_Sub_Master, Expense_Type_Sub_MasterAdmin)
admin.site.register(Expense_Type_Sub_Sub_Master)
admin.site.register(Vendor)
admin.site.register(Expense,ExpenseAdmin)
admin.site.register(Expense_Product)
