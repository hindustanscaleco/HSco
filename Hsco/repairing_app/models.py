import datetime

from django.db import models
from django.utils import timezone

from customer_app.models import Customer_Details

from user_app.models import SiteUser


class Repairing_after_sales_service(models.Model):
    user_id = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    manager_id = models.CharField(max_length=60, null=True, blank=True)
    crm_no = models.ForeignKey(Customer_Details, on_delete=models.CASCADE)
    repairingnumber = models.CharField(max_length=40,null=True,blank=True) #combination of pk and 'rep'
    previous_repairing_number = models.CharField(max_length=30,null=True,blank=True)
    in_warranty = models.CharField(default='NO',max_length=30,null=True,blank=True)
    date_of_purchase = models.DateField(default=datetime.date.today,null=True,blank=True)
    today_date = models.DateField(default=datetime.date.today,null=True,blank=True)
    name = models.CharField(max_length=60,null=True,blank=True)
    # company_name = models.CharField(max_length=80,null=True,blank=True)
    # phone_no = models.CharField(max_length=13,null=True,blank=True)
    # customer_email_id = models.EmailField(max_length=255,null=True,blank=True)
    location = models.CharField(max_length=255,null=True,blank=True)

    # products_to_be_repaired = models.CharField(max_length=30,null=True,blank=True)
    current_stage = models.CharField(default='Scale is collected but estimate is not given',max_length=50,null=True,blank=True)
    total_cost = models.FloatField(default=0.0)
    informed_on = models.CharField(max_length=60,null=True,blank=True)
    informed_by = models.CharField(max_length=60,null=True,blank=True)
    confirmed_estimate = models.CharField(default='NO',max_length=30,null=True,blank=True)
    repaired = models.CharField(default='NO',max_length=30,null=True,blank=True)
    repaired_date = models.DateField(default=datetime.date.today,null=True,blank=True)
    delivery_date = models.DateField(default=datetime.date.today,null=True,blank=True)
    delivery_by = models.CharField(max_length=50,null=True,blank=True)
    feedback_given = models.CharField(default='NO',max_length=10,null=True,blank=True)
    avg_feedback = models.FloatField(default=0.0)
    entry_timedate = models.DateField(default=datetime.date.today)



    def __int_(self):
        return self.repairingnumber


class Repairing_Product(models.Model):
    user_id = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    manager_id = models.CharField(max_length=60, null=True, blank=True)
    repairing_id = models.ForeignKey(Repairing_after_sales_service,on_delete=models.CASCADE)
    type_of_machine = models.CharField(max_length=30, null=True, blank=True)
    model = models.CharField(max_length=30, null=True, blank=True)
    sub_model = models.CharField(max_length=30, null=True, blank=True)
    problem_in_scale = models.CharField(max_length=90, null=True, blank=True)
    components_replaced = models.CharField(max_length=90, null=True, blank=True)
    components_replaced_in_warranty = models.CharField(max_length=90,null=True,blank=True)
    replaced_scale_given = models.CharField(default='NO', max_length=30, null=True, blank=True)
    Replaced_scale_serial_no = models.CharField(max_length=60, null=True, blank=True)
    deposite_taken_for_replaced_scale = models.CharField(max_length=60, null=True, blank=True)
    cost = models.FloatField(default=0.0)


    def __int__(self):
        return self.repairing_id

class Repairing_Feedback(models.Model):
    satisfied_with_communication = models.FloatField(default=0.00)
    speed_of_performance = models.FloatField(default=0.00)
    price_of_reparing = models.FloatField(default=0.00)
    overall_interaction = models.FloatField(default=0.00)
    about_hsco = models.CharField(max_length=60, null=True, blank=True)
    any_suggestion = models.CharField(max_length=90, null=True, blank=True)




