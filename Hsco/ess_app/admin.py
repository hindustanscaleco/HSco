from django.contrib import admin

# Register your models here.
from .models import Ess,Employee_Leave,Defects_Warning,Employee_Analysis

admin.site.register(Ess)
admin.site.register(Employee_Leave)
admin.site.register(Defects_Warning)
admin.site.register(Employee_Analysis)