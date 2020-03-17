from django.db import models
from django.utils import timezone
from customer_app.models import Customer_Details

# from stock_system.models import Product
from stock_system.models import  Stock_System,Product
from django.core.validators import URLValidator


class Lead(models.Model):
    customer_id = models.ForeignKey(Customer_Details,on_delete=models.CASCADE)
    current_stage = models.CharField(max_length=50,null=True,blank=True)
    new_existing_customer = models.CharField(max_length=50,null=True,blank=True)
    date_of_initiation = models.DateTimeField(default=timezone.now,)
    channel = models.CharField(max_length=50,null=True,blank=True)
    requirement = models.CharField(max_length=80,null=True,blank=True)
    upload_requirement_file = models.FileField(upload_to='lead_requirement_file/',null=True,blank=True)
    owner_of_opportunity = models.CharField(max_length=80,null=True,blank=True)

    def __int__(self):
        return self.id

class Pi_section(models.Model):
    lead_id = models.ForeignKey(Lead,on_delete=models.CASCADE, null=True, blank=True)
    discount = models.CharField(max_length=80,null=True,blank=True)
    upload_pi_file = models.FileField(null=True,blank=True)
    select_pi_template = models.CharField(max_length=45,null=True, blank=True)
    call = models.TextField(max_length=120, null=True,blank=True)
    email = models.BooleanField(default=False, null=True,blank=True)
    whatsapp = models.BooleanField(default=False, null=True,blank=True)
    call2 = models.BooleanField(default=False, null=True,blank=True)
    auto_manual_email = models.CharField(default='Automatic',max_length=50, null=True, blank=True)
    payment_channel = models.CharField(default='Check Payment',max_length=50, null=True, blank=True)
    payment_receipt = models.FileField(null=True, blank=True)
    upload_po_file = models.FileField(null=True, blank=True)
    payment_received_date = models.DateTimeField(default=timezone.now, )
    notes = models.TextField(max_length=120, null=True,blank=True)

    def __int__(self):
        return self.id

class Pi_product(models.Model):
    lead_id = models.ForeignKey(Lead, on_delete=models.CASCADE, null=True, blank=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.FloatField(null=True, blank=True)
    pf = models.CharField(max_length=80, null=True, blank=True)

    def __int__(self):
        return self.id

class Pi_History(models.Model):
    url = models.TextField(validators=[URLValidator()])
    lead_id = models.ForeignKey(Lead, on_delete=models.CASCADE, null=True, blank=True)
    pi_product_id = models.ForeignKey(Pi_product, on_delete=models.CASCADE, null=True, blank=True)

    def __int__(self):
        return self.id