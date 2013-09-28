from base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

INTERNAL_IPS = ('127.0.0.1',)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': 'localhost',
        'NAME': 'otpme',
        'USER': 'otpme',
        'PASSWORD': ''
    }
}

SECRET_KEY = '@e1@=^+b(sjy+^35drdp0myg@p32=kkq&#&=!^(xee$ut&s5qj'
