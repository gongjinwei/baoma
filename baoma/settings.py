"""
Django settings for baoma project.

Generated by 'django-admin startproject' using Django 1.11.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""
import datetime
import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXTRA_APP_PATH=os.path.join(BASE_DIR,'extra_app')
sys.path.insert(0, BASE_DIR)
sys.path.insert(0,EXTRA_APP_PATH)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'z58k9owb!33=#$y7p#asts#a^1xql3ff170=kfjwpcny4au1t4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'ims_fa',
    'corsheaders',
    'guardian',
    'kombu.transport.django',
    'djcelery',
    'rest_pandas',
    'authadmin',
    'django_redis',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'baoma.urls'

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
                # 'django.template.context_processors.media',
            ],
        },
    },
    {
        'BACKEND': 'django_mustache.Mustache',
        'APP_DIRS': True,
    }
]

WSGI_APPLICATION = 'baoma.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'baoma',
        'HOST': '127.0.0.1',
        'USER': 'baoma',
        'PASSWORD': '123456',
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
# MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

REST_FRAMEWORK_TOKEN_EXPIRE_MINUTES = 60 * 10

REST_FRAMEWORK = {

    'DEFAULT_PERMISSION_CLASSES': (
        # 'rest_framework.permissions.IsAuthenticated',
        'ims_fa.authentication.ExceptionsIsAuthenticated',
        # 'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework.authentication.SessionAuthentication',
        'ims_fa.authentication.CsrfExemptSessionAuthentication',
        'ims_fa.authentication.ExpiringTokenAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    # 'UPLOADED_FILES_USE_URL':False,
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,
}

CORS_ORIGIN_ALLOW_ALL = True

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # this is default
    'guardian.backends.ObjectPermissionBackend',
)

QINIU_ACCESS_KEY = 'CsXZpUmY1L4ivYER9KYcIJw3mLmWFr8WhAhHNAlE'
QINIU_SECRET_KEY = 'Yb33ujAu-AvoAyhZOOCNgk2imDUyEmqqsMBEys7d'
QINIU_BUCKET_NAME = 'weibar'
QINIU_BUCKET_DOMAIN = 'res.yiwuwei.com'

QINIU_BUCKET_DOMAIN2 = 'mp.yiwuwei.com'
QINIU_BUCKET_NAME2 = 'attachment/'
DEFAULT_FILE_STORAGE = 'ims_fa.backends.QiniuStorage'
# MEDIA_URL = QINIU_BUCKET_DOMAIN+'/media/'

CACHES = {
    "default":{
        "BACKEND":"django_redis.cache.RedisCache",
        "LOCATION":"redis://127.0.0.1:6379/1",
        "OPTIONS":{
            "CLIENT_CLASS":"django_redis.client.DefaultClient",
        }
    }
}

CELERY_BROKER_URL='redis://localhost/0'
CELERY_ACCEPT_CONTENT=['json']
CELERY_RESULT_BACKEND='redis://localhost'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Shanghai'
CELERYD_MAX_TASKS_PER_CHILD=100

import djcelery
djcelery.setup_loader()

BROKER_URL='redis://localhost/0'
BACKEND_URL='redis://localhost'


CELERYBEAT_SCHEDULER='djcelery.schedulers.DatabaseScheduler'
