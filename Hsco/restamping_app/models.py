from django.db import models
from django.utils import timezone

class Restamping(models.Model):
    restampingno = models.CharField(max_length=30)

    def __str__(self):
        return self.restampingno


class Restamping_after_sales_service(models.Model):
    customer_no = models.CharField(max_length=13)
    company_address = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    today_date = models.DateField(timezone.now)
    mobile_no = models.CharField(max_length=13)
    customer_email_id = models.EmailField(max_length=255, unique=True)
    product_to_stampped = models.CharField(max_length=150)
    scale_type = models.CharField(max_length=150)
    sub_model = models.CharField(max_length=150)
    capacity = models.CharField(max_length=150)
    old_serial_no = models.CharField(max_length=150)
    old_brand = models.CharField(max_length=150)
    amount = models.CharField(max_length=150)
    new_serial_no = models.CharField(max_length=150)
    brand = models.CharField(max_length=150)
    scale_delivery_date = models.DateField(timezone.now)



    def __str__(self):
        return self.customer_no