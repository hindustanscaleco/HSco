import datetime
from django.dispatch import receiver
from django.db import models
from django.db.models import Sum, F
from django.db.models.signals import post_save
from django.utils import timezone
from customer_app.models import Customer_Details, DynamicDropdown
from user_app.models import SiteUser
from model_utils import FieldTracker
from simple_history.models import HistoricalRecords
# from stock_management_system_app.models import Product  # Import the Product model


choices = (('NO', 'NO'),
           ('YES', 'YES'),)


class Purchase_Details(models.Model):  # cleaned
    user_id = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    manager_id = models.CharField(max_length=150, null=True, blank=True)
    crm_no = models.ForeignKey(
        Customer_Details, on_delete=models.CASCADE, null=True, blank=True)
    date_of_purchase = models.DateField(
        default=datetime.date.today, null=True, blank=True)
    bill_no = models.CharField(max_length=150, null=True, blank=True)
    bill_address = models.CharField(max_length=150, null=True, blank=True)
    shipping_address = models.CharField(max_length=150, null=True, blank=True)
    second_person = models.CharField(max_length=150, null=True, blank=True)
    second_company_name = models.CharField(
        max_length=150, null=True, blank=True)
    company_email = models.CharField(max_length=150, null=True, blank=True)
    company_address = models.CharField(max_length=250, null=True, blank=True)
    second_contact_no = models.CharField(max_length=150, null=True, blank=True)
    third_contact_no = models.CharField(max_length=150, null=True, blank=True)
    upload_op_file = models.FileField(upload_to='', null=True, blank=True)
    po_number = models.CharField(max_length=150, null=True, blank=True)
    # old fields
    channel_of_sales = models.CharField(max_length=150, null=True, blank=True)
    channel_of_marketing = models.CharField(
        max_length=150, null=True, blank=True)
    industry = models.CharField(max_length=150, null=True, blank=True)
    channel_of_dispatch = models.CharField(
        max_length=150, null=True, blank=True)
    # new fields
    channel_of_sales_id = models.ForeignKey(
        DynamicDropdown, on_delete=models.CASCADE, related_name='channel_sales', null=True, blank=True)
    channel_of_marketing_id = models.ForeignKey(
        DynamicDropdown, on_delete=models.CASCADE, related_name='channel_marketing', null=True, blank=True)
    industry_id = models.ForeignKey(
        DynamicDropdown, on_delete=models.CASCADE, related_name='industry', null=True, blank=True)
    channel_of_dispatch_id = models.ForeignKey(
        DynamicDropdown, on_delete=models.CASCADE, related_name='channel_dispatch', null=True, blank=True)

    value_of_goods = models.DecimalField(
        default=0.0, null=True, blank=True, decimal_places=2, max_digits=65)
    notes = models.CharField(max_length=300, null=True, blank=True)
    feedback_form_filled = models.BooleanField(default=False)
    sales_person = models.CharField(max_length=150, null=True, blank=True)
    new_repeat_purchase = models.CharField(
        max_length=150, null=True, blank=True)
    # remaining make forenkey of this with Dispatch module
    dispatch_id_assigned = models.ForeignKey(
        'dispatch_app.Dispatch', on_delete=models.CASCADE, null=True, blank=True)
    entry_timedate = models.DateField(default=datetime.date.today)
    feedback_stars = models.DecimalField(
        default=0.0, decimal_places=2, max_digits=65)
    is_last_product = models.BooleanField(default=False)
    feedback_link = models.URLField(max_length=200, null=True, blank=True)
    purchase_no = models.BigIntegerField(null=True, blank=True)
    log_entered_by = models.CharField(blank=True, null=True, max_length=100)
    tracker = FieldTracker()
    is_quick_entry = models.BooleanField(default=False)

    payment_mode = models.CharField(max_length=150, null=True, blank=True)
    # cheque details
    bank_name = models.CharField(max_length=150, null=True, blank=True)
    cheque_no = models.TextField(null=True, blank=True)
    cheque_date = models.DateField(default=datetime.date.today)

    # neft details
    neft_bank_name = models.CharField(max_length=150, null=True, blank=True)
    neft_date = models.DateField(default=datetime.date.today)
    reference_no = models.CharField(max_length=150, null=True, blank=True)

    # credit details
    credit_pending_amount = models.DecimalField(
        default=0.0, null=True, blank=True, decimal_places=2, max_digits=65)
    credit_authorised_by = models.CharField(
        max_length=250, null=True, blank=True)

    tax_amount = models.DecimalField(
        default=0.0, decimal_places=2, max_digits=65)
    round_off_total = models.DecimalField(
        default=0.0, decimal_places=2, max_digits=65)
    total_amount = models.DecimalField(
        default=0.0, decimal_places=2, max_digits=65)
    total_pf = models.DecimalField(
        default=0.0, decimal_places=2, max_digits=65)
    is_gst = models.BooleanField(default=False)

    cgst = models.DecimalField(default=0.0, decimal_places=2, max_digits=65)
    sgst = models.DecimalField(default=0.0, decimal_places=2, max_digits=65)
    igst = models.DecimalField(default=0.0, decimal_places=2, max_digits=65)

    bill_notes = models.TextField(null=True, blank=True)

    history = HistoricalRecords()

    def __int__(self):
        return self.id

    @property
    def grand_total(self):
        if self.tax_amount != None and self.total_amount != None and self.total_pf != None:
            return self.tax_amount+self.total_amount+self.total_pf
        elif self.total_amount != None and self.total_pf != None:
            return self.total_amount + self.total_pf
        else:
            return 0.0

    # @staticmethod
    @receiver(post_save, sender='purchase_app.Purchase_Details')
    def update_customer_details_on_purchase_update(sender, instance, **kwargs):
        customer = instance.crm_no
        if customer:
            # Update the customer details based on the purchase details
            customer.customer_name = instance.second_person
            customer.company_name = instance.second_company_name
            customer.address = instance.company_address
            customer.customer_email_id = instance.company_email
            customer.contact_no = instance.second_contact_no
            customer.customer_industry = instance.industry_id.name if instance.industry_id else None
            customer.channel_of_marketing = instance.channel_of_marketing_id.name if instance.channel_of_marketing_id else None
            customer.channel_of_sales = instance.channel_of_sales_id.name if instance.channel_of_sales_id else None
            customer.channel_of_dispatch = instance.channel_of_dispatch_id.name if instance.channel_of_dispatch_id else None
            customer.notes = instance.notes
            customer.bill_address = instance.bill_address
            customer.shipping_address = instance.shipping_address
            customer.bill_notes = instance.bill_notes
            # for future
            # customer.city = instance.city
            # customer.state = instance.state
            # customer.pincode = instance.pincode
            # customer.save()
            customer.save(update_fields=[
                'customer_name', 'company_name', 'address', 'customer_email_id',
                'contact_no', 'customer_industry', 'channel_of_marketing',
                'channel_of_sales', 'channel_of_dispatch', 'notes',
                'bill_address', 'shipping_address', 'bill_notes'
            ])


# def save_purchase_details(sender,instance, **kwargs):
#
# post_save.connect(save_purchase_details, sender = Purchase_Details)

class Product_Details(models.Model):
    user_id = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    godown_id = models.ForeignKey(
        'stock_management_system_app.Godown', on_delete=models.CASCADE, null=True, blank=True)
    manager_id = models.CharField(max_length=60, null=True, blank=True)
    purchase_id = models.ForeignKey(
        Purchase_Details, on_delete=models.CASCADE, null=True, blank=True, related_name='product_details')
    product_dispatch_id = models.ForeignKey(
        'dispatch_app.Product_Details_Dispatch', on_delete=models.CASCADE, null=True, blank=True)
    # product = models.ForeignKey(
    #     Product, on_delete=models.CASCADE, null=True, blank=True
    # )
    # product_name = models.CharField(max_length=30,null=True,blank=True)
    quantity = models.CharField(max_length=30, null=True, blank=True)
    type_of_scale = models.CharField(max_length=30, null=True, blank=True)
    model_of_purchase = models.CharField(max_length=30, null=True, blank=True)
    sub_model = models.CharField(max_length=60, null=True, blank=True)
    sub_sub_model = models.CharField(max_length=30, null=True, blank=True)
    serial_no_scale = models.CharField(max_length=30, null=True, blank=True)
    brand = models.CharField(max_length=30, null=True, blank=True)
    capacity = models.CharField(max_length=30, null=True, blank=True)
    unit = models.CharField(max_length=30, null=True, blank=True)
    amount = models.DecimalField(default=0.0, decimal_places=2, max_digits=65)
    log_entered_by = models.CharField(blank=True, null=True, max_length=100)

    entry_timedate = models.DateTimeField(default=timezone.now,)
    tracker = FieldTracker()

    history = HistoricalRecords()

    def __int__(self):
        return self.purchase_id

    @property
    def product_id(self):
        from stock_management_system_app.models import Product
        if self.godown_id:
            attributes = {
                'scale_type__name': self.type_of_scale,
                'main_category__name': self.model_of_purchase,
                'sub_category__name': self.sub_model,
                'sub_sub_category__name': self.sub_sub_model,
            }
            # print('attributes -->', attributes)
            for i in range(4, 0, -1):
                subset_attributes = {key: attributes[key]
                                     for key in list(attributes.keys())[:i]}

                try:
                    products = Product.objects.filter(**subset_attributes)

                    if products.count() == 1:
                        return Product.objects.get(**subset_attributes).id
                    else:
                        subset_attributes['sub_category__name'] = self.sub_sub_model or self.sub_model
                        product = Product.objects.filter(
                            **subset_attributes).first()
                        print(product)
                        return product.id
                    # print('subset_attributes-->', subset_attributes)
                    # product = Product.objects.get(**subset_attributes)
                    # print('product --->', product)
                    # return product.id
                except Product.DoesNotExist:
                    pass
        return None
        # try:
        #     product = Product.objects.get(
        #         scale_type__name=self.type_of_scale,
        #         main_category__name=self.model_of_purchase,
        #         sub_category__name=self.sub_model,
        #         sub_sub_category__name=self.sub_sub_model
        #     )
        #     return product.id
        # except Product.DoesNotExist:
        #     print(f"Product not found with the following attributes:")
        #     print(f"scale_type: {self.type_of_scale}")
        #     print(f"main_category: {self.model_of_purchase}")
        #     print(f"sub_category: {self.sub_model}")
        #     print(f"sub_sub_category: {self.sub_sub_model}")
        #     return None

    @property
    def cost_price(self):
        from stock_management_system_app.models import Product
        if self.godown_id:
            try:
                # print('prodcut id --->', self.product_id)
                product = Product.objects.get(id=self.product_id)

                cost_price = product.cost_price
                # Check if cost_price is a valid numeric value
                if isinstance(cost_price, (int, float)):
                    return cost_price
                else:
                    return 0.0
                # return godown_product.product_id.cost_price
            except Product.DoesNotExist:
                return 0.0
        return 0.0


class Feedback(models.Model):
    user_id = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
    customer_id = models.ForeignKey(Customer_Details, on_delete=models.CASCADE)
    purchase_id = models.ForeignKey(Purchase_Details, on_delete=models.CASCADE)
    knowledge_of_person = models.DecimalField(
        default=0.0, null=True, blank=True, decimal_places=1, max_digits=18)
    timeliness_of_person = models.DecimalField(
        default=0.0, null=True, blank=True, decimal_places=1, max_digits=18)
    price_of_product = models.DecimalField(
        default=0.0, null=True, blank=True, decimal_places=1, max_digits=18)
    overall_interaction = models.DecimalField(
        default=0.0, null=True, blank=True, decimal_places=1, max_digits=18)
    about_hsco = models.CharField(max_length=60, null=True, blank=True)
    any_suggestion = models.CharField(max_length=120, null=True, blank=True)
    entry_timedate = models.DateTimeField(default=timezone.now,)

    history = HistoricalRecords()

    class Meta:
        unique_together = ('user_id', 'customer_id', 'purchase_id',)


@receiver(post_save, sender=Product_Details)
def update_purchase_details(sender, instance, **kwargs):
    purchase = instance.purchase_id

    if (purchase.value_of_goods in [None, 'None'] and purchase.total_amount in [None, 'None']):
        pro_sum = Product_Details.objects.filter(
            purchase_id=purchase.id).aggregate(Sum('amount'))
        total_value = sum(
            filter(None, [pro_sum['amount__sum'], purchase.total_pf, purchase.tax_amount]))

        Purchase_Details.objects.filter(id=purchase.id).update(
            total_amount=total_value,
            value_of_goods=pro_sum['amount__sum']
        )

    elif purchase.total_amount in [0, None, 'None']:
        try:
            Purchase_Details.objects.filter(id=purchase.id).update(
                total_amount=F("value_of_goods"))
        except:
            pass
