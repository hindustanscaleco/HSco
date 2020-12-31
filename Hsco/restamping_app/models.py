import datetime
from django.db import models
from customer_app.models import Customer_Details
from user_app.models import SiteUser
from model_utils import FieldTracker


class Restamping_after_sales_service(models.Model):
    user_id = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    manager_id = models.CharField(max_length=150, null=True, blank=True)
    crm_no = models.ForeignKey(Customer_Details, on_delete=models.CASCADE)
    second_person = models.CharField(max_length=150,null=True,blank=True)
    third_person = models.CharField(max_length=150,null=True,blank=True)
    second_contact_no = models.CharField(max_length=150,null=True,blank=True)
    third_contact_no = models.CharField(max_length=150,null=True,blank=True)
    second_company_name = models.CharField(max_length=150,null=True,blank=True)
    company_email = models.CharField(max_length=150,null=True,blank=True)
    company_address = models.CharField(max_length=250,null=True,blank=True)
    today_date = models.DateField(default=datetime.date.today, blank=True)
    total_amount = models.FloatField(default=0.0, null=True, blank=True)
    scale_delivery_date = models.DateField(null=True, blank=True)
    entry_timedate = models.DateField(default=datetime.date.today)
    current_stage= models.CharField(max_length=150,null=True,blank=True)
    restamping_no = models.BigIntegerField(null=True,blank=True)

    restamping_start_timedate = models.DateTimeField(null=True, blank=True)
    restamping_done_timedate = models.DateTimeField(null=True, blank=True)
    total_restamping_time = models.FloatField(default=0.0)
    restamping_time_calculated = models.BooleanField(default=False)
    log_entered_by = models.CharField(blank= True, null=True, max_length=100)

    tracker = FieldTracker()

    def __int__(self):
        return self.id

class Restamping_Product(models.Model):
    user_id = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    manager_id = models.CharField(max_length=150, null=True, blank=True)
    restamping_id = models.ForeignKey(Restamping_after_sales_service,on_delete=models.CASCADE)
    # customer_email_id = models.EmailField(max_length=90,null=True, blank=True)
    # product_to_stampped = models.CharField(max_length=150, null=True, blank=True)
    scale_type = models.CharField(max_length=150, null=True, blank=True)
    model_of_purchase = models.CharField(max_length=150, null=True, blank=True)
    sub_model = models.CharField(max_length=150, null=True, blank=True)
    capacity = models.CharField(max_length=150, null=True, blank=True)
    old_serial_no = models.CharField(max_length=150, null=True, blank=True)
    # old_brand = models.CharField(max_length=150, null=True, blank=True)
    amount = models.FloatField(default=0.0, null=True, blank=True)
    new_sr_no = models.CharField(max_length=150, null=True, blank=True)
    brand = models.CharField(max_length=150, null=True, blank=True)
    entry_timedate = models.DateField(default=datetime.date.today)
    log_entered_by = models.CharField(blank= True, null=True, max_length=100)

    tracker = FieldTracker()


    def __int__(self):
        return self.id