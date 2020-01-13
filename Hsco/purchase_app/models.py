import datetime
from django.db import models
from django.utils import timezone
from customer_app.models import Customer_Details
from dispatch_app.models import Dispatch
from user_app.models import SiteUser
from dispatch_app.models import Product_Details_Dispatch

choices = (('NO', 'NO'),
    ('YES', 'YES'),)

class Purchase_Details(models.Model):   #cleaned
    user_id = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    manager_id = models.CharField(max_length=60, null=True, blank=True)
    crm_no = models.ForeignKey(Customer_Details,on_delete=models.CASCADE,null=True,blank=True)
    date_of_purchase = models.DateField(default=datetime.date.today,null=True,blank=True)
    bill_no = models.CharField(max_length=30,null=True,blank=True)
    second_person = models.CharField(max_length=80,null=True,blank=True)
    second_company_name = models.CharField(max_length=80,null=True,blank=True)
    company_email = models.CharField(max_length=80,null=True,blank=True)
    company_address = models.CharField(max_length=120,null=True,blank=True)
    second_contact_no = models.CharField(max_length=80,null=True,blank=True)
    third_contact_no = models.CharField(max_length=80,null=True,blank=True)
    upload_op_file = models.FileField(upload_to='',null=True,blank=True)
    po_number = models.CharField(max_length=30,null=True,blank=True)
    channel_of_sales = models.CharField(max_length=80,null=True,blank=True)
    industry = models.CharField(max_length=80,null=True,blank=True)
    value_of_goods = models.FloatField(default=0.0,null=True,blank=True)
    channel_of_dispatch = models.CharField(max_length=100,null=True,blank=True)
    notes = models.CharField(max_length=300,null=True,blank=True)
    feedback_form_filled = models.BooleanField(default=False)
    sales_person = models.CharField(max_length=30, null=True, blank=True)
    new_repeat_purchase = models.CharField(max_length=10, null=True, blank=True)
    dispatch_id_assigned = models.ForeignKey(Dispatch,on_delete=models.CASCADE,null=True,blank=True)  #remaining make forenkey of this with Dispatch module
    entry_timedate = models.DateField(default=datetime.date.today)
    feedback_stars=models.FloatField(default=0.0)
    is_last_product = models.BooleanField(default=False)
    feedback_link = models.URLField(max_length=200, null=True, blank=True)
    purchase_no = models.BigIntegerField(null=True,blank=True)

    def __int__(self):
        return self.id

class Product_Details(models.Model):
    user_id = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    manager_id = models.CharField(max_length=60, null=True, blank=True)
    purchase_id = models.ForeignKey(Purchase_Details,on_delete=models.CASCADE, null=True, blank=True)
    product_dispatch_id = models.ForeignKey(Product_Details_Dispatch,on_delete=models.CASCADE,null=True, blank=True)
    # product_name = models.CharField(max_length=30,null=True,blank=True)
    quantity = models.CharField(max_length=30,null=True,blank=True)
    type_of_scale = models.CharField(max_length=30,null=True,blank=True)
    model_of_purchase = models.CharField(max_length=30,null=True,blank=True)
    sub_model = models.CharField(max_length=60,null=True,blank=True)
    sub_sub_model = models.CharField(max_length=30,null=True,blank=True)
    serial_no_scale = models.CharField(max_length=30,null=True,blank=True)
    brand = models.CharField(max_length=30,null=True,blank=True)
    capacity = models.CharField(max_length=30,null=True,blank=True)
    unit = models.CharField(max_length=30,null=True,blank=True)
    amount = models.FloatField(default=0.0,)

    entry_timedate = models.DateTimeField(default=timezone.now,)

    def __int__(self):
        return self.purchase_id

class Feedback(models.Model):
    user_id = models.ForeignKey(SiteUser,on_delete=models.CASCADE)
    customer_id = models.ForeignKey(Customer_Details,on_delete=models.CASCADE)
    purchase_id = models.ForeignKey(Purchase_Details,on_delete=models.CASCADE)
    knowledge_of_person = models.FloatField(default=0.00,null=True,blank=True)
    timeliness_of_person = models.FloatField(default=0.00,null=True,blank=True)
    price_of_product = models.FloatField(default=0.00,null=True,blank=True)
    overall_interaction = models.FloatField(default=0.00,null=True,blank=True)
    about_hsco = models.CharField(max_length=60,null=True,blank=True)
    any_suggestion = models.CharField(max_length=120,null=True,blank=True)
    entry_timedate = models.DateTimeField(default=timezone.now,)

    class Meta:
        unique_together = ('user_id', 'customer_id', 'purchase_id',)









