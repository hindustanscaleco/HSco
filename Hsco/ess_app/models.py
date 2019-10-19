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
    # ess_id = models.ForeignKey(Ess, on_delete=models.CASCADE)
    type = models.CharField(max_length=60) #value can be: Defect OR Warning
    content = models.CharField(max_length=255)
    entry_timedate = models.DateTimeField(default=timezone.now,)
    given_by = models.CharField(max_length=90)

    def __str__(self):
        return str(self.user_id)

class Employee_Leave(models.Model):
    user_id = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    # ess_id=models.ForeignKey(Ess, on_delete=models.CASCADE)
    requested_leave_date_from= models.DateTimeField(default=timezone.now, blank=True)
    requested_leave_date_to= models.DateTimeField(default=timezone.now, blank=True)
    reason=models.CharField(max_length=300,)
    is_approved =models.BooleanField(default=False,null=True, blank=True)     #YES Or NO
    in_process = models.BooleanField(default=False ,null=True, blank=True)      #Decide Later option for manager
    leave_approved_by = models.CharField(max_length=60,null=True, blank=True)
    is_employee_of_month = models.BooleanField(default=False)

    entry_timedate = models.DateTimeField(default=timezone.now,)


    def __str__(self):
        return str(self.user_id)

    class Meta:
        unique_together = ('requested_leave_date_from', 'requested_leave_date_to', 'user_id','reason')


class Employee_Analysis_month(models.Model):
    user_id = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    manager_id = models.CharField(max_length=60, null=True, blank=True)
    is_employee_of_month = models.BooleanField(default=False)
    #TARGETS_GIVEN
    sales_target_given = models.FloatField(default=0.0, )  # in amount
    reparing_target_given = models.FloatField(default=0.0, )  # in amount
    restamping_target_given = models.FloatField(default=0.0, )  # in amount
    #DONE_THIS_MONTH
    total_sales_done = models.FloatField(default=0.0, )  # Customer module sales done in this month in amount
    total_dispatch_done = models.BigIntegerField(default=0, )  # Dispatch module dispatch done in this month
    total_reparing_done = models.BigIntegerField(default=0, )  # Reparing module Reparing done in this month in units
    total_restamping_done = models.BigIntegerField(default=0, )  # Restamping module restamping done in this month in unit
    total_reparing_done_onsite = models.BigIntegerField(default=0, )  # Reparing onsite module sales done in this month in amount
    #AVERAGE
    avg_time_to_repair_single_scale = models.FloatField(default=0.0, )  # Reparing module avg_time_to_repair_single_scale in this month
    avg_time_to_give_estimate = models.FloatField(default=0.0, )  # Reparing module savg_time_to_give_estimate in this month
    avg_time_dispatch_form_to_done = models.FloatField(default=0.0, )  # Reparing module avg_time_dispatch_form submit_to_done in this month
    avg_time_collect_to_dispatch_restamping = models.FloatField(default=0.0, )  # Restamping module avg_time_collect_to_dispatch_restamping
    #ACHIEVED_TILL_NOW
    sales_target_achived_till_now = models.FloatField(default=0.0, null=True, blank=True)
    reparing_target_achived_till_now = models.FloatField(default=0.0, null=True, blank=True)


    entry_timedate = models.DateTimeField(default=timezone.now,)     # extract month and year from date
    month = models.CharField(max_length=20, null=True, blank=True,choices=list_of_month)    # extract month and year from date
    year = models.IntegerField()    # extract month and year from date


    class Meta:
        unique_together = ('user_id','month','year')

    def __str__(self):
        return str(self.user_id)


class Employee_Analysis_date(models.Model):
    user_id = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    manager_id = models.CharField(max_length=60, null=True, blank=True)

    # DONE_THIS_DATE
    total_sales_done_today = models.FloatField(default=0.0, )  # Customer module sales done in this month in amount
    total_dispatch_done_today = models.BigIntegerField(default=0, )  # Dispatch module dispatch done in this month
    total_reparing_done_today = models.BigIntegerField(default=0, )  # Reparing module Reparing done in this month in units
    total_restamping_done_today = models.BigIntegerField(default=0, )  # Restamping module restamping done in this month in unit
    total_reparing_done_onsite_today = models.BigIntegerField(default=0, )  # Reparing onsite module sales done in this month in amount
    # AVERAGE
    avg_time_to_repair_single_scale_today = models.FloatField(default=0.0, )  # Reparing module avg_time_to_repair_single_scale in this month
    avg_time_to_give_estimate_today = models.FloatField(default=0.0, )  # Reparing module savg_time_to_give_estimate in this month
    avg_time_dispatch_form_to_done_today = models.FloatField(default=0.0, )  # Reparing module avg_time_dispatch_form submit_to_done in this month
    avg_time_collect_to_dispatch_restamping_today = models.FloatField(default=0.0, )  # Restamping module avg_time_collect_to_dispatch_restamping
    # ACHIEVED_TILL_NOW
    sales_target_achived_till_now = models.FloatField(default=0.0, null=True, blank=True)
    reparing_target_achived_till_now = models.FloatField(default=0.0, null=True, blank=True)

    entry_timedate = models.DateTimeField(default=timezone.now, )  # extract month and year from date
    entry_date = models.DateField(default=datetime.date.today, )  # extract month and year from date
    month = models.CharField(max_length=20, null=True, blank=True,choices=list_of_month)  # extract month and year from date
    year = models.IntegerField()  # extract month and year from date

    class Meta:
        unique_together = ('user_id', 'entry_date', 'year','month')

    def __str__(self):
        return str(self.user_id)



