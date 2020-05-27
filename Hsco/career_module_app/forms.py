import datetime

from django import forms
from .models import Career_module, EducationalDetails, WorkExperience

current_stage_field = [
    ('Applied but Not called for Interview', 'Applied but Not called for Interview'),
    ('Called for Interview', 'Called for Interview'),
    ('Selection in Progress', 'Selection in Progress'),
    ('Selected', 'Selected'),
    ('Rejected', 'Rejected'),
    ('Future Reference', 'Future Reference'),
    ('Did not Joined', 'Did not Joined'),
]

choose_position_dropdown = [
    ('--', '--'),
    ('Sales Position', 'Sales Position'),
    ('Technical Position', 'Technical Position'),

]

choose_yes_no = [
    ('No', 'No'),
    ('Yes', 'Yes'),

]


choose_1_to_10 = [
    ('01', '01'),
    ('02', '02'),
    ('03', '03'),
    ('04', '04'),
    ('05', '05'),
    ('06', '06'),
    ('07', '07'),
    ('08', '08'),
    ('09', '09'),
    ('10', '10'),

]




class Career_moduleForm(forms.ModelForm):
    current_stage = forms.CharField(
        widget=forms.Select(
            choices=current_stage_field,
            attrs={
                'default':"Applied but not call for interview",
                'class':'btn btn-secondary dropdown-toggle',

            }
        ))

    application_no = forms.CharField(max_length=80, required=False,
       widget=forms.TextInput(
           attrs={
               'type': 'text',
               'placeholder': "Application No.",
               'class': 'form-control',
               'onkeypress': 'return isNumberKey(event)',
               'readonly': 'readonly',

           }))


    phone_no = forms.CharField(max_length=10,min_length=10, required=True,
       widget=forms.TextInput(
           attrs={
               'type': 'text',
               'placeholder': "Phone No.",
               'class': 'form-control',
               'onkeypress': 'return isNumberKey(event)',
           }))



    candidate_name = forms.CharField(max_length=60, required=True,
       widget=forms.TextInput(
           attrs={
               'type': 'text',
               'placeholder': "Candidate Name",
               'class': 'form-control',
           }))

    choose_position = forms.CharField(
        widget=forms.Select(
            choices=choose_position_dropdown,
            attrs={
                'default':"--",
                'class':'btn btn-secondary dropdown-toggle',
            }
        ))

    candidate_email = forms.CharField(max_length=80, required=False,
       widget=forms.TextInput(
           attrs={
               'type': 'email',
               'placeholder': "Customer Email ID",
               'class': 'form-control',
           }))

    address = forms.CharField(max_length=1024, required=True,
       widget=forms.Textarea(
           attrs={
               'type': 'textarea',
               'placeholder': "Address",
               'class': 'form-control',
               'rows': '6',

           }))







    date_of_birth = forms.DateField( required=True,
                                         widget=forms.DateInput(
                                             attrs={
                                                 'placeholder': "Date of birth",
                                                 'class': 'form-control',
                                                 'id': 'my_date_picker',
                                             }
                                         ))




    current_salary = forms.CharField(max_length=100, required=False,
       widget=forms.TextInput(
           attrs={
               'type': 'text',
               'placeholder': "Salary",
               'class': 'form-control',

           }))

    candidate_resume = forms.FileField(required=False,
        widget=forms.FileInput(
            attrs={
                'type': 'file',
                'class': 'form-control',

            })

    )


    aadhar_card = forms.CharField(
        widget=forms.Select(
            choices=choose_yes_no,
            attrs={
                'default':"Yes",
                'class':'btn btn-secondary dropdown-toggle',
            }
        ))


    pan_card_availabe = forms.CharField(
        widget=forms.Select(
            choices=choose_yes_no,
            attrs={
                'default':"Yes",
                'class':'btn btn-secondary dropdown-toggle',
            }
        ))


    bank_account = forms.CharField(
        widget=forms.Select(
            choices=choose_yes_no,
            attrs={
                'default':"Yes",
                'class':'btn btn-secondary dropdown-toggle',
            }
        ))
    say_yourself = forms.CharField(
        widget=forms.Select(
            choices=choose_yes_no,
            attrs={
                'default': "Yes",
                'class': 'btn btn-secondary dropdown-toggle',
            }
        ))

    confidance = forms.CharField(
        widget=forms.Select(
            choices=choose_1_to_10,
            attrs={
                'default': "01",
                'class': 'btn btn-secondary dropdown-toggle',
            }
        ))

    without_job_with_reason = forms.CharField(max_length=100, required=False,
                                              widget=forms.TextInput(
                                                  attrs={
                                                      'type': 'text',
                                                      'placeholder': "Reason",
                                                      'class': 'form-control',
                                                  }))

    reason_for_last_job_before = forms.CharField(max_length=100, required=False,
                                                 widget=forms.TextInput(
                                                     attrs={
                                                         'type': 'text',
                                                         'placeholder': "Reason",
                                                         'class': 'form-control',
                                                     }))

    working_from_10_to_8_and = forms.CharField(
        widget=forms.Select(
            choices=choose_yes_no,
            attrs={
                'default': "Yes",
                'class': 'btn btn-secondary dropdown-toggle',
            }
        ))

    any_question = forms.CharField(
        widget=forms.Select(
            choices=choose_yes_no,
            attrs={
                'default': "No",
                'class': 'btn btn-secondary dropdown-toggle',
            }
        ))

    any_question_yes = forms.CharField(required=False,
                                       widget=forms.Textarea(
                                           attrs={
                                               'type': 'text',
                                               'placeholder': "Reason",
                                               'class': 'form-control',
                                               'rows':'40',
                                               'onkeyup': 'AnyQuestionChar(this)',

                                           }))

    comfortable_english = forms.CharField(
        widget=forms.Select(
            choices=choose_yes_no,
            attrs={
                'default': "Yes",
                'class': 'btn btn-secondary dropdown-toggle',
            }
        ))

    how_good_english = forms.CharField(
        widget=forms.Select(
            choices=choose_1_to_10,
            attrs={
                'default': "01",
                'class': 'btn btn-secondary dropdown-toggle',
            }
        ))

    comfortable_marathi = forms.CharField(
        widget=forms.Select(
            choices=choose_yes_no,
            attrs={
                'default': "Yes",
                'class': 'btn btn-secondary dropdown-toggle',
            }
        ))

    working_from_10_to_8 = forms.CharField(
        widget=forms.Select(
            choices=choose_yes_no,
            attrs={
                'default': "Yes",
                'class': 'btn btn-secondary dropdown-toggle',
            }
        ))

    weighting_scale_manufactures_mumbai = forms.CharField(max_length=100, required=False,
                                                          widget=forms.TextInput(
                                                              attrs={
                                                                  'type': 'text',
                                                                  'placeholder': "Min",
                                                                  'class': 'form-control',
                                                              }))

    excel_formate = forms.CharField(
        widget=forms.Select(
            choices=choose_yes_no,
            attrs={
                'default': "Yes",
                'class': 'btn btn-secondary dropdown-toggle',
            }
        ))

    sum_in_excel = forms.CharField(
        widget=forms.Select(
            choices=choose_yes_no,
            attrs={
                'default': "Yes",
                'class': 'btn btn-secondary dropdown-toggle',
            }
        ))

    time_taken = forms.CharField(max_length=100, required=False,
                                 widget=forms.TextInput(
                                     attrs={
                                         'type': 'text',
                                         'placeholder': "Sec",
                                         'class': 'form-control',
                                     }))

    take_out_60 = forms.CharField(
        widget=forms.Select(
            choices=choose_yes_no,
            attrs={
                'default': "Yes",
                'class': 'btn btn-secondary dropdown-toggle',
            }
        ))

    time_to_disorder_wire_pcb = forms.CharField(max_length=100, required=False,
                                                widget=forms.TextInput(
                                                    attrs={
                                                        'type': 'text',
                                                        'placeholder': "Sec",
                                                        'class': 'form-control',
                                                    }))

    time_to_solder_wire_back = forms.CharField(max_length=100, required=False,
                                               widget=forms.TextInput(
                                                   attrs={
                                                       'type': 'text',
                                                       'placeholder': "Sec",
                                                       'class': 'form-control',
                                                   }))

    soldering_strong = forms.CharField(
        widget=forms.Select(
            choices=choose_yes_no,
            attrs={
                'default': "Yes",
                'class': 'btn btn-secondary dropdown-toggle',
            }
        ))

    value_of_resister = forms.CharField(
        widget=forms.Select(
            choices=choose_yes_no,
            attrs={
                'default': "Yes",
                'class': 'btn btn-secondary dropdown-toggle',
            }
        ))
    open_and_short_circuit = forms.CharField(
        widget=forms.Select(
            choices=choose_yes_no,
            attrs={
                'default': "Yes",
                'class': 'btn btn-secondary dropdown-toggle',
            }
        ))

    notes = forms.CharField( required=False,
     widget=forms.Textarea(
         attrs={
             'type': 'text',
             'placeholder': "Notes",
             'class': 'form-control',
             'onkeyup': 'NotesChar(this)',
             'rows': '40',

         }))
    class Meta:
        model = Career_module
        fields = "__all__"

class EducationForm(forms.ModelForm):
    institute_name = forms.CharField(max_length=100, required=False,
     widget=forms.TextInput(
         attrs={
             'type': 'text',
             'placeholder': "Institute Name / University",
             'class': 'form-control',

         }))

    course = forms.CharField(max_length=100, required=False,
     widget=forms.TextInput(
         attrs={
             'type': 'text',
             'placeholder': "Course",
             'class': 'form-control',

         }))

    year_of_completion = forms.CharField(min_length=4, max_length=4, required=False,
     widget=forms.TextInput(
         attrs={
             'type': 'number',
             'placeholder': "Year Of Completion",
             'class': 'form-control',
             'min': '1990',
             'max': '2020',
             'value': datetime.datetime.now().year
         }))


    percentage = forms.CharField(max_length=100, required=False,
       widget=forms.TextInput(
           attrs={
               'type': 'text',
               'placeholder': "Percentage or Grade",
               'class': 'form-control',

           }))

    achievements = forms.CharField(required=False,
      widget=forms.Textarea(
          attrs={
              'type': 'textarea',
              'placeholder': "Achievements",
              'class': 'form-control',
              'onkeyup': 'AchievementsChar(this)',
              'rows': '10',
              'cols': '4',
          }))
    class Meta:
        model = EducationalDetails
        fields = "__all__"


class WorkExpForm(forms.ModelForm):
    company_name = forms.CharField(max_length=100, required=False,
       widget=forms.TextInput(
           attrs={
               'type': 'text',
               'placeholder': "Company Name",
               'class': 'form-control',

           }))

    work_expirance_from = forms.DateField(required=False,
      widget=forms.DateInput(
          attrs={
              'placeholder': "Date of Initiation",
              'class': 'form-control',
              'size':'1',
          }
      ))

    work_expirance_to = forms.DateField(required=False,
        widget=forms.DateInput(
            attrs={
                'placeholder': "Date of Initiation",
                'class': 'form-control',
            }
        ))


    work_expirance_details = forms.CharField(required=False,
       widget=forms.Textarea(
           attrs={
               'type': 'text',
               'placeholder': "Experience Details",
               'class': 'form-control',
               'rows':'10',
               'cols':'4',
               'onkeyup': 'ExpandAchChar(this)',

           }))

    designation = forms.CharField(max_length=100, required=False,
       widget=forms.TextInput(
           attrs={
               'type': 'text',
               'placeholder': "Designation",
               'class': 'form-control',

           }))

    class Meta:
        model = WorkExperience
        fields = "__all__"







