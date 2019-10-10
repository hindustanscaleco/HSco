from django.shortcuts import render, redirect
from .models import Ess



def add_ess(request):
    form=(request.POST or None)
    if request.method =='POST':
        employee_name = request.POST.get('employee_name')
        details = request.POST.get('details')
        contact_no = request.POST.get('contact_no')
        email_id = request.POST.get('email_id')
        photo = request.POST.get('photo')
        pancard = request.POST.get('pancard')
        aadhar_card = request.POST.get('aadhar_card')
        bank_details = request.POST.get('bank_details')
        photo_of_cancelled_cheque = request.POST.get('photo_of_cancelled_cheque')
        calander = request.POST.get('calander')
        target_of_month = request.POST.get('target_of_month')
        target_achived_till_now = request.POST.get('target_achived_till_now')
        month_on_month_sale_achived = request.POST.get('month_on_month_sale_achived')
        defect_given = request.POST.get('defect_given')
        warnings_given = request.POST.get('warnings_given')



        item = Ess()

        item.employee_name = employee_name
        item.details = details
        item.contact_no = contact_no
        item.email_id = email_id
        item.photo = photo
        item.pancard = pancard
        item.aadhar_card = aadhar_card
        item.photo_of_cancelled_cheque = photo_of_cancelled_cheque
        item.calander = calander
        item.target_of_month = target_of_month
        item.target_achived_till_now = target_achived_till_now
        item.bank_details = bank_details
        item.month_on_month_sale_achived = month_on_month_sale_achived
        item.defect_given = defect_given
        item.warnings_given = warnings_given

        item.save()
        return redirect('/')



    context = {
        'form': form,
    }
    return render(request,'forms/ess_form.html',context)