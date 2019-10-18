from django.contrib import admin

from .models import Repairing_after_sales_service, Repairing_Product , Repairing_Feedback

admin.site.register(Repairing_after_sales_service)
admin.site.register(Repairing_Product)
admin.site.register(Repairing_Feedback)
