from django.shortcuts import render

# Create your views here.

def lead_home (request):
    return render(request,'lead_management/lead_home.html',)

