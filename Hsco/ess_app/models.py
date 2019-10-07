from django.db import models
from django.utils import timezone

class Ess(models.Model):
    employee_name=models.CharField(max_length=20)
    details=models.CharField(max_length=250)
    contact_no=models.CharField(max_length=20)
    email_id=models.CharField(max_length=20)
    photo=models.ImageField(upload_to='')
    pancard=models.CharField(max_length=20)
    aadhar_card=models.CharField(max_length=20)
    bank_details=models.CharField(max_length=20)
    photo_of_cancelled_cheque=models.ImageField(upload_to='')
    calander=models.DateTimeField(default=timezone.now)
    target_of_month=models.CharField(max_length=20)
    target_achived_till_now=models.CharField(max_length=20)
    month_on_month_sale_achived=models.CharField(max_length=20)
    defect_given=models.CharField(max_length=20)
    warnings_given=models.CharField(max_length=20)


    def __str__(self):
        return self.employee_name
