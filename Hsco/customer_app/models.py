import datetime
import uuid
from django.db import models
from django.dispatch import receiver
from django.utils import timezone
from django.db.models.signals import post_save

dropdown_choices = (('CHANNEL OF MARKETING', 'CHANNEL OF MARKETING'),
                    ('CHANNEL OF SALES', 'CHANNEL OF SALES'),
                    ('INDUSTRY', 'INDUSTRY'),
                    ('CHANNEL OF DISPATCH', 'CHANNEL OF DISPATCH'),)


class DynamicDropdown(models.Model):
    name = models.CharField(max_length=90)
    type = models.CharField(max_length=20, choices=dropdown_choices)
    is_enabled = models.BooleanField(default=True)
    entry_timedate = models.DateTimeField(default=timezone.now, )

    def __str__(self):
        return self.name


class Customer_Details(models.Model):
    # crn_number = models.UUIDField(unique=True, default=uuid.uuid4)
    # crn_number = models.BigIntegerField(unique=True, null=True, blank=True)
    customer_name = models.CharField(max_length=150,)
    company_name = models.CharField(max_length=150, null=True, blank=True)
    address = models.CharField(max_length=250, null=True, blank=True)
    contact_no = models.CharField(max_length=30,)
    customer_email_id = models.EmailField(max_length=80, null=True, blank=True)
    customer_gst_no = models.CharField(max_length=15, null=True, blank=True)
    customer_industry = models.CharField(max_length=80, null=True, blank=True)
    channel_of_marketing = models.CharField(
        max_length=100, null=True, blank=True)
    channel_of_sales = models.CharField(max_length=100, null=True, blank=True)
    channel_of_dispatch = models.CharField(
        max_length=100, null=True, blank=True)
    # entry_timedate = models.DateTimeField(default=timezone.now, )
    entry_timedate = models.DateField(default=datetime.date.today)
    latitude = models.DecimalField(
        max_digits=22, decimal_places=15, null=True, blank=True)
    longitude = models.DecimalField(
        max_digits=22, decimal_places=15, null=True, blank=True)
    api_cal_count = models.FloatField(default=0.0, null=True, blank=True)

    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    pincode = models.CharField(max_length=10, null=True, blank=True)
    new_repeat_purchase = models.CharField(
        max_length=10, null=True, blank=True)  # New or Repeat

    # this field is not in use
    industry = models.CharField(max_length=80, null=True, blank=True)

    notes = models.CharField(max_length=150, null=True, blank=True)
    bill_address = models.TextField(null=True, blank=True)
    shipping_address = models.TextField(null=True, blank=True)
    bill_notes = models.TextField(null=True, blank=True)
    # Notes field in the Sales Module
    marketing_whatsapp = models.BooleanField(default=True)
    lead_whatsapp = models.BooleanField(default=True)
    sales_whatsapp = models.BooleanField(default=True)
    repairing_whatsapp = models.BooleanField(default=True)

    class Meta:
        unique_together = ('customer_name', 'contact_no', 'customer_gst_no')
        ordering = ['-entry_timedate']

    def __int__(self):
        return self.id

    def short_address(self):
        address = str(self.address)
        return address

    @property
    def customer_exists(self):
        from purchase_app.models import Purchase_Details

        if Purchase_Details.objects.filter(crm_no=self).exists():
            return True
        else:
            return False

    # @staticmethod
    # @receiver(post_save, sender='customer_app.Customer_Details')
    def update_purchase_on_update_customer_detail(instance, **kwargs):
        from purchase_app.models import Purchase_Details
        from customer_app.models import DynamicDropdown

        # Get the corresponding DynamicDropdown instance for the customer industry
        industry_instance = DynamicDropdown.objects.filter(
            name=instance.customer_industry, type='industry', is_enabled=True
        ).first()

        channel_of_marketing_instance = DynamicDropdown.objects.filter(
            name=instance.channel_of_marketing, type='channel of marketing', is_enabled=True
        ).first()

        channel_of_sales_instance = DynamicDropdown.objects.filter(
            name=instance.channel_of_sales, type='channel of sales', is_enabled=True
        ).first()

        channel_of_dispatch_instance = DynamicDropdown.objects.filter(
            name=instance.channel_of_dispatch, type='channel of dispatch', is_enabled=True
        ).first()

        # Update Purchase_Details in bulk
        Purchase_Details.objects.filter(crm_no=instance).update(
            second_person=instance.customer_name,
            second_company_name=instance.company_name,
            company_address=instance.address,
            company_email=instance.customer_email_id,
            second_contact_no=instance.contact_no,
            notes=instance.notes,
            bill_address=instance.bill_address,
            shipping_address=instance.shipping_address,
            bill_notes=instance.bill_notes,
            industry_id=industry_instance.id if industry_instance else None,
            channel_of_marketing_id=channel_of_marketing_instance.id if channel_of_marketing_instance else None,
            channel_of_sales_id=channel_of_sales_instance.id if channel_of_sales_instance else None,
            channel_of_dispatch_id=channel_of_dispatch_instance.id if channel_of_dispatch_instance else None
        )


class Lead_Customer_Details(models.Model):
    # crn_number = models.UUIDField(unique=True, default=uuid.uuid4)
    # crn_number = models.BigIntegerField(unique=True, null=True, blank=True)
    customer_name = models.CharField(max_length=150,)
    company_name = models.CharField(max_length=150, null=True, blank=True)
    address = models.CharField(max_length=250, null=True, blank=True)
    contact_no = models.CharField(max_length=30,)
    customer_email_id = models.EmailField(max_length=80, null=True, blank=True)
    optional_email = models.TextField(default=' ')
    customer_gst_no = models.CharField(max_length=15, null=True, blank=True)
    customer_industry = models.CharField(
        max_length=80, null=True, blank=True)
    is_entered_in_purchased = models.BooleanField(default=False)
    entry_timedate = models.DateField(default=datetime.date.today)

    class Meta:
        unique_together = ('customer_name', 'contact_no')
        ordering = ['-entry_timedate']

    def __int__(self):
        return self.id

    def short_address(self):
        if self.address:
            return self.address[:18]
        else:
            return 'N/A'

    @classmethod
    def get_leads_customer_id(cls, customer_id):
        try:
            customer = Customer_Details.objects.get(id=customer_id)
            lead_customer = cls.objects.filter(
                customer_name=customer.customer_name,
                contact_no=customer.contact_no,
            )
            if lead_customer:
                return lead_customer[0].id
            else:
                return None
        except Customer_Details.DoesNotExist:
            return None


class type_purchase(models.Model):
    name = models.CharField(max_length=120)
    entry_timedate = models.DateTimeField(default=timezone.now, )

    def __str__(self):
        return self.name


class main_model(models.Model):
    name = models.CharField(max_length=120)
    type_purchase = models.ForeignKey(type_purchase, on_delete=models.CASCADE)
    entry_timedate = models.DateTimeField(default=timezone.now, )

    def __str__(self):
        return self.name


class sub_model(models.Model):
    name = models.CharField(max_length=120)
    main_model = models.ForeignKey(main_model, on_delete=models.CASCADE)
    entry_timedate = models.DateTimeField(default=timezone.now, )

    def __str__(self):
        return self.name


class sub_sub_model(models.Model):
    name = models.CharField(max_length=120)
    sub_model = models.ForeignKey(sub_model, on_delete=models.CASCADE)
    entry_timedate = models.DateTimeField(default=timezone.now, )

    def __str__(self):
        return self.name


class Log(models.Model):
    entered_by = models.CharField(max_length=120, null=True, blank=True)
    module_name = models.CharField(max_length=120, null=True, blank=True)
    action_type = models.CharField(max_length=120, null=True, blank=True)
    table_name = models.CharField(max_length=120, null=True, blank=True)
    reference = models.CharField(max_length=120, null=True, blank=True)
    action = models.CharField(null=True, blank=True, max_length=300)
    entry_timedate = models.DateTimeField(default=timezone.now, )

    class Meta:
        unique_together = ('entered_by', 'module_name',
                           'action_type', 'table_name', 'reference', 'action')

    def __int__(self):
        return self.pk
