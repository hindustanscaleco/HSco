from django import forms
from .models import Lead
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



class Customer_detail_disabledForm(forms.ModelForm):
    customer_name = forms.CharField(max_length=80, required=True,
       widget=forms.TextInput(
           attrs={
               'type': 'text',
               'placeholder': "Customer Name",
               'class': 'form-control',
               'disabled':'disabled',
           }
       ))




    company_name = forms.CharField(max_length=80, required=True,
       widget=forms.TextInput(
           attrs={
               'type': 'text',
               'placeholder': "Company Name",
               'class': 'form-control',
               'disabled': 'disabled',
           }
       ))

    contact_no = forms.CharField(max_length=80, required=True,
       widget=forms.TextInput(
           attrs={
               'type': 'text',
               'placeholder': "Customer Name",
               'class': 'form-control',
               'disabled': 'disabled',
           }
       ))

    customer_email_id = forms.CharField(max_length=80, required=True,
       widget=forms.TextInput(
           attrs={
               'type': 'email',
               'placeholder': "Customer Email ID",
               'class': 'form-control',
               'disabled': 'disabled',
           }
       ))

    address = forms.CharField(max_length=100, required=True,
       widget=forms.TextInput(
           attrs={
               'type': 'textarea',
               'placeholder': "Address",
               'class': 'form-control',
               'disabled': 'disabled',

           }
       ))

    customer_industry = forms.CharField(max_length=80, required=True,
       widget=forms.TextInput(
           attrs={
               'type': 'text',
               'placeholder': "Industry",
               'class': 'form-control',
               'disabled': 'disabled',
           }
       ))

    customer_gst_no = forms.CharField(max_length=80, required=True,
       widget=forms.TextInput(
           attrs={
               'type': 'text',
               'placeholder': "Customer GST Number",
               'class': 'form-control',
               'disabled': 'disabled',
               'maxlength':'15',
               'minlength':'15',
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

    whatsapp2 = forms.CharField(max_length=80, required=True,
                                    widget=forms.TextInput(
                                        attrs={
                                            'type': 'text',
                                            'placeholder': "Whatsapp",
                                            'class': 'form-control',
                                        }
                                    ))



    whatsappcontent = forms.CharField(max_length=80, required=True,
                                    widget=forms.Textarea(
                                        attrs={
                                            'type': 'text',
                                            'placeholder': "Content",
                                            'class': 'form-control',
                                        }
                                    ))




    new_existing_customer = forms.CharField(max_length=80, required=True,
                                            widget=forms.TextInput(
                                                attrs={
                                                    'type': 'text',
                                                    'placeholder': "New/Existing Customer",
                                                    'class': 'form-control',
                                                }
                                            ))

    date_of_initiation = forms.CharField(max_length=80, required=True,
                                         widget=forms.TextInput(
                                             attrs={
                                                 'type': 'date',
                                                 'placeholder': "Date of Initiation",
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

    requirement = forms.CharField(max_length=80, required=True,
                                  widget=forms.TextInput(
                                      attrs={
                                          'type': 'text',
                                          'placeholder': "Requirement",
                                          'class': 'form-control',
                                      }
                                  ))

    upload_requirement_file = forms.CharField(max_length=80, required=True,
                                              widget=forms.TextInput(
                                                  attrs={
                                                      'type': 'file',
                                                      'placeholder': "FILE",
                                                      'class': 'form-control',
                                                  }
                                              ))

    owner_of_opportunity = forms.CharField(max_length=80, required=True,
                                           widget=forms.TextInput(
                                               attrs={
                                                   'type': 'Text',
                                                   'placeholder': "Owner of Opportunity",
                                                   'class': 'form-control',
                                               }
                                           ))
    discount = forms.CharField(max_length=80, required=True,
       widget=forms.TextInput(
           attrs={
               'type': 'text',
               'placeholder': "Discount",
               'class': 'form-control',
           }
       ))

    upload_pi_file = forms.CharField(max_length=80, required=True,
       widget=forms.TextInput(
           attrs={
               'type': 'text',
               'placeholder': "Upload PI File",
               'class': 'form-control',
           }
       ))

    select_pi_template = forms.CharField(max_length=80, required=True,
       widget=forms.TextInput(
           attrs={
               'type': 'date',
               'placeholder': "Select PI Template",
               'class': 'form-control',
           }
       ))

    call = forms.CharField(max_length=80, required=True,
       widget=forms.Textarea(
           attrs={
               'type': 'text',
               'placeholder': "Call",
               'class': 'form-control',
           }
       ))
    email = forms.CheckboxInput(
            attrs={
                'type':'checkbox',
                'id':'email',
                'value':'email',
                'class': 'form-control',
            }
        )


    whatsapp = forms.CheckboxInput(
            attrs={
                'type':'checkbox',
                'id':'whatsapp',
                'value':'whatsapp',
                'class': 'form-control',
            }
        )



    call2 = forms.CheckboxInput(
            attrs={
                'type':'checkbox',
                'id':'call',
                'value':'call',
                'class': 'form-control',
            }
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
        model = Lead
        fields = "__all__"