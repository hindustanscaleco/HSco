from django.contrib import admin

# Register your models here.
from .models import Onsite_aftersales_service, Onsite_Products, Onsite_Feedback

admin.site.register(Onsite_aftersales_service)
admin.site.register(Onsite_Products)
admin.site.register(Onsite_Feedback)