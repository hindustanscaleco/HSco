from django.db import models
import datetime
import random, os
from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,
    User)
choices = (('Super Admin', 'Super Admin'),
    ('Admin', 'Admin'),
   ('Manager', 'Manager'),
   ('Employee', 'Employee'),)
BANK_NAMES = (('Select Bank','Select Bank'),('Axis Bank','Axis Bank'),('HDFC Bank','HDFC Bank'),('ICICI Bank','ICICI Bank'),('State Bank of India','State Bank of India'),('Airtel Payments Bank','Airtel Payments Bank')
,('Allahabad Bank','Allahabad Bank'),('Andhra Bank','Andhra Bank'),('Bandhan bank','Bandhan bank'),('Bank of Bahrain and Kuwait','Bank of Bahrain and Kuwait'),('Bank of Baroda - Corporate Banking','Bank of Baroda - Corporate Banking'),
('Bank of Baroda - Retail Banking','Bank of Baroda - Retail Banking'),('Bank of India','Bank of India'),('Bank of Maharashtra','Bank of Maharashtra'),('Bassien Catholic Co-Operative Bank','Bassien Catholic Co-Operative Bank'),
('Bharatiya Mahila Bank','Bharatiya Mahila Bank'),('Canara Bank','Canara Bank'),('Catholic Syrian Bank','Catholic Syrian Bank'),('Central Bank of India','Central Bank of India'),('City Union Bank','City Union Bank'),
 ('Corporation Bank','Corporation Bank'),('Cosmos Bank','Cosmos Bank'),('Dena Bank','Dena Bank'),('Deutsche Bank','Deutsche Bank'),('Development Credit Bank','Development Credit Bank'),
('Dhanlakshmi Bank','Dhanlakshmi Bank'),('Digibank by DBS','Digibank by DBS'),    ('Dombivli Nagari Sahakari Bank Ltd.','Dombivli Nagari Sahakari Bank Ltd.'),('Federal Bank','Federal Bank'),('IDBI Bank','IDBI Bank'),('IDFC FIRST Bank','IDFC FIRST Bank'),('ING Vysya Bank','ING Vysya Bank'),
 ('Indian Bank','Indian Bank'),('Indian Overseas Bank','Indian Overseas Bank'),('IndusInd Bank','IndusInd Bank'),('Jammu & Kashmir Bank','Jammu & Kashmir Bank'),('Janata Sahakari Bank','Janata Sahakari Bank'),('Kalyan Janata Sahakari Bank','Kalyan Janata Sahakari Bank'),
('Karnataka Bank Ltd','Karnataka Bank Ltd'),('Karur Vysya Bank','Karur Vysya Bank'),('Kotak Bank','Kotak Bank'),('Laxmi Vilas Bank - Corporate','Laxmi Vilas Bank - Corporate'),('Laxmi Vilas Bank - Retail','Laxmi Vilas Bank - Retail'),('Oriental Bank of Commerce','Oriental Bank of Commerce'),
  ('PNB YUVA Netbanking','PNB YUVA Netbanking'),('Punjab & Maharashtra Co-operative Bank','Punjab & Maharashtra Co-operative Bank'),('Punjab & Sind Bank','Punjab & Sind Bank'),('Punjab National Bank - Corporate Banking','Punjab National Bank - Corporate Banking'),('Punjab National Bank - Retail Banking','Punjab National Bank - Retail Banking'),
  ('Ratnakar Bank','Ratnakar Bank'),('Saraswat Bank','Saraswat Bank'),('Shamrao Vitthal Co-operative Bank','Shamrao Vitthal Co-operative Bank'),('South Indian Bank','South Indian Bank'),('Standard Chartered Bank','Standard Chartered Bank'),('State Bank of Bikaner & Jaipur','State Bank of Bikaner & Jaipur'),
('State Bank of Hyderabad','State Bank of Hyderabad'),('State Bank of Mysore','State Bank of Mysore'),('State Bank of Patiala','State Bank of Patiala'),('State Bank of Travancore','State Bank of Travancore'),('Syndicate Bank','Syndicate Bank'),('TJSB Bank','TJSB Bank'),('Tamil Nadu State Co-operative Bank','Tamil Nadu State Co-operative Bank'),('Tamilnad Mercantile Bank Ltd.','Tamilnad Mercantile Bank Ltd.'),
  ('The Mehsana Urban Co Op Bank Ltd','The Mehsana Urban Co Op Bank Ltd'),('The Royal Bank of Scotland','The Royal Bank of Scotland'),('Union Bank of India','Union Bank of India'),('United Bank of India','United Bank of India'),('Vijaya Bank','Vijaya Bank'),('Yes Bank Ltd','Yes Bank Ltd'),)

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,10}$',
                             message="Phone number must be entered in the format: '+999999999'. Up to 10 digits allowed.")


class SiteUserManager(BaseUserManager):
    """Creates and saves a User with the given email, mobile, first_name, last_name  and password."""
    def create_user(self, email, mobile, password=None, is_staff=False, is_active=True,
                    is_admin=False,):
        if not mobile:
            raise ValueError('user must have a phone number')
        if not password:
            raise ValueError('user must have a password')

        user = self.model(
            email=email,
            password=password,
            mobile=mobile,
        )

        user.set_password(password)
        user.staff = is_staff
        user.admin = is_admin
        user.active = is_active
        user.save(using=self._db)
        return user

    def create_superuser(self, email, mobile, password=None,):
        user = self.create_user(
            email=email,
            mobile=mobile,
            password=password,

        )
        user.is_admin = True
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, mobile, password=None, ):
        user = self.create_user(
            email=email,
            mobile=mobile,
            password=password,

        )
        user.is_staff = True
        user.save(using=self._db)
        return user



class SiteUser(AbstractBaseUser):
    #user details(i.e super admin,admin, manager, employee)
    mobile = models.CharField(validators=[phone_regex], max_length=10, unique=True)
    email = models.EmailField( 'Email-id', max_length=255, unique=True )
    name =models.CharField('Name',max_length=50,null=True,blank=True)
    user_type = models.CharField('Type Of User',max_length=20, choices=choices,null=True,blank=True)
    group = models.CharField(max_length=50)
    is_deleted = models.BooleanField(default=False)
    modules_assigned = models.CharField()
    #customer_module
    sales_target =models.FloatField(default=0.0)                 #in numbers (customer module)
    target_achieved = models.FloatField(default=0.0)             #in percentage (customer module)
    #repairing_module
    repairing_no_of_repairs =models.FloatField(default=0.0)       #in numbers (repairing module)
    repairing_target_achieved = models.FloatField(default=0.0)   #in percentage (repairing module)
    # avg_time_repairing_scale = models.FloatField(default=0.0)
    # avg_time_for_estimation = models.FloatField(default=0.0)


    date_of_joining = models.DateField(default=datetime.date.today())
    average_rating = models.FloatField(default=0.0)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    #bank details
    bank_name = models.CharField(choices=BANK_NAMES, max_length=150,null=True,blank=True)
    account_no = models.CharField(max_length=100,null=True,blank=True)
    branch_name = models.CharField(max_length=100,null=True,blank=True)
    ifsc_code = models.CharField(max_length=100,null=True,blank=True)
    auto_timedate = models.DateTimeField(default=timezone.now, blank=True)

    objects = SiteUserManager()

    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = ['email',]

    def __str__(self):
        return self.mobile


    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    @is_staff.setter
    def is_staff(self, value):
        self._is_staff = value

