from typing import List

SECRET_KEY = NotImplemented
DEBUG = False
ALLOWED_HOSTS: List[str] = []

CORS_ALLOW_ALL_ORIGINS = True
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'drf_yasg',
    'corsheaders',
    # Apps
    'core.authentication.apps.AuthenticationConfig',
    'core.expenses.apps.ExpensesConfig',
    'core.income.apps.IncomeConfig',
    'core.social_auth.apps.SocialAuthConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'core.project.wsgi.application'
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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'core',
        'USER': 'core',
        'PASSWORD': 'core',
        'HOST': 'localhost',
        'PORT': '5432',
        'ATOMIC_REQUESTS': True,
        # TODO(dmu) MEDIUM: Unfortunately Daphne / ASGI / Django Channels do not properly reuse database connections
        #                   and therefore we are getting resource (connection) leak that leads to the following:
        #                   django.db.utils.OperationalError: FATAL:  sorry, too many clients already
        #                   `'CONN_MAX_AGE': 0` is used as workaround. In case it notably affects performance
        #                   implement a solution that either closes database connections on WebSocket client
        #                   disconnect and implement connection pooling outside Django (BgBouncer or similar)
        'CONN_MAX_AGE': 0,
    }
}
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp-mail.outlook.com'  # Set your SMTP server address
EMAIL_PORT = 587
EMAIL_USE_TLS = True  # Use TLS (True/False depending on your SMTP server)
DEFAULT_FROM_EMAIL = 'mohsin.mirza1991@hotmail.com'  # Your email address
EMAIL_HOST_USER = 'mohsin.mirza1991@hotmail.com'  # Your email address

AUTH_USER_MODEL = 'authentication.User'

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
        },
    },
    'LOGIN_URL': 'core.authentication:login',
    'LOGOUT_URL': 'core.authentication:logout',
    'USE_SESSION_AUTH': False,
    'PERSIST_AUTH': True,
}
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzMyNDA0NzU4LCJpYXQiOjE3MDA4Njg3NTgsImp0aSI6IjFlYjdlODE2NzA5ZDRkNGFiMGVlYzVhZWJlNmMwZjhkIiwidXNlcl9pZCI6Im1vaHNpbi5zaGFmaXF1ZTE5OTFAZ21haWwuY29tIn0.2oFUWCNjBhgAvObGoU-g1wj08vg7yjqw-mUiDO7TUeg
