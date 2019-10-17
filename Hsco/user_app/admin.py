from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import SiteUser


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = SiteUser
        fields = ('email', 'mobile',)

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password=(self.cleaned_data.get("password"))
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    # password = ReadOnlyPasswordHashField()

    class Meta:
        model = SiteUser
        fields = ('name','email', 'password', 'mobile',  'role')

    def clean_password(self):
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'name','mobile',  'role')
    list_filter = ( 'role',)

    fieldsets = (
                ('Login Credentials', {'fields': ('mobile', 'password')}),
        ('Personal info', {'fields': ('modules_assigned','email', 'name', 'role','date_of_joining','average_rating','group')}),
        ('Bank Details', {'fields': ('bank_name', 'account_number', 'bank_address','IFSC_code')}),
        ('Seen', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('mobile', 'email', 'name','role','date_of_joining','average_rating',
                       'bank_name','account_number','bank_address','IFSC_code','auto_timedate','password', 'password2', )}
         ),
    )
    search_fields = ('mobile', 'name')
    ordering = ('id',)
    filter_horizontal = ()




admin.site.register(SiteUser, UserAdmin)
admin.site.unregister(Group)






