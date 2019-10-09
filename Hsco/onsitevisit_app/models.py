from django.db import models
from django.utils import timezone


class Onsite_visit(models.Model):
    repairingno=models.CharField(max_length=50)
    customer_name = models.CharField(max_length=80)
    company_name = models.CharField(max_length=80)


    def __str__(self):
        return self.repairingno

class Onsite_aftersales_service(models.Model):
    customer_no = models.CharField(max_length=13)
    previous_repairing_number = models.CharField(max_length=30)
    in_warranty = models.BooleanField(default=True)
    phone_no = models.CharField(max_length=13)
    customer_email_id = models.EmailField(max_length=255, unique=True)
    date_of_complaint_received = models.DateField(timezone.now)
    customer_address = models.CharField(max_length=250)
    complaint_received_by = models.CharField(max_length=30)
    nearest_railwaystation = models.CharField(max_length=30)
    train_line = models.CharField(max_length=30)
    products_to_be_repaired = models.CharField(max_length=30)
    type_of_machine = models.CharField(max_length=30)
    model = models.CharField(max_length=30)
    sub_model = models.CharField(max_length=30)
    capacity = models.CharField(max_length=30)
    problem_in_scale = models.CharField(max_length=255)
    components_replaced_in_warranty = models.CharField(max_length=255)
    components_replaced = models.CharField(max_length=255)
    cost = models.CharField(max_length=30)
    visiting_charges_told_customer = models.CharField(max_length=30)
    total_cost = models.CharField(max_length=30)
    complaint_assigned_to = models.CharField(max_length=30)
    complaint_assigned_on = models.CharField(max_length=30)
    time_taken_destination_return_office_min = models.CharField(max_length=30)
    notes = models.CharField(max_length=255)
    feedback_given = models.BooleanField(default=False)




    def __str__(self):
        return self.customer_no

