from django.contrib import admin
from .models import type_purchase,main_model,sub_model,sub_sub_model, Log

# Register your models here.
from .models import Customer_Details,Lead_Customer_Details

admin.site.register(Customer_Details)
admin.site.register(Lead_Customer_Details)
admin.site.register(type_purchase)
admin.site.register(main_model)
admin.site.register(sub_model)
admin.site.register(sub_sub_model)
admin.site.register(Log)

