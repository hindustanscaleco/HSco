import datetime
from django.db import models
from customer_app.models import Customer_Details
from user_app.models import SiteUser


class Restamping_after_sales_service(models.Model):
    user_id = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    manager_id = models.CharField(max_length=60, null=True, blank=True)
    crm_no = models.ForeignKey(Customer_Details, on_delete=models.CASCADE)
    second_person = models.CharField(max_length=80,null=True,blank=True)
    third_person = models.CharField(max_length=80,null=True,blank=True)
    second_contact_no = models.CharField(max_length=80,null=True,blank=True)
    third_contact_no = models.CharField(max_length=80,null=True,blank=True)
    second_company_name = models.CharField(max_length=80,null=True,blank=True)
    company_email = models.CharField(max_length=80,null=True,blank=True)
    company_address = models.CharField(max_length=120,null=True,blank=True)
    today_date = models.DateField(default=datetime.date.today, blank=True)
    total_amount = models.FloatField(default=0.0, null=True, blank=True)
    scale_delivery_date = models.DateField(null=True, blank=True)
    entry_timedate = models.DateField(default=datetime.date.today)
    current_stage= models.CharField(max_length=50,null=True,blank=True)

    def __int__(self):
        return self.id

class Restamping_Product(models.Model):
    user_id = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    manager_id = models.CharField(max_length=60, null=True, blank=True)
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
    new_sr_no = models.CharField(max_length=80, null=True, blank=True)
    brand = models.CharField(max_length=50, null=True, blank=True)


    def __int__(self):
        return self.id