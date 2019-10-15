from django.contrib import admin

# Register your models here.
from .models import Restamping_after_sales_service, Restamping_Product

admin.site.register(Restamping_after_sales_service)
admin.site.register(Restamping_Product)