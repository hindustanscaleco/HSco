
import os

# Print the Django settings module
print("DJANGO_SETTINGS_MODULE:", os.environ.get('DJANGO_SETTINGS_MODULE'))
import sys
import os
import os
import django



# Get the directory of the current script file
current_file_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print('current_file_dir--->',current_file_dir)
# Add the directory to sys.path
sys.path.append(current_file_dir)

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Hsco.settings')

# Initialize Django
django.setup()

# Import and use Django settings
from django.conf import settings
print(settings.INSTALLED_APPS)

from customer_app.models import DynamicDropdown
from customer_app.models import Customer_Details
from purchase_app.models import Purchase_Details

import logging
from django.db import transaction

# Setup Django environment (adjust the settings module to your project)
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')
# django.setup()


# Set up logging
logging.basicConfig(
    filename='update_customer_details.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def update_customer_details():
    try:
        with transaction.atomic():
            purchases = Purchase_Details.objects.all()

            for purchase in purchases:
                customer = purchase.crm_no
                if customer:
                    # Fetch DynamicDropdown instances based on purchase details
                    industry_instance = DynamicDropdown.objects.filter(
                        name=purchase.industry_id.name if purchase.industry_id else '',
                        type='industry',
                        is_enabled=True
                    ).first()

                    channel_of_marketing_instance = DynamicDropdown.objects.filter(
                        name=purchase.channel_of_marketing_id.name if purchase.channel_of_marketing_id else '',
                        type='channel of marketing',
                        is_enabled=True
                    ).first()

                    channel_of_sales_instance = DynamicDropdown.objects.filter(
                        name=purchase.channel_of_sales_id.name if purchase.channel_of_sales_id else '',
                        type='channel of sales',
                        is_enabled=True
                    ).first()

                    channel_of_dispatch_instance = DynamicDropdown.objects.filter(
                        name=purchase.channel_of_dispatch_id.name if purchase.channel_of_dispatch_id else '',
                        type='channel of dispatch',
                        is_enabled=True
                    ).first()

                    # Prepare update fields, only update if fields are None or empty
                    update_fields = {}
                    if not customer.customer_name:
                        update_fields['customer_name'] = purchase.second_person
                    if not customer.company_name:
                        update_fields['company_name'] = purchase.second_company_name
                    if not customer.address:
                        update_fields['address'] = purchase.company_address
                    if not customer.customer_email_id:
                        update_fields['customer_email_id'] = purchase.company_email
                    if not customer.contact_no:
                        update_fields['contact_no'] = purchase.second_contact_no
                    if not customer.customer_industry:
                        update_fields['customer_industry'] = industry_instance.name if industry_instance else None
                    if not customer.channel_of_marketing:
                        update_fields['channel_of_marketing'] = channel_of_marketing_instance.name if channel_of_marketing_instance else None
                    if not customer.channel_of_sales:
                        update_fields['channel_of_sales'] = channel_of_sales_instance.name if channel_of_sales_instance else None
                    if not customer.channel_of_dispatch:
                        update_fields['channel_of_dispatch'] = channel_of_dispatch_instance.name if channel_of_dispatch_instance else None
                    if not customer.notes:
                        update_fields['notes'] = purchase.notes
                    if not customer.bill_address:
                        update_fields['bill_address'] = purchase.bill_address
                    if not customer.shipping_address:
                        update_fields['shipping_address'] = purchase.shipping_address
                    if not customer.bill_notes:
                        update_fields['bill_notes'] = purchase.bill_notes

                    # Update the Customer_Details instance if there are fields to update
                    if update_fields:
                        Customer_Details.objects.filter(
                            pk=customer.pk).update(**update_fields)
                        logging.info(
                            f"Updated customer {customer.id} from purchase {purchase.id}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise

    logging.info(
        "Successfully updated Customer_Details from Purchase_Details where applicable.")


if __name__ == "__main__":
    update_customer_details()
