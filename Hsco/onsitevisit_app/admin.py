from django.contrib import admin

# Register your models here.
from .models import Onsite_aftersales_service, Onsite_Products, Onsite_Feedback

class Onsite_aftersales_serviceAdmin(admin.ModelAdmin):

    list_display = ('onsite_no','id')

    search_fields = ('onsite_no','id')

class Onsite_ProductsAdmin(admin.ModelAdmin):

    list_display = ('onsite_repairing_id','id')

    search_fields = ('onsite_repairing_id','id')
admin.site.register(Onsite_aftersales_service, Onsite_aftersales_serviceAdmin)
admin.site.register(Onsite_Products, Onsite_ProductsAdmin)
admin.site.register(Onsite_Feedback)