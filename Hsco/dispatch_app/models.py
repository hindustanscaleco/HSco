from django.db import models

class Dispatch(models.Model):
    dispatch_id = models.CharField(max_length=30,null=True,blank=True)
    customer_no = models.CharField(max_length=30,null=True,blank=True)
    customer_email = models.CharField(max_length=30,null=True,blank=True)
    customer_name = models.CharField(max_length=30,null=True,blank=True)
    company_name = models.CharField(max_length=30,null=True,blank=True)
    customer_address = models.CharField(max_length=250,null=True,blank=True)
    #goods_to_dispatch = models.ForeignKey()
    date_of_dispatch = models.DateField()
    dispatch_by = models.CharField(max_length=80,null=True,blank=True)
    packed_by = models.CharField(max_length=80,null=True,blank=True)
    hamal_name = models.CharField(max_length=80,null=True,blank=True)
    no_bundles = models.FloatField(default=0.0)
    transport_name = models.CharField(max_length=80,null=True,blank=True)
    lr_no = models.CharField(max_length=30,null=True,blank=True)
    photo_lr_no = models.ImageField(upload_to='',null=True,blank=True)
    channel_of_dispatch = models.CharField(max_length=30,null=True,blank=True)
    notes = models.CharField(max_length=30,null=True,blank=True)


    def __str__(self):
        return self.dispatch_id