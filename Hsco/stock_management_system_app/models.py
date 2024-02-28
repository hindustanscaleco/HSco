from django.db import models
from customer_app.models import type_purchase, main_model, sub_model, sub_sub_model
from model_utils import FieldTracker
from user_app.models import SiteUser
import datetime
from purchase_app.models import Purchase_Details
from django.utils import timezone

from purchase_app.models import Product_Details
from simple_history.models import HistoricalRecords


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
    product_desc = models.TextField(null=True, blank=True)
    product_brochure = models.FileField(upload_to='lead_product_brochure/', blank=True, null=True)
    product_document = models.FileField(upload_to='lead_product_document/', blank=True, null=True)
    cost_price = models.FloatField( null=True, blank=True)
    selling_price = models.FloatField( null=True, blank=True)
    carton_size = models.CharField(max_length=150)
    history = HistoricalRecords()

    def __int__(self):
        return self.id


class Godown(models.Model):
    name_of_godown = models.CharField(max_length=50,unique=True)
    goddown_assign_to = models.ForeignKey(SiteUser,on_delete=models.CASCADE,related_name='goddown_assign_to', null=True, blank=True)
    godown_admin = models.ForeignKey(SiteUser,on_delete=models.CASCADE,related_name='godown_admin', null=True, blank=True)
    location = models.CharField(max_length=60)
    contact_no = models.CharField(max_length=15)
    entry_timedate = models.DateField(default=datetime.date.today)
    default_godown_purchase = models.BooleanField(default=False)
    tracker = FieldTracker()
    log_entered_by = models.CharField(blank=True, null=True, max_length=100)
    history = HistoricalRecords()


class GodownProduct(models.Model):
    godown_id = models.ForeignKey(Godown,on_delete=models.CASCADE, related_name='godown_products')
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    added_by_id = models.ForeignKey(SiteUser,on_delete=models.CASCADE)
    quantity = models.FloatField(default=0.0)
    critical_limit = models.FloatField(default=0.0)
    individual_faulty = models.FloatField(default=0.0)
    entry_timedate = models.DateField(default=datetime.date.today)

    tracker = FieldTracker()
    log_entered_by = models.CharField(blank=True, null=True, max_length=100)
    history = HistoricalRecords()

    @property
    def carton_count(self):
        product = Product.objects.get(id=self.product_id)
        quantity = self.quantity
        if product.carton_size != "" and float(product.carton_size) != 0.0 and float(product.carton_size) != 0:
            return (float(quantity) / float(product.carton_size))
        else:
            return "N/A"

    @property
    def carton_critical_limit(self):
        product = Product.objects.get(id=self.product_id)
        critical_limit = self.critical_limit
        if product.carton_size != "" and float(product.carton_size) != 0.0 and float(product.carton_size) != 0:
            return (float(critical_limit) / float(product.carton_size))
        else:
            return "N/A"

    @property
    def carton_faulty(self):
        product = Product.objects.get(id=self.product_id)
        individual_faulty = self.individual_faulty
        if product.carton_size != "" and float(product.carton_size) != 0.0 and float(product.carton_size) != 0:
            return (float(individual_faulty) / float(product.carton_size))
        else:
            return "N/A"

    def __int__(self):
        return self.id


class GoodsRequest(models.Model):
    req_from_godown = models.ForeignKey(Godown,on_delete=models.CASCADE,related_name='Godown1',null=True,blank=True)
    req_to_godown = models.ForeignKey(Godown,on_delete=models.CASCADE,related_name='Godown2',null=True,blank=True)
    is_all_req = models.BooleanField(default=False)
    goods_sent = models.BooleanField(default=False)
    goods_received = models.BooleanField(default=False)
    entered_by = models.ForeignKey(SiteUser,on_delete=models.CASCADE,null=True,blank=True)
    status = models.CharField(max_length=50,null=True,blank=True)
    request_admin = models.BooleanField(default=False)
    outside_workstation = models.BooleanField(default=False)
    notify = models.BooleanField(default=False)
    request_admin_id = models.ForeignKey(SiteUser,on_delete=models.CASCADE,related_name='request_admin', null=True, blank=True)
    entry_timedate = models.DateField(default=datetime.date.today)
    tracker = FieldTracker()
    log_entered_by = models.CharField(blank=True, null=True, max_length=100)
    history = HistoricalRecords()

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
    faulty_quantity = models.FloatField(default=0.0)
    faulty_carton = models.FloatField(default=0.0)
    req_type = models.CharField(max_length=20,null=True,blank=True)
    entry_timedate = models.DateField(default=datetime.date.today)
    tracker = FieldTracker()
    log_entered_by = models.CharField(blank=True, null=True, max_length=100)
    entry_timedate_time = models.DateTimeField(default=timezone.now,)
    history = HistoricalRecords()

    def __int__(self):
        return self.id

class AcceptGoods(models.Model):
    from_godown = models.ForeignKey(Godown,on_delete=models.CASCADE,null=True,blank=True)
    notes = models.TextField(null=True,blank=True)
    good_added = models.BooleanField(default=False)
    entry_timedate = models.DateField(default=datetime.date.today)
    tracker = FieldTracker()
    log_entered_by = models.CharField(blank=True, null=True, max_length=100)
    history = HistoricalRecords()

    def __int__(self):
        return self.id

class AGProducts(models.Model):
    godown_id = models.ForeignKey(Godown,on_delete=models.CASCADE,null=True,blank=True)
    accept_product_id = models.ForeignKey(AcceptGoods, on_delete=models.CASCADE,null=True, blank=True)
    godown_product_id = models.ForeignKey(GodownProduct, on_delete=models.CASCADE,null=True,blank=True)
    quantity = models.FloatField(default=0.0)
    carton_count = models.FloatField(default=0.0)
    type = models.CharField(max_length=20,null=True, blank=True)
    entry_timedate = models.DateField(default=datetime.date.today)
    tracker = FieldTracker()
    log_entered_by = models.CharField(blank=True, null=True, max_length=100)
    history = HistoricalRecords()

    def __int__(self):
        return self.id


class GodownTransactions(models.Model):
    goods_req_id = models.OneToOneField(GoodsRequest, on_delete=models.CASCADE,null=True, blank=True)
    accept_goods_id = models.OneToOneField(AcceptGoods, on_delete=models.CASCADE,null=True, blank=True)
    purchase_id = models.OneToOneField(Purchase_Details, on_delete=models.CASCADE,null=True, blank=True)
    purchase_product_id = models.ForeignKey(Product_Details, on_delete=models.CASCADE,null=True,blank=True)
    purchase_quantity = models.FloatField(default=0.0)
    godown_product_id = models.ForeignKey(GodownProduct, on_delete=models.CASCADE,null=True,blank=True)
    loss_quantity = models.FloatField(default=0.0)
    adjustment_quantity = models.FloatField(default=0.0)

    entry_timedate = models.DateField(default=datetime.date.today)
    tracker = FieldTracker()
    log_entered_by = models.CharField(blank=True, null=True, max_length=100)
    notes = models.TextField(null=True,blank=True)
    history = HistoricalRecords()

    def __int__(self):
        return self.id

    @property
    def type(self):
        type = ''
        if self.goods_req_id:
            type = 'transfer'
        elif self.accept_goods_id:
            type = 'purchase'
        elif self.purchase_id:
            type = 'sale'
        elif self.loss_quantity != 0.0:
            type = 'loss'
        elif self.adjustment_quantity != 0.0:
            type = 'adjustment'
        return (str(type))

# class Faulty_History(models.Model):
#     godown_product_id = models.ForeignKey(GodownProduct, on_delete=models.CASCADE,null=True,blank=True)
#     quantity = models.FloatField(default=0.0 )
#     notes = models.TextField(null=True,blank=True)
#     entry_timedate = models.DateField(default=datetime.date.today)
#
#     def __int__(self):
#         return self.id
#
# class Adjustment_History(models.Model):
#     godown_product_id = models.ForeignKey(GodownProduct, on_delete=models.CASCADE,null=True,blank=True)
#     quantity = models.FloatField(default=0.0 )
#     notes = models.TextField(null=True,blank=True)
#     entry_timedate = models.DateField(default=datetime.date.today)
#
#     def __int__(self):
#         return self.id


class DailyStock(models.Model):
    godown_products = models.ForeignKey(GodownProduct,on_delete=models.CASCADE) #Done
    closing_stock = models.FloatField() #Done
    sales_quantity = models.FloatField(default=0.0) #Done
    goods_request_quantity = models.FloatField(default=0.0) #Done
    accept_goods_quantity = models.FloatField(default=0.0) #Purchase_quantity
    faulty_quantity = models.FloatField(default=0.0) #Done
    adjustment_quantity = models.FloatField(default=0.0)
    loss_quantity = models.FloatField(default=0.0)
    sales_ids = models.TextField(null=True,blank=True)  #doubt
    accept_goods_ids = models.TextField(null=True,blank=True) #doubt
    goods_request_ids = models.TextField(null=True,blank=True) #doubt
    entry_timedate = models.DateField(default=datetime.date.today)




