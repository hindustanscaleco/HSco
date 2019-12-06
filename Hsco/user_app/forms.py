from django import forms
from django.contrib.auth import authenticate
from django.core.validators import RegexValidator

from .models import SiteUser

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                             message="Phone number must be entered in the format: '+999999999'. Up to 10 digits allowed.")

class SiteUser_Form(forms.ModelForm):
    class Meta:
        model = SiteUser
        fields = ('is_deleted',)

class LoginForm(forms.Form):

    mobile = forms.IntegerField(validators=[phone_regex],
         widget=forms.TextInput(
             attrs={
                 'type': 'text',
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
        fields = ( 'mobile', 'password','employee_number')


    def clean(self):
        mobile = self.cleaned_data.get('mobile')
        password = self.cleaned_data.get('password')
        user = authenticate(employee_number=mobile, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Incorrect Mobile Number or Password. Please try again !!!")
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



