from django.contrib import admin

# Register your models here.
from .models import Dispatch,Product_Details_Dispatch

admin.site.register(Dispatch)
admin.site.register(Product_Details_Dispatch)