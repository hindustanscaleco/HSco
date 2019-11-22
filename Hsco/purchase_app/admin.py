from django.contrib import admin

# Register your models here.
from .models import Purchase_Details, Product_Details, Feedback

admin.site.register(Purchase_Details)
admin.site.register(Product_Details)
admin.site.register(Feedback)
