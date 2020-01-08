from rest_framework import serializers
from customer_app.models import Customer_Details

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer_Details
        fields = 'id', 'customer_name','company_name','address','contact_no','customer_email_id'