from .common import *  # noqa

ALLOWED_HOSTS = ["*"]
INSTALLED_APPS += ["gunicorn", ]

# Postgres
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT'),
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# Social
SOCIAL_AUTH_REDIRECT_IS_HTTPS = True

# Statics
STATIC_ROOT = os.getenv('STATIC_ROOT_PATH')
MEDIA_ROOT = os.getenv('MEDIA_ROOT_PATH')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

# Static files (CSS, JavaScript, Images)

STATIC_URL = 'static/'
MEDIA_URL = 'media/'
