from django.db import models

class Restamping(models.Model):
    restampingno = models.CharField(max_length=30)

    def __str__(self):
        return self.restampingno