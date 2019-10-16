import datetime
import uuid

from django.db import models
from django.utils import timezone
from dispatch_app.models import Dispatch

choices = (('NO', 'NO'),
    ('YES', 'YES'),)

feedback = (('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10'),)


class Customer_Details(models.Model):
    crn_number = models.UUIDField(unique=True, default=uuid.uuid4)
    customer_name = models.CharField(max_length=80, null=True, blank=True)
    company_name = models.CharField(max_length=80,null=True,blank=True)
    address = models.CharField(max_length=250,null=True,blank=True)
    contact_no = models.CharField(max_length=30,null=True,blank=True)
    customer_email_id = models.CharField(max_length=30,null=True,blank=True)
    date_of_purchase = models.DateField(default=datetime.date.today,null=True,blank=True)
    product_purchase_date = models.DateField(default=datetime.date.today,null=True,blank=True)


    bill_no = models.CharField(max_length=30,null=True,blank=True)
    upload_op_file = models.FileField(upload_to='',null=True,blank=True)
    po_number = models.CharField(max_length=30,null=True,blank=True)
    photo_lr_no = models.FileField(upload_to='',null=True,blank=True)
    channel_of_sales = models.CharField(max_length=30,null=True,blank=True)
    industry = models.CharField(max_length=30,null=True,blank=True)
    value_of_goods = models.CharField(max_length=30,null=True,blank=True)
    channel_of_dispatch = models.CharField(max_length=30,null=True,blank=True)
    notes = models.CharField(max_length=30,null=True,blank=True)
    feedback_form_filled = models.CharField(max_length=30,null=True,blank=True, choices=choices)
    dispatch_id_assigned = models.ForeignKey(Dispatch,on_delete=models.CASCADE,null=True,blank=True)  #remaining make forenkey of this with Dispatch module

    def __str__(self):
        return self.customer_name

class Product_Details(models.Model):
    customer_id = models.ForeignKey(Customer_Details,on_delete=models.CASCADE)
    product_name = models.CharField(max_length=30,null=True,blank=True)
    quantity = models.CharField(max_length=30,null=True,blank=True)
    type_of_scale = models.CharField(max_length=30,null=True,blank=True)
    model_of_purchase = models.CharField(max_length=30,null=True,blank=True)
    sub_model = models.CharField(max_length=30,null=True,blank=True)
    sub_sub_model = models.CharField(max_length=30,null=True,blank=True)
    serial_no_scale = models.CharField(max_length=30,null=True,blank=True)
    brand = models.CharField(max_length=30,null=True,blank=True)
    capacity = models.CharField(max_length=30,null=True,blank=True)
    unit = models.CharField(max_length=30,null=True,blank=True)
    sales_person = models.CharField(max_length=30,null=True,blank=True)
    new_repeat_purchase = models.CharField(max_length=30,null=True,blank=True)

    def __int__(self):
        return self.customer_id

class Feedback(models.Model):

    name = models.CharField(max_length=60,null=True,blank=True)
    performance = models.CharField(max_length=30,null=True,blank=True,choices=feedback)
    co_operation     = models.CharField(max_length=30,null=True,blank=True,choices=feedback)
    communication = models.CharField(max_length=30,null=True,blank=True,choices=feedback)
    quality_of_work = models.CharField(max_length=30,null=True,blank=True,choices=feedback)
    stars_count        = models.BigIntegerField()

    def __str__(self):
        return self.name








