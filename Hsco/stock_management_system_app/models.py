from django.db import models
from customer_app.models import type_purchase, main_model, sub_model, sub_sub_model
from model_utils import FieldTracker
from user_app.models import SiteUser
import datetime

class Product(models.Model):
    # lead_id = models.ForeignKey(Lead,on_delete=models.CASCADE, null=True, blank=True)
    scale_type = models.ForeignKey(type_purchase, null=True, blank=True,on_delete=models.CASCADE)
    main_category = models.ForeignKey(main_model, null=True, blank=True,on_delete=models.CASCADE)
    sub_category = models.ForeignKey(sub_model, null=True, blank=True,on_delete=models.CASCADE)
    sub_sub_category = models.ForeignKey(sub_sub_model, null=True, blank=True,on_delete=models.CASCADE)  #PRODUCT CODE
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


class Godown(models.Model):
    name_of_godown = models.CharField(max_length=50,unique=True)
    goddown_assign_to = models.ForeignKey(SiteUser,on_delete=models.CASCADE)
    location = models.CharField(max_length=60)
    contact_no = models.CharField(max_length=15)
    entry_timedate = models.DateField(default=datetime.date.today)
    tracker = FieldTracker()
    log_entered_by = models.CharField(blank=True, null=True, max_length=100)

class GodownProduct(models.Model):
    godown_id = models.ForeignKey(Godown,on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    added_by_id = models.ForeignKey(SiteUser,on_delete=models.CASCADE)
    quantity = models.FloatField(null=True, blank=True)
    carton_count = models.FloatField(null=True, blank=True)
    entry_timedate = models.DateField(default=datetime.date.today)
    tracker = FieldTracker()
    log_entered_by = models.CharField(blank=True, null=True, max_length=100)

    def __int__(self):
        return self.id

class GoodsRequest(models.Model):
    req_from_godown = models.ForeignKey(Godown,on_delete=models.CASCADE,related_name='Godown1',null=True,blank=True)
    req_to_godown = models.ForeignKey(Godown,on_delete=models.CASCADE,related_name='Godown2',null=True,blank=True)
    is_all_req = models.BooleanField(default=False)
    entered_by = models.ForeignKey(SiteUser,on_delete=models.CASCADE,null=True,blank=True)
    status = models.CharField(max_length=50,null=True,blank=True)
    entry_timedate = models.DateField(default=datetime.date.today)
    tracker = FieldTracker()
    log_entered_by = models.CharField(blank=True, null=True, max_length=100)

class RequestedProducts(models.Model):
    godown_id = models.ForeignKey(Godown,on_delete=models.CASCADE,null=True,blank=True)
    godown_product_id = models.ForeignKey(GodownProduct, on_delete=models.CASCADE,null=True,blank=True)
    goods_req_id = models.ForeignKey(GoodsRequest, on_delete=models.CASCADE,null=True,blank=True)

    req_quantity = models.FloatField(default=0.0)
    sent_quantity = models.FloatField(default=0.0)
    received_quantity = models.FloatField(default=0.0)

    req_carton_count = models.FloatField(default=0.0)
    sent_carton_count = models.FloatField(default=0.0)
    received_carton_count = models.FloatField(default=0.0)

    faulty = models.FloatField(default=0.0)

    req_type = models.CharField(max_length=20,null=True,blank=True)
    entry_timedate = models.DateField(default=datetime.date.today)
    tracker = FieldTracker()
    log_entered_by = models.CharField(blank=True, null=True, max_length=100)

    def __int__(self):
        return self.id

class AcceptGoods(models.Model):
    from_godown = models.ForeignKey(Godown,on_delete=models.CASCADE,)
    notes = models.TextField()
    entry_timedate = models.DateField(default=datetime.date.today)
    tracker = FieldTracker()
    log_entered_by = models.CharField(blank=True, null=True, max_length=100)

    def __int__(self):
        return self.id

class AGProducts(models.Model):
    accept_product_id = models.ForeignKey(AcceptGoods, on_delete=models.CASCADE,)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.FloatField()
    carton_count = models.FloatField()
    type = models.CharField(max_length=20)
    entry_timedate = models.DateField(default=datetime.date.today)
    tracker = FieldTracker()
    log_entered_by = models.CharField(blank=True, null=True, max_length=100)

    def __int__(self):
        return self.id

class GodownTransactions(models.Model):
    goods_req_id = models.ForeignKey(GoodsRequest, on_delete=models.CASCADE,)
    entry_timedate = models.DateField(default=datetime.date.today)
    tracker = FieldTracker()
    log_entered_by = models.CharField(blank=True, null=True, max_length=100)

    def __int__(self):
        return self.id










