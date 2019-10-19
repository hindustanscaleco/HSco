import datetime

from django.db import models
from django.utils import timezone

from customer_app.models import Customer_Details


class Amc_After_Sales(models.Model):
    # amc_visit_id = models.ForeignKey(Amcvisit, on_delete=models.CASCADE)
    crm_no = models.ForeignKey(Customer_Details,on_delete=models.CASCADE)
    amcno = models.CharField(max_length=50, null=True,unique=True, blank=True)
    customer_name = models.CharField(max_length=80, null=True, blank=True)
    company_name = models.CharField(max_length=80, null=True, blank=True)
    customer_no =models.CharField(max_length=13,null=True,blank=True)
    customer_email_id = models.EmailField(max_length=255,null=True,blank=True)
    type_of_scale = models.CharField(max_length=30,null=True,blank=True)
    serial_no_scale = models.CharField(max_length=80,null=True,blank=True)
    contract_valid_in_years = models.CharField(max_length=30,null=True,blank=True)
    contract_amount = models.CharField(max_length=50,null=True,blank=True)
    contract_no_reporting_breakdown = models.CharField(max_length=30,null=True,blank=True)
    contract_start_date = models.DateField(default=datetime.date.today,null=True,blank=True)
    contract_end_date = models.DateField(default=datetime.date.today,null=True,blank=True)
    visit_1 = models.CharField(max_length=255,null=True,blank=True)
    repot_1 = models.CharField(max_length=255,null=True,blank=True)
    visit_2 = models.CharField(max_length=255,null=True,blank=True)
    repot_2 = models.CharField(max_length=255,null=True,blank=True)
    visit_3 = models.CharField(max_length=255,null=True,blank=True)
    repot_3 = models.CharField(max_length=255,null=True,blank=True)
    visit_4 = models.CharField(max_length=255,null=True,blank=True)
    repot_4 = models.CharField(max_length=255,null=True,blank=True)
    entry_timedate = models.DateTimeField(default=timezone.now,)

    #for future use
    # visit_1 = models.DateField(default=datetime.date.today, null=True, blank=True)
    # repot_1 = models.CharField(max_length=255, null=True, blank=True)
    # visit_2 = models.DateField(default=datetime.date.today, null=True, blank=True)
    # repot_2 = models.CharField(max_length=255, null=True, blank=True)
    # visit_3 = models.DateField(default=datetime.date.today, null=True, blank=True)
    # repot_3 = models.CharField(max_length=255, null=True, blank=True)
    # visit_4 = models.DateField(default=datetime.date.today, null=True, blank=True)
    # repot_4 = models.CharField(max_length=255, null=True, blank=True)


    def __str__(self):
        return self.amcno

class AMC_Feedback(models.Model):
    satisfied_with_work = models.FloatField(default=0.00)
    speed_of_performance = models.FloatField(default=0.00)
    price_of_amc = models.FloatField(default=0.00)
    overall_interaction = models.FloatField(default=0.00)
    about_hsco = models.CharField(max_length=60, null=True, blank=True)
    any_suggestion = models.CharField(max_length=255, null=True, blank=True)








