import datetime

from django.db import models
from user_app.models import SiteUser
from django.utils import timezone

list_of_month=(
    ('January','January'),
    ('February','February'),
    ('March','March'),
    ('April','April'),
    ('May','May'),
    ('June','June'),
    ('July','July'),
    ('August','August'),
    ('September','September'),
    ('October','October'),
    ('November','November'),
    ('December','December'),
)

class Defects_Warning(models.Model):
    user_id = models.ForeignKey(SiteUser,on_delete=models.CASCADE)
    type = models.CharField(max_length=60) #value can be: Defect OR Warning
    content = models.CharField(max_length=255)
    entry_timedate = models.DateTimeField(default=timezone.now,)

    def __str__(self):
        return self.user_id


class Employee_Leave(models.Model):
    user_id = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    requested_leave_date= models.DateTimeField(default=timezone.now, blank=True)
    reason=models.CharField(max_length=300,)
    is_approved =models.BooleanField(default=False)     #YES Or NO
    in_process = models.BooleanField(default=False)      #Decide Later option for manager
    leave_approved_by = models.CharField(max_length=60,)
    entry_timedate = models.DateTimeField(default=timezone.now,)


    def __str__(self):
        return self.user_id


class Ess(models.Model):
    user_id = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    employee_name=models.CharField(max_length=20,null=True, blank=True)
    details=models.CharField(max_length=250,null=True, blank=True)
    contact_no=models.CharField(max_length=20,null=True, blank=True)
    email_id=models.EmailField(max_length=20,null=True, blank=True)
    photo=models.ImageField(upload_to='profile_image/',null=True, blank=True)
    pancard=models.CharField(max_length=20,null=True, blank=True)
    aadhar_card=models.CharField(max_length=20,null=True, blank=True)

    # bank_details=models.CharField(max_length=20,null=True, blank=True)
    bank_name=models.CharField(max_length=20,null=True, blank=True)
    bank_address=models.CharField(max_length=20,null=True, blank=True)
    IFSC_code=models.CharField(max_length=20,null=True, blank=True)
    account_number=models.CharField(max_length=40,null=True, blank=True)

    photo_of_cancelled_cheque=models.ImageField(upload_to='cheque_photo/',null=True, blank=True)
    calendar=models.ForeignKey(Employee_Leave, on_delete=models.CASCADE)

    sales_target_given = models.FloatField(default=0.0, )  # in amount
    reparing_target_given = models.FloatField(default=0.0, )  # in amount


    sales_target_achived_till_now=models.FloatField(default=0.0,null=True, blank=True)
    reparing_target_achived_till_now=models.FloatField(default=0.0,null=True, blank=True)

    # month_on_month_sale_achived=models.CharField(max_length=20,null=True, blank=True)
    defect_warnings=models.ForeignKey(Defects_Warning, on_delete=models.CASCADE,null=True, blank=True)


    def __str__(self):
        return self.employee_name






class Employee_Analysis(models.Model):
    user_id = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    total_sales_done = models.FloatField(default=0.0, )  #Customer module sales done in this month in amount

    total_reparing_done = models.BigIntegerField(default=0, )  #Reparing module Reparing done in this month in units
    avg_time_to_repair_single_scale = models.FloatField(default=0.0, )  #Reparing module avg_time_to_repair_single_scale in this month
    avg_time_to_give_estimate = models.FloatField(default=0.0, )  #Reparing module savg_time_to_give_estimate in this month

    total_dispatch_done = models.BigIntegerField(default=0, )  #Dispatch module dispatch done in this month
    avg_time_dispatch_form_to_done = models.FloatField(default=0.0, )  # Reparing module avg_time_dispatch_form submit_to_done in this month

    total_restamping_done = models.BigIntegerField(default=0, )  #Restamping module restamping done in this month in unit
    avg_time_collect_to_dispatch_restamping = models.FloatField(default=0.0, )  # Restamping module avg_time_collect_to_dispatch_restamping
    total_reparing_done_onsite = models.BigIntegerField(default=0, )  # Reparing onsite module sales done in this month in amount

    month_year = models.DateTimeField(default=timezone.now,)     # extract month and year from date


    def __str__(self):
        return self.user_id



