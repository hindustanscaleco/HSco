import datetime

from django.db import models
from django.utils import timezone
choices = (('YES', 'YES'),
    ('NO', 'NO'),)

choices2 = (('Mechanical', 'Mechanical'),
            ('Digital', 'Digital'))

choices3 = (('Table Top', 'Table Top'),
            ('Platform Scale', 'Platform Scale'),
            ('POS Scales', 'POS Scales'),
            ('Water Proof Scales', 'Water Proof Scales'),
            ('Jewellery Scales', 'Jewellery Scales'),
            ('Lab Scales', 'Lab Scales'),
            ('Crane Scales', 'Crane Scales'),
            ('Platform Scales', 'Platform Scales'),
            ('Mobile Platforms', 'Mobile Platforms'),
            ('Infant Scales', 'Infant Scales'),
            ('Baby Cum Adult Scales', 'Baby Cum Adult Scales'),
            ('Animal Scales', 'Animal Scales'),
            ('Cattle Scales', 'Cattle Scales'),
            ('Supra Pall Scales', 'Supra Pall Scales'),
            )


choices4 = (('Scale not turning On', 'Scale not turning On'),
            ('Scale is showing incorrect weight', 'Scale is showing incorrect weight'),
            ('Scale only shows 888888','Scale only shows 888888'),
            ('Scale only shows zero', 'Scale only shows zero'),
            ('Weight is slowly increasing or','Weight is slowly increasing or'),
            ('decreasing', 'decreasing'),
            ('buttons are not working','buttons are not working'),
            ('Scale doesnt show stable weight','Scale doesnt show stable weight'),
            ('Display problems (Display gets distorted while showing weight)', 'Display problems (Display gets distorted while showing weight)'),
            ('Scale is not working on battery or scale is not charging', 'Scale is not working on battery or scale is not charging'),
            ('Scale turns OFF automatically','Scale turns OFF automatically'),
            ('Others','Others'),
            )
choices5 = (('Display', 'Display'),
           ('Touch Pad', 'Touch Pad'),
           ('LED', 'LED'),
           ('Transformer', 'Transformer'),
           ('Battery', 'Battery'),
           ('Switch', 'Switch'),
           ('Main Cord wire', 'Main Cord wire'),
           ('Main Circuit Board', 'Main Circuit Board'),
           ('SMPS', 'SMPS'),
           ('Load Cell', 'Load Cell'),
           ('Misc', 'Misc'),
           )

class Repairing_after_sales_service(models.Model):
    repairingnumber = models.CharField(max_length=40,null=True,blank=True) #combination of pk and 'rep'
    customer_no = models.CharField(max_length=13,null=True,blank=True)
    previous_repairing_number = models.CharField(max_length=30,null=True,blank=True)
    in_warranty = models.CharField(choices=choices,default='NO',max_length=30,null=True,blank=True)
    date_of_purchase = models.DateField(default=datetime.date.today())
    today_date = models.DateField(default=datetime.date.today())
    name = models.CharField(max_length=60,null=True,blank=True)
    company_name = models.CharField(max_length=80,null=True,blank=True)
    phone_no = models.CharField(max_length=13,null=True,blank=True)
    customer_email_id = models.EmailField(max_length=255, unique=True,null=True,blank=True)
    location = models.CharField(max_length=255,null=True,blank=True)
    products_to_be_repaired = models.CharField(max_length=30,null=True,blank=True)
    type_of_machine = models.CharField(max_length=30,null=True,blank=True, choices=choices2)
    model = models.CharField(max_length=30,null=True,blank=True, choices=choices3)
    sub_model = models.CharField(max_length=30,null=True,blank=True)
    problem_in_scale = models.CharField(max_length=255,null=True,blank=True,choices=choices4)
    components_replaced_in_warranty = models.CharField(max_length=255,null=True,blank=True,choices=choices5)
    components_replaced = models.CharField(max_length=255,null=True,blank=True,choices=choices5)
    replaced_scale_given = models.CharField(choices=choices,default='NO',max_length=30,null=True,blank=True)
    Replaced_scale_serial_no = models.CharField(max_length=60,null=True,blank=True)
    deposite_taken_for_replaced_scale = models.CharField(max_length=60,null=True,blank=True)
    cost = models.FloatField(default=0.00)
    total_cost = models.FloatField(default=0.00)
    informed_on = models.CharField(max_length=60,null=True,blank=True)
    informed_by = models.CharField(max_length=60,null=True,blank=True)
    confirmed_estimate = models.CharField(choices=choices,default='NO',max_length=30,null=True,blank=True)
    repaired = models.CharField(choices=choices,default='NO',max_length=30,null=True,blank=True)
    repaired_date = models.DateField(default=datetime.date.today())
    delivery_date = models.DateField(default=datetime.date.today())
    delivery_by = models.CharField(max_length=50,null=True,blank=True)
    feedback_given = models.CharField(max_length=255,null=True,blank=True)



    def __str__(self):
        return self.customer_no




