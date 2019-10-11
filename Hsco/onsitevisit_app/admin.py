from django.contrib import admin

# Register your models here.
from .models import Onsite_visit, Onsite_aftersales_service

admin.site.register(Onsite_visit)
admin.site.register(Onsite_aftersales_service)