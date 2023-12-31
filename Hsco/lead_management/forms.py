from django import forms
from .models import Lead, Pi_section, Follow_up_section, History_followup, Payment_details

import sys
sys.path.append("..")
from customer_app.models import Lead_Customer_Details

auto_manual_email = [
    ('Automatic', 'Automatic'),
    ('Manual', 'Manual'),
]

payment_channel = [
    ('Check Payment', 'Check Payment'),
    ('Cash', 'Cash'),
]


payment_method = [
    ('Cheque','Cheque'),
    ('Card','Card'),
    ('Cash','Cash')
]

industory_dropdown = [
        ('','Select industry'),
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
        ('Fishing','Fishing'),
        ('Dealer','Dealer'),
]

auto_manual_email = [
    ('Select Mode', 'Select Mode'),
    ('Automatic', 'Automatic'),
    ('Manual', 'Manual'),
]

select_pi_template = [
    ('','Select'),
    ('1','Proforma Invoice For Hindustan Scale Company'),
    ('2','Proforma Invoice For Hindustan Scales And Consultancy'),
]


select_gst_type= [
    ('','Select'),
    ('CGST / SGST','CGST / SGST'),
    ('IGST','IGST'),
]

discount_type= [
    ('rupee','₹'),
    ('percent','%'),
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
           }))

    company_name = forms.CharField(max_length=80, required=False,
       widget=forms.TextInput(
           attrs={
               'type': 'text',
               'placeholder': "Company Name",
               'class': 'form-control',
           }))

    contact_no = forms.CharField(max_length=80, required=True,
       widget=forms.TextInput(
           attrs={
               'type': 'text',
               'placeholder': "Contact No",
               'class': 'form-control',
           }))

    customer_email_id = forms.CharField(max_length=80, required=False,
       widget=forms.TextInput(
           attrs={
               'type': 'email',
               'placeholder': "Customer Email ID",
               'class': 'form-control',
           }))

    address = forms.CharField(max_length=1000, required=True,
       widget=forms.Textarea(
           attrs={
               'type': 'textarea',
               'placeholder': "Address",
               'class': 'form-control',

           }))

    optional_email = forms.CharField(max_length=700, required=False,
      widget=forms.Textarea(
          attrs={
              'type': 'textarea',
              'placeholder': "Optional Email(Comma Separated)",
              'class': 'form-control',

          }))

    customer_industry = forms.CharField(max_length=80, required=True,
    widget=forms.Select(
        choices=industory_dropdown,
           attrs={
               'type': 'text',
               'placeholder': "Industry",
               'class': 'form-control',
           }))

    customer_gst_no = forms.CharField(max_length=15, min_length=15, required=False,
       widget=forms.TextInput(
           attrs={
               'type': 'text',
               'placeholder': "Customer GST Number",
               'class': 'form-control',
           }))


    class Meta:
        model = Lead_Customer_Details
        fields = "__all__"




class Deal_detailForm(forms.ModelForm):
    current_stage = forms.CharField(max_length=80, required=True,
                                    widget=forms.Select(
                                        choices=stage,
                                        attrs={
                                            'default': "Not Yet Initiated",
                                            'class': 'btn btn-outline-primary',
                                            'id': 'deal_stage',

                                        }
                                    ))

    new_existing_customer = forms.CharField(max_length=80, required=True,
                                    widget=forms.Select(
                                        choices=customer_exist_new,
                                        attrs={
                                            'type': 'text',
                                            'placeholder': "Person",
                                            'class': 'form-control',
                                            'id': 'new_existing_customer_id',
                                        }
                                    ))



    requirement = forms.CharField(required=True,
                                    widget=forms.Textarea(
                                        attrs={
                                            'type': 'text',
                                            'placeholder': "Requirement",
                                            'class': 'form-control',
                                            'onkeyup': 'RequirementcountChar(this)',

                                        }
                                    ))




    channel = forms.CharField(max_length=80, required=True,
                                            widget=forms.TextInput(
                                                attrs={
                                                    'type': 'text',
                                                    'placeholder': "Channel Of Sales",
                                                    'class': 'form-control',
                                                }
                                            ))

    channel_of_marketing = forms.CharField(max_length=80, required=True,
                                            widget=forms.TextInput(
                                                attrs={
                                                    'type': 'text',
                                                    'placeholder': "Channel Of Marketing",
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

    postpond_time_date = forms.DateField( required=False,
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

    owner_of_opportunity = forms.CharField(max_length=80, required=True,
                                  widget=forms.TextInput(
                                      attrs={
                                          'type': 'text',
                                          'placeholder': "Owner",
                                          'class': 'form-control',
                                      }
                                  ))

    owner_of_opportunity_employee = forms.CharField(max_length=80, required=True,
                   widget=forms.TextInput(
                       attrs={
                           'type': 'text',
                           'placeholder': "Owner",
                           'class': 'form-control',
                           'disabled': 'disabled',
                       }
                   ))

    lost_reason = forms.CharField( max_length=1024,required=False,
                                    widget=forms.Textarea(
                                        attrs={
                                            'type': 'text',
                                            'placeholder': "Reason",
                                            'class': 'form-control',
                                        }
                                    ))
    postponed_reason = forms.CharField(max_length=80, required=False,
                                    widget=forms.Textarea(
                                        attrs={
                                            'type': 'text',
                                            'placeholder': "Reason",
                                            'class': 'form-control',
                                        }
                                    ))
    class Meta:
        model = Lead
        fields = "__all__"



class Pi_sectionForm(forms.ModelForm):


    discount = forms.CharField(max_length=80, required=False,
       widget=forms.TextInput(
           attrs={
               'type': 'text',
               'default': '0',
               'placeholder': "Discount",
               'class': 'form-control',
               'value': '0',
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
               'id': 'select_pi_template_id',
           }
       ))

    select_gst_type = forms.CharField(required=False,
       widget=forms.Select(choices=select_gst_type,
             attrs={
                 'type': 'text',
                 'placeholder': "Select GST Type",
                 'class': 'form-control',
                 'id': 'select_gst_type_id',
             }
             ))

    discount_type = forms.CharField(required=False,
          widget=forms.Select(choices=discount_type,
          attrs={
              'type': 'text',
              'placeholder': "Discount Type",
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
        widget=forms.CheckboxInput(
            attrs={
                'type':'checkbox',
                'id':'email',
            })
        )
    whatsapp = forms.BooleanField(required=False,
        widget=forms.CheckboxInput(
            attrs={
                'type':'checkbox',
                'id':'whatsapp',
            })
        )
    call2 = forms.BooleanField(required=False,
        widget=forms.CheckboxInput(
            attrs={
                'type': 'checkbox',
                'id': 'call2',
                'onclick': 'myFunction_call()',
            })
    )

    email_auto_manual = forms.CharField(
        widget=forms.Select(
            choices=auto_manual_email,
            attrs={
                'default':"Select Mode",
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

    grand_total = forms.CharField(max_length=80, required=False,
                                         widget=forms.TextInput(
                                             attrs={
                                                 'type': 'text',
                                                 'placeholder':'External PI Amount',
                                                 'class': 'form-control',
                                                 'id': 'grand_total_id',
                                             }
                                         ))

    email_auto_manual = forms.CharField(
        widget=forms.Select(
            choices=auto_manual_email,
            attrs={
                'default':"automatic",
                'class':'btn btn-outline-primary',


            }
        ))


    class Meta:
        model = Pi_section
        fields = "__all__"

class History_followupForm(forms.ModelForm):
    is_email = forms.BooleanField(required=False,
                               widget=forms.CheckboxInput(
                                    attrs={
                                        'type': 'checkbox',
                                        'onclick': 'hisFunction()',

        }))


    is_whatsapp = forms.BooleanField(required=False,
                               widget=forms.CheckboxInput(
                                   attrs={
                                       'type': 'checkbox',
                                       'onclick': 'yourFunction()',
                                   })
                               )

    is_call = forms.BooleanField(required=False,
                               widget=forms.CheckboxInput(
                                    attrs={
                                        'type': 'checkbox',
                                        'id': 'is_call',
                                        'onclick': 'herFunction()',
                                    }
                                ))

    is_sms = forms.BooleanField(required=False,
                               widget=forms.CheckboxInput(
                                    attrs={
                                        'type': 'checkbox',
                                        'id': 'is_sms',
                                        'onclick': 'whosFunction()',
                                    }
                                ))


    wa_no = forms.CharField(max_length=20, required=False,
                                 widget=forms.TextInput(
                                     attrs={
                                         'type': 'text',
                                         'placeholder': "Whatsapp No",
                                         'class': 'form-control',

                                     }
                                 ))

    wa_msg = forms.CharField(max_length=1024, required=False,
                             widget=forms.Textarea(
                                 attrs={
                                     'type': 'text',
                                     'placeholder': "Content",
                                     'class': 'form-control',
                                     'onkeyup': 'WhatsappcountChar(this)',
                                 }))
    email_subject = forms.CharField(max_length=120, required=False,
                                    widget=forms.TextInput(
                                        attrs={
                                            'type': 'text',
                                            'placeholder': "Subject",
                                            'class': 'form-control',
                                        }
                                    ))
    email_msg = forms.CharField(max_length=1024, required=False,
                                    widget=forms.Textarea(
                                        attrs={
                                            'type': 'text',
                                            'placeholder': "Emai Content",
                                            'class': 'form-control',
                                            'onkeyup': 'EmailcountChar(this)',

                                        }))
    call_response = forms.CharField(max_length=1024, required=False,
                                    widget=forms.Textarea(
                                        attrs={
                                            'type': 'text',
                                            'placeholder': "Call Response",
                                            'class': 'form-control',
                                            'onkeyup': 'CallcountChar(this)',

                                        }))
    sms_msg = forms.CharField(max_length=120, required=False,
                                    widget=forms.Textarea(
                                        attrs={
                                            'type': 'text',
                                            'placeholder': "Content",
                                            'class': 'form-control',
                                            'onkeyup': 'SMScountChar(this)',

                                        }))

    class Meta:
        model = History_followup
        fields = "__all__"



class Follow_up_sectionForm(forms.ModelForm):

    subject = forms.CharField(max_length=80, required=True,
       widget=forms.Textarea(
           attrs={
               'type': 'text',
               'placeholder': "Call",
               'class': 'form-control',
           }))


    email_auto_manual = forms.CharField(
        widget=forms.Select(
            choices=auto_manual_email,
            attrs={
                'default':"automatic",
                'class':'btn btn-outline-primary',
                'id': 'purpose',
            }
        ))

    whatsappno = forms.CharField(max_length=80, required=True,
       widget=forms.TextInput(
           attrs={
               'type': 'text',
               'placeholder': "Whatsapp No",
               'class': 'form-control',

           }
       ))



    class Meta:
        model = Follow_up_section
        fields = "__all__"


class Payment_detailsForm(forms.ModelForm):
    payment_channel = forms.CharField(
        widget=forms.Select(
            choices=payment_method,
            attrs={
                'default':"Cheque",
                'class':'btn btn-outline-primary',
            }
        ))

    payment_receipt = forms.CharField(max_length=80, required=False,
                                              widget=forms.TextInput(
                                                  attrs={
                                                      'type': 'file',
                                                      'placeholder': "FILE",
                                                      'class': 'form-control',
                                                  }
                                              ))

    upload_pofile = forms.CharField(max_length=80, required=False,
                                              widget=forms.TextInput(
                                                  attrs={
                                                      'type': 'file',
                                                      'placeholder': "FILE",
                                                      'class': 'form-control',
                                                  }
                                              ))

    payment_recived_date = forms.DateField( required=True,
                                         widget=forms.DateInput(
                                             attrs={
                                                 'type': 'date',
                                                 'class': 'form-control',
                                             }
                                         ))

    Payment_notes = forms.CharField(max_length=80, required=False,
                                         widget=forms.Textarea(
                                             attrs={
                                                 'type': 'text',
                                                 'placeholder':'Notes',
                                                 'class': 'form-control',
                                             }
                                         ))


    class Meta:
        model = Payment_details
        fields = "__all__"
