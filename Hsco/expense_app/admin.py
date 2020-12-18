from django.contrib import admin
from .models import Expense_Type_Sub_Master, Expense_Type_Sub_Sub_Master, Vendor, Expense, Expense_Product
# Register your models here.

admin.site.register(Expense_Type_Sub_Master)
admin.site.register(Expense_Type_Sub_Sub_Master)
admin.site.register(Vendor)
admin.site.register(Expense)
admin.site.register(Expense_Product)
