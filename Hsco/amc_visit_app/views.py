from django.shortcuts import render, redirect


def add_customer_details(request):
    form = (request.POST or None)
    if request.method == 'POST':
        amcno = request.POST.get('amcno')
        company_name = request.POST.get('company_name')
        address = request.POST.get('address')



        item = Customer_Details()

        item.amcno = amcno
        item.company_name = company_name
        item.company_name = company_name



        item.save()

        return redirect('/')


    context = {
        'form': form,
    }
    return render(request,'forms/amc_form.html',context)