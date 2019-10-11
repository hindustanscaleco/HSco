from django import forms

from .models import Repairing_after_sales_service


class Repairing_after_sales_service_form(forms.ModelForm):



    class Meta:
        model = Repairing_after_sales_service
        fields = (
        'in_warranty',
        'replaced_scale_given',
        'confirmed_estimate',
        'repaired',)





