from django import forms

from .models import Onsite_aftersales_service, Onsite_Feedback


class add_Onsite_aftersales_service_form(forms.ModelForm):



    class Meta:
        model = Onsite_aftersales_service
        fields = (
        'feedback_given',
        'in_warranty',
        )

class Onsite_Repairing_Feedback_Form(forms.ModelForm):
    backend_team = forms.FloatField(required=True,
                               widget=forms.TextInput(
                                   attrs={
                                       'type': 'hidden',
                                       'class': '',
                                       'placeholder': "Stars",
                                       'name': 'email',
                                       'id': 'stars',
                                   }
                               ))

    onsite_worker = forms.FloatField(required=True,
                                             widget=forms.TextInput(
                                                 attrs={
                                                     'type': 'hidden',
                                                     'class': '',
                                                     'placeholder': "Stars",
                                                     'name': 'email',
                                                     'id': 'stars2',
                                                 }
                                             ))
    speed_of_performance = forms.FloatField(required=True,
                                             widget=forms.TextInput(
                                                 attrs={
                                                     'type': 'hidden',
                                                     'class': '',
                                                     'placeholder': "Stars",
                                                     'name': 'email',
                                                     'id': 'stars3',
                                                 }
                                             ))

    overall_interaction = forms.FloatField(required=True,
                                             widget=forms.TextInput(
                                                 attrs={
                                                     'type': 'hidden',
                                                     'class': '',
                                                     'placeholder': "Stars",
                                                     'name': 'email',
                                                     'id': 'stars4',
                                                 }
                                             ))
    price_of_reparing = forms.FloatField(required=True,
                                           widget=forms.TextInput(
                                               attrs={
                                                   'type': 'hidden',
                                                   'class': '',
                                                   'placeholder': "Stars",
                                                   'name': 'email',
                                                   'id': 'stars5',
                                               }
                                           ))

    class Meta:
        model = Onsite_Feedback  # model
        fields = (
        'backend_team',
        'onsite_worker',
        'speed_of_performance',
        'price_of_reparing',
        'overall_interaction',
        'about_hsco',
        'any_suggestion',
       )


