import datetime

from django.db import models
from django.utils import timezone

class Ess(models.Model):
    employee_name=models.CharField(max_length=20,null=True, blank=True)
    details=models.CharField(max_length=250,null=True, blank=True)
    contact_no=models.CharField(max_length=20,null=True, blank=True)
    email_id=models.CharField(max_length=20,null=True, blank=True)
    photo=models.ImageField(upload_to='',null=True, blank=True)
    pancard=models.CharField(max_length=20,null=True, blank=True)
    aadhar_card=models.CharField(max_length=20,null=True, blank=True)
    bank_details=models.CharField(max_length=20,null=True, blank=True)
    photo_of_cancelled_cheque=models.ImageField(upload_to='',null=True, blank=True)
    calendar=models.DateField(default=datetime.date.today, )
    target_of_month=models.CharField(max_length=20,null=True, blank=True)
    target_achived_till_now=models.CharField(max_length=20,null=True, blank=True)
    month_on_month_sale_achived=models.CharField(max_length=20,null=True, blank=True)
    defect_given=models.CharField(max_length=20,null=True, blank=True)
    warnings_given=models.CharField(max_length=20,null=True, blank=True)


    def __str__(self):
        return self.employee_name
