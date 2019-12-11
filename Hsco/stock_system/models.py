from django.db import models

class Stock_System(models.Model):
    type_of_scale = models.CharField(max_length=50,)
    hsn_code = models.CharField(max_length=50,)
    product_code = models.CharField(max_length=50,)
    product_sub_code = models.CharField(max_length=50,)
    product_sub_sub_code = models.CharField(max_length=50,)
    photo = models.FileField(max_length=50,)
    description = models.CharField(max_length=50,)
    plate_size = models.CharField(max_length=50,)



    def __str__(self):
        return str(self.pk)