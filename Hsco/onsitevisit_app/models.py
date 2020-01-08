import datetime

from django.db import models
from django.utils import timezone

from customer_app.models import Customer_Details

from user_app.models import SiteUser

choices = (('YES', 'YES'),
    ('NO', 'NO'),)


class Onsite_aftersales_service(models.Model):
    user_id = models.ForeignKey(SiteUser, on_delete=models.CASCADE, null=True, blank=True)
    crm_no = models.ForeignKey(Customer_Details,on_delete=models.CASCADE)
    # repairingno = models.CharField(max_length=50, null=True, blank=True)
    # customer_name = models.CharField(max_length=80, null=True, blank=True)
    # company_name = models.CharField(max_length=80, null=True, blank=True)
    # customer_no = models.CharField(max_length=13, null=True, blank=True)
    previous_repairing_number = models.CharField(max_length=30, null=True, blank=True)
    # phone_no = models.CharField(max_length=13, null=True, blank=True)
    # customer_email_id = models.EmailField(max_length=255, null=True, blank=True)
    second_person = models.CharField(max_length=80,null=True,blank=True)
    third_person = models.CharField(max_length=80,null=True,blank=True)
    second_contact_no = models.CharField(max_length=80,null=True,blank=True)
    third_contact_no = models.CharField(max_length=80,null=True,blank=True)
    second_company_name = models.CharField(max_length=80,null=True,blank=True)
    company_email = models.CharField(max_length=80,null=True,blank=True)
    company_address = models.CharField(max_length=120,null=True,blank=True)
    nearest_railwaystation = models.CharField(max_length=30, null=True, blank=True)
    train_line = models.CharField(max_length=30, null=True, blank=True)
    current_stage = models.CharField(max_length=50,null=True,blank=True)
    date_of_complaint_received = models.DateField(null=True, blank=True)
    # products_to_be_repaired = models.CharField(max_length=30, null=True, blank=True)
    visiting_charges_told_customer = models.FloatField(default=0.0, null=True, blank=True)
    total_cost = models.FloatField(default=0.0, null=True, blank=True)
    complaint_assigned_to = models.CharField( max_length=30,null=True, blank=True)
    complaint_assigned_on = models.DateField( null=True, blank=True)
    complaint_received_by = models.CharField(max_length=30, null=True, blank=True)
    time_taken_destination_return_office_min = models.CharField(max_length=30, null=True, blank=True)
    notes = models.CharField(max_length=300, null=True, blank=True)
    feedback_given = models.BooleanField(default=False)
    avg_feedback = models.FloatField(default=0.0)
    entry_timedate = models.DateTimeField(default=timezone.now,)
    is_done = models.BooleanField(default=False)
    assigned_to = models.CharField(max_length=30, null=True, blank=True)
    assigned_by = models.CharField(max_length=30, null=True, blank=True)
    done_on = models.DateTimeField(default=timezone.now,)
    feedback_link = models.URLField(max_length=200, null=True, blank=True)
    onsite_no = models.BigIntegerField(null=True,blank=True)


    def __int__(self):
        return self.id


class Onsite_Products(models.Model):
    manager_id = models.CharField(max_length=60, null=True, blank=True)
    crm_no = models.ForeignKey(Customer_Details, on_delete=models.CASCADE, null=True, blank=True)
    onsite_repairing_id = models.ForeignKey(Onsite_aftersales_service,on_delete=models.CASCADE)
    type_of_machine = models.CharField(max_length=30, null=True, blank=True)
    model = models.CharField(max_length=30, null=True, blank=True)
    sub_model = models.CharField(max_length=30, null=True, blank=True)
    capacity = models.CharField(max_length=30, null=True, blank=True)
    problem_in_scale = models.CharField(max_length=90, null=True, blank=True)
    components_replaced_in_warranty = models.CharField(max_length=90, null=True, blank=True)
    components_replaced = models.CharField(max_length=90, null=True, blank=True)
    cost = models.FloatField(default=0.0,)
    entry_timedate = models.DateTimeField(default=timezone.now, )
    in_warranty = models.CharField(default='NO', max_length=30, choices=choices, null=True, blank=True)

    def __int__(self):
        return self.onsite_repairing_id


class Onsite_Feedback(models.Model):
    user_id = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    customer_id = models.ForeignKey(Customer_Details, on_delete=models.CASCADE)
    onsite_repairing_id = models.ForeignKey(Onsite_aftersales_service, on_delete=models.CASCADE)
    backend_team = models.FloatField(default=0.00, null=True, blank=True)
    onsite_worker = models.FloatField(default=0.00, null=True, blank=True)
    speed_of_performance = models.FloatField(default=0.00, null=True, blank=True)
    price_of_reparing = models.FloatField(default=0.00, null=True, blank=True)
    overall_interaction = models.FloatField(default=0.00, null=True, blank=True)
    about_hsco = models.CharField(max_length=60, null=True, blank=True)
    any_suggestion = models.CharField(max_length=90, null=True, blank=True)
    entry_timedate = models.DateTimeField(default=timezone.now, )

    def __int__(self):
        return self.user_id


    class Meta:
        unique_together = ('user_id', 'customer_id', 'onsite_repairing_id',)

