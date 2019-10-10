from django.db import models
from django.utils import timezone

class Repairing(models.Model):
    repairingnumber = models.CharField(max_length=40)

    def __str__(self):
        return self.repairingnumber


class Repairing_after_sales_service(models.Model):
    customer_no = models.CharField(max_length=13)
    previous_repairing_number = models.CharField(max_length=30)
    in_warranty = models.BooleanField(default=True)
    date_of_purchase = models.DateField()
    today_date = models.DateField(timezone.now)
    name = models.CharField(max_length=60)
    company_name = models.CharField(max_length=80)
    phone_no = models.CharField(max_length=13)
    customer_email_id = models.EmailField(max_length=255, unique=True)
    loaction = models.CharField(max_length=255)
    products_to_be_repaired = models.CharField(max_length=30)
    type_of_machine = models.CharField(max_length=30)
    model = models.CharField(max_length=30)
    sub_model = models.CharField(max_length=30)
    problem_in_scale = models.CharField(max_length=255)
    components_replaced_in_warranty = models.CharField(max_length=255)
    components_replaced = models.CharField(max_length=255)
    replaced_scale_given = models.BooleanField(default=True)
    Replaced_scale_serial_no = models.CharField(max_length=60)
    deposite_taken_for_replaced_scale = models.CharField(max_length=60)
    cost = models.CharField(max_length=60)
    informed_on = models.CharField(max_length=60)
    informed_by = models.CharField(max_length=60)
    confirmed_estimate = models.BooleanField(default=True)
    repaired = models.BooleanField(default=True)
    repaired_date = models.BooleanField(default=True)
    delivery_date = models.DateField(timezone.now)
    delivery_by = models.CharField(max_length=50)
    feedback_given = models.CharField(max_length=255)



    def __str__(self):
        return self.customer_no



