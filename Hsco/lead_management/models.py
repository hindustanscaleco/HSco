from django.db import models
from django.utils import timezone

class Customer_details_section(models.Model):
    customer_name = models.CharField(max_length=60,null=True,blank=True)
    company_name = models.CharField(max_length=120,null=True,blank=True)
    customer_no = models.CharField(max_length=12,null=True,blank=True)
    customer_email_id = models.CharField(max_length=12,null=True,blank=True)
    address = models.CharField(max_length=120,null=True,blank=True)
    industry = models.CharField(max_length=120,null=True,blank=True)
    customer_gst_no = models.CharField(max_length=50,null=True,blank=True)
    current_stage = models.CharField(max_length=50,null=True,blank=True)
    new_existing_customer = models.CharField(max_length=50,null=True,blank=True)
    date_of_initiation = models.DateTimeField(default=timezone.now,)
    channel = models.CharField(max_length=50,null=True,blank=True)
    requirement = models.CharField(max_length=80,null=True,blank=True)
    upload_requirement_file = models.CharField(max_length=80,null=True,blank=True)
    owner_of_opportunity = models.CharField(max_length=80,null=True,blank=True)
    discount = models.CharField(max_length=80,null=True,blank=True)
    upload_pi_file = models.FileField(null=True,blank=True)
    select_pi_template = models.CharField(max_length=50, null=True, blank=True)
    call = models.TextField(max_length=120, null=True,blank=True)
    email = models.BooleanField(default=False)
    whatsapp = models.BooleanField(default=False)
    call2 = models.BooleanField(default=False)
    auto_manual_email = models.CharField(default='Automatic',max_length=50, null=True, blank=True)
    payment_channel = models.CharField(default='Check Payment',max_length=50, null=True, blank=True)
    payment_receipt = models.FileField(null=True, blank=True)
    upload_po_file = models.FileField(null=True, blank=True)
    payment_received_date = models.DateTimeField(default=timezone.now, )
    notes = models.TextField(max_length=120, null=True,blank=True)

    def __int__(self):
        return self.customer_name
