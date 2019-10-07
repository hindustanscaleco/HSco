from django.db import models

class Dispatch(models.Model):
    dispatch_id = models.CharField(max_length=30)
    customer_no = models.CharField(max_length=30)
    customer_email = models.CharField(max_length=30)
    customer_name = models.CharField(max_length=30)
    company_name = models.CharField(max_length=30)
    customer_address = models.CharField(max_length=250)
    #goods_to_dispatch = models.ForeignKey()
    date_of_dispatch = models.DateField()
    dispatch_by = models.CharField(max_length=80)
    packed_by = models.CharField(max_length=80)
    hamal_name = models.CharField(max_length=80)
    no_bundles = models.FloatField()
    transport_name = models.CharField(max_length=80)
    lr_no = models.CharField(max_length=30)
    photo_lr_no = models.ImageField(upload_to='')
    channel_of_dispatch = models.CharField(max_length=30)
    notes = models.CharField(max_length=30)


    def __str__(self):
        return self.dispatch_id