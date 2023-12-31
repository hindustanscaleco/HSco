import datetime
from django.db import models
from django.utils import timezone
from customer_app.models import Lead_Customer_Details, DynamicDropdown
from user_app.models import SiteUser
from stock_management_system_app.models import Product
from django.core.validators import URLValidator
from model_utils import FieldTracker
from purchase_app.models import Purchase_Details


class Lead(models.Model):
    purchase_id = models.ForeignKey(Purchase_Details, on_delete=models.CASCADE,null=True,blank=True)
    customer_id = models.ForeignKey(Lead_Customer_Details,on_delete=models.CASCADE)
    owner_of_opportunity = models.ForeignKey(SiteUser,null=True,blank=True,on_delete=models.CASCADE)
    current_stage = models.CharField(max_length=50,null=True,blank=True)
    new_existing_customer = models.CharField(max_length=50,null=True,blank=True)
    date_of_initiation = models.DateField(null=True,blank=True)
    #old field
    channel = models.CharField(max_length=50,null=True,blank=True)
    #new field
    channel_id = models.ForeignKey(DynamicDropdown,on_delete=models.CASCADE,related_name='channel_marketing_lead', null=True, blank=True)
    channel_of_marketing = models.CharField(max_length=50,null=True,blank=True)
    requirement = models.TextField(null=True,blank=True)
    requirement_indiamart_unique = models.CharField(max_length=120,null=True,blank=True)
    lost_reason = models.CharField(blank= True, null=True, max_length=180)
    postponed_reason = models.CharField(blank= True, null=True, max_length=180)
    upload_requirement_file = models.FileField(upload_to='lead_requirement_file/',null=True,blank=True)
    is_entered_purchase = models.BooleanField(default=False)
    postpond_time_date = models.DateField(null=True,blank=True)
    is_indiamart_purchased_lead = models.BooleanField(default=False)
    # owner_of_opportunity = models.CharField(max_length=80,null=True,blank=True)
    is_manual_mode_followup = models.BooleanField(default=True)
    no_of_times_followup_done = models.IntegerField(default=0)
    indiamart_time = models.CharField(max_length=15,default='29-May-20')

    # entry_timedate = models.DateTimeField(default=timezone.now, )
    entry_timedate = models.DateField(default=datetime.date.today)
    tracker = FieldTracker()
    log_entered_by = models.CharField(blank= True, null=True, max_length=100)

    def __int__(self):
        return self.id

    class Meta:
        unique_together = ('customer_id','channel','requirement_indiamart_unique','indiamart_time')

class Pi_section(models.Model):
    lead_id = models.ForeignKey(Lead,on_delete=models.CASCADE, null=True, blank=True)
    discount = models.CharField(max_length=80,null=True,blank=True,default=0.0)
    discount_type = models.CharField(default='rupee',max_length=80,null=True,blank=True,)
    upload_pi_file = models.FileField(null=True,blank=True)
    select_pi_template = models.CharField(max_length=45,null=True, blank=True)
    select_gst_type = models.CharField(max_length=45,null=True, blank=True)
    manual_pi_no = models.CharField(max_length=45,null=True, blank=True)
    call = models.TextField(null=True,blank=True)
    email = models.BooleanField(default=False, null=True,blank=True)
    whatsapp = models.BooleanField(default=False, null=True,blank=True)
    call2 = models.BooleanField(default=False, null=True,blank=True)
    auto_manual_email = models.CharField(default='Automatic',max_length=50, null=True, blank=True)
    payment_channel = models.CharField(default='Check Payment',max_length=50, null=True, blank=True)
    payment_receipt = models.FileField(null=True, blank=True)
    upload_po_file = models.FileField(null=True, blank=True)
    payment_received_date = models.DateTimeField(default=timezone.now, )
    notes = models.TextField( null=True,blank=True)
    cgst_sgst = models.FloatField(null=True,blank=True)
    igst = models.FloatField(null=True,blank=True)
    pf_total = models.FloatField(null=True,blank=True)
    total_cost = models.FloatField(null=True,blank=True)
    net_total = models.FloatField(null=True,blank=True)
    round_up_total = models.FloatField(null=True,blank=True)
    grand_total = models.FloatField(null=True,blank=True)

    # entry_timedate = models.DateTimeField(default=timezone.now, )
    first_submit = models.BooleanField(default=False)
    show_external_pi_first = models.BooleanField(default=False)
    entry_timedate = models.DateField(default=datetime.date.today)

    tracker = FieldTracker()
    log_entered_by = models.CharField(blank= True, null=True, max_length=100)



    def __int__(self):
        return self.id

class Pi_product(models.Model):
    lead_id = models.ForeignKey(Lead, on_delete=models.CASCADE, null=True, blank=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.FloatField(null=True, blank=True)
    pf = models.FloatField(null=True, blank=True)

    rate = models.FloatField( null=True, blank=True)
    product_desc = models.TextField(null=True, blank=True)
    hsn_code = models.CharField(max_length=150, null=True, blank=True)
    product_image = models.ImageField(upload_to='lead_pi_product_image/', blank=True, null=True)

    entry_timedate = models.DateField(default=datetime.date.today)
    tracker = FieldTracker()
    log_entered_by = models.CharField(blank= True, null=True, max_length=100)
    product_total_cost = models.FloatField(null=True,blank=True)
    add_brochure = models.BooleanField(default=True)
    add_product_document = models.BooleanField(default=True)
    def __int__(self):
        return self.id

class Pi_History(models.Model):
    pi_history_file = models.FileField(null=True,blank=True, upload_to='pi_history_file/')
    lead_id = models.ForeignKey(Lead, on_delete=models.CASCADE, null=True, blank=True)
    # pi_product_id = models.ForeignKey(Pi_product, on_delete=models.CASCADE, null=True, blank=True)
    # entry_timedate = models.DateTimeField(default=timezone.now, )
    medium_of_selection = models.CharField(blank= True, null=True, max_length=100)
    call_detail = models.CharField(blank= True, null=True, max_length=100)
    entry_timedate = models.DateField(default=datetime.date.today)
    tracker = FieldTracker()
    log_entered_by = models.CharField(blank= True, null=True, max_length=100)
    entry_timedate_time = models.DateTimeField(default=timezone.now,)


    def __int__(self):
        return self.id

#=================Follow UP Section=======================================================================


class Follow_up_section(models.Model):
    lead_id = models.ForeignKey(Lead,on_delete=models.CASCADE,null=True,blank=True)
    whatsappno = models.CharField(max_length=120,null=True,blank=True)
    auto_manual_mode = models.CharField(default='Select Mode', max_length=50, null=True, blank=True)
    fields = models.TextField(null=True, blank=True)
    email_subject = models.CharField(max_length=150,null=True, blank=True)
    entry_timedate = models.DateField(default=datetime.date.today)
    tracker = FieldTracker()
    log_entered_by = models.CharField(blank= True, null=True, max_length=100)


    def __int__(self):
        return self.id



class History_followup(models.Model):
    follow_up_section = models.ForeignKey(Follow_up_section,on_delete=models.CASCADE,null=True,blank=True)
    lead_id = models.ForeignKey(Lead, on_delete=models.CASCADE, null=True, blank=True)
    fields = models.TextField(null=True, blank=True)
    product_ids = models.CharField(max_length=100)
    is_email = models.BooleanField(default=False)
    is_whatsapp = models.BooleanField(default=False)
    is_call = models.BooleanField(default=False)
    is_sms = models.BooleanField(default=False)
    wa_msg = models.TextField(null=True, blank=True)
    wa_no = models.CharField(max_length=12)
    email_subject = models.CharField(max_length=120)
    email_msg = models.TextField(null=True, blank=True)
    call_response = models.TextField(null=True, blank=True)
    sms_msg = models.TextField()
    sms_con = models.TextField()
    is_manual_mode = models.BooleanField(default=True)
    is_auto_follow_deleted = models.BooleanField(default=False)
    followup_history_file = models.FileField(null=True, blank=True, upload_to='followup_history_file/')
    html_content = models.TextField(null=True, blank=True)
    entry_timedate_time = models.DateTimeField(default=timezone.now,)
    entry_timedate = models.DateField(default=datetime.date.today)


class Auto_followup_details(models.Model):
    follow_up_history = models.ForeignKey(History_followup,on_delete=models.CASCADE,null=True,blank=True)
    followup_date = models.DateField(default=datetime.date.today,)
    is_followed = models.BooleanField(default=False)
    no_of_times_fdone = models.IntegerField(default=0)
    # entry_timedate = models.DateTimeField(default=timezone.now,)
    entry_timedate = models.DateField(default=datetime.date.today)
    tracker = FieldTracker()
    log_entered_by = models.CharField(blank= True, null=True, max_length=100)


class Followup_product(models.Model):
    lead_id = models.ForeignKey(Lead,on_delete=models.CASCADE,null=True,blank=True)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    scale_type = models.CharField(max_length=150, null=True, blank=True)
    main_category = models.CharField(max_length=150, null=True, blank=True)
    sub_category = models.CharField(max_length=150, null=True, blank=True)
    sub_sub_category = models.CharField(max_length=150, null=True, blank=True)  # PRODUCT CODE
    hsn_code = models.CharField(max_length=150, null=True, blank=True)
    max_capacity = models.CharField(max_length=150, null=True, blank=True)
    accuracy = models.CharField(max_length=150, null=True, blank=True)
    platform_size = models.CharField(max_length=150, null=True, blank=True)
    product_desc = models.TextField(null=True, blank=True)
    cost_price = models.FloatField(null=True, blank=True)
    selling_price = models.FloatField(null=True, blank=True)
    carton_size = models.CharField(max_length=150, null=True, blank=True)
    # entry_timedate = models.DateTimeField(default=timezone.now, )
    # is_whatsapp_check = models.BooleanField(default=False, null=True,blank=True)
    # is_call2_check = models.BooleanField(default=False, null=True,blank=True)
    # email_check = models.BooleanField(default=False, null=True,blank=True)
    # sms_check = models.BooleanField(default=False, null=True,blank=True)
    entry_timedate = models.DateField(default=datetime.date.today)
    tracker = FieldTracker()
    log_entered_by = models.CharField(blank= True, null=True, max_length=100)

class IndiamartLeadDetails(models.Model):
    from_date = models.DateField()
    to_date = models.DateField()
    lead_count = models.BigIntegerField()
    entry_datetime = models.DateTimeField(default=timezone.now, )
    entry_timedate = models.DateField(default=datetime.date.today)
    tracker = FieldTracker()
    log_entered_by = models.CharField(blank= True, null=True, max_length=100)


    class Meta:
        unique_together = ('from_date','to_date','lead_count')

class Payment_details(models.Model):
    lead_id = models.ForeignKey(Lead, on_delete=models.CASCADE, null=True, blank=True)
    payment_channel = models.CharField(max_length=60, null=True, blank=True)
    payment_receipt = models.FileField(upload_to='payment_receipt/',null=True,blank=True)
    # payment_recived_date = models.DateField(default=datetime.date.today)
    upload_pofile = models.FileField(upload_to='payment_section_po_file/',null=True,blank=True)
    Payment_notes = models.TextField(null=True, blank=True)

    import datetime

    payment_mode = models.CharField(max_length=150,null=True, blank=True )
    #cheque details
    bank_name = models.CharField(max_length=150, null=True, blank=True)
    cheque_no = models.TextField(null=True, blank=True)
    cheque_date = models.DateField(default=datetime.date.today)

    #neft details
    neft_bank_name = models.CharField(max_length=150, null=True, blank=True)
    neft_date = models.DateField(default=datetime.date.today)
    reference_no = models.CharField(max_length=150, null=True, blank=True)

    #credit details
    credit_pending_amount =  models.FloatField(default=0.0,null=True,blank=True)
    credit_authorised_by = models.CharField(max_length=250,null=True, blank=True )


    entry_timedate = models.DateField(default=datetime.date.today)
    tracker = FieldTracker()
    log_entered_by = models.CharField(blank= True, null=True, max_length=100)

    def __int__(self):
        return self.id




