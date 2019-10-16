import datetime

from django.db import models
from django.utils import timezone



class Restamping_after_sales_service(models.Model):
    # restamping_id = models.ForeignKey(Restamping,on_delete=models.CASCADE)
    restampingno = models.CharField(max_length=30)
    customer_no = models.CharField(max_length=13,null=True, blank=True)
    company_name = models.CharField(max_length=250,null=True, blank=True)
    address = models.CharField(max_length=250,null=True, blank=True)
    today_date = models.DateField(default=datetime.date.today, blank=True)
    mobile_no = models.CharField(max_length=13,null=True, blank=True)

    new_serial_no = models.CharField(max_length=150,null=True, blank=True)
    brand = models.CharField(max_length=150,null=True, blank=True)
    scale_delivery_date = models.DateField(default=datetime.date.today, blank=True)



    def __str__(self):
        return self.customer_no

class Restamping_Product(models.Model):
    restamping_id = models.ForeignKey(Restamping_after_sales_service,on_delete=models.CASCADE)
    customer_email_id = models.EmailField(max_length=255,null=True, blank=True)
    product_to_stampped = models.CharField(max_length=150, null=True, blank=True)
    scale_type = models.CharField(max_length=150, null=True, blank=True)
    sub_model = models.CharField(max_length=150, null=True, blank=True)
    capacity = models.CharField(max_length=150, null=True, blank=True)
    old_serial_no = models.CharField(max_length=150, null=True, blank=True)
    old_brand = models.CharField(max_length=150, null=True, blank=True)
    amount = models.CharField(max_length=150, null=True, blank=True)