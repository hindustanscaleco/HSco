from django.contrib import admin

# Register your models here.
from .models import Amc_After_Sales, AMC_Feedback

admin.site.register(Amc_After_Sales)
admin.site.register(AMC_Feedback)