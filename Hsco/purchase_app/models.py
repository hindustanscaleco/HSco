
import datetime
from django.db import models
from django.utils import timezone

from customer_app.models import Customer_Details
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


class Purchase_Details(models.Model):
    crm_no = models.ForeignKey(Customer_Details,on_delete=models.CASCADE)
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
    entry_timedate = models.DateField(default=datetime.date.today)
    feedback_stars=models.FloatField(default=0.0)

    def __str__(self):
        return self.notes

class Product_Details(models.Model):
    purchase_id = models.ForeignKey(Purchase_Details,on_delete=models.CASCADE)
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
    entry_timedate = models.DateTimeField(default=timezone.now,)

    def __int__(self):
        return self.purchase_id

class Feedback(models.Model):
    knowledge_of_person = models.FloatField(default=0.00,null=True,blank=True)
    timeliness_of_person = models.FloatField(default=0.00,null=True,blank=True)
    price_of_product = models.FloatField(default=0.00,null=True,blank=True)
    overall_interaction = models.FloatField(default=0.00,null=True,blank=True)
    about_hsco = models.CharField(max_length=60,null=True,blank=True)
    any_suggestion = models.CharField(max_length=255,null=True,blank=True)
    entry_timedate = models.DateTimeField(default=timezone.now,)









