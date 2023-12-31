"""Hsco URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static

from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('user_app.urls')),
    path('', include('dispatch_app.urls')),
    path('', include('customer_app.urls')),
    path('', include('ess_app.urls')),
    path('', include('onsitevisit_app.urls')),
    path('', include('repairing_app.urls')),
    path('', include('amc_visit_app.urls')),
    path('', include('restamping_app.urls')),
    path('', include('onsitevisit_app.urls')),
    path('', include('onsitevisit_app.urls')),
    path('', include('notif_dec_app.urls')),
    path('', include('purchase_app.urls')),
    path('', include('lead_management.urls')),
    path('', include('stock_management_system_app.urls')),
    path('', include('career_module_app.urls')),
    path('session_security/', include('session_security.urls')),
    path('', include('expense_app.urls')),


]
#if settings.DEBUG:

urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
