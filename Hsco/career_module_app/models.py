from django.db import models
from django.utils import timezone
import datetime

class Position(models.Model):
    position = models.CharField(max_length=50,null=True,blank=True)

    def __int__(self):
        return self.id

    class  Meta():
        ordering = ['-id']


class Career_module(models.Model):
    current_stage = models.CharField(max_length=50,null=True,blank=True)
    application_no = models.IntegerField(null=True,blank=True)
    phone_no = models.CharField(max_length=10,null=True,blank=True)
    candidate_name = models.CharField(max_length=50,null=True,blank=True)
    choose_position = models.ForeignKey(Position, on_delete=models.CASCADE,null=True, blank=True )
    candidate_email = models.CharField(max_length=60, null=True,blank=True)
    address = models.CharField(max_length=300,null=True,blank=True)
    date_of_birth = models.DateTimeField(blank= True, null=True)

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
    any_question_yes = models.TextField(null=True,blank=True)
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
    notes = models.TextField( null=True, blank=True)
    candidate_resume = models.FileField(upload_to='candidate_resume/',null=True,blank=True)
    entry_timedate = models.DateField(default=datetime.date.today)



    class Meta:
        unique_together = ('candidate_name','choose_position','phone_no','candidate_email')

    def __str__(self):
        return self.candidate_name


    class  Meta():
        ordering = ['-id']



class EducationalDetails(models.Model):
    career_id = models.ForeignKey(Career_module, on_delete=models.CASCADE,null=True, blank=True)
    institute_name = models.CharField(max_length=50, null=True, blank=True)
    course = models.CharField(max_length=50, null=True, blank=True)
    year_of_completion = models.CharField(max_length=4, null=True, blank=True)
    percentage = models.CharField(max_length=50, null=True, blank=True)
    achievements = models.TextField( null=True, blank=True)
    entry_timedate = models.DateField(default=datetime.date.today)

    def __int__(self):
        return self.id

    class  Meta():
        ordering = ['-id']

class WorkExperience(models.Model):
    career_id = models.ForeignKey(Career_module, on_delete=models.CASCADE,null=True, blank=True)
    company_name = models.CharField(max_length=80, null=True, blank=True)
    work_expirance_from = models.DateTimeField(blank=True, null=True)
    work_expirance_to = models.DateTimeField(blank=True, null=True)
    work_expirance_details = models.CharField(max_length=250, null=True, blank=True)
    designation = models.CharField(max_length=80, null=True, blank=True)
    entry_timedate = models.DateField(default=datetime.date.today)

    @property
    def exp_yrs(self):
        if self.work_expirance_to :
            years = (self.work_expirance_to) - (self.work_expirance_from)
            total_years = years.total_seconds() // 31536000
            return (int(total_years))

    @property
    def exp_months(self):
        if self.work_expirance_to:
            duration_1 = (self.work_expirance_to) - (self.work_expirance_from)
            duration = duration_1.total_seconds()
            years = duration % 31536000

            total_months = float(years) / 2628002.88

            return (int(total_months))
    def __int__(self):
        return self.id

    class  Meta():
        ordering = ['-id']