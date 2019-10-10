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
    #sales_person = models.CharField(max_length=30)
    #new_repeat_purchase = models.CharField(max_length=30)
    bill_no = models.CharField(max_length=30)
    upload_op_file = models.ImageField(upload_to='')
    po_number = models.CharField(max_length=30)
    photo_lr_no = models.ImageField(upload_to='')
    channel_of_sales = models.CharField(max_length=30)
    industry = models.CharField(max_length=30)
    value_of_goods = models.CharField(max_length=30)
    channel_of_dispatch = models.CharField(max_length=30)
    notes = models.CharField(max_length=30)
    feedback_form_filled = models.BooleanField(default=False)
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

    def __str__(self):
        return self.product_name







