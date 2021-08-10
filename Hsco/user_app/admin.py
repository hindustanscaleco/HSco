from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from import_export.admin import ImportExportModelAdmin

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
        fields = ('name','email', 'password', 'mobile',  'role')

    def clean_password(self):
        return self.initial["password"]


def flush_users(modeladmin, request, queryset):
    # if queryset.filter(is_admin=True):
    #     pass
    # else:
    queryset.update(is_active=False)

flush_users.short_description = "Flush Selected Users"

def allow_users_login(modeladmin, request, queryset):
    queryset.update(is_active=True)
allow_users_login.short_description = "Allow Selected Users To Login"

class UserAdmin(ImportExportModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'employee_number', 'name','mobile',  'role', 'is_active')
    list_filter = ( 'role','is_deleted')

    fieldsets = (
                ('Login Credentials', {'fields': ('mobile', 'password', 'name','employee_number','can_reply_to_sa','product_master_access','professional_email','professional_email_password','is_active')}),
        ('Personal info', {'fields': ('modules_assigned','login_sms_number','email', 'profile_name', 'role','manager','admin','super_admin','date_of_joining','average_rating','group','pancard','aadhar_card','photo','upload_pancard','upload_aadhar_card','is_deleted','is_admin')}),
        ('Bank Details', {'fields': ('bank_name', 'account_number', 'branch_name','ifsc_code')}),
        ('Seen', {'fields': ('last_login','password_text')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('mobile', 'email', 'name','role','date_of_joining','average_rating',
                       'bank_name','account_number','branch_name','ifsc_code','auto_timedate','password', 'password2', )}
         ),
    )
    search_fields = ('mobile', 'name')
    ordering = ('id',)
    filter_horizontal = ()
    actions = [flush_users,allow_users_login]




admin.site.register(SiteUser, UserAdmin)
admin.site.unregister(Group)






