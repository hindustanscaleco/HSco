from django.db import models
from django.utils import timezone


class Amcvisit(models.Model):
    amcno=models.CharField(max_length=50)
    customer_name = models.CharField(max_length=80)
    company_name = models.CharField(max_length=80)


    def __str__(self):
        return self.amcno


class Amc_After_Sales(models.Model):
    customer_no =models.CharField(max_length=13)
    customer_email_id = models.EmailField(max_length=255, unique=True)
    type_of_scale = models.CharField(max_length=30)
    serial_no_scale = models.CharField(max_length=80)
    contract_valid_in_years = models.DateField(default=timezone.now)
    contract_amount = models.CharField(max_length=50)
    contract_no_reporting_breakdown = models.CharField(max_length=30)
    contract_start_date = models.DateField(default=timezone.now)
    contract_end_date = models.DateField(default=timezone.now)
    visit_1 = models.DateField(default=timezone.now)
    repot_1 = models.CharField(max_length=255)
    visit_2 = models.DateField(default=timezone.now)
    repot_2 = models.CharField(max_length=255)
    visit_3 = models.DateField(default=timezone.now)
    repot_3 = models.CharField(max_length=255)
    visit_4 = models.DateField(default=timezone.now)
    repot_4 = models.CharField(max_length=255)


    def __str__(self):
        return self.customer_no



