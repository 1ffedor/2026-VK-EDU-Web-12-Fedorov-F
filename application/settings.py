import os
from pathlib import Path

from celery.schedules import crontab
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / '.env.local')
load_dotenv(BASE_DIR / '.env')


def get_env(name, default=None):
    return os.environ.get(name, default)


SECRET_KEY = get_env('SECRET_KEY', 'django-insecure-dev-key-change-in-production')
DEBUG = get_env('DEBUG', 'True').lower() in ('1', 'true', 'yes')

ALLOWED_HOSTS = [h.strip() for h in get_env('ALLOWED_HOSTS', 'localhost,127.0.0.1,web').split(',') if h.strip()]
INTERNAL_IPS = ['127.0.0.1']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'core',
    'questions',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if DEBUG:
    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware')

ROOT_URLCONF = 'application.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'questions.context_processors.sidebar',
            ],
        },
    },
]

WSGI_APPLICATION = 'application.wsgi.application'
ASGI_APPLICATION = 'application.asgi.application'

DATABASES = {
    'default': {
        'ENGINE': get_env('DB_ENGINE', 'django.db.backends.postgresql'),
        'NAME': get_env('DB_NAME', 'vk_dz_3'),
        'USER': get_env('DB_USER', 'vk_user'),
        'PASSWORD': get_env('DB_PASSWORD', 'vk_password'),
        'HOST': get_env('DB_HOST', 'localhost'),
        'PORT': get_env('DB_PORT', '5432'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

REDIS_HOST = get_env('REDIS_HOST', 'localhost')
REDIS_PORT = get_env('REDIS_PORT', '6379')
REDIS_CACHE_DB = get_env('REDIS_CACHE_DB', '0')
REDIS_BROKER_DB = get_env('REDIS_BROKER_DB', '1')
REDIS_BEAT_DB = get_env('REDIS_BEAT_DB', '2')

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_CACHE_DB}',
        'OPTIONS': {'CLIENT_CLASS': 'django_redis.client.DefaultClient'},
        'TIMEOUT': 60 * 10,
    }
}

CELERY_BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_BROKER_DB}'
CELERY_RESULT_BACKEND = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_BEAT_DB}'
CELERY_BEAT_SCHEDULER = 'redbeat.RedBeatScheduler'
CELERY_REDBEAT_REDIS_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_BEAT_DB}'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

CELERY_BEAT_SCHEDULE = {
    'refresh-popular-tags': {
        'task': 'questions.tasks.refresh_popular_tags_cache',
        'schedule': crontab(minute='*/15'),
    },
    'refresh-best-members': {
        'task': 'questions.tasks.refresh_best_members_cache',
        'schedule': crontab(minute='*/10'),
    },
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = get_env('EMAIL_HOST', 'localhost')
EMAIL_PORT = int(get_env('EMAIL_PORT', '1025'))
EMAIL_USE_TLS = get_env('EMAIL_USE_TLS', 'False').lower() in ('1', 'true', 'yes')
DEFAULT_FROM_EMAIL = get_env('DEFAULT_FROM_EMAIL', 'noreply@vk-dz.local')

CENTRIFUGO_API_URL = get_env('CENTRIFUGO_API_URL', 'http://localhost:8001')
CENTRIFUGO_WS_URL = get_env('CENTRIFUGO_WS_URL', 'ws://localhost:8001/connection/websocket')
CENTRIFUGO_API_KEY = get_env('CENTRIFUGO_API_KEY', 'centrifugo-dev-api-key')
CENTRIFUGO_TOKEN_SECRET = get_env('CENTRIFUGO_TOKEN_SECRET', 'centrifugo-dev-secret-change-me')
CENTRIFUGO_NAMESPACE = get_env('CENTRIFUGO_NAMESPACE', 'questions')

CACHE_KEY_POPULAR_TAGS = 'sidebar:popular_tags'
CACHE_KEY_BEST_MEMBERS = 'sidebar:best_members'

SITE_URL = get_env('SITE_URL', 'http://127.0.0.1:8000')
