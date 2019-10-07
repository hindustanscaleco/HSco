from django.db import models

class Repairing(models.Model):
    repairingnumber = models.CharField(max_length=40)

    def __str__(self):
        return self.repairingnumber