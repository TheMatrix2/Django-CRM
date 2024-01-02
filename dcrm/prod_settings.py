from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-y74n+zksnf=nh5sh334$as^0az3ws&j!ow$m4(&'

DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', '77.246.100.101', 'crm-systemx.ru']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'personal',
        'USER': 'admin',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

STATIC_URL = '/static/'
