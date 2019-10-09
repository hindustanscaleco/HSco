import datetime

from django.db import models
from django.utils import timezone
choices = (('YES', 'YES'),
    ('NO', 'NO'),)

class Repairing_after_sales_service(models.Model):
    repairingnumber = models.CharField(max_length=40,null=True,blank=True) #combination of pk and 'rep'
    customer_no = models.CharField(max_length=13,null=True,blank=True)
    previous_repairing_number = models.CharField(max_length=30,null=True,blank=True)
    in_warranty = models.CharField(choices=choices,default='NO',max_length=30,null=True,blank=True)
    date_of_purchase = models.DateField(default=datetime.date.today())
    today_date = models.DateField(default=datetime.date.today())
    name = models.CharField(max_length=60,null=True,blank=True)
    company_name = models.CharField(max_length=80,null=True,blank=True)
    phone_no = models.CharField(max_length=13,null=True,blank=True)
    customer_email_id = models.EmailField(max_length=255, unique=True,null=True,blank=True)
    location = models.CharField(max_length=255,null=True,blank=True)
    products_to_be_repaired = models.CharField(max_length=30,null=True,blank=True)
    type_of_machine = models.CharField(max_length=30,null=True,blank=True)
    model = models.CharField(max_length=30,null=True,blank=True)
    sub_model = models.CharField(max_length=30,null=True,blank=True)
    problem_in_scale = models.CharField(max_length=255,null=True,blank=True)
    components_replaced_in_warranty = models.CharField(max_length=255,null=True,blank=True)
    components_replaced = models.CharField(max_length=255,null=True,blank=True)
    replaced_scale_given = models.CharField(choices=choices,default='NO',max_length=30,null=True,blank=True)
    Replaced_scale_serial_no = models.CharField(max_length=60,null=True,blank=True)
    deposite_taken_for_replaced_scale = models.CharField(max_length=60,null=True,blank=True)
    cost = models.FloatField(default=0.00)
    total_cost = models.FloatField(default=0.00)
    informed_on = models.CharField(max_length=60,null=True,blank=True)
    informed_by = models.CharField(max_length=60,null=True,blank=True)
    confirmed_estimate = models.CharField(choices=choices,default='NO',max_length=30,null=True,blank=True)
    repaired = models.CharField(choices=choices,default='NO',max_length=30,null=True,blank=True)
    repaired_date = models.DateField(default=datetime.date.today())
    delivery_date = models.DateField(default=datetime.date.today())
    delivery_by = models.CharField(max_length=50,null=True,blank=True)
    feedback_given = models.CharField(max_length=255,null=True,blank=True)



    def __str__(self):
        return self.customer_no




