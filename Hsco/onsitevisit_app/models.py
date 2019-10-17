import datetime

from django.db import models
from django.utils import timezone

choices = (('YES', 'YES'),
    ('NO', 'NO'),)


class Onsite_aftersales_service(models.Model):
    repairingno = models.CharField(max_length=50, null=True, blank=True)
    customer_name = models.CharField(max_length=80, null=True, blank=True)
    company_name = models.CharField(max_length=80, null=True, blank=True)
    customer_no = models.CharField(max_length=13, null=True, blank=True)
    previous_repairing_number = models.CharField(max_length=30, null=True, blank=True)
    in_warranty = models.CharField(default='NO', max_length=30, choices=choices)
    phone_no = models.CharField(max_length=13, null=True, blank=True)
    customer_email_id = models.EmailField(max_length=255, null=True, blank=True)
    nearest_railwaystation = models.CharField(max_length=30, null=True, blank=True)
    train_line = models.CharField(max_length=30, null=True, blank=True)
    products_to_be_repaired = models.CharField(max_length=30, null=True, blank=True)
    visiting_charges_told_customer = models.CharField(max_length=30, null=True, blank=True)
    total_cost = models.CharField(max_length=30, null=True, blank=True)
    complaint_assigned_to = models.CharField(max_length=30, null=True, blank=True)
    complaint_assigned_on = models.CharField(max_length=30, null=True, blank=True)
    time_taken_destination_return_office_min = models.CharField(max_length=30, null=True, blank=True)
    notes = models.CharField(max_length=255, null=True, blank=True)
    feedback_given = models.CharField(max_length=30,choices=choices,default='NO')
    entry_timedate = models.DateTimeField(default=timezone.now,)

    def __int__(self):
        return self.repairingno


class Onsite_Products(models.Model):
    onsite_repairing_id = models.ForeignKey(Onsite_aftersales_service,on_delete=models.CASCADE)
    type_of_machine = models.CharField(max_length=30, null=True, blank=True)
    model = models.CharField(max_length=30, null=True, blank=True)
    sub_model = models.CharField(max_length=30, null=True, blank=True)
    capacity = models.CharField(max_length=30, null=True, blank=True)
    problem_in_scale = models.CharField(max_length=255, null=True, blank=True)
    components_replaced_in_warranty = models.CharField(max_length=255, null=True, blank=True)
    components_replaced = models.CharField(max_length=255, null=True, blank=True)
    cost = models.CharField(max_length=30, null=True, blank=True)

    def __int__(self):
        return self.onsite_repairing_id


class Onsite_Feedback(models.Model):
    backend_team = models.FloatField(default=0.00)
    onsite_worker = models.FloatField(default=0.00)
    speed_of_performance = models.FloatField(default=0.00)
    price_of_reparing = models.FloatField(default=0.00)
    overall_interaction = models.FloatField(default=0.00)
    about_hsco = models.CharField(max_length=60)
    any_suggestion = models.CharField(max_length=255)

    def __int__(self):
        return self.onsite_worker

