from django.shortcuts import render, redirect


from .models import Customer_Details


def add_customer_details(request):
    if request.method == 'POST' or request.method=='FILES':
        customer_name = request.POST.get('customer_name')
        company_name = request.POST.get('company_name')
        address = request.POST.get('address')
        contact_no = request.POST.get('contact_no')
        customer_email_id = request.POST.get('customer_email_id')

        item = Customer_Details()

        item.customer_name = customer_name
        item.company_name = company_name
        item.date = address
        item.company_name = company_name
        item.address = address
        item.contact_no = contact_no
        item.customer_email_id = customer_email_id
        item.date_of_purchase = date_of_purchase
        item.product_purchase_date = product_purchase_date
        item.bill_no = bill_no
        item.upload_op_file = upload_op_file
        item.photo_lr_no = photo_lr_no
        item.po_number = po_number
        item.channel_of_sales = channel_of_sales
        item.industry = industry
        item.value_of_goods = value_of_goods
        item.channel_of_dispatch = channel_of_dispatch
        item.notes = notes
        item.feedback_form_filled = feedback_form_filled
        item.save()





        dispatch = Dispatch()


        dispatch.customer_no = item.pk
        dispatch.customer_email = customer_email_id
        dispatch.customer_name = customer_name
        dispatch.company_name = company_name
        dispatch.customer_address = address

        dispatch.save()


        dispatch2 = Dispatch.objects.get(id=dispatch.pk)
        dispatch2.dispatch_id = str(dispatch.pk + 00000)
        dispatch2.save(update_fields=['dispatch_id'])

        customer_id = Customer_Details.objects.get(id=item.pk)
        customer_id.dispatch_id_assigned = Dispatch.objects.get(id=dispatch.pk) #str(dispatch.pk + 00000)
        customer_id.save(update_fields=['dispatch_id_assigned'])

        send_mail('Feedback Form','Click on the link to give feedback' , settings.EMAIL_HOST_USER, [customer_email_id])

        message = 'txt'


        # url = "http://smshorizon.co.in/api/sendsms.php?user="+settings.user+"&apikey="+settings.api+"&mobile="+contact_no+"&message="+message+"&senderid="+settings.senderid+"&type=txt"
        # payload = ""
        # headers = {'content-type': 'application/x-www-form-urlencoded'}
        #
        # response = requests.request("GET", url, data=json.dumps(payload), headers=headers)
        # x = response.text


        item.save()

    return render(request,'forms/cust_mod_form.html',)


