from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-y74n+z*kxadxa57__8d5du&f=&gbkbufn^0az3ws&j!ow$m4(&'

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '77.246.100.101']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'personal',
        'USER': 'root',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

STATIC_URL = 'static/'
