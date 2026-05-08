import locale

from pathlib import Path

import os



# Força o locale para Português do Brasil para que os meses e números apareçam corretamente

try:

    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

except locale.Error:

    locale.setlocale(locale.LC_ALL, 'portuguese')





"""

Django settings for CRM_Comercial project.

"""



BASE_DIR = Path(__file__).resolve().parent.parent



SECRET_KEY = '5f=cb11jx+s0c2&!&mua57y%s830w#m%gle11ibs-@($s)1938'

DEBUG = True

ALLOWED_HOSTS = ['CRMintalog.pythonanywhere.com', '127.0.0.1', 'testserver', 'localhost']



INSTALLED_APPS = [

    'django.contrib.admin',

    'django.contrib.auth',

    'django.contrib.contenttypes',

    'django.contrib.sessions',

    'django.contrib.messages',

    'django.contrib.staticfiles',

    # Nossos Apps

    'app',

    'django_bootstrap5',

    'django.contrib.humanize',

    'django_htmx',

    'webpush',

]



MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.common.CommonMiddleware',

    'django.middleware.csrf.CsrfViewMiddleware',

    'django.contrib.auth.middleware.AuthenticationMiddleware',

    'django.contrib.messages.middleware.MessageMiddleware',

    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'django_htmx.middleware.HtmxMiddleware',

]



ROOT_URLCONF = 'CRM_Comercial.urls'



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
                'app.context_processors.webpush_settings',

            ],

        },

    },

]



WSGI_APPLICATION = 'CRM_Comercial.wsgi.application'



DATABASES = {

    'default': {

        'ENGINE': 'django.db.backends.sqlite3',

        'NAME': BASE_DIR / 'db.sqlite3',

    }

}



AUTH_PASSWORD_VALIDATORS = [

    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},

    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},

    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},

    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},

]



# --- CONFIGURAÇÕES DE IDIOMA E LOCALIZAÇÃO ---

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True

USE_THOUSAND_SEPARATOR = True



STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'static_root')

STATICFILES_DIRS = [

    os.path.join(BASE_DIR, 'static'),

]



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'





# --- CONFIGURAÇÕES DE REDIRECIONAMENTO DE LOGIN/LOGOUT ---



# Define qual é a URL de login do nosso sistema

LOGIN_URL = 'login'



# Redireciona para a home do nosso app após o login

LOGIN_REDIRECT_URL = 'app:home'



# Redireciona para a página de login após o logout

LOGOUT_REDIRECT_URL = 'login'



# --- CONFIGURAÇÕES DE ARQUIVOS DE MÍDIA (UPLOADS) ---

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')



# API REST

INSTALLED_APPS += ['rest_framework']



REST_FRAMEWORK = {

    'DEFAULT_PERMISSION_CLASSES': [

        'rest_framework.permissions.IsAuthenticated',

    ],

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',

    'PAGE_SIZE': 50,

}
# --- CONFIGURAES DE WEB PUSH NOTIFICATIONS ---
WEBPUSH_SETTINGS = {
    "VAPID_PUBLIC_KEY": "BFelGUDmcUP5fAVU4JmribTBT8lUb8nXKHJFN8obGw8FW-iokAi1r4fUc5HMI5G1Kcdm2jbzG0C94XvOBeKkOnE",
    "VAPID_PRIVATE_KEY": "CmpFNxVDt4jDR0ZU3H79sbcflLYjcMSfyjSha71cOXg",
    "VAPID_ADMIN_EMAIL": "eduardo.luparele@gmail.com",
}

# --- CONFIGURAÇÕES DE BACKUP (Google Drive) ---
# Substitua pelo ID da pasta do Google Drive onde os backups serão salvos
GOOGLE_DRIVE_BACKUP_FOLDER_ID = '1yMyVjyxdVE5s0AXwdlZvN5L5z5kxcqe_'

