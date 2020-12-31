from django.contrib import admin

# Register your models here.
from .models import Amc_After_Sales, AMC_Feedback

class Amc_After_SalesAdmin(admin.ModelAdmin):

    list_display = ('amc_no','id')

    search_fields = ('amc_no','id')

admin.site.register(Amc_After_Sales, Amc_After_SalesAdmin)
admin.site.register(AMC_Feedback)