from django.contrib import admin

# Register your models here.
from .models import Customer_Details, Product_Details

admin.site.register(Customer_Details)
admin.site.register(Product_Details)