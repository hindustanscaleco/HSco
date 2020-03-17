from django import forms
from .models import Lead, Pi_product
import sys
sys.path.append("..")
from customer_app.models import Customer_Details


auto_manual_email = [
    ('Automatic', 'Automatic'),
    ('Manual', 'Manual'),
]

payment_channel = [
    ('Check Payment', 'Check Payment'),
    ('Cash', 'Cash'),
]


industory_dropdown = [
        ('Energy industry','Energy industry'),
        ('Chemicals','Chemicals'),
        ('Industrial Metals ','Industrial Metals '),
        ('Gold/Gems and precious Metals ','Gold/Gems and precious Metals '),
        ('Home and Heavy Construction companies ','Home and Heavy Construction companies '),
        ('Electrical and Electronic Manufacturers','Electrical and Electronic Manufacturers'),
        ('Industrial Transportation','Industrial Transportation'),
        ('Agriculture','Agriculture'),
        ('Poultry/Livestock','Poultry/Livestock'),
        ('Healthcare Equipment and Services','Healthcare Equipment and Services'),
        ('Textiles','Textiles'),
        ('Hotels','Hotels'),
        ('Grocery/Retail','Grocery/Retail'),
        ('Bakery','Bakery'),
        ('Supplier','Supplier'),
        ('BNI','BNI'),
        ('Online Promotion','Online Promotion'),
]

select_pi_template = [
    ('Proforma Invoice Hindustan Sales and Consultancy','Proforma Invoice Hindustan Sales and Consultancy'),
    ('HSI PI Format','HSI PI Format'),
]



customer_exist_new = [
    ('New','New'),
    ('Existing','Existing'),
]

stage = [
    ('Not Yet Initiated','Not Yet Initiated'),
    ('Customer Called','Customer Called'),
    ('PI Sent & Follow-up','PI Sent & Follow-up'),
    ('PO Issued - Payment not done','PO Issued - Payment not done'),
    ('PO Issued - Payment Done - Dispatch Pending','PO Issued - Payment Done - Dispatch Pending'),
    ('Dispatch Done - Closed','Dispatch Done - Closed'),
    ('Lost','Lost'),
    ('Not Relevant','Not Relevant'),
    ('Postponed','Postponed'),
]



class Customer_detailForm(forms.ModelForm):
    customer_name = forms.CharField(max_length=80, required=True,
       widget=forms.TextInput(
           attrs={
               'type': 'text',
               'placeholder': "Customer Name",
               'class': 'form-control',
           }
       ))




    company_name = forms.CharField(max_length=80, required=False,
       widget=forms.TextInput(
           attrs={
               'type': 'text',
               'placeholder': "Company Name",
               'class': 'form-control',
           }
       ))

    contact_no = forms.CharField(max_length=80, required=True,
       widget=forms.TextInput(
           attrs={
               'type': 'text',
               'placeholder': "Customer Name",
               'class': 'form-control',
           }
       ))

    customer_email_id = forms.CharField(max_length=80, required=False,
       widget=forms.TextInput(
           attrs={
               'type': 'email',
               'placeholder': "Customer Email ID",
               'class': 'form-control',
           }
       ))

    address = forms.CharField(max_length=100, required=True,
       widget=forms.TextInput(
           attrs={
               'type': 'textarea',
               'placeholder': "Address",
               'class': 'form-control',

           }
       ))

    customer_industry = forms.CharField(max_length=80, required=True,
    widget=forms.Select(
        choices=industory_dropdown,
           attrs={
               'type': 'text',
               'placeholder': "Industry",
               'class': 'form-control',
           }
       ))

    customer_gst_no = forms.CharField(max_length=15, min_length=15, required=False,
       widget=forms.TextInput(
           attrs={
               'type': 'text',
               'placeholder': "Customer GST Number",
               'class': 'form-control',

           }
       ))


    class Meta:
        model = Customer_Details
        fields = "__all__"






class Deal_detailForm(forms.ModelForm):
    current_stage = forms.CharField(max_length=80, required=True,
                                    widget=forms.Select(
                                        choices=stage,
                                        attrs={
                                            'default': "automatic",
                                            'class': 'btn btn-outline-primary',

                                        }
                                    ))

    new_existing_customer = forms.CharField(max_length=80, required=True,
                                    widget=forms.Select(
                                        choices=customer_exist_new,
                                        attrs={
                                            'type': 'text',
                                            'placeholder': "Person",
                                            'class': 'form-control',
                                        }
                                    ))



    requirement = forms.CharField(max_length=80, required=True,
                                    widget=forms.Textarea(
                                        attrs={
                                            'type': 'file',
                                            'placeholder': "Requirement",
                                            'class': 'form-control',
                                        }
                                    ))




    channel = forms.CharField(max_length=80, required=True,
                                            widget=forms.TextInput(
                                                attrs={
                                                    'type': 'text',
                                                    'placeholder': "Channel",
                                                    'class': 'form-control',
                                                }
                                            ))

    date_of_initiation = forms.DateField( required=True,
                                         widget=forms.DateInput(

                                             attrs={
                                                 'type': 'date',
                                                 'placeholder': "Date of Initiation",
                                                 'class': 'form-control',
                                             }
                                         ))

    upload_requirement_file = forms.CharField(max_length=80,required=False,
                              widget=forms.TextInput(
                                  attrs={
                                      'type': 'file',
                                      'class': 'form-control',
                                  }
                              ))

    owner_of_opportunity = forms.CharField(max_length=80, required=False,
                                  widget=forms.TextInput(
                                      attrs={
                                          'type': 'text',
                                          'placeholder': "Owner",
                                          'class': 'form-control',
                                      }
                                  ))
    class Meta:
        model = Lead
        fields = "__all__"


class Pi_sectionForm(forms.ModelForm):


    discount = forms.CharField(max_length=80, required=True,
       widget=forms.TextInput(
           attrs={
               'type': 'text',
               'placeholder': "Discount",
               'class': 'form-control',
           }
       ))

    upload_pi_file = forms.FileField(required=False,
       widget=forms.FileInput(
           attrs={
               'type': 'file',
               'placeholder': "Upload PI File",
               'class': 'form-control',
           }
       ))

    select_pi_template = forms.CharField(required=False,
       widget=forms.Select(choices=select_pi_template,
           attrs={
               'type': 'text',
               'placeholder': "Select PI Template",
               'class': 'form-control',
           }
       ))

    call = forms.CharField(required=False,
        widget=forms.Textarea(
            attrs={
                'type':'text',
                'id':'call',
            })
        )
    email = forms.BooleanField(required=False,
        widget=forms.TextInput(
            attrs={
                'type':'checkbox',
                'id':'email',
            })
        )
    whatsapp = forms.BooleanField(required=False,
        widget=forms.TextInput(
            attrs={
                'type':'checkbox',
                'id':'whatsapp',
            })
        )
    call2 = forms.BooleanField(required=False,
        widget=forms.TextInput(
            attrs={
                'type': 'checkbox',
                'id': 'call2',
                'onclick' : 'myFunction_call()',
                'calss' : 'form-control',
            })
    )





    email_auto_manual = forms.CharField(
        widget=forms.Select(
            choices=auto_manual_email,
            attrs={
                'default':"automatic",
                'class':'btn btn-outline-primary',


            }
        ))

    payment_channel = forms.CharField(
        widget=forms.Select(
            choices=auto_manual_email,
            attrs={
                'default':"Check Payment",
                'class':'btn btn-primary',
                'style':'background-color: #FC6E20;'
            }
        ))

    payment_receipt = forms.CharField(max_length=80, required=True,
                                              widget=forms.TextInput(
                                                  attrs={
                                                      'type': 'file',
                                                      'placeholder': "FILE",
                                                      'class': 'form-control',
                                                  }
                                              ))
    upload_po_file = forms.CharField(max_length=80, required=True,
                                              widget=forms.TextInput(
                                                  attrs={
                                                      'type': 'file',
                                                      'placeholder': "FILE",
                                                      'class': 'form-control',
                                                  }
                                              ))


    payment_received_date = forms.CharField(max_length=80, required=True,
                                         widget=forms.TextInput(
                                             attrs={
                                                 'type': 'date',
                                                 'class': 'form-control',
                                             }
                                         ))

    notes = forms.CharField(max_length=80, required=True,
                                         widget=forms.Textarea(
                                             attrs={
                                                 'type': 'text',
                                                 'placeholder':'Notes',
                                                 'class': 'form-control',
                                             }
                                         ))
    class Meta:
        model = Pi_product
        fields = "__all__"