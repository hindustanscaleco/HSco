from django.contrib import admin

from .models import Repairing_after_sales_service, Repairing_Product , Repairing_Feedback,Component_Replaced


class Repairing_FeedbackDetailsInline(admin.TabularInline):
    model = Repairing_Feedback

class Repairing_ProductDetailsInline(admin.TabularInline):
    model = Repairing_Product

class Repairing_after_sales_serviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'second_company_name', 'second_contact_no', 'entry_timedate', 'user_id', 'entered_by',)
    list_filter = ('id',)

    inlines = [
        Repairing_FeedbackDetailsInline,
        Repairing_ProductDetailsInline,

    ]

admin.site.register(Repairing_after_sales_service,Repairing_after_sales_serviceAdmin)
admin.site.register(Repairing_Product)
admin.site.register(Repairing_Feedback)
admin.site.register(Component_Replaced)
