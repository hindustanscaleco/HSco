import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'f)wwo#to$=7lobqe%53%x^0hu0+o*#k3_k=t@3wf-1rn21h4a5'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

from django.contrib.auth.hashers import make_password
# print "Hashed password is:", make_password("plain_text")

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'user_app',
    'customer_app',
    'ess_app',
    'onsitevisit_app',
    'repairing_app',
    'restamping_app',
    'dispatch_app',
    'amc_visit_app',
    'notif_dec_app',
    'purchase_app',
    'session_security',
    'lead_management',
    'stock_management_system_app',
    'career_module_app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'session_security.middleware.SessionSecurityMiddleware'
]
AUTH_USER_MODEL = 'user_app.SiteUser'
ROOT_URLCONF = 'Hsco.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'notif_dec_app.views.notification_context',
            ],
        },
    },
]

TEMPLATE_CONTEXT_PROCESSORS = [
    'django.core.context_processors.request',
]
WSGI_APPLICATION = 'Hsco.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
 'default': {
     'ENGINE': 'django.db.backends.mysql',
    'NAME': 'hsco_db_test',
    'USER': 'root2',
    'PASSWORD': '',
    'HOST': '127.0.0.1',
    'PORT': '3306',
    'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
 }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/



STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static_local"),
]
STATIC_ROOT = os.path.join(BASE_DIR, "static_cdn", "static_root")

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "static_cdn", "media_root")
GEOIP_PATH = os.path.join(BASE_DIR, 'geo')
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
# EMAIL_HOST_USER = 'harshkumarpathak01@gmail.com'
# EMAIL_HOST_PASSWORD = 'ipv6netuser'

EMAIL_HOST_USER = 'website.hindustanscale.com@gmail.com'
# EMAIL_HOST_USER = 'vikas.pandey9323@gmail.com'
# EMAIL_HOST_USER = 'leosagarfcb10@gmail.com'
EMAIL_HOST_PASSWORD = 'Hsco123456789@'
# EMAIL_HOST_PASSWORD = 'Vikas@7786'
# EMAIL_HOST_PASSWORD = 'leosagar10'

SESSION_SECURITY_EXPIRE_AFTER = 3600
SESSION_SECURITY_WARN_AFTER = 3500
SESSION_EXPIRE_AT_BROWSER_CLOSE=True

user = 'HSCo'
#user_test = 'vikka'
api = 'PF8MzCBOGTopfpYFlSZT'
#api_test = 'puU087yJ0uAQdhggM3T0'
senderid = 'HSCALE'
