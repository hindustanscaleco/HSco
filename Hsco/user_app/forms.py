from django import forms

from .models import SiteUser



class SiteUser_Form(forms.ModelForm):
    class Meta:
        model = SiteUser
        fields = ('is_deleted',)