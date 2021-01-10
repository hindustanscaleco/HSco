from django.db import models
from user_app.models import SiteUser
from stock_management_system_app.models import Godown
import datetime
# Create your models here.

# class Expense_Details(models.Model):   
    # user_id = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    # manager_id = models.CharField(max_length=150, null=True, blank=True)
    # crm_no = models.ForeignKey(Customer_Details,on_delete=models.CASCADE,null=True,blank=True)
    # date_of_purchase = models.DateField(default=datetime.date.today,null=True,blank=True)
    # bill_no = models.CharField(max_length=150,null=True,blank=True)
class Expense_Type_Sub_Master(models.Model):
    user_id = models.ForeignKey(SiteUser, on_delete=models.CASCADE,null=True,blank=True)
    expense_type_master = models.CharField(max_length=250,null=True,blank=True)
    expense_type_sub_master = models.CharField(max_length=250,null=True,blank=True)
    notes = models.CharField(max_length=300,null=True,blank=True)
    log_entered_by = models.CharField(blank= True, null=True, max_length=100)

class Expense_Type_Sub_Sub_Master(models.Model):
    user_id = models.ForeignKey(SiteUser, on_delete=models.CASCADE,null=True,blank=True)
    expense_type_sub_master_id = models.ForeignKey(Expense_Type_Sub_Master,on_delete=models.SET_NULL,null=True,blank=True)
    expense_type_sub_sub_master = models.CharField(max_length=250,null=True,blank=True)
    notes = models.CharField(max_length=300,null=True,blank=True)
    log_entered_by = models.CharField(blank= True, null=True, max_length=100)

class Vendor(models.Model):
    user_id = models.ForeignKey(SiteUser, on_delete=models.CASCADE,null=True,blank=True)
    expense_type_sub_sub_master_id = models.ForeignKey(Expense_Type_Sub_Sub_Master,on_delete=models.CASCADE,null=True,blank=True)

    name = models.CharField(max_length=250,null=True,blank=True)
    phone_no = models.CharField(max_length=250,null=True,blank=True)
    company_name = models.CharField(max_length=250,null=True,blank=True)
    detailed_address = models.CharField(max_length=250,null=True,blank=True)
    email_id = models.CharField(max_length=250,null=True,blank=True)
    gst_no = models.CharField(max_length=250,null=True,blank=True)

    hsn_code = models.CharField(max_length=250,null=True,blank=True)
    sgst_per = models.CharField(max_length=250,null=True,blank=True)
    cgst_per = models.CharField(max_length=250,null=True,blank=True)
    igst_per = models.CharField(max_length=250,null=True,blank=True)
    tds_per = models.CharField(max_length=250,null=True,blank=True)
    notes = models.CharField(max_length=250,null=True,blank=True)
    log_entered_by = models.CharField(blank= True, null=True, max_length=100)

class Expense(models.Model):
    user_id = models.ForeignKey(SiteUser, on_delete=models.CASCADE,null=True,blank=True)
    expense_type_sub_sub_master_id = models.ForeignKey(Expense_Type_Sub_Sub_Master,on_delete=models.CASCADE,null=True,blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE,null=True,blank=True)
    # name = models.CharField(max_length=250,null=True,blank=True)
    notes = models.CharField(max_length=250,null=True,blank=True)
    our_company_name = models.CharField(max_length=250,null=True,blank=True)
    import datetime
    
    bill_no = models.CharField(max_length=250,null=True,blank=True)
    bill_date = models.DateField(default=datetime.date.today)
    total_basic_amount = models.CharField(max_length=250,null=True,blank=True)
    pf = models.CharField(max_length=250,null=True,blank=True)
    gst = models.BooleanField(default=False)

    sgst_per = models.CharField(max_length=250,null=True,blank=True)
    cgst_per = models.CharField(max_length=250,null=True,blank=True)
    igst_per = models.CharField(max_length=250,null=True,blank=True)
    tds_per = models.CharField(max_length=250,null=True,blank=True)
    discount_per = models.CharField(max_length=250,null=True,blank=True)

    sgst_amt = models.CharField(max_length=250,null=True,blank=True)
    cgst_amt = models.CharField(max_length=250,null=True,blank=True)
    igst_amt = models.CharField(max_length=250,null=True,blank=True)
    tds_amt = models.CharField(max_length=250,null=True,blank=True)
    discount_amt = models.CharField(max_length=250,null=True,blank=True)    

    total_amount = models.CharField(max_length=250,null=True,blank=True)    
    gst_no = models.CharField(max_length=250,null=True,blank=True)    

    date_of_payment = models.DateField(default=datetime.date.today)
    name_of_payee = models.CharField(max_length=250,null=True,blank=True)    
    po_issued = models.FileField(null=True,blank=True)    
    bill_copy = models.FileField(null=True,blank=True)    
    voucher_no = models.CharField(max_length=250,null=True,blank=True)   

    payment_type = models.CharField(max_length=250,null=True,blank=True)    
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
    log_entered_by = models.CharField(blank= True, null=True, max_length=100)
    entry_date = models.DateField(default=datetime.date.today)

class Expense_Product(models.Model):
    user_id = models.ForeignKey(SiteUser, on_delete=models.CASCADE,null=True,blank=True)
    expense_id = models.ForeignKey(Expense, on_delete=models.CASCADE,null=True,blank=True)
    godown_id = models.ForeignKey(Godown, on_delete=models.CASCADE,null=True,blank=True)

    expense_type = models.CharField(max_length=50,null=True,blank=True)
    type_of_scale = models.CharField(max_length=50,null=True,blank=True)
    model_of_purchase = models.CharField(max_length=50,null=True,blank=True)
    sub_model = models.CharField(max_length=60,null=True,blank=True)
    sub_sub_model = models.CharField(max_length=50,null=True,blank=True)
    serial_no = models.CharField(max_length=50,null=True,blank=True)
    brand = models.CharField(max_length=50,null=True,blank=True)
    capacity = models.CharField(max_length=50,null=True,blank=True)
    unit = models.CharField(max_length=50,null=True,blank=True)
    amount = models.FloatField(default=0.0,)
    quantity = models.CharField(max_length=30,null=True,blank=True)
    rate = models.CharField(max_length=30,null=True,blank=True)

    log_entered_by = models.CharField(blank= True, null=True, max_length=100)
    entry_date = models.DateField(default=datetime.date.today)