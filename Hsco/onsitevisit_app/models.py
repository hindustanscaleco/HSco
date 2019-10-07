from django.db import models

class Onsite_visit(models.Model):
    repairingno=models.CharField(max_length=50)
    customer_name = models.CharField(max_length=80)
    company_name = models.CharField(max_length=80)


    def __str__(self):
        return self.repairingno
