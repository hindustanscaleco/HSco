from django import forms

from .models import Onsite_aftersales_service


class add_Onsite_aftersales_service_form(forms.ModelForm):



    class Meta:
        model = Onsite_aftersales_service
        fields = (
        'feedback_given',
        )

