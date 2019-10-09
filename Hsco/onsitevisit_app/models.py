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
    date_of_complaint_received = models.DateField(default=datetime.date.today,blank=True)
    customer_address = models.CharField(max_length=250, null=True, blank=True)
    complaint_received_by = models.CharField(max_length=30, null=True, blank=True)
    nearest_railwaystation = models.CharField(max_length=30, null=True, blank=True)
    train_line = models.CharField(max_length=30, null=True, blank=True)
    products_to_be_repaired = models.CharField(max_length=30, null=True, blank=True)
    type_of_machine = models.CharField(max_length=30, null=True, blank=True)
    model = models.CharField(max_length=30, null=True, blank=True)
    sub_model = models.CharField(max_length=30, null=True, blank=True)
    capacity = models.CharField(max_length=30, null=True, blank=True)
    problem_in_scale = models.CharField(max_length=255, null=True, blank=True)
    components_replaced_in_warranty = models.CharField(max_length=255, null=True, blank=True)
    components_replaced = models.CharField(max_length=255, null=True, blank=True)
    cost = models.CharField(max_length=30, null=True, blank=True)
    visiting_charges_told_customer = models.CharField(max_length=30, null=True, blank=True)
    total_cost = models.CharField(max_length=30, null=True, blank=True)
    complaint_assigned_to = models.CharField(max_length=30, null=True, blank=True)
    complaint_assigned_on = models.CharField(max_length=30, null=True, blank=True)
    time_taken_destination_return_office_min = models.CharField(max_length=30, null=True, blank=True)
    notes = models.CharField(max_length=255, null=True, blank=True)
    feedback_given = models.CharField(max_length=30,choices=choices,default='NO')




    def __str__(self):
        return self.customer_no

