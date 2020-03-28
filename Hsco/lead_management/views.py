from datetime import datetime

from django.db import connection
from django.db.models import Sum

from django.core.files.base import ContentFile
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render, redirect

from customer_app.models import type_purchase

from stock_system.models import Product

from Hsco import settings
from user_app.models import SiteUser

from .forms import Deal_detailForm, Customer_detailForm, Pi_sectionForm, Follow_up_sectionForm, History_followupForm, Payment_detailsForm

from .form2 import Customer_detail_disabledForm
from customer_app.models import Customer_Details
from .models import Lead, Pi_section, IndiamartLeadDetails, History_followup, Follow_up_section, Followup_product

from .models import Lead, Pi_section, Pi_product, Pi_History
from customer_app.models import sub_model, main_model, sub_sub_model
import requests
import json

# Create your views here.
from .utils import send_html_mail


def lead_home(request):
    import requests
    import json

    mobile = '7045922250'
    api = 'MTU4MzQ5OTg1NS42MTU2IzI5OTI4NzM='
    last_date = IndiamartLeadDetails.objects.latest('to_date').to_date.strftime('%d-%b-%Y')
    from_date = last_date
    from datetime import datetime
    to_date = datetime.today().strftime('%d-%b-%Y')
    lead_count=0
    error2 = None
    error = None
    error_exist = False

    if request.method == 'POST':

        url = "https://mapi.indiamart.com/wservce/enquiry/listing/GLUSR_MOBILE/" + mobile + "/GLUSR_MOBILE_KEY/" + api + "/Start_Time/" + from_date + "/End_Time/" + to_date + "/"
        response = requests.get(url=url).json()
        lead_count = len(response)

        from_date =  request.POST.get('from_date_form')
        to_date =  request.POST.get('to_date_form')
        import time
        conv = time.strptime(from_date, "%d-%b-%Y")
        conv2 = time.strptime(to_date, "%d-%b-%Y")


        if(lead_count>1):
            for item in response:

                item3 = Customer_Details()
                item3.customer_name= item['SENDERNAME']
                item3.company_name = item['GLUSR_USR_COMPANYNAME']
                item3.address = item['ENQ_ADDRESS']
                item3.customer_email_id = item['SENDEREMAIL']
                item3.contact_no = item['MOB']
                item3.customer_industry = ''
                try:
                    item3.save()
                    item2 = Lead()
                    item2.customer_id = Customer_Details.objects.get(id=item3.pk)
                    item2.current_stage = 'Not Yet Initiated'
                    item2.new_existing_customer = 'New'
                    item2.date_of_initiation = time.strftime("%Y-%m-%d", conv2)
                    item2.channel = 'Indiamart'

                    item2.requirement = item['SUBJECT'] + item['ENQ_MESSAGE'] + item['PRODUCT_NAME']
                    try:
                        item2.save()
                    except Exception as e:
                        error_exist = True
                        error2 = e
                except Exception as e:
                    error_exist = True
                    error = e

            obj = IndiamartLeadDetails()
            obj.from_date = time.strftime("%Y-%m-%d", conv)
            obj.to_date = time.strftime("%Y-%m-%d", conv2)
            obj.lead_count = lead_count
            try:
                obj.save()
            except:
                print("error")
        else:
            row_count = response[0]
            if(row_count!=None):
                error = row_count['Error_Message']
                error_exist = True




    lead_list = Lead.objects.all()
    cust_sugg = Customer_Details.objects.all()
    if Lead.objects.all().count() == 0:
        latest_lead_id = 1
    else:
        latest_lead_id = Lead.objects.latest('id').id + 1
    context={
        'lead_list':lead_list,
        'latest_lead_id':latest_lead_id,

        'lead_count':lead_count,
        'from_date':from_date,
        'to_date':to_date,
        'error':error,
        'error2':error2,
        'error_exist':error_exist,


        'cust_sugg':cust_sugg,

    }
    return render(request,'lead_management/lead_home.html',context)



def add_lead(request):
    if Lead.objects.all().count() == 0:
        latest_lead_id = 1
    else:
        latest_lead_id = Lead.objects.latest('id').id

    cust_sugg = Customer_Details.objects.all()
    form = Customer_detailForm()
    form2 = Deal_detailForm()
    if request.method == 'POST' or request.method=='FILES':
        customer_name = request.POST.get('customer_name')
        company_name = request.POST.get('company_name')
        address = request.POST.get('address')
        contact_no = request.POST.get('contact_no')
        customer_industry = request.POST.get('customer_email_id')
        customer_email_id = request.POST.get('customer_email_id')
        customer_gst_no = request.POST.get('customer_gst_no')

        current_stage = request.POST.get('current_stage')
        new_existing_customer = request.POST.get('new_existing_customer')
        date_of_initiation = request.POST.get('date_of_initiation')
        channel = request.POST.get('channel')
        requirement = request.POST.get('requirement')
        upload_requirement_file = request.FILES.get('upload_requirement_file')
        owner_of_opportunity = request.POST.get('owner_of_opportunity')



        item2 = Lead()
        if Customer_Details.objects.filter(customer_name=customer_name,
                                           contact_no=contact_no).count() > 0:

            item2.customer_id = Customer_Details.objects.filter(contact_no=contact_no).first()

            item3 = Customer_Details.objects.filter(customer_name=customer_name,
                                                    contact_no=contact_no).first()
            if company_name != '' and company_name != None:
                item3.company_name = company_name
                item3.save(update_fields=['company_name'])
            if address != '' and address != None:
                item3.address = address
                item3.save(update_fields=['address'])
            if customer_email_id != '' and customer_email_id != None:
                item3.customer_email_id = customer_email_id
                item3.save(update_fields=['customer_email_id'])
            if customer_gst_no != '' and customer_gst_no != None:
                item3.customer_gst_no = customer_gst_no
                item3.save(update_fields=['customer_gst_no'])
            if customer_industry != '' and customer_industry != None:
                item3.customer_industry = customer_industry
                item3.save(update_fields=['customer_industry'])
        else:
            new_cust = Customer_Details()

            new_cust.customer_name = customer_name
            if company_name != '':
                new_cust.company_name = company_name
            if address != '':
                new_cust.address = address
            new_cust.contact_no = contact_no
            if customer_email_id != '':
                new_cust.customer_email_id = customer_email_id
            if customer_gst_no != '':
                new_cust.customer_gst_no = customer_gst_no
            if customer_industry != '':
                new_cust.customer_industry = customer_industry
            try:
                new_cust.save()
                item2.customer_id = Customer_Details.objects.get(id=new_cust.pk)
            except:
                pass


        item2.current_stage = current_stage
        item2.new_existing_customer = new_existing_customer
        item2.date_of_initiation = date_of_initiation
        item2.channel = channel
        item2.requirement = requirement
        item2.owner_of_opportunity = SiteUser.objects.filter(profile_name=owner_of_opportunity).first()
        item2.upload_requirement_file = upload_requirement_file

        item2.save()

        fp=Follow_up_section()
        fp.lead_id= Lead.objects.get(id=item2.pk)
        fp.save()
        return redirect('/update_view_lead/'+str(item2.id))
        # item.save()
    context={
        'form':form,
        'form2':form2,
        'latest_lead_id':latest_lead_id,
        'cust_sugg':cust_sugg,
    }
    return render(request, 'lead_management/add_lead.html',context)

def update_view_lead(request,id):
    lead_id = Lead.objects.get(id=id)

    lead_pi_products = Pi_product.objects.filter(lead_id=id)
    hfu = Follow_up_section.objects.filter(lead_id=id).last()

    followup_products_list = Followup_product.objects.filter(lead_id=id)

    table = ''
    table2 = ''
    total = 0.0
    try:
        for product in lead_pi_products:
            single_product_total = float(product.product_id.selling_price) * (product.quantity)
            total += single_product_total
            row = '<tr> <td>'+ str(product.quantity) +' </td><td>'+ str(product.product_id.hsn_code)+'</td><td>'+ str(product.product_id.sub_sub_category)+'</td><td><img src="'+str(product.product_id.product_image.url)+'" height="100" width="100"></td><td>'+str(product.product_id.product_desc) +'</td><td>'+str(product.product_id.selling_price) +'</td><td>'+str(single_product_total) +'</td>  </tr>'
            row2 = '<tr> <td>'+ str(product.quantity) +' </td><td>'+ str(product.product_id.hsn_code)+'</td><td>'+str(product.product_id.product_desc) +'</td><td></td><td></td>  </tr>'
            table+=row
            table2+=row2
    except:
        pass
    customer_id = Customer_Details.objects.get(id=lead_id.customer_id)
    customer_initial_data = {
        'customer_name': customer_id.customer_name,
        'company_name': customer_id.company_name,
        'contact_no': customer_id.contact_no,
        'customer_email_id': customer_id.customer_email_id,
        'address': customer_id.address,
        'customer_industry': customer_id.customer_industry,
        'customer_gst_no': customer_id.customer_gst_no,
    }
    deal_details_initial_data = {
        'current_stage': lead_id.current_stage,
        'new_existing_customer': lead_id.new_existing_customer,
        'date_of_initiation': lead_id.date_of_initiation,
        'channel': lead_id.channel,
        'requirement': lead_id.requirement,
        'upload_requirement_file': lead_id.upload_requirement_file,
        'owner_of_opportunity': lead_id.owner_of_opportunity,
    }
    form = Customer_detailForm(initial=customer_initial_data)
    form2 = Deal_detailForm(initial=deal_details_initial_data)
    form3 = Pi_sectionForm()
    form4 = Follow_up_sectionForm(initial={'email_auto_manual':hfu.auto_manual_mode,})
    form6 = History_followupForm(initial={'wa_no':hfu.whatsappno,'email_subject':hfu.email_subject})
    form5 = Payment_detailsForm()
    context = {
        'form': form,
        'form2': form2,
        'form3': form3,
        'form4': form4,
        'form5': form5,
        'lead_id': lead_id,
        'lead_pi_products': lead_pi_products,
       'followup_products_list': followup_products_list,
        'hfu':hfu.fields,
        'hfu_id':hfu.id,
        'form6':form6,
    }
    if Pi_section.objects.filter(lead_id=id).count() > 0:
        pi_id = Pi_section.objects.get(lead_id=id)
        pi_initial_data = {
            'discount': pi_id.discount,
            'upload_pi_file': pi_id.upload_pi_file,
            'call': pi_id.call,
            'payment_channel': pi_id.payment_channel,
            'payment_receipt': pi_id.payment_receipt,
            'upload_po_file': pi_id.upload_po_file,
            'payment_received_date': pi_id.payment_received_date,
            'notes': pi_id.notes,
            'select_gst_type': pi_id.select_gst_type,
            'discount_type': pi_id.discount_type,
        }
        form3 = Pi_sectionForm(initial=pi_initial_data)
        context2 = {
            'form': form,
            'form2': form2,
            'form3': form3,
            'lead_id': lead_id,
            'lead_pi_products': lead_pi_products,

        }
        context.update(context2)
    else:
        pass

    if request.method == 'POST' or request.method == 'FILES':
        if 'submit1' in request.POST:                                            #for customer and deal details section
            customer_name = request.POST.get('customer_name')
            company_name = request.POST.get('company_name')
            address = request.POST.get('address')
            contact_no = request.POST.get('contact_no')
            customer_industry = request.POST.get('customer_email_id')
            customer_email_id = request.POST.get('customer_email_id')
            customer_gst_no = request.POST.get('customer_gst_no')

            current_stage = request.POST.get('current_stage')
            new_existing_customer = request.POST.get('new_existing_customer')
            date_of_initiation = request.POST.get('date_of_initiation')
            channel = request.POST.get('channel')
            requirement = request.POST.get('requirement')
            upload_requirement_file = request.FILES.get('upload_requirement_file')
            owner_of_opportunity = request.POST.get('owner_of_opportunity')
            payment_channel = request.POST.get('payment_channel')
            payment_receipt = request.POST.get('payment_receipt')
            upload_pofile = request.POST.get('upload_pofile')
            payment_received_date = request.POST.get('payment_received_date')

            item2 = Lead.objects.get(id=id)



            item3 = Customer_Details.objects.get(id=lead_id.customer_id)

            if customer_name != '' and customer_name != None:
                item3.customer_name = customer_name
                item3.save(update_fields=['customer_name'])
            if contact_no != '' and contact_no != None:
                item3.contact_no = contact_no
                item3.save(update_fields=['contact_no'])
            if company_name != '' and company_name != None:
                item3.company_name = company_name
                item3.save(update_fields=['company_name'])
            if address != '' and address != None:
                item3.address = address
                item3.save(update_fields=['address'])
            if customer_email_id != '' and customer_email_id != None:
                item3.customer_email_id = customer_email_id
                item3.save(update_fields=['customer_email_id'])
            if customer_gst_no != '' and customer_gst_no != None:
                item3.customer_gst_no = customer_gst_no
                item3.save(update_fields=['customer_gst_no'])
            if customer_industry != '' and customer_industry != None:
                item3.customer_industry = customer_industry
                item3.save(update_fields=['customer_industry'])

            item2.current_stage = current_stage
            item2.new_existing_customer = new_existing_customer
            item2.date_of_initiation = date_of_initiation
            item2.channel = channel
            item2.requirement = requirement
            item2.upload_requirement_file = upload_requirement_file
            item2.owner_of_opportunity = SiteUser.objects.get(profile_name=owner_of_opportunity)
            item2.save(update_fields=['current_stage','new_existing_customer','date_of_initiation','channel',
                                      'requirement','upload_requirement_file','owner_of_opportunity',])
            return redirect('/update_view_lead/'+str(id))
        elif 'submit2' in request.POST:                                         #for pi section
            discount = request.POST.get('discount')
            upload_pi_file = request.FILES.get('upload_pi_file')
            select_pi_template = request.POST.get('select_pi_template')
            select_gst_type = request.POST.get('select_gst_type')
            call = request.POST.get('call')
            email = request.POST.get('email')
            whatsapp = request.POST.get('whatsapp')
            call2 = request.POST.get('call2')
            discount_type = request.POST.get('discount_type')
            if call2 == 'on':
                call2 = 'True'
            else:
                call2 = 'False'
            if email == 'on':
                email = 'True'
            else:
                email = 'False'
            if whatsapp == 'on':
                whatsapp = 'True'
            else:
                whatsapp = 'False'
            if Pi_section.objects.filter(lead_id=id).count() > 0:

                item2 = Pi_section.objects.filter(lead_id=id).first()
                item2.discount = discount
                if upload_pi_file != None  or '':
                    item2.upload_pi_file = upload_pi_file
                item2.select_pi_template = select_pi_template
                item2.call = call
                item2.email = email
                item2.whatsapp = whatsapp
                item2.call2 = call2
                item2.select_gst_type = select_gst_type
                item2.discount_type = discount_type
                # if discount_type == 'percent':
                #
                # elif discount_type == 'rupee':
                #     pass
                item2.save(update_fields=['discount', 'upload_pi_file', 'select_pi_template', 'call',
                                        'email', 'whatsapp','call2','select_gst_type','discount_type'  ])

                if request.user.is_authenticated:
                        todays_date = str(datetime.now())
                        # gst_no = str(lead_id.customer_id.customer_gst_no)
                        text_content = ''
                        subject = 'Support'
                        html_content1 = '''<html>
<head>
  <title>
    HSCO
  </title>

  <meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">

  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
  <link href='https://fonts.googleapis.com/css?family=Poppins' rel='stylesheet'>


  <style>
      * {
    font-family: 'Poppins';
    font-size: 0.99em;

  }

  table {
  border-collapse: collapse;
  width: 85%;
  font-size: 18px;
  border-color: black;
  color: black;



}


th {

  font-size: 13px;
    border: 1px solid black;
    text-align: left;
    padding:5px;

}

td {
  border: 1px solid black;
  padding: 3px;
}


 @media print and (width: 10.5cm) and (height: 14.8cm) {
    @page {
       margin: 3cm;
    }
 }


  </style>

</head>
<body>

<div  id="printableArea" style="margin-left: 10%; margin-right: 10%;">
<div class="row" style="padding: 5px; border-bottom: 5px solid black;">
    <div class="col-xl-2 col-md-2 ">
<img src="/media/pi_history_file/hsco.jpg" class="img-rounded" width="200" height="120" style="float: right;">
</div>
    <div class="col-xl-1 col-md-1 ">
    </div>
    <div class="col-xl-4 col-md-4 ">
        <center>Subject to Mumbai Jurisdiction</center><br>
        <center><h3 style="font: italic bold 22px/30px Georgia, serif;">Proforma Invoice</h3></center>
</div>
    <div class="col-xl-1 col-md-1 ">
    </div>
    <div class="col-xl-4 col-md-4 ">
        <p>Ph: 022-23423183, 7045922250/51/52<br>
Manufacture Licence No. LM/MH/H004<br>
Dealer Licence No. LD/MH/H004<br>
Repairing Licence No. LR/MH/H004</p>
</div>
</div>


        <div class="row">
         <div class="col-md-12" style="padding:10px;">
        <center><h1 style="font-weight:bold;"> Hindustan Scale Company</h1>
        </center></div>
        </div>
        <div class="row">
         <div class="col-md-12" style="padding:0px;">
        <center><p style="font-weight:bold;"> A one stop shop for all your weighing needs<br><font color="#FC6E20" style="font-weight:bold;"> AN ISO 9001: 2015 CERTIFIED COMPANY</font></p>
        </center></div>
        </div>


    <div class="row">
         <div class="col-md-12" style="padding:10px;">
        <center><p style="font-weight:bold;"> All kinds of Mechanical and Digital Weighing Scales, Weights & Measures.<br>
        186/188 Janjikar Street, Near Crawford Market, Mumbai- 400003/<font color="#FC6E20">www.hindustanscale.com/hsc@hindustanscale.com</font></p>
        </center></div>
        </div>


    <div class="row">
         <div class="col-md-2">
             <center><p style="font-weight:bold; float:left;"> Messrs</p>
        </center></div>
        <div class="col-md-5">
             </div>
        <div class="col-md-1">
             </div>
        <div class="col-md-2">
             <center><p style="font-weight:bold; float:left;"> Date :</p>
        </center></div>
        <div class="col-md-2">
             <center><p style="font-weight:bold; float:left;"> '''+todays_date+'''</p>
                            </center></div>
                            </div>
                    
                        
                            <div class="row">
                                 <div class="col-md-2">
                                     <center><p style="font-weight:bold; float:left;"> Company Name</p>
                                </center></div>
                                <div class="col-md-5">
                                     <center><p style="font-weight:bold; float:left; text-decoration: underline;"> '''+str(lead_id.customer_id.company_name)+'''</p>
                                </center></div>
                        
                                <div class="col-md-1">
                                     </div>
                                <div class="col-md-2">
                                     <center><p style="font-weight:bold; float:left;">PI Number:</p>
                                </center></div>
                                <div class="col-md-2">
                                     <center><p style="font-weight:bold; float:left;"> '''+str(item2.id)+'''</p>
                                </center></div>
                                </div>
                        
                            <div class="row">
                                 <div class="col-md-2">
                                     <center><p style="font-weight:bold; float:left;">Contact Person</p>
                                </center></div>
                                <div class="col-md-5">
                                     <center><p style="font-weight:bold; float:left;"> '''+str(lead_id.customer_id.customer_name)+'''</p>
                                </center></div>
                        
                                <div class="col-md-1">
                                     </div>
                                <div class="col-md-2">
                                     <center><p style="font-weight:bold; float:left;">Proforma Made By :</p>
                                </center></div>
                                <div class="col-md-2">
                                     <center><p style="font-weight:bold; float:left;"> '''+str(request.user.name)+'''</p>
                                </center></div>
                                </div>


                            <div class="row">
                                 <div class="col-md-2">
                                     <center><p style="font-weight:bold; float:left;">Address/State</p>
                                </center></div>
                                <div class="col-md-5">
                                     <center><p style="font-weight:bold; float:left;"> '''+str(lead_id.customer_id.address)+'''</p>
                                </center></div>
                        
                                <div class="col-md-1">
                                     </div>
                                <div class="col-md-2">
                                     <center><p style="font-weight:bold; float:left;">Contact Number:</p>
                                </center></div>
                                <div class="col-md-2">
                                     <center><p style="font-weight:bold; float:left;"> '''+str(request.user.mobile)+'''</p>
                                </center></div>
                                </div>
                        
                        
                        
                        
                            <div class="row">
                                 <div class="col-md-2">
                                     <center><p style="font-weight:bold; float:left;">Phone</p>
                                </center></div>
                                <div class="col-md-5">
                                     <center><p style="font-weight:bold; float:left;"> '''+str(lead_id.customer_id.contact_no)+'''</p>
        </center></div>

        <div class="col-md-1">
             </div>
        <div class="col-md-2">
             <center><p style="font-weight:bold; float:left;">Customer GST Number: </p>
        </center></div>
        <div class="col-md-2">
             <center><p style="font-weight:bold; float:left;"> '''+str(lead_id.customer_id.customer_gst_no)+'''</p>
        </center></div>
        </div>




<style>
    .border_class {
    border:1px solid black;
    height:45px;
    text-align:center;
    vertical-align: middle;
    line-height: 45px;
    }


  table {
  border-collapse: collapse;
  width: 100%;
  font-size: 12px;
  border-color: black;
  color: black;



}


th {

  font-size: 13px;
    border: 1px solid black;
    text-align: left;
    padding:5px;

}

td {
  border: 1px solid black;
  padding: 3px;
  font-size: 13px;
  padding: 5px;
  text-align: center;
}


            </style>


<div style="min-height: 26vw;">

        
        <div class="row" id="id_manager_view">

    <table>
        <tr style="background-color: gray; color: white;">
            <td style="border-radius: 0px 0px 0px 0px; border: 0px solid gray;">Quantity</td>
            <td style="border: 0px solid gray;">HSN Code</td>
            <td style="border: 0px solid gray;">Product Code</td>
            <td style="border: 0px solid gray;">Product Image</td>
            <td style="border: 0px solid gray;">Product Description</td>
            <td style="border: 0px solid gray;">Rate</td>
            <td style="border: 0px solid gray;">Total</td>
        </tr>


 '''+table+'''

        <tr>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
        <td>Total</td>
        <td>'''+str(total)+''' INR</td>
        </tr>

        <tr>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
        <td>Discount%</td>
        <td>from PI form</td>
        </tr>


        <tr>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
        <td>Net Total</td>
        <td></td>
        </tr>



        <tr>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
        <td>P&F</td>
        <td>from PI form</td>
        </tr>



        <tr>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
        <td>CGST @ 9%</td>
        <td>from PI form</td>
        </tr>




        <tr>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
        <td>SGST @ 9%</td>
        <td>from PI form</td>
        </tr>




        <tr>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
        <td>IGST @ 18%</td>
        <td>from PI form</td>
        </tr>



        <tr>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
        <td>Round Up</td>
        <td>INR</td>
        </tr>

        <tr>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
        <td></td>
        <td>Grand Total</td>
        <td>INR</td>
        </tr>


    </table>
        </div>
            </div>
        <div class="row">
            <div class="col-md-4" style="padding:10px;">
                <p>GST ID - <b>27AACFH2329F1ZP</b><br>
                    PAN Number - <b>AACFH2329F</b><br>
                    TAN Number - <b>MUMH17092F</b></p>
            </div>
         <div class="col-md-3" style="padding:10px;">
<img src="/media/pi_history_file/okay.png" style="width: 100%;">
         </div>


	         <div class="col-md-5" style="padding:10px;">
<img src="/media/pi_history_file/l.png" style="width: 100%;">
         </div>
        </div>
    <div class="row">
            <div class="col-md-12" style="padding:10px;"><p>
I/We hereby certify that my/our registration certificate under the Goods and Service Tax Laws is in force on the date of which the sale of goods specified in this “Proforma Invoice” is made by me/us and that the transaction of sale is covered <br><center>by this and has been effected by me/us and it shall be accounted for in the turnover of sales while filing of return and the due tax, if any, payable on the sale has been paid
  </center> </p>     </div>
        </div>
</div>


<div class="row">
            <div class="col-md-6" style="padding-left: 40px;">
<p>All prices are Ex-Workshop. Packing and forwarding is extra as indicated<br>
                All products have an warranty of 1 year against any manufacturing defect unless stated<br>
                There is no warranty for Loadcell, Battery and Mains Cord<br>
                Damages due to transportation is out of the scope of warranty<br>
                Payment is 50% advance with order and remaining 50% before Dispatch<br>
                This offer is valid for the next 10 days <br>
    Cheque should be in the name of "Hindustan Scale Co".</p></div>

    <div class="col-md-6" style="padding-left: 40px;">
<p>Bank details are as follows<br>
                <b>DCB Bank<br>
                Name – Hindustan Scale Co.<br>
                Acct No – 01922412121947<br>
                IFSC Code-DCBL0000019<br>
                Type of account – Current Account <br>
                Bank Name – DCB Bank<br>
                    Address Mohamedali Road Branch</b></p></div>
        </div>
</div>

	<hr>

<span style="font-size: 11px;">HINDUSTAN SCALE COMPANY, 186/188 Janjikar Street, Crawford Market, Mumbai - 400003</span>
  </p>


</div>

</center>



<script>
  function printDiv(divName) {
     var printContents = document.getElementById(divName).innerHTML;
     var originalContents = document.body.innerHTML;

     document.body.innerHTML = printContents;

     window.print();

     document.body.innerHTML = originalContents;
}
</script>

</body>
</html>'''
                        msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER,
                                                     ['liocause@gmail.com','sagarsingh27998@gmail.com'])
                        html_content2 = '''
                        
<html>
<head>
  <title>
    HSCO
  </title>

  <meta name="viewport" content="width=device-width, initial-scale=1">

  <style>
      * {
    font-family: 'Poppins';
    font-size: 0.99em;

  }

  table {
  border-collapse: collapse;
  width: 85%;
  font-size: 18px;
  border-color: black;
  color: black;



}


th {

  font-size: 13px;
    border: 1px solid black;
    text-align: left;
    padding:5px;

}

td {
  border: 1px solid black;
  padding: 3px;
}


 @media print and (width: 10.5cm) and (height: 14.8cm) {
    @page {
       margin: 3cm;
    }
 }


  </style>

</head>
<body>

<div  id="printableArea" style="margin-left: 10%; margin-right: 10%;">
<div class="row" style="padding: 5px; border-bottom: 5px solid black;">
    <div class="col-xl-2 col-md-2 ">
<img src="/media/pi_history_file/hsco_template2.jpg" class="img-rounded" width="200" height="120" style="float: right;">
</div>
    <div class="col-xl-1 col-md-1 ">
    </div>
    <div class="col-xl-4 col-md-4 ">
<!--        <center>Subject to Mumbai Jurisdiction</center><br>-->
<!--        <center><h3 style="font: italic bold 22px/30px Georgia, serif;">Proforma Invoice</h3></center>-->
</div>
    <div class="col-xl-1 col-md-1 ">
    </div>
    <div class="col-xl-4 col-md-4 ">
        <p>Ph: 022-23423183, 7045922250/51/52<br>
Manufacture Licence No. LM/MH/H004<br>
Dealer Licence No. LD/MH/H004<br>
Repairing Licence No. LR/MH/H004</p>
</div>
</div>


        <div class="row">
         <div class="col-md-12" style="padding:10px;">
        <center><h1 style="font-weight:bold;"> Hindustan Sales and Consultancy</h1>
        </center></div>
        </div>
        <div class="row">
         <div class="col-md-12" style="padding:0px;">
        <center><p style="font-weight:bold;"> A one stop shop for all your weighing needs<br><font color="#FC6E20" style="font-weight:bold;"> AN ISO 9001: 2015 CERTIFIED COMPANY</font></p>
        </center></div>
        </div>


    <div class="row">
         <div class="col-md-12" style="padding:10px;">
        <center><p style="font-weight:bold;"> All kinds of Mechanical and Digital Weighing Scales, Weights & Measures.<br>
        186/188 Janjikar Street, Near Crawford Market, Mumbai- 400003/<font color="#FC6E20">www.hindustanscale.com/hsc@hindustanscale.com</font></p>
        </center></div>
        </div>


    <div class="row">
         <div class="col-md-2">
             <center><p style="font-weight:bold; float:left;"> Messrs</p>
        </center></div>
        <div class="col-md-5">
             </div>
        <div class="col-md-1">
             </div>
        <div class="col-md-2">
             <center><p style="font-weight:bold; float:left;"> Date :</p>
        </center></div>
        <div class="col-md-2">
             <center><p style="font-weight:bold; float:left;">'''+todays_date+''' </p>
        </center></div>
        </div>


    <div class="row">
         <div class="col-md-2">
             <center><p style="font-weight:bold; float:left;"> Company Name</p>
        </center></div>
        <div class="col-md-5">
             <center><p style="font-weight:bold; float:left; text-decoration: underline;">'''+str(lead_id.customer_id.company_name)+''' </p>
        </center></div>

        <div class="col-md-1">
             </div>
        <div class="col-md-2">
             <center><p style="font-weight:bold; float:left;">PI Number:</p>
        </center></div>
        <div class="col-md-2">
             <center><p style="font-weight:bold; float:left;">'''+str(item2.id)+''' </p>
        </center></div>
        </div>

    <div class="row">
         <div class="col-md-2">
             <center><p style="font-weight:bold; float:left;">Contact Person</p>
        </center></div>
        <div class="col-md-5">
             <center><p style="font-weight:bold; float:left;">'''+str(lead_id.customer_id.customer_name)+''' </p>
        </center></div>

        <div class="col-md-1">
             </div>
        <div class="col-md-2">
             <center><p style="font-weight:bold; float:left;">Proforma Made By :</p>
        </center></div>
        <div class="col-md-2">
             <center><p style="font-weight:bold; float:left;">'''+str(request.user.name)+''' </p>
        </center></div>
        </div>




    <div class="row">
         <div class="col-md-2">
             <center><p style="font-weight:bold; float:left;">Address/State</p>
        </center></div>
        <div class="col-md-5">
             <center><p style="font-weight:bold; float:left;"> '''+str(lead_id.customer_id.address)+'''</p>
        </center></div>

        <div class="col-md-1">
             </div>
        <div class="col-md-2">
             <center><p style="font-weight:bold; float:left;">Contact Number:</p>
        </center></div>
        <div class="col-md-2">
             <center><p style="font-weight:bold; float:left;">'''+str(request.user.mobile)+'''</p>
        </center></div>
        </div>




    <div class="row">
         <div class="col-md-2">
             <center><p style="font-weight:bold; float:left;">Phone</p>
        </center></div>
        <div class="col-md-5">
             <center><p style="font-weight:bold; float:left;"> '''+str(lead_id.customer_id.contact_no)+'''</p>
        </center></div>

        <div class="col-md-1">
             </div>
        <div class="col-md-2">
             <center><p style="font-weight:bold; float:left;">Customer GST Number: </p>
        </center></div>
        <div class="col-md-2">
             <center><p style="font-weight:bold; float:left;">'''+str(lead_id.customer_id.customer_gst_no)+''' </p>
        </center></div>
        </div>




<style>
    .border_class {
    border:1px solid black;
    height:45px;
    text-align:center;
    vertical-align: middle;
    line-height: 45px;
    }


  table {
  border-collapse: collapse;
  width: 100%;
  font-size: 12px;
  border-color: black;
  color: black;



}


th {

  font-size: 13px;
    border: 1px solid black;
    text-align: left;
    padding:5px;

}

td {
  border: 1px solid black;
  padding: 3px;
  font-size: 13px;
  padding: 5px;
  text-align: center;
}


            </style>


<div style="min-height: 26vw;">

        <div class="row" id="id_manager_view">

    <table>
        <tr style="background-color: gray; color: white;">
            <td style="border-radius: 0px 0px 0px 0px; border: 0px solid gray;">Quantity</td>
            <td style="border: 0px solid gray;">HSN Code</td>
            <td style="border: 0px solid gray;">Product Description</td>
            <td style="border: 0px solid gray;">Rate</td>
            <td style="border: 0px solid gray;">Total</td>
        </tr>


 '''+table2+'''

        <tr>
        <td></td>
        <td></td>
        <td></td>
        <td>Total</td>
        <td>INR</td>
        </tr>

        <tr>
        <td></td>

        <td></td>
        <td></td>
        <td>Discount%</td>
        <td>from PI form</td>
        </tr>


        <tr>
        <td></td>

        <td></td>
        <td></td>
        <td>Net Total</td>
        <td></td>
        </tr>



        <tr>
        <td></td>

        <td></td>
        <td> Delivery Charges </td>
        <td>P&F</td>
        <td>from PI form</td>
        </tr>



        <tr>
        <td></td>

        <td></td>
        <td></td>
        <td>CGST @ 9%</td>
        <td>from PI form</td>
        </tr>




        <tr>
        <td></td>
        <td></td>
        <td></td>
        <td>SGST @ 9%</td>
        <td>from PI form</td>
        </tr>




        <tr>
        <td></td>

        <td></td>
        <td></td>
        <td>IGST @ 18%</td>
        <td>from PI form</td>
        </tr>



        <tr>
        <td></td>

        <td></td>
        <td></td>
        <td>Round Up</td>
        <td>INR</td>
        </tr>

        <tr>
        <td></td>

        <td></td>
        <td></td>
        <td>Grand Total</td>
        <td>INR</td>
        </tr>


    </table>
        </div>
            </div>
        <div class="row">
            <div class="col-md-4" style="padding:10px;">
                <p>GST ID - <b>27AACFH2329F1ZP</b><br>
                    PAN Number - <b>AACFH2329F</b></p>
            </div>
         <div class="col-md-3" style="padding:10px;">
<!--<img src="/media/pi_history_file/okay.png" style="width: 100%;">-->
         </div>


	         <div class="col-md-5" style="padding:10px;">
<img src="/media/pi_history_file/l.png" style="width: 100%;">
         </div>
            #######################################################################################################################
        </div>
    <div class="row">
            <div class="col-md-12" style="padding:10px; float:left; "><p>
                This offer is valid for the next 10 days <br>
                All prices are Ex-Workshop. Packing and forwarding is extra<br>
                Cheque should be in the name of "Hindustan Sales and Consultancy"<br>
                Bank details are as follows<br>
 </p>     </div>
        </div>



<div class="row">
    <div class="col-md-6" style="padding-left: 40px;">
<p>Bank details are as follows<br>
                <b>DCB Bank<br>
                Name – Hindustan Scale Co.<br>
                Acct No – 01922412121947<br>
                IFSC Code-DCBL0000019<br>
                Type of account – Current Account <br>
                Bank Name – DCB Bank<br>
                    Address Mohamedali Road Branch</b></p></div>
        </div>
</div>
</div>

	<hr>

<!--<span style="font-size: 11px;">HINDUSTAN SCALE COMPANY, 186/188 Janjikar Street, Crawford Market, Mumbai - 400003</span>-->
  </p>


</div>

</center>



<script>
  function printDiv(divName) {
     var printContents = document.getElementById(divName).innerHTML;
     var originalContents = document.body.innerHTML;

     document.body.innerHTML = printContents;

     window.print();

     document.body.innerHTML = originalContents;
}
</script>

</body>
</html>
                        '''

                        if email == 'True' and select_pi_template == '1':
                            msg.attach_alternative(html_content1, "text/html")
                            msg.send()
                            history = Pi_History()
                            file = ContentFile(html_content1)
                            # pdfkit.from_file(file, 'out.pdf')
                            history.file.save('ProformaInvoice.html', file, save=False)
                            history.lead_id = Lead.objects.get(id=id)

                            history.save()
                        elif email == 'True' and select_pi_template == '2':
                            msg.attach_alternative(html_content2, "text/html")
                            msg.send()
                            history = Pi_History()
                            file = ContentFile(html_content2)
                            history.file.save('ProformaInvoice.html', file, save=False)
                            history.lead_id = Lead.objects.get(id=id)

                            history.save()
                # if whatsapp == 'True':
                #     return redirect('https://api.whatsapp.com/send?phone=91' + customer_id.contact_no + '&text=' + 'hi')
            else :
                item2 = Pi_section()
                item2.discount = discount
                item2.upload_pi_file = upload_pi_file
                item2.select_pi_template = select_pi_template
                item2.call = call
                item2.email = email
                item2.whatsapp = whatsapp
                item2.call2 = call2
                item2.select_gst_type = select_gst_type
                item2.discount_type = discount_type
                item2.lead_id = Lead.objects.get(id=id)
                item2.save()
                if request.user.is_authenticated:
                    todays_date = str(datetime.now())
                    # gst_no = str(lead_id.customer_id.customer_gst_no)
                    text_content = ''
                    subject = 'Support'
                    html_content1 = '''<html>
                <head>
                  <title>
                    HSCO
                  </title>

                  <meta name="viewport" content="width=device-width, initial-scale=1">
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">

                  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
                  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
                  <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
                  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
                  <link href='https://fonts.googleapis.com/css?family=Poppins' rel='stylesheet'>


                  <style>
                      * {
                    font-family: 'Poppins';
                    font-size: 0.99em;

                  }

                  table {
                  border-collapse: collapse;
                  width: 85%;
                  font-size: 18px;
                  border-color: black;
                  color: black;



                }


                th {

                  font-size: 13px;
                    border: 1px solid black;
                    text-align: left;
                    padding:5px;

                }

                td {
                  border: 1px solid black;
                  padding: 3px;
                }


                 @media print and (width: 10.5cm) and (height: 14.8cm) {
                    @page {
                       margin: 3cm;
                    }
                 }


                  </style>

                </head>
                <body>

                <div  id="printableArea" style="margin-left: 10%; margin-right: 10%;">
                <div class="row" style="padding: 5px; border-bottom: 5px solid black;">
                    <div class="col-xl-2 col-md-2 ">
                <img src="/media/pi_history_file/hsco.jpg" class="img-rounded" width="200" height="120" style="float: right;">
                </div>
                    <div class="col-xl-1 col-md-1 ">
                    </div>
                    <div class="col-xl-4 col-md-4 ">
                        <center>Subject to Mumbai Jurisdiction</center><br>
                        <center><h3 style="font: italic bold 22px/30px Georgia, serif;">Proforma Invoice</h3></center>
                </div>
                    <div class="col-xl-1 col-md-1 ">
                    </div>
                    <div class="col-xl-4 col-md-4 ">
                        <p>Ph: 022-23423183, 7045922250/51/52<br>
                Manufacture Licence No. LM/MH/H004<br>
                Dealer Licence No. LD/MH/H004<br>
                Repairing Licence No. LR/MH/H004</p>
                </div>
                </div>


                        <div class="row">
                         <div class="col-md-12" style="padding:10px;">
                        <center><h1 style="font-weight:bold;"> Hindustan Scale Company</h1>
                        </center></div>
                        </div>
                        <div class="row">
                         <div class="col-md-12" style="padding:0px;">
                        <center><p style="font-weight:bold;"> A one stop shop for all your weighing needs<br><font color="#FC6E20" style="font-weight:bold;"> AN ISO 9001: 2015 CERTIFIED COMPANY</font></p>
                        </center></div>
                        </div>


                    <div class="row">
                         <div class="col-md-12" style="padding:10px;">
                        <center><p style="font-weight:bold;"> All kinds of Mechanical and Digital Weighing Scales, Weights & Measures.<br>
                        186/188 Janjikar Street, Near Crawford Market, Mumbai- 400003/<font color="#FC6E20">www.hindustanscale.com/hsc@hindustanscale.com</font></p>
                        </center></div>
                        </div>


                    <div class="row">
                         <div class="col-md-2">
                             <center><p style="font-weight:bold; float:left;"> Messrs</p>
                        </center></div>
                        <div class="col-md-5">
                             </div>
                        <div class="col-md-1">
                             </div>
                        <div class="col-md-2">
                             <center><p style="font-weight:bold; float:left;"> Date :</p>
                        </center></div>
                        <div class="col-md-2">
                             <center><p style="font-weight:bold; float:left;"> ''' + todays_date + '''</p>
                                            </center></div>
                                            </div>


                                            <div class="row">
                                                 <div class="col-md-2">
                                                     <center><p style="font-weight:bold; float:left;"> Company Name</p>
                                                </center></div>
                                                <div class="col-md-5">
                                                     <center><p style="font-weight:bold; float:left; text-decoration: underline;"> ''' + str(
                        lead_id.customer_id.company_name) + '''</p>
                                                </center></div>

                                                <div class="col-md-1">
                                                     </div>
                                                <div class="col-md-2">
                                                     <center><p style="font-weight:bold; float:left;">PI Number:</p>
                                                </center></div>
                                                <div class="col-md-2">
                                                     <center><p style="font-weight:bold; float:left;"> ''' + str(
                        item2.id) + '''</p>
                                                </center></div>
                                                </div>

                                            <div class="row">
                                                 <div class="col-md-2">
                                                     <center><p style="font-weight:bold; float:left;">Contact Person</p>
                                                </center></div>
                                                <div class="col-md-5">
                                                     <center><p style="font-weight:bold; float:left;"> ''' + str(
                        lead_id.customer_id.customer_name) + '''</p>
                                                </center></div>

                                                <div class="col-md-1">
                                                     </div>
                                                <div class="col-md-2">
                                                     <center><p style="font-weight:bold; float:left;">Proforma Made By :</p>
                                                </center></div>
                                                <div class="col-md-2">
                                                     <center><p style="font-weight:bold; float:left;"> ''' + str(
                        request.user.name) + '''</p>
                                                </center></div>
                                                </div>


                                            <div class="row">
                                                 <div class="col-md-2">
                                                     <center><p style="font-weight:bold; float:left;">Address/State</p>
                                                </center></div>
                                                <div class="col-md-5">
                                                     <center><p style="font-weight:bold; float:left;"> ''' + str(
                        lead_id.customer_id.address) + '''</p>
                                                </center></div>

                                                <div class="col-md-1">
                                                     </div>
                                                <div class="col-md-2">
                                                     <center><p style="font-weight:bold; float:left;">Contact Number:</p>
                                                </center></div>
                                                <div class="col-md-2">
                                                     <center><p style="font-weight:bold; float:left;"> ''' + str(
                        request.user.mobile) + '''</p>
                                                </center></div>
                                                </div>




                                            <div class="row">
                                                 <div class="col-md-2">
                                                     <center><p style="font-weight:bold; float:left;">Phone</p>
                                                </center></div>
                                                <div class="col-md-5">
                                                     <center><p style="font-weight:bold; float:left;"> ''' + str(
                        lead_id.customer_id.contact_no) + '''</p>
                        </center></div>

                        <div class="col-md-1">
                             </div>
                        <div class="col-md-2">
                             <center><p style="font-weight:bold; float:left;">Customer GST Number: </p>
                        </center></div>
                        <div class="col-md-2">
                             <center><p style="font-weight:bold; float:left;"> ''' + str(
                        lead_id.customer_id.customer_gst_no) + '''</p>
                        </center></div>
                        </div>




                <style>
                    .border_class {
                    border:1px solid black;
                    height:45px;
                    text-align:center;
                    vertical-align: middle;
                    line-height: 45px;
                    }


                  table {
                  border-collapse: collapse;
                  width: 100%;
                  font-size: 12px;
                  border-color: black;
                  color: black;



                }


                th {

                  font-size: 13px;
                    border: 1px solid black;
                    text-align: left;
                    padding:5px;

                }

                td {
                  border: 1px solid black;
                  padding: 3px;
                  font-size: 13px;
                  padding: 5px;
                  text-align: center;
                }


                            </style>


                <div style="min-height: 26vw;">


                        <div class="row" id="id_manager_view">

                    <table>
                        <tr style="background-color: gray; color: white;">
                            <td style="border-radius: 0px 0px 0px 0px; border: 0px solid gray;">Quantity</td>
                            <td style="border: 0px solid gray;">HSN Code</td>
                            <td style="border: 0px solid gray;">Product Code</td>
                            <td style="border: 0px solid gray;">Product Image</td>
                            <td style="border: 0px solid gray;">Product Description</td>
                            <td style="border: 0px solid gray;">Rate</td>
                            <td style="border: 0px solid gray;">Total</td>
                        </tr>


                 ''' + table + '''

                        <tr>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td>Total</td>
                        <td>INR</td>
                        </tr>

                        <tr>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td>Discount%</td>
                        <td>from PI form</td>
                        </tr>


                        <tr>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td>Net Total</td>
                        <td></td>
                        </tr>



                        <tr>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td>P&F</td>
                        <td>from PI form</td>
                        </tr>



                        <tr>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td>CGST @ 9%</td>
                        <td>from PI form</td>
                        </tr>




                        <tr>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td>SGST @ 9%</td>
                        <td>from PI form</td>
                        </tr>




                        <tr>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td>IGST @ 18%</td>
                        <td>from PI form</td>
                        </tr>



                        <tr>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td>Round Up</td>
                        <td>INR</td>
                        </tr>

                        <tr>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td>Grand Total</td>
                        <td>INR</td>
                        </tr>


                    </table>
                        </div>
                            </div>
                        <div class="row">
                            <div class="col-md-4" style="padding:10px;">
                                <p>GST ID - <b>27AACFH2329F1ZP</b><br>
                                    PAN Number - <b>AACFH2329F</b><br>
                                    TAN Number - <b>MUMH17092F</b></p>
                            </div>
                         <div class="col-md-3" style="padding:10px;">
                <img src="/media/pi_history_file/okay.png" style="width: 100%;">
                         </div>


                	         <div class="col-md-5" style="padding:10px;">
                <img src="/media/pi_history_file/l.png" style="width: 100%;">
                         </div>
                        </div>
                    <div class="row">
                            <div class="col-md-12" style="padding:10px;"><p>
                I/We hereby certify that my/our registration certificate under the Goods and Service Tax Laws is in force on the date of which the sale of goods specified in this “Proforma Invoice” is made by me/us and that the transaction of sale is covered <br><center>by this and has been effected by me/us and it shall be accounted for in the turnover of sales while filing of return and the due tax, if any, payable on the sale has been paid
                  </center> </p>     </div>
                        </div>
                </div>


                <div class="row">
                            <div class="col-md-6" style="padding-left: 40px;">
                <p>All prices are Ex-Workshop. Packing and forwarding is extra as indicated<br>
                                All products have an warranty of 1 year against any manufacturing defect unless stated<br>
                                There is no warranty for Loadcell, Battery and Mains Cord<br>
                                Damages due to transportation is out of the scope of warranty<br>
                                Payment is 50% advance with order and remaining 50% before Dispatch<br>
                                This offer is valid for the next 10 days <br>
                    Cheque should be in the name of "Hindustan Scale Co".</p></div>

                    <div class="col-md-6" style="padding-left: 40px;">
                <p>Bank details are as follows<br>
                                <b>DCB Bank<br>
                                Name – Hindustan Scale Co.<br>
                                Acct No – 01922412121947<br>
                                IFSC Code-DCBL0000019<br>
                                Type of account – Current Account <br>
                                Bank Name – DCB Bank<br>
                                    Address Mohamedali Road Branch</b></p></div>
                        </div>
                </div>

                	<hr>

                <span style="font-size: 11px;">HINDUSTAN SCALE COMPANY, 186/188 Janjikar Street, Crawford Market, Mumbai - 400003</span>
                  </p>


                </div>

                </center>



                <script>
                  function printDiv(divName) {
                     var printContents = document.getElementById(divName).innerHTML;
                     var originalContents = document.body.innerHTML;

                     document.body.innerHTML = printContents;

                     window.print();

                     document.body.innerHTML = originalContents;
                }
                </script>

                </body>
                </html>'''
                    msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER,
                                                 ['liocause@gmail.com', 'sagarsingh27998@gmail.com'])
                    html_content2 = '''

                <html>
                <head>
                  <title>
                    HSCO
                  </title>

                  <meta name="viewport" content="width=device-width, initial-scale=1">

                  <style>
                      * {
                    font-family: 'Poppins';
                    font-size: 0.99em;

                  }

                  table {
                  border-collapse: collapse;
                  width: 85%;
                  font-size: 18px;
                  border-color: black;
                  color: black;



                }


                th {

                  font-size: 13px;
                    border: 1px solid black;
                    text-align: left;
                    padding:5px;

                }

                td {
                  border: 1px solid black;
                  padding: 3px;
                }


                 @media print and (width: 10.5cm) and (height: 14.8cm) {
                    @page {
                       margin: 3cm;
                    }
                 }


                  </style>

                </head>
                <body>

                <div  id="printableArea" style="margin-left: 10%; margin-right: 10%;">
                <div class="row" style="padding: 5px; border-bottom: 5px solid black;">
                    <div class="col-xl-2 col-md-2 ">
                <img src="/media/pi_history_file/hsco_template2.jpg" class="img-rounded" width="200" height="120" style="float: right;">
                </div>
                    <div class="col-xl-1 col-md-1 ">
                    </div>
                    <div class="col-xl-4 col-md-4 ">
                <!--        <center>Subject to Mumbai Jurisdiction</center><br>-->
                <!--        <center><h3 style="font: italic bold 22px/30px Georgia, serif;">Proforma Invoice</h3></center>-->
                </div>
                    <div class="col-xl-1 col-md-1 ">
                    </div>
                    <div class="col-xl-4 col-md-4 ">
                        <p>Ph: 022-23423183, 7045922250/51/52<br>
                Manufacture Licence No. LM/MH/H004<br>
                Dealer Licence No. LD/MH/H004<br>
                Repairing Licence No. LR/MH/H004</p>
                </div>
                </div>


                        <div class="row">
                         <div class="col-md-12" style="padding:10px;">
                        <center><h1 style="font-weight:bold;"> Hindustan Sales and Consultancy</h1>
                        </center></div>
                        </div>
                        <div class="row">
                         <div class="col-md-12" style="padding:0px;">
                        <center><p style="font-weight:bold;"> A one stop shop for all your weighing needs<br><font color="#FC6E20" style="font-weight:bold;"> AN ISO 9001: 2015 CERTIFIED COMPANY</font></p>
                        </center></div>
                        </div>


                    <div class="row">
                         <div class="col-md-12" style="padding:10px;">
                        <center><p style="font-weight:bold;"> All kinds of Mechanical and Digital Weighing Scales, Weights & Measures.<br>
                        186/188 Janjikar Street, Near Crawford Market, Mumbai- 400003/<font color="#FC6E20">www.hindustanscale.com/hsc@hindustanscale.com</font></p>
                        </center></div>
                        </div>


                    <div class="row">
                         <div class="col-md-2">
                             <center><p style="font-weight:bold; float:left;"> Messrs</p>
                        </center></div>
                        <div class="col-md-5">
                             </div>
                        <div class="col-md-1">
                             </div>
                        <div class="col-md-2">
                             <center><p style="font-weight:bold; float:left;"> Date :</p>
                        </center></div>
                        <div class="col-md-2">
                             <center><p style="font-weight:bold; float:left;">''' + todays_date + ''' </p>
                        </center></div>
                        </div>


                    <div class="row">
                         <div class="col-md-2">
                             <center><p style="font-weight:bold; float:left;"> Company Name</p>
                        </center></div>
                        <div class="col-md-5">
                             <center><p style="font-weight:bold; float:left; text-decoration: underline;">''' + str(
                        lead_id.customer_id.company_name) + ''' </p>
                        </center></div>

                        <div class="col-md-1">
                             </div>
                        <div class="col-md-2">
                             <center><p style="font-weight:bold; float:left;">PI Number:</p>
                        </center></div>
                        <div class="col-md-2">
                             <center><p style="font-weight:bold; float:left;">''' + str(item2.id) + ''' </p>
                        </center></div>
                        </div>

                    <div class="row">
                         <div class="col-md-2">
                             <center><p style="font-weight:bold; float:left;">Contact Person</p>
                        </center></div>
                        <div class="col-md-5">
                             <center><p style="font-weight:bold; float:left;">''' + str(
                        lead_id.customer_id.customer_name) + ''' </p>
                        </center></div>

                        <div class="col-md-1">
                             </div>
                        <div class="col-md-2">
                             <center><p style="font-weight:bold; float:left;">Proforma Made By :</p>
                        </center></div>
                        <div class="col-md-2">
                             <center><p style="font-weight:bold; float:left;">''' + str(request.user.name) + ''' </p>
                        </center></div>
                        </div>




                    <div class="row">
                         <div class="col-md-2">
                             <center><p style="font-weight:bold; float:left;">Address/State</p>
                        </center></div>
                        <div class="col-md-5">
                             <center><p style="font-weight:bold; float:left;"> ''' + str(lead_id.customer_id.address) + '''</p>
                        </center></div>

                        <div class="col-md-1">
                             </div>
                        <div class="col-md-2">
                             <center><p style="font-weight:bold; float:left;">Contact Number:</p>
                        </center></div>
                        <div class="col-md-2">
                             <center><p style="font-weight:bold; float:left;">''' + str(request.user.mobile) + '''</p>
                        </center></div>
                        </div>




                    <div class="row">
                         <div class="col-md-2">
                             <center><p style="font-weight:bold; float:left;">Phone</p>
                        </center></div>
                        <div class="col-md-5">
                             <center><p style="font-weight:bold; float:left;"> ''' + str(
                        lead_id.customer_id.contact_no) + '''</p>
                        </center></div>

                        <div class="col-md-1">
                             </div>
                        <div class="col-md-2">
                             <center><p style="font-weight:bold; float:left;">Customer GST Number: </p>
                        </center></div>
                        <div class="col-md-2">
                             <center><p style="font-weight:bold; float:left;">''' + str(
                        lead_id.customer_id.customer_gst_no) + ''' </p>
                        </center></div>
                        </div>




                <style>
                    .border_class {
                    border:1px solid black;
                    height:45px;
                    text-align:center;
                    vertical-align: middle;
                    line-height: 45px;
                    }


                  table {
                  border-collapse: collapse;
                  width: 100%;
                  font-size: 12px;
                  border-color: black;
                  color: black;



                }


                th {

                  font-size: 13px;
                    border: 1px solid black;
                    text-align: left;
                    padding:5px;

                }

                td {
                  border: 1px solid black;
                  padding: 3px;
                  font-size: 13px;
                  padding: 5px;
                  text-align: center;
                }


                            </style>


                <div style="min-height: 26vw;">

                        <div class="row" id="id_manager_view">

                    <table>
                        <tr style="background-color: gray; color: white;">
                            <td style="border-radius: 0px 0px 0px 0px; border: 0px solid gray;">Quantity</td>
                            <td style="border: 0px solid gray;">HSN Code</td>
                            <td style="border: 0px solid gray;">Product Description</td>
                            <td style="border: 0px solid gray;">Rate</td>
                            <td style="border: 0px solid gray;">Total</td>
                        </tr>


                 ''' + table2 + '''

                        <tr>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td>Total</td>
                        <td>INR</td>
                        </tr>

                        <tr>
                        <td></td>

                        <td></td>
                        <td></td>
                        <td>Discount%</td>
                        <td>from PI form</td>
                        </tr>


                        <tr>
                        <td></td>

                        <td></td>
                        <td></td>
                        <td>Net Total</td>
                        <td></td>
                        </tr>



                        <tr>
                        <td></td>

                        <td></td>
                        <td> Delivery Charges </td>
                        <td>P&F</td>
                        <td>from PI form</td>
                        </tr>



                        <tr>
                        <td></td>

                        <td></td>
                        <td></td>
                        <td>CGST @ 9%</td>
                        <td>from PI form</td>
                        </tr>




                        <tr>
                        <td></td>
                        <td></td>
                        <td></td>
                        <td>SGST @ 9%</td>
                        <td>from PI form</td>
                        </tr>




                        <tr>
                        <td></td>

                        <td></td>
                        <td></td>
                        <td>IGST @ 18%</td>
                        <td>from PI form</td>
                        </tr>



                        <tr>
                        <td></td>

                        <td></td>
                        <td></td>
                        <td>Round Up</td>
                        <td>INR</td>
                        </tr>

                        <tr>
                        <td></td>

                        <td></td>
                        <td></td>
                        <td>Grand Total</td>
                        <td>INR</td>
                        </tr>


                    </table>
                        </div>
                            </div>
                        <div class="row">
                            <div class="col-md-4" style="padding:10px;">
                                <p>GST ID - <b>27AACFH2329F1ZP</b><br>
                                    PAN Number - <b>AACFH2329F</b></p>
                            </div>
                         <div class="col-md-3" style="padding:10px;">
                <!--<img src="/media/pi_history_file/okay.png" style="width: 100%;">-->
                         </div>


                	         <div class="col-md-5" style="padding:10px;">
                <img src="/media/pi_history_file/l.png" style="width: 100%;">
                         </div>
                            #######################################################################################################################
                        </div>
                    <div class="row">
                            <div class="col-md-12" style="padding:10px; float:left; "><p>
                                This offer is valid for the next 10 days <br>
                                All prices are Ex-Workshop. Packing and forwarding is extra<br>
                                Cheque should be in the name of "Hindustan Sales and Consultancy"<br>
                                Bank details are as follows<br>
                 </p>     </div>
                        </div>



                <div class="row">
                    <div class="col-md-6" style="padding-left: 40px;">
                <p>Bank details are as follows<br>
                                <b>DCB Bank<br>
                                Name – Hindustan Scale Co.<br>
                                Acct No – 01922412121947<br>
                                IFSC Code-DCBL0000019<br>
                                Type of account – Current Account <br>
                                Bank Name – DCB Bank<br>
                                    Address Mohamedali Road Branch</b></p></div>
                        </div>
                </div>
                </div>

                	<hr>

                <!--<span style="font-size: 11px;">HINDUSTAN SCALE COMPANY, 186/188 Janjikar Street, Crawford Market, Mumbai - 400003</span>-->
                  </p>


                </div>

                </center>



                <script>
                  function printDiv(divName) {
                     var printContents = document.getElementById(divName).innerHTML;
                     var originalContents = document.body.innerHTML;

                     document.body.innerHTML = printContents;

                     window.print();

                     document.body.innerHTML = originalContents;
                }
                </script>

                </body>
                </html>
                                        '''

                    if email == 'True' and select_pi_template == '1':
                        msg.attach_alternative(html_content1, "text/html")
                        msg.send()
                        history = Pi_History()
                        file = ContentFile(html_content1)
                        # pdfkit.from_file(file, 'out.pdf')
                        history.file.save('ProformaInvoice.html', file, save=False)
                        history.lead_id = Lead.objects.get(id=id)

                        history.save()
                    elif email == 'True' and select_pi_template == '2':
                        msg.attach_alternative(html_content2, "text/html")
                        msg.send()
                        history = Pi_History()
                        file = ContentFile(html_content2)
                        history.file.save('ProformaInvoice.html', file, save=False)
                        history.lead_id = Lead.objects.get(id=id)

                        history.save()
                # if whatsapp == 'True':
                #     return redirect('https://api.whatsapp.com/send?phone=91' + customer_id.contact_no + '&text=' + 'hi')

        elif 'submit3' in request.POST:
            selected_fields = request.POST.getlist('checks[]')
            Follow_up_section.objects.filter(lead_id=id).update(fields=selected_fields)
            hfu = Follow_up_section.objects.filter(lead_id=id).last()
            context23 = {

                'hfu': hfu.fields,
            }
            context.update(context23)

        elif 'submit5' in request.POST:

            is_email = request.POST.get('is_email')
            is_whatsapp = request.POST.get('is_whatsapp')
            is_call = request.POST.get('is_call')
            is_sms = request.POST.get('is_sms')
            wa_msg = request.POST.get('wa_msg')
            wa_no = request.POST.get('wa_no')
            email_auto_manual = request.POST.get('email_auto_manual')
            selected_products = request.POST.getlist('checks_pro[]')
            selected_fields = Follow_up_section.objects.get(lead_id=id).fields

            if(len(selected_products)<1):

                context22={
                    'error':"No Product Selected\nPlease Select Products And Try Again",
                    'error_exist':True,
                }
                context.update(context22)
            elif(is_call!='on' and is_sms!='on' and is_whatsapp!='on' and is_email!='on' ):
                context28 = {
                    'error': "Please Select Atleast One Medium For Followup",
                    'error_exist': True,
                }
                context.update(context28)
            elif (len(selected_fields)<6):

                context28 = {
                    'error': "Please Select Atleast One Product Field",
                    'error_exist': True,
                }
                context.update(context28)
            else:

                final_list = []
                Follow_up_section.objects.filter(lead_id=id).update(whatsappno=wa_no,)
                Follow_up_section.objects.filter(lead_id=id).update(auto_manual_mode=email_auto_manual,)

                history_follow= History_followup()
                history_follow.follow_up_section=Follow_up_section.objects.get(id=hfu.id)


                selected_fields2 = selected_fields.replace("'", "").strip('][').split(', ')  # convert string to list
                history_follow.fields = selected_fields2
                history_follow.product_ids = selected_products

                length_of_list = 1
                count_list = 0

                html_head = '''<thead> '''
                for item in selected_fields2:
                    pro_list = Followup_product.objects.filter(lead_id=id,pk__in=selected_products).values_list(item, flat=True)
                    list_pro = []
                    if (count_list == 0):
                        for ite, lt in enumerate(pro_list):
                            if (ite == 0):
                                html_head = html_head + '''<th>''' + item + '''</th>'''
                            final_list.append([item + ' : ' + str(lt)])
                        count_list = count_list + 1
                    else:
                        for ite, lt in enumerate(pro_list):
                            if (ite == 0):
                                html_head = html_head + '''<th>''' + item + '''</th>'''
                            final_list[ite] = final_list[ite] + [item + ' : ' + str(lt)]
                            # final_list[ite].append(list_pro)
                html_head = html_head + '''</thead> '''

                html_rows = ''' '''
                count = 1
                sms_content=''' '''
                for count_for,single in enumerate(final_list):
                    html_rows = html_rows + '''<tr> '''
                    count = count + 1
                    sms_content=sms_content+''' Product #'''+str(count_for+1)+''':\n'''
                    for item in single:
                        sms_content = sms_content + item.partition(":")[0] +''' :'''+item.partition(":")[2]+'''\n'''
                        html_rows = html_rows + '''<td>''' + item.partition(":")[2] + '''</td>'''
                    html_rows = html_rows + '''</tr>'''


                if(is_email=='on'):
                    email_subject = request.POST.get('email_subject')
                    email_msg = request.POST.get('email_msg')
                    history_follow.is_email=True
                    history_follow.email_subject=email_subject
                    history_follow.email_msg=email_msg
                    Follow_up_section.objects.filter(lead_id=id).update(email_subject=email_subject, )

                    html_content='''<html>
    <head>
      <title>
        HSCO
      </title>
    
      <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
    
      <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
      <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
      <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js"></script>
      <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js"></script>
      <link href='https://fonts.googleapis.com/css?family=Poppins' rel='stylesheet'>
    
    <body>
    
    <style>
        .border_class {
        border:1px solid black;
        height:45px;
        text-align:center;
        vertical-align: middle;
        line-height: 45px;
        }
      table {
      border-collapse: collapse;
      width: 100%;
      font-size: 12px;
      border-color: black;
      color: black;
    }
    th {
      font-size: 13px;
        border: 1px solid black;
        text-align: left;
        padding:5px;
    }
td {
  border: 1px solid black;
  padding: 3px;
  font-size: 13px;
  padding: 5px;
  text-align: center;
}


            </style>

                          <div class="card shadow">

<div class="card-body row" style="padding: 15px;color: black; font-weight: 300; font-size: 14px;">
    <!--<div class="col-xl-4 col-md-1 mb-1" style="border-right: 1px solid black;"><center> Product Name: {{list.product_name}} </center></div>-->
    <table style="font-size: 14px;">
  <tr>
    <td style="border: solid gray; background-color: gray; color: white;">Product Code: </td>
    <td style="border: solid gray; background-color: gray; color: white;">HSN Code:</td>
    <td style="border: solid gray; background-color: gray; color: white;">Quantity:</td>
    <td style="border: solid gray; background-color: gray; color: white;">Product Description: </td>
      <td style="border: solid gray; background-color: gray; color: white;">Rate:</td>
      <td style="border: solid gray; background-color: gray; color: white;">Product Images:</td>
         

  </tr>
  <tr>
    <td>{{ product.product_id.sub_sub_category }}</td>
    <td>{{ product.product_id.hsn_code }}</td>
    <td>{{ product.quantity }}</td>
    <td>{{ product.product_id.product_desc }}</td>
    <td>{{ product.product_id.selling_price }}</td>
    <td>{{ product.product_id.product_image.url }}</td>
    
  </tr>
</table>
              </div>
          </style>
                              <div class="card shadow">
    
    <div class="card-body row" style="padding: 15px;color: black; font-weight: 300; font-size: 14px;">
        <!--<div class="col-xl-4 col-md-1 mb-1" style="border-right: 1px solid black;"><center> Product Name: {{list.product_name}} </center></div>-->
        
        <h4>'''+email_msg+'''</h4>
        
        <table style="font-size: 14px;">
        
        '''+html_head+''' 
        
    '''+html_rows+''' 
    </table>
                  </div>
                              </div>
    </body>
    </html>'''

                    send_html_mail(email_subject, html_content, settings.EMAIL_HOST_USER, [customer_id.customer_email_id, ])
                    context28 = {
                        'success': "Email Sent on email Id: "+customer_id.customer_email_id,
                        'success_exist': True,
                    }
                    context.update(context28)


                if(is_whatsapp=='on'):

                    history_follow.is_whatsapp = True
                    history_follow.wa_msg = wa_msg
                    history_follow.wa_no = wa_no
                    # selected_fields = Follow_up_section.objects.get(lead_id=id).fields
                    # selected_fields2 = selected_fields.replace("'", "").strip('][').split(', ')  # convert string to list
                    # length_of_list = 1
                    # count_list = 0
                    # html_head='''<tr> '''
                    # for item in selected_fields2:
                    #     pro_list = Followup_product.objects.filter(lead_id=id).values_list(item, flat=True)
                    #     list_pro=[]
                    #     if(count_list==0):
                    #         for ite, lt in enumerate(pro_list):
                    #             if(ite==0):
                    #                 html_head =html_head+ '''<td>'''+item+'''</td>'''
                    #             final_list.append([item + ' : ' + str(lt)])
                    #         count_list=count_list+1
                    #     else:
                    #         for ite, lt in enumerate(pro_list):
                    #             if (ite == 0):
                    #                 html_head = html_head + '''<td>''' + item + '''</td>'''
                    #             final_list[ite] = final_list[ite] + [item + ' : ' + str(lt)]
                    #             # final_list[ite].append(list_pro)
                    # html_head = html_head + '''</tr> '''
                    #
                    #
                    # html_rows = ''' '''
                    # count=1
                    # for single in final_list:
                    #     html_rows = html_rows+'''<tr> '''
                    #     count=count+1
                    #     for item in single:
                    #         html_rows = html_rows + '''<td>''' + item.partition(":")[2] + '''</td>'''
                    #     html_rows = html_rows + '''</tr>'''
                    context28 = {
                        'success_2': "WhatsApp Redirect Successful On WhatsApp No : " + wa_no,
                        'success_exist_2': True,
                    }
                    context.update(context28)





                if(is_sms=='on'):
                    sms_msg = request.POST.get('sms_msg')
                    history_follow.is_sms = True
                    history_follow.sms_msg = sms_msg+'\n'+sms_content
                    print("sms_contentsms_content")
                    print("sms_contentsms_content")
                    print(sms_content)
                    url = "http://smshorizon.co.in/api/sendsms.php?user=" + settings.user + "&apikey=" + settings.api + "&mobile=" + customer_id.contact_no + "&message=" + sms_msg + "&senderid=" + settings.senderid + "&type=txt"
                    payload = ""
                    headers = {'content-type': 'application/x-www-form-urlencoded'}

                    response = requests.request("GET", url, data=json.dumps(payload), headers=headers)
                    x = response.text
                    print(x)
                    context28 = {
                        'success_4': "SMS Sent Successfully To : " + customer_id.contact_no,
                        'success_exist_4': True,
                    }
                    context.update(context28)




                if(is_call=='on'):
                    call_response = request.POST.get('call_response')
                    history_follow.is_call = True
                    history_follow.call_response = call_response
                    context28 = {
                        'success_5': "Call Response Recorded Successfully" ,
                        'success_exist_5': True,
                    }
                    context.update(context28)

                history_follow.save()

                if (is_whatsapp):
                    return redirect('https://api.whatsapp.com/send?phone=91' + wa_no + '&text=' + wa_msg + str(final_list))




    return render(request, 'lead_management/update_view_lead.html',context)

def lead_report(request):
    if request.method =='POST' :
        selected_list = request.POST.getlist('checks[]')
        start_date = request.POST.get('date1')
        end_date = request.POST.get('date2')
        string = ','.join(selected_list)

        request.session['start_date'] = start_date
        request.session['end_date'] = end_date
        request.session['string'] = string
        request.session['selected_list'] = selected_list
        print(string)
        print(string)
        if 'submit1' in request.POST:
            table_name = 'Customer Details Section'
            request.session['table_name'] = table_name
        elif 'submit2' in request.POST:
            table_name = 'Deal Details Section'
            request.session['table_name'] = table_name
        elif 'submit3' in request.POST:
            table_name = 'PI Section'
            request.session['table_name'] = table_name
        elif 'submit4' in request.POST:
            table_name = 'Follow-up Section'
            request.session['table_name'] = table_name
        elif 'submit5' in request.POST:
            table_name = 'Payment Details Form'
            request.session['table_name'] = table_name
        return redirect('/final_lead_report/')
    return render(request,'lead_management/report_lead.html')

def final_lead_report(request):
    table_name = request.session.get('table_name')
    start_date = request.session.get('start_date')
    end_date = request.session.get('end_date')
    string = request.session.get('string')
    selected_list = request.session.get('selected_list')
    final_row_product = []
    final_row=[]
    context = {
        'final_row': final_row,
        'final_row_product': final_row_product,
        'selected_list': selected_list,
    }
    if table_name == 'Customer Details Section':
        # customer_list = Customer_Details.objects.filter(entry_timedate__range=(start_date, end_date)).values_list(string)
        with connection.cursor() as cursor:
            if string != '' :
                    cursor.execute("SELECT " +  string + " from customer_app_customer_details  PRODUCT  where "
                    " entry_timedate between'" + start_date + "' and '" + end_date + "';")
                    row = cursor.fetchall()
                    final_row_product = [list(x) for x in row]
                    repairing_data = []
                    for i in row:
                        repairing_data.append(list(i))

                    final_row = [list(x) for x in row]
                    repairing_data = []
                    for i in row:
                        repairing_data.append(list(i))

        try:
            del request.session['start_date']
            del request.session['end_date']
            del request.session['string']
            del request.session['selected_list']
        except:
            pass
    if table_name == 'Deal Details Section':

        # customer_list = Customer_Details.objects.filter(entry_timedate__range=(start_date, end_date)).values_list(string)
        with connection.cursor() as cursor:
            if string != '' :
                    cursor.execute("SELECT " +  string + " from lead_management_lead  PRODUCT  where "
                    " entry_timedate between '" + start_date + "' and '" + end_date + "';")
                    row = cursor.fetchall()
                    final_row_product = [list(x) for x in row]
                    repairing_data = []
                    for i in row:
                        repairing_data.append(list(i))

                    final_row = [list(x) for x in row]
                    repairing_data = []
                    for i in row:
                        repairing_data.append(list(i))

        try:
            del request.session['start_date']
            del request.session['end_date']
            del request.session['string']
            del request.session['selected_list']
        except:
            pass
    if table_name == 'PI Section':
        # customer_list = Customer_Details.objects.filter(entry_timedate__range=(start_date, end_date)).values_list(string)
        selected_list = ['lead_id','discount','discount_type','payment_channel','payment_received_date','notes','cgst_sgst','igst','grand_total','entry_timedate']


        with connection.cursor() as cursor:

            cursor.execute("SELECT lead_id_id,discount,discount_type,payment_channel,payment_received_date,notes,cgst_sgst,igst,grand_total,entry_timedate from lead_management_pi_section where entry_timedate between'" + start_date + "' and '" + end_date + "';")
            row = cursor.fetchall()
            final_row_product = [list(x) for x in row]
            repairing_data = []
            for i in row:
                repairing_data.append(list(i))

            final_row = [list(x) for x in row]
            repairing_data = []
            for i in row:
                repairing_data.append(list(i))
        try:
            del request.session['start_date']
            del request.session['end_date']
            del request.session['string']
            del request.session['selected_list']
        except:
            pass
    if table_name == 'Follow-up Section':
        # customer_list = Customer_Details.objects.filter(entry_timedate__range=(start_date, end_date)).values_list(string)
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT lead_id_id,discount,discount_type,payment_channel,payment_received_date,notes,cgst_sgst,igst,grand_total,entry_timedate from lead_management_pi_section where entry_timedate between'" + start_date + "' and '" + end_date + "';")
            row = cursor.fetchall()
            final_row_product = [list(x) for x in row]
            repairing_data = []
            for i in row:
                repairing_data.append(list(i))

            final_row = [list(x) for x in row]
            repairing_data = []
            for i in row:
                repairing_data.append(list(i))

        try:
            del request.session['start_date']
            del request.session['end_date']
            del request.session['string']
            del request.session['selected_list']
        except:
            pass
    if table_name == 'Payment Details Form':
        # customer_list = Customer_Details.objects.filter(entry_timedate__range=(start_date, end_date)).values_list(string)
        with connection.cursor() as cursor:
            if string != '' :
                    cursor.execute("SELECT " +  string + " from lead_management_payment_details  PRODUCT  where "
                    " entry_timedate between'" + start_date + "' and '" + end_date + "';")
                    row = cursor.fetchall()
                    final_row_product = [list(x) for x in row]
                    repairing_data = []
                    for i in row:
                        repairing_data.append(list(i))

                    final_row = [list(x) for x in row]
                    repairing_data = []
                    for i in row:
                        repairing_data.append(list(i))

        try:
            del request.session['start_date']
            del request.session['end_date']
            del request.session['string']
            del request.session['selected_list']
        except:
            pass

    context={
        'final_row':final_row,
        'final_row_product':final_row_product,
        'selected_list':selected_list,
    }
    return render(request,"report/final_lead_report.html",context)

def select_product_followup(request,id):
    type_of_purchase_list =type_purchase.objects.all() #1
    lead_id = Lead.objects.get(id=id)
    products = Product.objects.all()
    context={}
    if request.method == 'POST' or request.method == 'FILES' :
        if 'product_id' in request.POST:
            is_last_product_yes = request.POST.get('is_last_product_yes')
            product_id = request.POST.get('product_id')

            requested_product = Product.objects.get(id=product_id)
            print("product_id")
            print(product_id)
            print(requested_product)
            print("requested_product")
            fol_pro=Followup_product()
            fol_pro.product_id = requested_product
            fol_pro.lead_id = Lead.objects.get(id=id)
            fol_pro.scale_type = requested_product.scale_type
            fol_pro.main_category = requested_product.main_category
            fol_pro.sub_category = requested_product.sub_category
            fol_pro.sub_sub_category = requested_product.sub_sub_category
            fol_pro.hsn_code = requested_product.hsn_code
            fol_pro.max_capacity = requested_product.max_capacity
            fol_pro.accuracy = requested_product.accuracy
            fol_pro.platform_size = requested_product.platform_size
            fol_pro.product_desc = requested_product.product_desc
            fol_pro.cost_price = requested_product.cost_price
            fol_pro.selling_price = requested_product.selling_price
            fol_pro.carton_size = requested_product.carton_size
            fol_pro.save()


            if is_last_product_yes == 'yes':
                return redirect('/update_view_lead/' + str(id))
            elif is_last_product_yes == 'no':
                return redirect('/select_product_followup/' + str(id))
        else:
            model_of_purchase_str = request.POST.get('model_of_purchase')
            type_of_scale_str = request.POST.get('type_of_scale')
            sub_model_str = request.POST.get('sub_model')
            sub_sub_model_str = request.POST.get('sub_sub_model')

            print("model_of_purchase")
            print(model_of_purchase_str)
            print(type_of_scale_str)
            print(sub_model_str)
            print(sub_sub_model_str)
            print("sub_sub_model")

            if (sub_sub_model == None or sub_sub_model == ""):
                product_avail = Product.objects.filter(scale_type=type_purchase.objects.get(id=type_of_scale_str).name, main_category=main_model.objects.get(id=model_of_purchase_str).name,
                                                       sub_category=sub_model.objects.get(id=sub_model_str).name)
            else:
                product_avail = Product.objects.filter(scale_type=type_purchase.objects.get(id=type_of_scale_str).id, main_category=main_model.objects.get(id=model_of_purchase_str).id,
                                                       sub_category=sub_model.objects.get(id=sub_model_str).id, sub_sub_category=sub_sub_model.objects.get(id=sub_sub_model_str).id)

            context23 = {
                # 'lead_id': lead_id,
                # 'type_purchase': type_of_purchase_list,
                'product_avail': product_avail,
            }
            context.update(context23)





    context2={
        'lead_id':lead_id,
        'type_purchase':type_of_purchase_list,
        'products':products,
    }
    context.update(context2)
    return render(request,'lead_management/select_product_followup.html', context)

def select_product(request,id):
    type_of_purchase_list =type_purchase.objects.all() #1
    lead_id = Lead.objects.get(id=id)
    products = Product.objects.all()
    if request.method == 'POST' or request.method == 'FILES':
        hsn_code = request.POST.get('hsn_code')
        pf = request.POST.get('pf')
        quantity = request.POST.get('quantity')
        is_last_product_yes = request.POST.get('is_last_product_yes')
        # model_of_purchase = request.POST.get('model_of_purchase')
        type_of_scale = request.POST.get('scale_type')
        main_category = request.POST.get('main_category')
        sub_category = request.POST.get('sub_category')
        sub_sub_category = request.POST.get('sub_sub_category')    #product code or sub_sub_category

        item = Pi_product()
        if sub_sub_category != '' :
            item.product_id = Product.objects.get( scale_type=type_of_scale ,main_category=main_category,
                                                   sub_category=sub_category, sub_sub_category=sub_sub_category)
        item.lead_id = Lead.objects.get(id=lead_id)
        item.quantity = quantity
        item.pf = pf

        item.save()
        if is_last_product_yes == 'yes':
            return redirect('/update_view_lead/'+str(id))
        elif is_last_product_yes == 'no':
            return redirect('/select_product/'+str(id))
    context={
        'lead_id':lead_id,
        'type_of_purchase_list':type_of_purchase_list,
        'products':products,
    }
    return render(request,'lead_management/select_product.html', context)

def lead_manager_view(request):
    loggedin_user = SiteUser.objects.get(id=request.user.id).name
    # u_list=Pi_section.objects.filter(lead_id__owner_of_opportunity__super_admin=loggedin_user).values_list("lead_id__owner_of_opportunity").distinct()
    # users_list = []
    # for item in u_list:
    #     for ite in item:
    #         users_list.append(ite)
    # print("users_list")
    # print(users_list)
    currentMonth = datetime.now().month

    # for item in users_list:
        # pi_list=Pi_section.objects.filter(lead_id__owner_of_opportunity__id=item,lead_id__current_stage='PO Issued - Payment Done - Dispatch Pending')\
        #     .aggregate(Sum('grand_total'))
    pi_list=Pi_section.objects.filter(lead_id__owner_of_opportunity__super_admin=loggedin_user,entry_timedate__month=currentMonth).distinct().extra(select={
        'converted': "select SUM(grand_total) from lead_management_pi_section PI, lead_management_lead LEAD ,user_app_siteuser USER"
                     "where PI.lead_id_id = LEAD.id and LEAD.owner_of_opportunity_id = USER.id and super_admin='"+loggedin_user+"' and current_stage='PO Issued - Payment Done - Dispatch Pending'",
        'lost': "select SUM(grand_total) from lead_management_pi_section PI, lead_management_lead LEAD where PI.lead_id_id = LEAD.id and current_stage='Lost'",
        'postponed': "select SUM(grand_total) from lead_management_pi_section PI, lead_management_lead LEAD where PI.lead_id_id = LEAD.id and current_stage='Postponed'",

    }).values_list('lead_id__owner_of_opportunity__profile_name', 'converted', 'lost', 'postponed')
        # values_list('first_name', 'last_name', 'guide_like', 'news_like')
    print("u_listu_list")
    print("u_listu_list")
    print(pi_list)
    # for item in pi_list:
    #     print("item")
    #     print(item)
    context={
        'pi_list':pi_list,
    }




    return render(request,'lead_management/lead_manager.html',context)

def lead_follow_up_histroy(request,follow_up_id):
    obj_list = History_followup.objects.filter(follow_up_section=follow_up_id).order_by("-entry_timedate")

    context={
        'obj_list':obj_list,
    }

    return render(request,'lead_management/follow_up_history.html',context)

def pi_section_history(request,id):
    lead_id = Lead.objects.get(id=id)
    # lead_pi_id = Pi_section.objects.get(lead_id=id)
    lead_pi_history = Pi_History.objects.filter(lead_id=id).order_by('-id')
    context = {
        'lead_id': lead_id,
        'lead_pi_history': lead_pi_history,
    }
    return render(request,'lead_management/lead_history.html',context)

def lead_delete_product(request,id):
    leads = Pi_product.objects.filter(lead_id=id).order_by('-id')
    if request.method == 'POST' or request.method=='FILES':
        delete_id = request.POST.getlist('check[]')
        for i in delete_id:
            Pi_product.objects.filter(id=i).delete()
    context={
        'leads':leads,
    }
    return render(request,'lead_management/lead_delete_product.html',context)

def lead_analytics(request):
    #this month lead
    current_month_lead = Pi_section.objects.filter(lead_id__current_stage='PO Issued - Payment Done - Dispatch Pending',
                                                entry_timedate__month=datetime.now().month) \
        .values('entry_timedate').annotate(data_sum=Sum('grand_total'))
    current_month_lead_date = []
    current_month_lead_sum = []
    for i in current_month_lead:
        x = i
        current_month_lead_date.append(x['entry_timedate'].strftime('%Y-%m-%d'))
        current_month_lead_sum.append(x['data_sum'])

    #previous month lead
    mon = (datetime.now().month)
    if mon == 1:
        previous_mon = 12
    else:
        previous_mon = (datetime.now().month) - 1
    previous_month_lead = Pi_section.objects.filter(lead_id__current_stage='PO Issued - Payment Done - Dispatch Pending',
                                                   entry_timedate__month=previous_mon) \
        .values('entry_timedate').annotate(data_sum=Sum('grand_total'))
    previous_month_lead_date = []
    previous_month_lead_sum = []
    for i in previous_month_lead:
        x = i
        previous_month_lead_date.append(x['entry_timedate'].strftime('%Y-%m-%d'))
        previous_month_lead_sum.append(x['data_sum'])
    context = {
        'current_month_lead_date': current_month_lead_date,
        'current_month_lead_sum': current_month_lead_sum,
        'previous_month_lead_date': previous_month_lead_date,
        'previous_month_lead_sum': previous_month_lead_sum,

    }
    if request.method=='POST' and 'date1' in request.POST :
        start_date = request.POST.get('date1')
        lead_conversion = Pi_section.objects.filter(lead_id__current_stage='PO Issued - Payment Done - Dispatch Pending',
                                                    entry_timedate__month=datetime.strptime(start_date, '%Y-%m-%d').month) \
            .values('entry_timedate').annotate(data_sum=Sum('grand_total'))

        lead_conversion_date = []
        lead_conversion_sum = []
        for i in lead_conversion:
            x = i
            lead_conversion_date.append(x['entry_timedate'].strftime('%Y-%m-%d'))
            lead_conversion_sum.append(x['data_sum'])


        context = {
            'current_month_lead_date': current_month_lead_date,
            'current_month_lead_sum': current_month_lead_sum,
            'previous_month_lead_date': previous_month_lead_date,
            'previous_month_lead_sum': previous_month_lead_sum,
            'lead_conversion_date': lead_conversion_date,
            'lead_conversion_sum': lead_conversion_sum,

        }

    return render(request,'lead_management/lead_analytics.html',context)

def lead_employee_graph(request,id):
    lead_conversion = Pi_section.objects.filter(lead_id__current_stage='PO Issued - Payment Done - Dispatch Pending',lead_id__owner_of_opportunity=SiteUser.objects.get(id=id),entry_timedate__month=datetime.now().month)\
            .values('entry_timedate').annotate(data_sum=Sum('grand_total'))

    lead_conversion_date = []
    lead_conversion_sum = []
    for i in lead_conversion:
        x = i
        lead_conversion_date.append(x['entry_timedate'].strftime('%Y-%m-%d'))
        lead_conversion_sum.append(x['data_sum'])

    lead_lost = Pi_section.objects.filter(lead_id__current_stage='Lost',
                                                lead_id__owner_of_opportunity=SiteUser.objects.get(id=id),
                                                entry_timedate__month=datetime.now().month) \
        .values('entry_timedate').annotate(data_sum=Sum('grand_total'))

    lead_lost_date = []
    lead_lost_sum = []
    for i in lead_lost:
        x = i
        lead_lost_date.append(x['entry_timedate'].strftime('%Y-%m-%d'))
        lead_lost_sum.append(x['data_sum'])

    lead_postponed = Pi_section.objects.filter(lead_id__current_stage='Postponed',
                                                lead_id__owner_of_opportunity=SiteUser.objects.get(id=id),
                                                entry_timedate__month=datetime.now().month) \
        .values('entry_timedate').annotate(data_sum=Sum('grand_total'))
    lead_postponed_date = []
    lead_postponed_sum = []
    for i in lead_postponed:
        x = i
        lead_postponed_date.append(x['entry_timedate'].strftime('%Y-%m-%d'))
        lead_postponed_sum.append(x['data_sum'])
    context = {

        'lead_conversion_date': lead_conversion_date,
        'lead_conversion_sum': lead_conversion_sum,
        'lead_lost_date': lead_lost_date,
        'lead_lost_sum': lead_lost_sum,
        'lead_postponed_date': lead_postponed_date,
        'lead_postponed_sum': lead_postponed_sum,
    }
    if request.method=='POST' and 'date1' in request.POST :
        start_date = request.POST.get('date1')
        lead_conversion = Pi_section.objects.filter(lead_id__current_stage='PO Issued - Payment Done - Dispatch Pending',
            lead_id__owner_of_opportunity=SiteUser.objects.get(id=id), entry_timedate__month=datetime.strptime(start_date, '%Y-%m-%d').month) \
            .values('entry_timedate').annotate(data_sum=Sum('grand_total'))

        lead_conversion_date = []
        lead_conversion_sum = []
        for i in lead_conversion:
            x = i
            lead_conversion_date.append(x['entry_timedate'].strftime('%Y-%m-%d'))
            lead_conversion_sum.append(x['data_sum'])

        lead_lost = Pi_section.objects.filter(lead_id__current_stage='Lost',
                                              lead_id__owner_of_opportunity=SiteUser.objects.get(id=id),
                                              entry_timedate__month=datetime.strptime(start_date, '%Y-%m-%d').month) \
            .values('entry_timedate').annotate(data_sum=Sum('grand_total'))

        lead_lost_date = []
        lead_lost_sum = []
        for i in lead_lost:
            x = i
            lead_lost_date.append(x['entry_timedate'].strftime('%Y-%m-%d'))
            lead_lost_sum.append(x['data_sum'])

        lead_postponed = Pi_section.objects.filter(lead_id__current_stage='Postponed',
                                                   lead_id__owner_of_opportunity=SiteUser.objects.get(id=id),
                                                   entry_timedate__month=datetime.strptime(start_date, '%Y-%m-%d').month) \
            .values('entry_timedate').annotate(data_sum=Sum('grand_total'))
        lead_postponed_date = []
        lead_postponed_sum = []
        for i in lead_postponed:
            x = i
            lead_postponed_date.append(x['entry_timedate'].strftime('%Y-%m-%d'))
            lead_postponed_sum.append(x['data_sum'])
        context = {

            'lead_conversion_date': lead_conversion_date,
            'lead_conversion_sum': lead_conversion_sum,
            'lead_lost_date': lead_lost_date,
            'lead_lost_sum': lead_lost_sum,
            'lead_postponed_date': lead_postponed_date,
            'lead_postponed_sum': lead_postponed_sum,
        }

    return render(request,'lead_management/lead_employee_graph.html', context)

def lead_pi_form(request):
    return render(request,'lead_management/lead_pi_form.html')

def alpha_pi_form(request):
    return render(request,'lead_management/alpha_pi_template.html')

def report_2(request):
    return render(request,'lead_management/report_2.html')



def download_pi_image(request):
    return render(request,'lead_management/download_pi_image.html')

def download_pi_pdf(request):
    return render(request,'lead_management/download_pi_pdf.html')

