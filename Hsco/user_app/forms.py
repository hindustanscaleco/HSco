from django import forms
from django.contrib.auth import authenticate
from django.core.validators import RegexValidator
from django.contrib import messages
from django.db.models import F


from .models import SiteUser

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                             message="Phone number must be entered in the format: '+999999999'. Up to 10 digits allowed.")

class SiteUser_Form(forms.ModelForm):
    class Meta:
        model = SiteUser
        fields = ('is_deleted',)

class LoginForm(forms.Form):

    mobile = forms.CharField(
         widget=forms.TextInput(
             attrs={
                 'type': 'text',
                #  'onkeypress':"return isNumber(event)",
                 'class': 'form-control',
                 'placeholder': "Enter Employee Number",
                 'name': 'mobile',
             }))

    # employee_number = forms.IntegerField(
    #      widget=forms.TextInput(
    #          attrs={
    #              'type': 'text',
    #              'onkeypress':"return isNumber(event)",
    #              'class': 'form-control',
    #              'placeholder': "Employee Number",
    #              'name': 'employee_number',
    #          }))


    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'type': 'password',
                'class': 'form-control',
                'placeholder': "Password",
                'name': 'password',
            }))

    class Meta:
        model = SiteUser
        fields = ( 'mobile', 'password')


    def clean(self):
        mobile = self.cleaned_data.get('mobile')
        password = self.cleaned_data.get('password')
        
        
        user = authenticate(employee_number=mobile, password=password)

        # deleted user cannot be logged in !!!
        if SiteUser.objects.get(employee_number=mobile).is_deleted == True:
            raise forms.ValidationError("Deleted user cannot be logged in !")

        if not user or not user.is_active:

            # if user has been logged out by super admin using active=false
            if SiteUser.objects.get(employee_number=mobile).is_active == False:
                raise forms.ValidationError("You have been restricted to use this account!")

            # incorrect password for 10 times will locked the account !!!
            if SiteUser.objects.get(employee_number=mobile).role != 'Super Admin' :
                if SiteUser.objects.get(employee_number=mobile).incorrect_pass_count == 10:
                    raise forms.ValidationError("You have entered an incorrect pin several times ! Your profile has been locked !!!")
                else:
                    SiteUser.objects.filter(employee_number=mobile).update(incorrect_pass_count=(F("incorrect_pass_count") + 1))
            
            raise forms.ValidationError("Incorrect Mobile Number or Password. Please try again !!!")
        SiteUser.objects.filter(employee_number=mobile).update(incorrect_pass_count=0)
        return self.cleaned_data

    def login(self, request):
        mobile = self.cleaned_data.get('mobile')
        password = self.cleaned_data.get('password')
        user = authenticate(username=mobile, password=password)
        return user

class Password_reset_Form(forms.Form):

    email =forms.EmailField(
        widget=forms.PasswordInput(
        attrs={
            'type': 'email',
            'class': 'form-control form-control-user',
            ' placeholder': "Enter Email",
            'name': 'email',
        }))



