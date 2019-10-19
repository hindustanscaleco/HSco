from django import forms

from .models import Customer_Details, Feedback, Purchase_Details
from .models import Product_Details


class Purchase_Details_Form(forms.ModelForm):



    class Meta:
        model = Purchase_Details
        fields = (
        'date_of_purchase',
        'bill_no',
        'upload_op_file',
        'po_number',
        'photo_lr_no',
        'channel_of_sales',
        'industry',
        'value_of_goods',
        'channel_of_dispatch',
        'notes',
        'feedback_form_filled',)

class Product_Details_Form(forms.ModelForm):



    class Meta:
        model = Product_Details  # model
        fields = (
        'product_name',
        'quantity',
        'type_of_scale',
        'model_of_purchase',
        'sub_model',
        'sub_sub_model',
        'serial_no_scale',
        'brand',
        'capacity',
        'unit',)

class Feedback_Form(forms.ModelForm):
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
        model = Feedback  # model
        fields = (
        'knowledge_of_person',
        'timeliness_of_person',
        'price_of_product',
        'overall_interaction',
        'about_hsco',
        'any_suggestion',
       )
