from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY", default="django-insecure-fallback-for-dev-only")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="127.0.0.1", cast=lambda v: [s.strip() for s in v.split(",")])

# Security settings for production
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = config("SECURE_SSL_REDIRECT", default=True, cast=bool)
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    X_FRAME_OPTIONS = "DENY"

CSRF_TRUSTED_ORIGINS = config("CSRF_TRUSTED_ORIGINS", default="https://*.ngrok-free.dev", cast=lambda v: [s.strip() for s in v.split(",")])

# Application definition

INSTALLED_APPS = [
    "unfold",  # before django.contrib.admin
    "unfold.contrib.filters",  # optional, if special filters are needed
    "unfold.contrib.forms",  # optional, if special form elements are needed
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "widget_tweaks",

    #nos app
    'core',
    'abonnements',
    'agents',
    'clients',
    'paiements',
    'secteurs',
    'tournees',
    'accounts',
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

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'
LOGIN_REDIRECT_URL = "/dashboard/"



# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'fr-FR'

TIME_ZONE = 'Africa/Brazzaville'

USE_I18N = True 

USE_L10N = True 

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = "accounts.User"



# Unfold Configuration
UNFOLD = {
    "THEME": "default",  # "light" or "dark" or "auto" or "default"

    "COLORS": {
        "primary": {
            "50": "240 249 246",      # lightest shade
            "100": "220 242 231",     # lighter shade
            "200": "187 247 208",     # light shade
            "300": "134 239 172",     # medium light
            "400": "74 222 128",      # medium
            "500": "5 150 105",       # default - exact #059669
            "600": "5 122 85",        # medium dark
            "700": "4 100 70",        # dark
            "800": "4 84 58",         # darker
            "900": "4 75 55",         # darkest
            "950": "2 44 34",         # extra dark
        },
    },

    # Styles
    "STYLES": [
        {
            "name": "custom",
            "src": "/static/css/admin-custom.css",  # Optional custom CSS
        },
    ],

    # Templates
    "TEMPLATE": {
        "footer": {
            "links": [
                {
                    "title": "Documentation",
                    "href": "https://github.com/unfoldadmin/django-unfold",
                },
            ]
        }
    },
}

handler403 = "accounts.views.custom_permission_denied"

PASSWORD_RESET_TIMEOUT = 3600  # 1 hour (3600 seconds)


# Email configuration
# Settings for sending emails through SMTP (e.g., Gmail)
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"  # Use SMTP for sending emails
EMAIL_HOST = config("EMAIL_HOST")  # SMTP host address from environment variables
EMAIL_PORT = config("EMAIL_PORT", cast=int)  # SMTP port number from environment variables
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)  # Use TLS encryption for email
EMAIL_HOST_USER = config("EMAIL_HOST_USER")  # SMTP username from environment variables
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")  # SMTP password from environment variables


