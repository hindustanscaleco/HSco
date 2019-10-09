from django import forms

from .models import Customer_Details
from .models import Product_Details


class Customer_Details_Form(forms.ModelForm):



    class Meta:
        model = Customer_Details
        fields = (
        'crn_number',
        'company_name',
        'address',
        'contact_no',
        'customer_email_id',
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
