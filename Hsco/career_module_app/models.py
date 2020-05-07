from django.db import models
from django.utils import timezone
import datetime

class Career_module(models.Model):
    current_stage = models.CharField(max_length=50,null=True,blank=True)
    application_no = models.IntegerField(null=True,blank=True)
    phone_no = models.CharField(max_length=10,null=True,blank=True)
    candidate_name = models.CharField(max_length=50,null=True,blank=True)
    choose_position = models.CharField(max_length=20,null=True,blank=True)
    candidate_email = models.CharField(max_length=60, null=True,blank=True)
    address = models.CharField(max_length=120,null=True,blank=True)
    institute_name = models.CharField(max_length=50,null=True,blank=True)
    course = models.CharField(max_length=50,null=True,blank=True)
    year_of_completion = models.CharField(max_length=4,null=True,blank=True)
    percentage = models.CharField(max_length=50,null=True,blank=True)
    company_name = models.CharField(max_length=50,null=True,blank=True)
    work_expirance_from = models.DateTimeField(blank= True, null=True)
    work_expirance_to = models.DateTimeField(blank= True, null=True)
    date_of_birth = models.DateTimeField(blank= True, null=True)
    work_expirance_details = models.CharField(max_length=120,null=True,blank=True)
    designation = models.CharField(max_length=60,null=True,blank=True)
    current_salary = models.CharField(max_length=60,null=True,blank=True)
    aadhar_card = models.CharField(max_length=60,null=True,blank=True)
    pan_card_availabe = models.CharField(max_length=60,null=True,blank=True)
    bank_account = models.CharField(max_length=60,null=True,blank=True)
    entry_timedate = models.DateTimeField(default=timezone.now, )
    say_yourself = models.CharField(max_length=60,null=True,blank=True)
    confidance = models.CharField(max_length=60,null=True,blank=True)
    without_job_with_reason = models.CharField(max_length=120,null=True,blank=True)
    reason_for_last_job_before = models.CharField(max_length=120,null=True,blank=True)
    working_from_10_to_8_and = models.CharField(max_length=10,null=True,blank=True)
    any_question = models.CharField(max_length=10,null=True,blank=True)
    any_question_yes = models.CharField(max_length=10,null=True,blank=True)
    comfortable_english = models.CharField(max_length=10,null=True,blank=True)
    comfortable_marathi = models.CharField(max_length=10,null=True,blank=True)
    how_good_english = models.CharField(max_length=10,null=True,blank=True)
    working_from_10_to_8 = models.CharField(max_length=10, null=True, blank=True)
    weighting_scale_manufactures_mumbai = models.CharField(max_length=10, null=True, blank=True)
    excel_formate = models.CharField(max_length=10, null=True, blank=True)
    sum_in_excel = models.CharField(max_length=10, null=True, blank=True)
    time_taken = models.CharField(max_length=10, null=True, blank=True)
    take_out_60 = models.CharField(max_length=10, null=True, blank=True)
    time_to_disorder_wire_pcb = models.CharField(max_length=10, null=True, blank=True)
    time_to_solder_wire_back = models.CharField(max_length=10, null=True, blank=True)
    soldering_strong = models.CharField(max_length=10, null=True, blank=True)
    value_of_resister = models.CharField(max_length=10, null=True, blank=True)
    open_and_short_circuit = models.CharField(max_length=10, null=True, blank=True)
    is_sales_candidate = models.BooleanField(default=False)
    is_technical_candidate = models.BooleanField(default=False)

    class Meta:
        unique_together = ('phone_no','candidate_email')

    def __str__(self):
        return self.candidate_name


