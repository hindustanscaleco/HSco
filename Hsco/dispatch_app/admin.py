from django.contrib import admin

# Register your models here.
from .models import Dispatch,Product_Details_Dispatch

class DispatchAdmin(admin.ModelAdmin):

    list_display = ('dispatch_no','id')

    search_fields = ('dispatch_no','id')

admin.site.register(Dispatch, DispatchAdmin)
admin.site.register(Product_Details_Dispatch)