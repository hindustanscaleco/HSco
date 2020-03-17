from django.db import models
from django.utils import timezone

from lead_management.models import Lead


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

class Lead_Product(models.Model):
    # lead_id = models.ForeignKey(Lead,on_delete=models.CASCADE, null=True, blank=True)
    scale_type = models.CharField(max_length=150, null=True, blank=True)
    main_category = models.CharField(max_length=150, null=True, blank=True)
    sub_category = models.CharField(max_length=150, null=True, blank=True)
    sub_sub_category = models.CharField(max_length=150, null=True, blank=True)
    hsn_code = models.CharField(max_length=150, null=True, blank=True)
    product_image = models.ImageField(upload_to='lead_product_image/', blank=True, null=True)
    max_capacity = models.CharField(max_length=150, null=True, blank=True)
    accuracy = models.CharField(max_length=150, null=True, blank=True)
    platform_size = models.CharField(max_length=150, null=True, blank=True)
    product_desc = models.CharField(max_length=250, null=True, blank=True)
    product_brochure = models.FileField(upload_to='', blank=True, null=True)
    product_document = models.FileField(upload_to='', blank=True, null=True)
    cost_price = models.FloatField( null=True, blank=True)
    selling_price = models.FloatField( null=True, blank=True)
    carton_size = models.CharField(max_length=150, null=True, blank=True)

    def __int__(self):
        return self.id