import os
from pathlib import Path

from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = config("S_KEY")
# SECRET_KEY = "django-insecure-calfa6oj0vtz7s+d@l((!e*tumhz%a7xm@^8ml&doz^p3nm6!#"

DEBUG = True

ALLOWED_HOSTS = ["*"]

# CORS_ALLOWED_ORIGINS = [
#     "https://cdn.gamerstats.net"
# ]

# CORS_ALLOWED_ORIGIN_REGEXES = [
#     r"^https://\w+\.gamerstats\.net$",
# ]


INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    "localhost"
    # ...
]

# Application definition

INSTALLED_APPS = [
    "debug_toolbar",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.sitemaps",
    "django.contrib.redirects",
    "core",
    "compressor",
    "sorl.thumbnail",
    "jsoneditor",
    "ckeditor",
    "ckeditor_uploader",
    "storages",
    "corsheaders",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.contrib.redirects.middleware.RedirectFallbackMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = "gs_wik.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "gs_wik.wsgi.application"


# Database

DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.sqlite3',
       'NAME': 'mydatabase',
   }
}

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": config("DB_NAME"),
#         "USER": config("DB_USER"),
#         "PASSWORD": config("DB_PASS"),
#         "HOST": config("DB_HOST"),
#         "PORT": config("DB_PORT"),
#     }
# }


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = "static/"

STATIC_ROOT = os.path.join(BASE_DIR, "static")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "assets"),
]

MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

CKEDITOR_UPLOAD_PATH = 'uploads/'

# STATICFILES_FINDERS = (
#     "django.contrib.staticfiles.finders.FileSystemFinder",
#     "django.contrib.staticfiles.finders.AppDirectoriesFinder",
#     "compressor.finders.CompressorFinder",
# )

# COMPRESS_ENABLED = True

# COMPRESS_CSS_HASHING_METHOD = 'content'
# COMPRESS_CSS_FILTERS = [
#     'compressor.filters.css_default.CssAbsoluteFilter',
#     'compressor.filters.cssmin.CSSMinFilter',
# ]

SITE_ID = 1

# SECURE_SSL_REDIRECT = True

# SESSION_COOKIE_SECURE = True

# CSRF_COOKIE_SECURE = True

# SESSION_COOKIE_AGE = 1209600

# SESSION_COOKIE_DOMAIN = "gamerstats.net"

# SECURE_HSTS_SECONDS = 3600

# SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# SECURE_HSTS_PRELOAD = True

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

AWS_S3_OBJECT_PARAMETERS = {
    'CacheControl': 'max-age=86400',
}

# COMPRESS_URL = STATIC_URL

MEDIAFILES_LOCATION = "media"
DEFAULT_FILE_STORAGE = "core.custom_storages.MediaStorage"

JSON_EDITOR_JS = "https://cdnjs.cloudflare.com/ajax/libs/jsoneditor/8.6.4/jsoneditor.js"
JSON_EDITOR_CSS = (
    "https://cdnjs.cloudflare.com/ajax/libs/jsoneditor/8.6.4/jsoneditor.css"
)


# CKEDITOR

CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono',
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'toolbar_YourCustomToolbarConfig': [
            {'name': 'document', 'items': ['Source', '-', 'Save', 'NewPage', 'Preview', 'Print', '-', 'Templates']},
            {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
            {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
            {'name': 'forms',
             'items': ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton',
                       'HiddenField']},
            '/',
            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl',
                       'Language']},
            {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
            {'name': 'insert',
             'items': ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe']},
            '/',
            {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},
            {'name': 'about', 'items': ['About']},
            '/',  # put this to force next toolbar on new line
            {'name': 'yourcustomtools', 'items': [
                # put the name of your editor.ui.addButton here
                'Preview',
                'Maximize',

            ]},
        ],
        'toolbar': 'YourCustomToolbarConfig',
        'tabSpaces': 4,
        'extraPlugins': ','.join([
            'uploadimage',
            # your extra plugins here
            'div',
            'autolink',
            'autoembed',
            'embedsemantic',
            'autogrow',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath'
        ]),
    }
}

# Default primary key field type

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
