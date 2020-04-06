from django.db import models
import datetime
# Create your models here.
from django.utils import timezone
from user_app.models import SiteUser


class Chat_model(models.Model):
    message_to = models.ForeignKey(SiteUser,on_delete=models.CASCADE, related_name='message_to')
    message_from = models.ForeignKey(SiteUser,on_delete=models.CASCADE, related_name='message_from')
    message = models.CharField(max_length=160)
    is_warning = models.BooleanField(default=False)
    is_defect = models.BooleanField(default=False)
    is_employee = models.BooleanField()
    is_manager = models.BooleanField()
    is_admin = models.BooleanField()
    is_superadmin = models.BooleanField()
    entrytimedate = models.DateTimeField(default=timezone.now)