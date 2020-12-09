from django.db import models
from user_app.models import SiteUser
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

class Expense_Type_Sub_Sub_Master(models.Model):
    user_id = models.ForeignKey(SiteUser, on_delete=models.CASCADE,null=True,blank=True)
    expense_type_sub_master_id = models.ForeignKey(Expense_Type_Sub_Master,on_delete=models.CASCADE,null=True,blank=True)
    expense_type_sub_sub_master = models.CharField(max_length=250,null=True,blank=True)
    notes = models.CharField(max_length=300,null=True,blank=True)
    
class Vendor(models.Model):
    user_id = models.ForeignKey(SiteUser, on_delete=models.CASCADE,null=True,blank=True)
    expense_type_sub_sub_master_id = models.ForeignKey(Expense_Type_Sub_Sub_Master,on_delete=models.CASCADE,null=True,blank=True)

    name = models.CharField(max_length=250,null=True,blank=True)
    phone_no = models.CharField(max_length=250,null=True,blank=True)
    total_basic_amount = models.CharField(max_length=250,null=True,blank=True)
    pf = models.CharField(max_length=250,null=True,blank=True)
    gst = models.BooleanField(default=False)

    sgst_per = models.CharField(max_length=250,null=True,blank=True)
    sgst_amt = models.CharField(max_length=250,null=True,blank=True)
    cgst_per = models.CharField(max_length=250,null=True,blank=True)
    cgst_amt = models.CharField(max_length=250,null=True,blank=True)
    igst_per = models.CharField(max_length=250,null=True,blank=True)
    igst_amt = models.CharField(max_length=250,null=True,blank=True)
    discount_per = models.CharField(max_length=250,null=True,blank=True)
    discount_amt = models.CharField(max_length=250,null=True,blank=True)
    gst_no = models.CharField(max_length=250,null=True,blank=True)
    date_of_payment = models.DateField(default=datetime.date.today)
    gst_no = models.CharField(max_length=250,null=True,blank=True)
    name_of_payee = models.CharField(max_length=250,null=True,blank=True)
    po_issued = models.FileField(null=True,blank=True)
    bill_copy = models.FileField(null=True,blank=True)
    voucher_no = models.CharField(max_length=250,null=True,blank=True)
    payment_type = models.CharField(max_length=250,null=True,blank=True)


