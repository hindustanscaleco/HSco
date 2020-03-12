from django.db import models
from django.utils import timezone
from customer_app.models import Customer_Details

class Lead(models.Model):
    customer_id = models.ForeignKey(Customer_Details,on_delete=models.CASCADE)
    current_stage = models.CharField(max_length=50,null=True,blank=True)
    new_existing_customer = models.CharField(max_length=50,null=True,blank=True)
    date_of_initiation = models.DateTimeField(default=timezone.now,)
    channel = models.CharField(max_length=50,null=True,blank=True)
    requirement = models.CharField(max_length=80,null=True,blank=True)
    upload_requirement_file = models.CharField(max_length=80,null=True,blank=True)
    owner_of_opportunity = models.CharField(max_length=80,null=True,blank=True)

    def __int__(self):
        return self.id

class Pi_section(models.Model):
    lead_id = models.ForeignKey(Lead,on_delete=models.CASCADE, null=True, blank=True)
    discount = models.CharField(max_length=80,null=True,blank=True)
    upload_pi_file = models.FileField(null=True,blank=True)
    select_pi_template = models.CharField(max_length=50, null=True, blank=True)
    call = models.TextField(max_length=120, null=True,blank=True)
    email = models.BooleanField(default=False)
    whatsapp = models.BooleanField(default=False)
    call2 = models.BooleanField(default=False)
    auto_manual_email = models.CharField(default='Automatic',max_length=50, null=True, blank=True)
    payment_channel = models.CharField(default='Check Payment',max_length=50, null=True, blank=True)
    payment_receipt = models.FileField(null=True, blank=True)
    upload_po_file = models.FileField(null=True, blank=True)
    payment_received_date = models.DateTimeField(default=timezone.now, )
    notes = models.TextField(max_length=120, null=True,blank=True)

    def __int__(self):
        return self.customer_name

class Lead_Product(models.Model):
    lead_id = models.ForeignKey(Lead,on_delete=models.CASCADE, null=True, blank=True)
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