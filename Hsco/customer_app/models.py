import datetime
import uuid
from django.db import models
from django.utils import timezone



class Customer_Details(models.Model):
    # crn_number = models.UUIDField(unique=True, default=uuid.uuid4)
    # crn_number = models.BigIntegerField(unique=True, null=True, blank=True)
    customer_name = models.CharField(max_length=150,)
    company_name = models.CharField(max_length=150,null=True,blank=True)
    address = models.CharField(max_length=250,null=True,blank=True)
    contact_no = models.CharField(max_length=30,)
    customer_email_id = models.EmailField(max_length=80,null=True,blank=True)
    customer_gst_no = models.CharField(max_length=15,null=True,blank=True)
    customer_industry = models.CharField(max_length=80,null=True,blank=True)
    # entry_timedate = models.DateTimeField(default=timezone.now, )
    entry_timedate = models.DateField(default=datetime.date.today)

    class Meta:
        unique_together = ('customer_name','contact_no')

    def __int__(self):
        return self.id

    def short_address(self):
        if self.address:
            return self.address[:18]
        else:
            return 'N/A'

class type_purchase(models.Model):
    name= models.CharField(max_length=120)
    entry_timedate = models.DateTimeField(default=timezone.now, )

    def __str__(self):
        return self.name

class main_model(models.Model):
    name= models.CharField(max_length=120)
    type_purchase = models.ForeignKey(type_purchase,on_delete=models.CASCADE)
    entry_timedate = models.DateTimeField(default=timezone.now, )

    def __str__(self):
        return self.name

class sub_model(models.Model):
    name= models.CharField(max_length=120)
    main_model = models.ForeignKey(main_model,on_delete=models.CASCADE)
    entry_timedate = models.DateTimeField(default=timezone.now, )

    def __str__(self):
        return self.name

class sub_sub_model(models.Model):
    name= models.CharField(max_length=120)
    sub_model = models.ForeignKey(sub_model,on_delete=models.CASCADE)
    entry_timedate = models.DateTimeField(default=timezone.now, )

    def __str__(self):
        return self.name

class Log(models.Model):
    entered_by = models.CharField(max_length=120, null=True, blank=True)
    module_name = models.CharField(max_length=120, null=True, blank=True)
    action_type = models.CharField(max_length=120, null=True, blank=True)
    table_name = models.CharField(max_length=120, null=True, blank=True)
    reference = models.CharField(max_length=120, null=True, blank=True)
    action = models.CharField( null=True, blank=True, max_length=300)
    entry_timedate = models.DateTimeField(default=timezone.now, )

    class Meta:
        unique_together = ('entered_by', 'module_name', 'action_type','table_name','reference','action')

    def __int__(self):
        return self.pk
