import datetime

from django.db import models
from django.utils import timezone

from customer_app.models import Customer_Details

from user_app.models import SiteUser


class Repairing_after_sales_service(models.Model):
    user_id = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    manager_id = models.CharField(max_length=60, null=True, blank=True)
    crm_no = models.ForeignKey(Customer_Details, on_delete=models.CASCADE)
    # repairingnumber = models.CharField(max_length=40,null=True,blank=True) #combination of pk and 'rep'
    previous_repairing_number = models.BigIntegerField(default=0,null=True,blank=True)
    # date_of_purchase = models.DateField(default=datetime.date.today,null=True,blank=True)
    today_date = models.DateField(default=datetime.date.today,null=True,blank=True)
    # name = models.CharField(max_length=60,null=True,blank=True)
    # company_name = models.CharField(max_length=80,null=True,blank=True)
    # phone_no = models.CharField(max_length=13,null=True,blank=True)
    # customer_email_id = models.EmailField(max_length=255,null=True,blank=True)
    # location = models.CharField(max_length=255,null=True,blank=True)
    taken_by = models.CharField(max_length=60, null=True, blank=True)
    # products_to_be_repaired = models.CharField(max_length=30,null=True,blank=True)
    current_stage = models.CharField(max_length=50,null=True,blank=True)
    second_company_name = models.CharField(max_length=80,null=True,blank=True)
    company_email = models.CharField(max_length=80,null=True,blank=True)
    company_address = models.CharField(max_length=120,null=True,blank=True)
    second_person = models.CharField(max_length=80,null=True,blank=True)
    third_person = models.CharField(max_length=80,null=True,blank=True)
    second_contact_no = models.CharField(max_length=80,null=True,blank=True)
    third_contact_no = models.CharField(max_length=80,null=True,blank=True)
    total_cost = models.FloatField(default=0.0)
    informed_on = models.DateField(null=True,blank=True)
    informed_by = models.CharField(max_length=60,null=True,blank=True)
    confirmed_estimate = models.CharField(default='NO',max_length=30,null=True,blank=True)
    repaired = models.CharField(default='NO',max_length=30,null=True,blank=True)

    delivery_by = models.CharField(max_length=50,null=True,blank=True)
    repaired_by = models.CharField(max_length=50,null=True,blank=True)
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




    def __int__(self):
        return self.pk


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
    in_warranty = models.CharField(default='NO',max_length=10,null=True,blank=True)
    is_last_product = models.BooleanField(default=False,)
    entry_date = models.DateField(default=datetime.date.today)



    def __int__(self):
        return self.repairing_id

class Repairing_Feedback(models.Model):
    user_id = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    customer_id = models.ForeignKey(Customer_Details, on_delete=models.CASCADE)
    reparing_id = models.ForeignKey(Repairing_after_sales_service, on_delete=models.CASCADE)
    satisfied_with_communication = models.FloatField(default=0.00)
    speed_of_performance = models.FloatField(default=0.00)
    price_of_reparing = models.FloatField(default=0.00)
    overall_interaction = models.FloatField(default=0.00)
    about_hsco = models.CharField(max_length=60, null=True, blank=True)
    any_suggestion = models.CharField(max_length=90, null=True, blank=True)

    class Meta:
        unique_together = ('user_id', 'customer_id', 'reparing_id',)

class Component_Replaced(models.Model):
    user_id = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Repairing_Product, on_delete=models.CASCADE,null=True,blank=True)
    replaced_name = models.CharField(max_length=80,null=True,blank=True)
    in_waranty = models.BooleanField(default=False)
    entry_timedate = models.DateField(default=datetime.date.today)






