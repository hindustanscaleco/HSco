import datetime

from django.db import models
from django.utils import timezone

from customer_app.models import Customer_Details

from user_app.models import SiteUser
from model_utils import FieldTracker

from customer_app.models import Log
from django.db.models.signals import pre_save,post_save
from simple_history.models import HistoricalRecords


class Repairing_after_sales_service(models.Model):
    user_id = models.ForeignKey(SiteUser, on_delete=models.CASCADE, null=True, blank=True)
    manager_id = models.CharField(max_length=150, null=True, blank=True)
    crm_no = models.ForeignKey(Customer_Details, on_delete=models.CASCADE, null=True, blank=True)
    # repairingnumber = models.CharField(max_length=40,null=True,blank=True) #combination of pk and 'rep'
    previous_repairing_number = models.BigIntegerField(default=0,null=True,blank=True)
    # date_of_purchase = models.DateField(default=datetime.date.today,null=True,blank=True)
    today_date = models.DateField(default=datetime.date.today,null=True,blank=True)
    # name = models.CharField(max_length=60,null=True,blank=True)
    # company_name = models.CharField(max_length=80,null=True,blank=True)
    # phone_no = models.CharField(max_length=13,null=True,blank=True)
    # customer_email_id = models.EmailField(max_length=255,null=True,blank=True)
    # location = models.CharField(max_length=255,null=True,blank=True)
    taken_by = models.CharField(max_length=150, null=True, blank=True)
    # products_to_be_repaired = models.CharField(max_length=30,null=True,blank=True)
    current_stage = models.CharField(max_length=150,null=True,blank=True)
    second_company_name = models.CharField(max_length=150,null=True,blank=True)
    company_email = models.CharField(max_length=150,null=True,blank=True)
    company_address = models.CharField(max_length=250,null=True,blank=True)
    second_person = models.CharField(max_length=150,null=True,blank=True)
    third_person = models.CharField(max_length=150,null=True,blank=True)
    second_contact_no = models.CharField(max_length=150,null=True,blank=True)
    third_contact_no = models.CharField(max_length=150,null=True,blank=True)
    total_cost = models.FloatField(default=0.0)
    informed_on = models.DateField(null=True,blank=True)
    informed_by = models.CharField(max_length=60,null=True,blank=True)
    confirmed_estimate = models.CharField(default='NO',max_length=150,null=True,blank=True)
    repaired = models.CharField(default='NO',max_length=150,null=True,blank=True)

    delivery_by = models.CharField(max_length=150,null=True,blank=True)
    repaired_by = models.CharField(max_length=150,null=True,blank=True)
    feedback_given = models.BooleanField(default=False,)
    avg_feedback = models.FloatField(default=0.0)
    entry_timedate = models.DateField(default=datetime.date.today,null=True,blank=True)
    stage_update_timedate = models.DateField(null=True,blank=True)
    repaired_date = models.DateField(null=True,blank=True)
    delivery_date = models.DateField(null=True,blank=True)
    scale_sub_sms_count = models.IntegerField(default=0)
    estimate_informed_sms_count = models.IntegerField(default=0)
    reparing_done_sms_count = models.IntegerField(default=0)
    late_mark_sms_count = models.IntegerField(default=0)
    final_del_sms_count = models.IntegerField(default=0)
    is_last_product_added = models.BooleanField(default=False,)
    entered_by = models.CharField(max_length=120,null=True,blank=True)
    feedback_link = models.URLField(max_length=200, null=True, blank=True)
    repairing_no = models.BigIntegerField(null=True,blank=True)
    notes = models.CharField(max_length=300,null=True,blank=True)

    repairing_start_timedate = models.DateTimeField(null=True, blank=True, auto_now=False, auto_now_add=False)
    repairing_done_timedate = models.DateTimeField(null=True,blank=True, auto_now=False, auto_now_add=False)
    total_repairing_time  = models.FloatField(default=0.0)

    repairing_time_calculated = models.BooleanField(default=False)
    ess_calculated = models.BooleanField(default=False)
    first_message_send = models.BooleanField(default=False)

    first_stage_timedate = models.DateTimeField(null=True,blank=True)
    second_stage_timedate = models.DateTimeField(null=True,blank=True)
    third_stage_timedate = models.DateTimeField(null=True,blank=True)
    fourth_stage_timedate = models.DateTimeField(null=True,blank=True)
    fifth_stage_timedate = models.DateTimeField(null=True,blank=True)
    log_entered_by = models.CharField(blank= True, null=True, max_length=100)

    tracker = FieldTracker()

    history = HistoricalRecords()

    def __int__(self):
        return self.pk

# def repairing_log(sender ,**kwargs):
#     if kwargs['created']:
#         log = Log()
#         print(kwargs)
#         print(kwargs)
#         print(kwargs)
#         print(kwargs)
#         print(kwargs)
#         print(kwargs)
#     if kwargs['update_fields'] != None:
#         print(kwargs)
#         print(kwargs)
#         print(kwargs)
#         print(kwargs)
#
# post_save.connect(repairing_log, sender = Repairing_after_sales_service)

class Repairing_Product(models.Model):
    user_id = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    manager_id = models.CharField(max_length=150, null=True, blank=True)
    repairing_id = models.ForeignKey(Repairing_after_sales_service,on_delete=models.CASCADE)
    type_of_machine = models.CharField(max_length=150, null=True, blank=True)
    model = models.CharField(max_length=150, null=True, blank=True)
    sub_model = models.CharField(max_length=150, null=True, blank=True)
    problem_in_scale = models.CharField(max_length=150, null=True, blank=True)
    components_replaced = models.CharField(max_length=250, null=True, blank=True)
    components_replaced_in_warranty = models.CharField(max_length=250,null=True,blank=True)
    replaced_scale_given = models.CharField(default='NO', max_length=150, null=True, blank=True)
    Replaced_scale_serial_no = models.CharField(max_length=150, null=True, blank=True)
    deposite_taken_for_replaced_scale = models.CharField(max_length=150, null=True, blank=True)
    cost = models.FloatField(default=0.0)
    in_warranty = models.CharField(default='NO',max_length=150,null=True,blank=True)
    is_last_product = models.BooleanField(default=False,)
    entry_timedate = models.DateField(default=datetime.date.today)
    log_entered_by = models.CharField(blank= True, null=True, max_length=100)

    tracker = FieldTracker()

    history = HistoricalRecords()

    def __int__(self):
        return self.pk

class Repairing_Feedback(models.Model):
    user_id = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    customer_id = models.ForeignKey(Customer_Details, on_delete=models.CASCADE)
    reparing_id = models.ForeignKey(Repairing_after_sales_service, on_delete=models.CASCADE)
    satisfied_with_communication = models.DecimalField(default=0.0, null=True, blank=True, decimal_places=1, max_digits=18)
    speed_of_performance = models.DecimalField(default=0.0, null=True, blank=True, decimal_places=1, max_digits=18)
    price_of_reparing = models.DecimalField(default=0.0, null=True, blank=True, decimal_places=1, max_digits=18)
    overall_interaction = models.DecimalField(default=0.0, null=True, blank=True, decimal_places=1, max_digits=18)
    about_hsco = models.CharField(max_length=150, null=True, blank=True)
    any_suggestion = models.CharField(max_length=150, null=True, blank=True)

    history = HistoricalRecords()

    class Meta:
        unique_together = ('user_id', 'customer_id', 'reparing_id',)

class Component_Replaced(models.Model):
    user_id = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Repairing_Product, on_delete=models.CASCADE,null=True,blank=True)
    replaced_name = models.CharField(max_length=150,null=True,blank=True)
    in_waranty = models.BooleanField(default=False)
    entry_timedate = models.DateField(default=datetime.date.today)

    history = HistoricalRecords()






