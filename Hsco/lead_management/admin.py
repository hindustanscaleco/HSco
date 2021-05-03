from django.contrib import admin
from .models import Lead ,Pi_section, IndiamartLeadDetails

from .models import Lead, Pi_section, Pi_product,Pi_History,Follow_up_section,Auto_followup_details,History_followup,Followup_product,Payment_details

from import_export.admin import ImportExportModelAdmin



class Lead_Admin(ImportExportModelAdmin):
    list_display = ('id','customer_id','current_stage','channel','entry_timedate')

class Indiamart_Admin(ImportExportModelAdmin):
    list_display = ('id', 'from_date', 'to_date', 'lead_count', 'entry_timedate')

class Pi_section_Admin(admin.ModelAdmin):
    list_display = ('id', 'pf_total', 'entry_timedate')

class Pi_product_Admin(admin.ModelAdmin):
    list_display = ('id', 'pf', 'entry_timedate')

admin.site.register(Lead,Lead_Admin)
admin.site.register(Pi_section,Pi_section_Admin)


admin.site.register(IndiamartLeadDetails, Indiamart_Admin)

admin.site.register(Pi_product, Pi_product_Admin)
admin.site.register(Pi_History)
admin.site.register(Follow_up_section)
admin.site.register(Auto_followup_details)
admin.site.register(History_followup)
admin.site.register(Followup_product)
admin.site.register(Payment_details)

