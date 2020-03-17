from django import forms

from .models import Godown
class GodownForm(forms.ModelForm):

    name_of_godown = forms.CharField(max_length=80, required=True,
       widget=forms.TextInput(
           attrs={
               'type': 'text',
               'placeholder': "Name Of Godown",
               'class': 'form-control',
           }
       ))


    goddown_assign_to = forms.CharField(max_length=80, required=True,
       widget=forms.TextInput(
           attrs={
               'type': 'text',
               'placeholder': "Godown Assigned To",
               'class': 'form-control',
           }
       ))

    location = forms.CharField(max_length=80, required=True,
       widget=forms.TextInput(
           attrs={
               'type': 'text',
               'placeholder': "Location",
               'class': 'form-control',
           }
       ))

    contact_no = forms.IntegerField(required=True,
       widget=forms.TextInput(
           attrs={
               'type': 'text',
               'placeholder': "Contact No",
               'class': 'form-control',
           }
       ))
    class Meta:
        model = Godown
        fields = ["name_of_godown",
                  "goddown_assign_to",
                  "location",
                  "contact_no",
                  ]
