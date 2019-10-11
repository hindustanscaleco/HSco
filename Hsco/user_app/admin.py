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
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = SiteUser
        fields = ('email', 'password', 'mobile',  'user_type')

    def clean_password(self):
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'mobile',  'user_type')
    list_filter = ( 'user_type',)

    fieldsets = (
                ('Login Credentials', {'fields': ('mobile', 'password')}),
        ('Personal info', {'fields': ('email', 'name', 'user_type','sales_target','target_achieved','repairing_no_of_repairs','repairing_target_achieved','date_of_joining','average_rating')}),
        ('Bank Details', {'fields': ('bank_name', 'account_no', 'branch_name','ifsc_code')}),
        ('Seen', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('mobile', 'email', 'name','user_type','sales_target','target_achieved','date_of_joining','average_rating',
                       'bank_name','account_no','branch_name','ifsc_code','auto_timedate','password', 'password2',   )}
         ),
    )
    search_fields = ('mobile', 'name')
    ordering = ('id',)
    filter_horizontal = ()




admin.site.register(SiteUser, UserAdmin)
admin.site.unregister(Group)






