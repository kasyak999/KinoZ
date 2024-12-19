import os
from dotenv import load_dotenv
from pathlib import Path


load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / 'templates'

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = ['89.110.75.220', '127.0.0.1', 'kinoz.ddns.net', 'localhost']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',

    'films.apps.FilmsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'kinoz.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'kinoz.wsgi.application'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('MYSQL_DB', 'django'),
        'USER': os.getenv('MYSQL_USER', 'user'),
        'PASSWORD': os.getenv('MYSQL_PASSWORD', 'user_password'),
        'HOST': os.getenv('MYSQL_HOST', 'db_mysql'),
        'PORT': os.getenv('MYSQL_PORT', 3306),
    }
}
# 'NAME': 'my_database',  # Имя базы данных
# 'USER': 'user',         # Пользователь базы данных
# 'PASSWORD': 'user_password',  # Пароль пользователя
# 'HOST': 'db_mysql',     # Имя контейнера базы данных (должно совпадать с db_mysql в Docker Compose)
# 'PORT': '3306',         # Порт, который проброшен в Docker Compose

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': os.getenv('POSTGRES_DB', 'django'),
#         'USER': os.getenv('POSTGRES_USER', 'django'),
#         'PASSWORD': os.getenv('POSTGRES_PASSWORD', ''),
#         'HOST': os.getenv('POSTGRES_HOST', ''),
#         'PORT': os.getenv('POSTGRES_PORT', 5432),
#     }
# }
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

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

LANGUAGE_CODE = 'ru-RU'
TIME_ZONE = 'Europe/Moscow'  # 'UTC'
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Добавьте в settings.py эту константу, чтобы DjDT знал,
# запросы с каких IP он должен обрабатывать.
INTERNAL_IPS = [
    '127.0.0.1',
]

# Директории, где собраны статические файлы проекта (список):
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static_dev',
]
STATIC_ROOT = BASE_DIR / 'static_backend'

# ссылка пользователя
LOGIN_REDIRECT_URL = 'films:index'
LOGIN_URL = 'login'

# Подключаем бэкенд filebased.EmailBackend:
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
# Указываем директорию, в которую будут сохраняться файлы писем:
EMAIL_FILE_PATH = BASE_DIR / 'sent_emails'

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:8000'
]  # для пост запросов на домене
