import datetime
import uuid

from django.db import models
from django.utils import timezone



class Customer_Details(models.Model):
    # crn_number = models.UUIDField(unique=True, default=uuid.uuid4)
    # crn_number = models.BigIntegerField(unique=True, null=True, blank=True)
    customer_name = models.CharField(max_length=80, null=True, blank=True)
    company_name = models.CharField(max_length=80,null=True,blank=True)
    address = models.CharField(max_length=250,null=True,blank=True)
    contact_no = models.CharField(max_length=30,null=True,blank=True)
    customer_email_id = models.CharField(max_length=30,null=True,blank=True)

    def __int__(self):
        return self.id










