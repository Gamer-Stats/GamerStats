import os
from pathlib import Path

from decouple import config
from gs_wik.settings.base import INSTALLED_APPS, MIDDLEWARE

BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = "django-insecure-calfa6oj0vtz7s+d@l((!e*tumhz%a7xm@^8ml&doz^p3nm6!#"

INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    "localhost"
    # ...
]

INSTALLED_APPS += ["debug_toolbar"]

MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

DEBUG = True

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AWS_S3_REGION_NAME = config("AWS_REGION")
AWS_ACCESS_KEY_ID = config("AWS_KEY")
AWS_SECRET_ACCESS_KEY = config("AWS_PASS")

AWS_S3_CUSTOM_DOMAIN = config("AWS_DOMAIN")
AWS_S3_SECURE_URLS = True

AWS_STORAGE_BUCKET_NAME = config("AWS_BUCKET")

# COMPRESS_STORAGE = "core.custom_storages.CachedS3BotoStorage"

# STATICFILES_LOCATION = "static"
# STATICFILES_STORAGE = "core.custom_storages.StaticStorage"

# STATIC_URL = config("AWS_DOMAIN") + "/"

AWS_IS_GZIPPED = True

# AWS_S3_OBJECT_PARAMETERS = {
#     'CacheControl': 'max-age=86400',
# }


MEDIAFILES_LOCATION = "media"
DEFAULT_FILE_STORAGE = "core.custom_storages.MediaStorage"
