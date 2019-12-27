from django.contrib import admin

from .models import Repairing_after_sales_service, Repairing_Product , Repairing_Feedback,Component_Replaced


class Repairing_FeedbackDetailsInline(admin.TabularInline):
    model = Repairing_Feedback

class Repairing_ProductDetailsInline(admin.TabularInline):
    model = Repairing_Product

class Repairing_after_sales_serviceAdmin(admin.ModelAdmin):
    list_display = ('repairing_no', 'id', 'second_company_name', 'second_contact_no',  'user_id', 'entered_by',)

    inlines = [
        Repairing_FeedbackDetailsInline,
        Repairing_ProductDetailsInline,

    ]

class Repairing_ProductAdmin(admin.ModelAdmin):

    list_display = ('repairing_id','id')

    search_fields = ('repairing_id','id')


admin.site.register(Repairing_after_sales_service,Repairing_after_sales_serviceAdmin)
admin.site.register(Repairing_Product, Repairing_ProductAdmin)
admin.site.register(Repairing_Feedback)
admin.site.register(Component_Replaced)
