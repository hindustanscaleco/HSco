from django.contrib import admin
from .models import Lead ,Pi_section, IndiamartLeadDetails

from .models import Lead, Pi_section, Pi_product,Pi_History


admin.site.register(Lead)
admin.site.register(Pi_section)

admin.site.register(IndiamartLeadDetails)

admin.site.register(Pi_product)
admin.site.register(Pi_History)

