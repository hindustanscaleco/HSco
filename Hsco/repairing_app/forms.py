from django import forms

from .models import Repairing_after_sales_service, Repairing_Feedback


class Repairing_Feedback_Form(forms.ModelForm):
    satisfied_with_communication = forms.IntegerField(required=True,
                               widget=forms.TextInput(
                                   attrs={
                                       'type': 'hidden',
                                       'class': '',
                                       'placeholder': "Stars",
                                       'name': 'email',
                                       'id': 'stars',
                                   }
                               ))

    speed_of_performance = forms.IntegerField(required=True,
                                             widget=forms.TextInput(
                                                 attrs={
                                                     'type': 'hidden',
                                                     'class': '',
                                                     'placeholder': "Stars",
                                                     'name': 'email',
                                                     'id': 'stars2',
                                                 }
                                             ))
    price_of_reparing = forms.IntegerField(required=True,
                                             widget=forms.TextInput(
                                                 attrs={
                                                     'type': 'hidden',
                                                     'class': '',
                                                     'placeholder': "Stars",
                                                     'name': 'email',
                                                     'id': 'stars3',
                                                 }
                                             ))
    overall_interaction = forms.IntegerField(required=True,
                                             widget=forms.TextInput(
                                                 attrs={
                                                     'type': 'hidden',
                                                     'class': '',
                                                     'placeholder': "Stars",
                                                     'name': 'email',
                                                     'id': 'stars4',
                                                 }
                                             ))

    class Meta:
        model = Repairing_Feedback  # model
        fields = (
        'satisfied_with_communication',
        'speed_of_performance',
        'price_of_reparing',
        'overall_interaction',
        'about_hsco',
        'any_suggestion',

       )






