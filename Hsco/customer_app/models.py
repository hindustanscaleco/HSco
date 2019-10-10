from django.db import models
from django.utils import timezone



class Customer_Details(models.Model):
    crn_number = models.UUIDField()
    company_name = models.CharField(max_length=80)
    address = models.CharField(max_length=250)
    contact_no = models.CharField(max_length=30)
    customer_email_id = models.EmailField('Email-id', max_length=255, unique=True )
    date_of_purchase = models.DateField()
    product_purchase = models.DateTimeField(default=timezone.now)
    quantity = models.CharField(max_length=30)
    customer_name = models.CharField(max_length=80,null=True,blank=True)
    company_name = models.CharField(max_length=80,null=True,blank=True)
    address = models.CharField(max_length=250,null=True,blank=True)
    contact_no = models.CharField(max_length=30,null=True,blank=True)
    customer_email_id = models.CharField(max_length=30,null=True,blank=True)
    date_of_purchase = models.DateField(null=True,blank=True)
    product_purchase_date = models.DateTimeField(default=timezone.now,null=True,blank=True)
    #sales_person = models.CharField(max_length=30)
    #new_repeat_purchase = models.CharField(max_length=30)
    bill_no = models.CharField(max_length=30,null=True,blank=True)
    upload_op_file = models.FileField(upload_to='',null=True,blank=True)
    po_number = models.CharField(max_length=30,null=True,blank=True)
    photo_lr_no = models.FileField(upload_to='',null=True,blank=True)
    channel_of_sales = models.CharField(max_length=30,null=True,blank=True)
    industry = models.CharField(max_length=30,null=True,blank=True)
    value_of_goods = models.CharField(max_length=30,null=True,blank=True)
    channel_of_dispatch = models.CharField(max_length=30,null=True,blank=True)
    notes = models.CharField(max_length=30,null=True,blank=True)
    feedback_form_filled = models.BooleanField(default=False,null=True,blank=True)
    #dispatch_id_assigned = models.CharField(max_length=30)


    def __str__(self):
        return self.crn_number




class Product_Details(models.Model):
    product_name = models.CharField(max_length=30)
    quantity = models.CharField(max_length=30)
    type_of_scale = models.CharField(max_length=30)
    model_of_purchase = models.CharField(max_length=30)
    sub_model = models.CharField(max_length=30)
    sub_sub_model = models.CharField(max_length=30)
    serial_no_scale = models.CharField(max_length=80)
    brand = models.CharField(max_length=30)
    capacity = models.CharField(max_length=30)
    unit = models.CharField(max_length=30)
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

    def __str__(self):
        return self.product_name







