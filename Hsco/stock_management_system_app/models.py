from django.db import models

class Godown(models.Model):
    name_of_godown = models.CharField(max_length=50)
    goddown_assign_to = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    contact_no = models.IntegerField()
