from django import forms

from .models import AMC_Feedback


class AMC_Feedback_Form(forms.ModelForm):
    satisfied_with_work = forms.IntegerField(required=True,
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
    price_of_amc = forms.IntegerField(required=True,
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
        model = AMC_Feedback  # model
        fields = (
        'satisfied_with_work',
        'speed_of_performance',
        'price_of_amc',
        'overall_interaction',
        'about_hsco',
        'any_suggestion',
       )
