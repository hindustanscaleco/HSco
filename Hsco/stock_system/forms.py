from django import forms

from .models import Stock_System


class StockRegisterForm(forms.ModelForm):
    type_of_scale = forms.CharField(required=True,
                               widget=forms.TextInput(
                                   attrs={
                                       'type': 'Text',
                                       'class': 'form-control',
                                       'placeholder': "Enter Type Of Scale ",
                                   }
                               ))
    hsn_code = forms.CharField(required=True,
                               widget=forms.TextInput(
                                   attrs={
                                       'type': 'Text',
                                       'class': 'form-control',
                                       'placeholder': "HSN Code ",
                                   }
                               ))

    product_code = forms.CharField(required=True,
                               widget=forms.TextInput(
                                   attrs={
                                       'type': 'Text',
                                       'class': 'form-control',
                                       'placeholder': "Product Code ",
                                   }
                               ))

    product_sub_code = forms.CharField(required=True,
                               widget=forms.TextInput(
                                   attrs={
                                       'type': 'Text',
                                       'class': 'form-control',
                                       'placeholder': "Product Code ",
                                   }
                               ))
    product_sub_sub_code = forms.CharField(required=True,
                               widget=forms.TextInput(
                                   attrs={
                                       'type': 'Text',
                                       'class': 'form-control',
                                       'placeholder': "Product Code ",
                                   }
                               ))
    photo = forms.CharField(required=True,
                               widget=forms.TextInput(
                                   attrs={
                                       'type': 'file',
                                       'class': 'form-control',
                                       'placeholder': "Upload Photo ",
                                   }
                               ))

    description = forms.CharField(required=True,
                               widget=forms.TextInput(
                                   attrs={
                                       'type': 'text',
                                       'class': 'form-control',
                                       'placeholder': "Description",
                                   }
                               ))


    plate_size = forms.CharField(required=True,
                               widget=forms.TextInput(
                                   attrs={
                                       'type': 'text',
                                       'class': 'form-control',
                                       'placeholder': "Plate Size",
                                   }
                               ))
    class Meta:
        model = Stock_System
        fields = (
            'type_of_scale',
            'hsn_code',
            'product_code',
            'product_sub_code',
            'product_sub_sub_code',
            'photo',
            'description',
            'plate_size',
            )