from django import forms

from .models import Repairing_after_sales_service, Repairing_Feedback


class Repairing_Feedback_Form(forms.ModelForm):
    knowledge_of_person = forms.IntegerField(required=True,
                               widget=forms.TextInput(
                                   attrs={
                                       'type': 'hidden',
                                       'class': '',
                                       'placeholder': "Stars",
                                       'name': 'email',
                                       'id': 'stars',
                                   }
                               ))

    timeliness_of_person = forms.IntegerField(required=True,
                                             widget=forms.TextInput(
                                                 attrs={
                                                     'type': 'hidden',
                                                     'class': '',
                                                     'placeholder': "Stars",
                                                     'name': 'email',
                                                     'id': 'stars2',
                                                 }
                                             ))
    price_of_product = forms.IntegerField(required=True,
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






