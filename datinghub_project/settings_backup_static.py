from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'clean-datinghub-2026-temp'
DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = ['django.contrib.staticfiles']
MIDDLEWARE = ['django.middleware.common.CommonMiddleware']
ROOT_URLCONF = 'datinghub_project.urls'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [BASE_DIR / 'templates'],
    'APP_DIRS': True,
}]

DATABASES = {'default': {'ENGINE': 'django.db.backends.dummy'}}
STATIC_URL = 'static/'
