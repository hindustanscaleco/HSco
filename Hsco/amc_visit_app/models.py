from django.db import models

class Amcvisit(models.Model):
    amcno=models.CharField(max_length=50)
    customer_name = models.CharField(max_length=80)
    company_name = models.CharField(max_length=80)


    def __str__(self):
        return self.amcno