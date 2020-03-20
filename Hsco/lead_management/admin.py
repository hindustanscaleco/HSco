from django.contrib import admin
from .models import Lead ,Pi_section, IndiamartLeadDetails

from .models import Lead, Pi_section, Pi_product,Pi_History,Follow_up_section,Auto_followup_details,History_followup,Followup_product


admin.site.register(Lead)
admin.site.register(Pi_section)


admin.site.register(IndiamartLeadDetails)

admin.site.register(Pi_product)
admin.site.register(Pi_History)
admin.site.register(Follow_up_section)
admin.site.register(Auto_followup_details)
admin.site.register(History_followup)
admin.site.register(Followup_product)

