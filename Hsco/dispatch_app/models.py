import datetime

from django.db import models
from django.utils import timezone
from customer_app.models import Customer_Details, DynamicDropdown
from user_app.models import SiteUser
from model_utils import FieldTracker

from stock_management_system_app.models import *


class Dispatch(models.Model):
    user_id = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    manager_id = models.CharField(max_length=150, null=True, blank=True)
    crm_no = models.ForeignKey(Customer_Details,on_delete=models.CASCADE,null=True,blank=True)
    # dispatch_id = models.CharField(max_length=8,null=True,blank=True,unique=True) #combination of PK and 00000000(8)
    # customer_no = models.CharField(max_length=30,null=True,blank=True)
    # customer_email = models.CharField(max_length=30,null=True,blank=True)
    # customer_name = models.CharField(max_length=30,null=True,blank=True)
    # company_name = models.CharField(max_length=30,null=True,blank=True)
    # customer_address = models.CharField(max_length=250,null=True,blank=True)
    #goods_to_dispatch = models.ForeignKey()
    second_person = models.CharField(max_length=150,null=True,blank=True)
    third_person = models.CharField(max_length=150,null=True,blank=True)
    second_company_name = models.CharField(max_length=150,null=True,blank=True)
    company_email = models.CharField(max_length=150,null=True,blank=True)
    company_address = models.CharField(max_length=250,null=True,blank=True)
    second_contact_no = models.CharField(max_length=150,null=True,blank=True)
    third_contact_no = models.CharField(max_length=150,null=True,blank=True)
    bill_address = models.CharField(max_length=150,null=True,blank=True)
    shipping_address = models.CharField(max_length=150,null=True,blank=True)
    date_of_dispatch = models.DateField(null=True,blank=True)
    dispatch_by = models.CharField(max_length=150,null=True,blank=True)
    packed_by = models.CharField(max_length=150,null=True,blank=True)
    hamal_name = models.CharField(max_length=150,null=True,blank=True)
    no_bundles = models.FloatField(default=0.0)
    transport_name = models.CharField(max_length=80,null=True,blank=True)
    lr_no = models.CharField(max_length=150,null=True,blank=True)
    photo_lr_no = models.ImageField(upload_to='',null=True,blank=True)
    channel_of_dispatch = models.CharField(max_length=150,null=True,blank=True)
    channel_of_dispatch_id = models.ForeignKey(DynamicDropdown,on_delete=models.CASCADE,null=True, blank=True)

    notes = models.CharField(max_length=300,null=True,blank=True)
    current_stage = models.CharField(max_length=150,null=True,blank=True)
    entry_timedate = models.DateField(default=datetime.date.today,null=True,blank=True)
    feedback_link = models.URLField(max_length=200,null=True,blank=True)
    dispatch_no = models.BigIntegerField(null=True,blank=True)

    dispatch_start_timedate = models.DateTimeField(null=True, blank=True)
    dispatch_done_timedate = models.DateTimeField(null=True,blank=True)
    total_dispatch_time  = models.FloatField(default=0.0)
    dispatch_time_calculated = models.BooleanField(default=False)
    log_entered_by = models.CharField(blank= True, null=True, max_length=100)

    tracker = FieldTracker()


    def __str__(self):
        return str(self.pk)


class Product_Details_Dispatch(models.Model):
    user_id = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    godown_id = models.ForeignKey(Godown, on_delete=models.CASCADE,null=True,blank=True)
    manager_id = models.CharField(max_length=150, null=True, blank=True)
    dispatch_id = models.ForeignKey(Dispatch,on_delete=models.CASCADE)
    # product_name = models.CharField(max_length=30,null=True,blank=True)
    quantity = models.CharField(max_length=150,null=True,blank=True)
    type_of_scale = models.CharField(max_length=150,null=True,blank=True)
    model_of_purchase = models.CharField(max_length=150,null=True,blank=True)
    sub_model = models.CharField(max_length=150,null=True,blank=True)
    sub_sub_model = models.CharField(max_length=150,null=True,blank=True)
    serial_no_scale = models.CharField(max_length=150,null=True,blank=True)
    brand = models.CharField(max_length=150,null=True,blank=True)
    capacity = models.CharField(max_length=150,null=True,blank=True)
    unit = models.CharField(max_length=150,null=True,blank=True)
    # sales_person = models.CharField(max_length=30,null=True,blank=True)
    new_repeat_purchase = models.CharField(max_length=150,null=True,blank=True)
    value_of_goods = models.FloatField(default=0.0, null=True,blank=True)
    entry_timedate = models.DateTimeField(default=timezone.now, )
    tracker = FieldTracker()
    log_entered_by = models.CharField(blank= True, null=True, max_length=100)

    tracker = FieldTracker()

    def __int__(self):
        return self.dispatch_id

class Product_Despatched(models.Model):
    user_id = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    manager_id = models.CharField(max_length=150, null=True, blank=True)
    dispatch_id = models.ForeignKey(Dispatch,on_delete=models.CASCADE, null=True, blank=True)
    value = models.CharField(max_length=120, null=True, blank=True)
    entry_timedate = models.DateTimeField(default=timezone.now, )
    tracker = FieldTracker()

    def __int__(self):
        return self.dispatch_id

