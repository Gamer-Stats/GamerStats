from decouple import config

SECRET_KEY = config("S_KEY")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASS"),
        "HOST": config("DB_HOST"),
        "PORT": config("DB_PORT"),
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
        },
    }
}

# AWS Settings

AWS_S3_REGION_NAME = config("AWS_REGION")
AWS_ACCESS_KEY_ID = config("AWS_KEY")
AWS_SECRET_ACCESS_KEY = config("AWS_PASS")

AWS_S3_CUSTOM_DOMAIN = config("AWS_DOMAIN")
AWS_S3_SECURE_URLS = True

AWS_STORAGE_BUCKET_NAME = config("AWS_BUCKET")

COMPRESS_STORAGE = "core.custom_storages.CachedS3BotoStorage"

STATICFILES_LOCATION = "static"
STATICFILES_STORAGE = "core.custom_storages.StaticStorage"

STATIC_URL = config("AWS_DOMAIN") + "/"

AWS_IS_GZIPPED = True

# AWS_S3_OBJECT_PARAMETERS = {
#     'CacheControl': 'max-age=86400',
# }


MEDIAFILES_LOCATION = "media"
DEFAULT_FILE_STORAGE = "core.custom_storages.MediaStorage"

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_AGE = 1209600
SESSION_COOKIE_DOMAIN = "gamerstats.net"
SECURE_HSTS_SECONDS = 3600
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
