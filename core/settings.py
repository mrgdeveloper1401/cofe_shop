from pathlib import Path
from dotenv import load_dotenv
import os
from datetime import timedelta

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY", "test")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(os.getenv("DEBUG", True))

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "*").split(",")

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',


    # internal apps 
    'user.apps.UserConfig',
    'apps.product.apps.ProductConfig',
    'apps.template.apps.TemplateConfig',
    'apps.authentication.apps.AuthenticationConfig',
    'apps.cart.apps.CartConfig',
    "apps.core_app.apps.CoreAppConfig",

    # external apps 
    'rest_framework',
    'drf_yasg',
    'corsheaders',
    'nested_inline',
    'rest_framework_simplejwt',
    "django_filters",
    "django_ckeditor_5",
    "mptt"
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# CORS settings
USE_CORS = bool(os.getenv("USE_CORS", True))
if USE_CORS:
    CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000").split(",")

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

ASGI_APPLICATION = 'core.asgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

AUTH_USER_MODEL = os.getenv("AUTH_USER_MODEL", "user.User")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("DATABASE_NAME", "cofedb"),
        'USER' : os.getenv("DATABASE_USER", "postgres"),
        'PASSWORD' : os.getenv("DATABASE_PASSWORD", "postgres"),
        'PORT' : os.getenv("DATABASE_PORT", 5434),
        'HOST' : os.getenv("DATABASE_HOST", "localhost"),
        # "CONN_HEALTH_CHECKS": os.getenv("CONN_HEALTH_CHECKS", True),
        "OPTIONS": {
            "pool": bool(os.getenv("USE_POOL", True))
        }
    }
}


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES" : (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",  
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME" : timedelta(minutes=20),
    "SLIDING_TOKEN_REFRESH_LIFETIME" : timedelta(hours=2),
    "SLIDING_TOKEN_LIFETIME" : timedelta(days=1),
}
if DEBUG:
    SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'] = timedelta(days=30)

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_TZ = True

# config storages
STORAGES = {
    'default':
        {
            'BACKEND': 'django.core.files.storage.FileSystemStorage',
        },
    'staticfiles':
        {
            'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
        }
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.getenv("STATIC_ROOT", BASE_DIR / "static")
MEDIA_URL = "media/"

# django storage settings
USE_DJANGO_STORAGE = os.getenv("USE_DJANGO_STORAGE", False)
if USE_DJANGO_STORAGE == "True":
    STORAGES['default']['BACKEND'] = 'storages.backends.s3.S3Storage'
    # config django storage
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_ENDPOINT_URL = os.getenv("AWS_S3_ENDPOINT_URL")
    AWS_S3_REGION_NAME = os.getenv("AWS_S3_REGION_NAME")
    AWS_DEFAULT_ACL = os.getenv("AWS_DEFAULT_ACL")
    AWS_QUERYSTRING_AUTH = bool(os.getenv("AWS_QUERYSTRING_AUTH", False))
else:
    MEDIA_ROOT = os.getenv("MEDIA_ROOT", BASE_DIR / "media")

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# celery settings
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
CELERY_ACCEPT_CONTENT = os.getenv("CELERY_ACCEPT_CONTENT", ["json"])

# config cache
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": os.getenv("REDIS_URL", "redis://127.0.0.1:6381/1"),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "SOCKET_CONNECT_TIMEOUT": os.getenv("SOCKET_CONNECT_TIMEOUT", 5),
            "SOCKET_TIMEOUT": os.getenv("SOCKET_TIMEOUT", 5),
            "SERIALIZER": os.getenv("REDIS_SERIALIZER", "django_redis.serializers.json.JSONSerializer"),
            "COMPRESSOR": os.getenv("REDIS_COMPRESSOR", "django_redis.compressors.zlib.ZlibCompressor"),
            "COMPRESSOR_KWARGS": {
                "level": int(os.getenv("COMPRESSOR_LEVEL_ARGS", 6))
            },
            "CONNECTION_POOL_KWARGS": {
                "max_connections": os.getenv("REDIS_POOL_MAX_CONNECTION", 100),
                "retry_on_timeout": os.getenv("REDIS_POOL_RETRY_TIMEOUT", True),
                "health_check_interval": bool(os.getenv("REDIS_HEALTH_CHECK_INTERVAL", True)),
                "socket_keepalive": bool(os.getenv("REDIS_SOCKET_KEEPALIVE", True)),
                }
        }
    }
}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
DJANGO_REDIS_IGNORE_EXCEPTIONS = bool(os.getenv("DJANGO_REDIS_IGNORE_EXCEPTIONS", True))
DJANGO_REDIS_LOG_IGNORED_EXCEPTIONS = bool(os.getenv("DJANGO_REDIS_LOG_IGNORED_EXCEPTIONS", True))

# security settings
USE_SSL_CONFIG = bool(os.getenv("USE_SSL_CONFIG", False))
if USE_SSL_CONFIG:
    # Https/ssl settings
    SECURE_SSL_REDIRECT = True # redirec http request into https request
    USE_X_FORWARDED_HOST = True # use header x-forwarded-host
    USE_X_FORWARDED_PORT = True # use header x-forwarded-port 

    # HSTS settings
    SECURE_HSTS_SECONDS = 31536000  # 1 year, hsts validity period
    SECURE_HSTS_PRELOAD = True # 
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True # active hsts into subdomain

    # coockie
    SESSION_COOKIE_SECURE = True # session cookie only https
    SESSION_COOKIE_DOMAIN = os.getenv("SESSION_COOKIE_DOMAIN", "") # for example --> .example.com, domain cookie
    SESSION_COOKIE_HTTPONLY = True # prevent access with by javascript

    # csrf
    CSRF_COOKIE_SECURE = True # send cookie csrf only https
    CSRF_COOKIE_HTTPONLY = True # csrf prevent access javascript
    CSRF_COOKIE_SAMESITE = 'Strict' # Prevent cookie requests on cross-site requests
    CSRF_COOKIE_DOMAIN = os.getenv("CSRF_COOKIE_DOMAIN", "") # for example --> .example.com, domain csrf cookie
    CSRF_COOKIE_AGE = 3600 # csrf cookie validity period

    # Content Security Settings
    SECURE_CONTENT_TYPE_NOSNIFF = True # prevent mime sniffing
    SECURE_BROWSER_XSS_FILTER = True # active filter xss in browser
    SECURE_REFERRER_POLICY = "strict-origin" # control information  on sourse request
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https") 

    # Frame & Clickjacking Protection
    X_FRAME_OPTIONS = "DENY" # prevent show iframe
    
# debug toolbar
DEBUG_TOOLBAR = bool(os.getenv("USE_DEBUG_TOOLBAR", False))
if DEBUG_TOOLBAR:
    INSTALLED_APPS.append("debug_toolbar")
    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")
    INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]

customColorPalette = [
        {
            'color': 'hsl(4, 90%, 58%)',
            'label': 'Red'
        },
        {
            'color': 'hsl(340, 82%, 52%)',
            'label': 'Pink'
        },
        {
            'color': 'hsl(291, 64%, 42%)',
            'label': 'Purple'
        },
        {
            'color': 'hsl(262, 52%, 47%)',
            'label': 'Deep Purple'
        },
        {
            'color': 'hsl(231, 48%, 48%)',
            'label': 'Indigo'
        },
        {
            'color': 'hsl(207, 90%, 54%)',
            'label': 'Blue'
        },
    ]

CKEDITOR_5_CUSTOM_CSS = 'path_to.css' # optional
CKEDITOR_5_FILE_STORAGE = STORAGES['default']['BACKEND']
CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': {
            'items': ['heading', '|', 'bold', 'italic', 'link',
                      'bulletedList', 'numberedList', 'blockQuote', 'imageUpload', ],
                    }

    },
    'extends': {
        'blockToolbar': [
            'paragraph', 'heading1', 'heading2', 'heading3',
            '|',
            'bulletedList', 'numberedList',
            '|',
            'blockQuote',
        ],
        'toolbar': {
            'items': ['heading', '|', 'outdent', 'indent', '|', 'bold', 'italic', 'link', 'underline', 'strikethrough',
                      'code','subscript', 'superscript', 'highlight', '|', 'codeBlock', 'sourceEditing', 'insertImage',
                    'bulletedList', 'numberedList', 'todoList', '|',  'blockQuote', 'imageUpload', '|',
                    'fontSize', 'fontFamily', 'fontColor', 'fontBackgroundColor', 'mediaEmbed', 'removeFormat',
                    'insertTable',
                    ],
            'shouldNotGroupWhenFull': 'true'
        },
        'image': {
            'toolbar': ['imageTextAlternative', '|', 'imageStyle:alignLeft',
                        'imageStyle:alignRight', 'imageStyle:alignCenter', 'imageStyle:side',  '|'],
            'styles': [
                'full',
                'side',
                'alignLeft',
                'alignRight',
                'alignCenter',
            ]

        },
        'table': {
            'contentToolbar': [ 'tableColumn', 'tableRow', 'mergeTableCells',
            'tableProperties', 'tableCellProperties' ],
            'tableProperties': {
                'borderColors': customColorPalette,
                'backgroundColors': customColorPalette
            },
            'tableCellProperties': {
                'borderColors': customColorPalette,
                'backgroundColors': customColorPalette
            }
        },
        'heading' : {
            'options': [
                { 'model': 'paragraph', 'title': 'Paragraph', 'class': 'ck-heading_paragraph' },
                { 'model': 'heading1', 'view': 'h1', 'title': 'Heading 1', 'class': 'ck-heading_heading1' },
                { 'model': 'heading2', 'view': 'h2', 'title': 'Heading 2', 'class': 'ck-heading_heading2' },
                { 'model': 'heading3', 'view': 'h3', 'title': 'Heading 3', 'class': 'ck-heading_heading3' }
            ]
        }
    },
    'list': {
        'properties': {
            'styles': 'true',
            'startIndex': 'true',
            'reversed': 'true',
        }
    }
}

# Define a constant in settings.py to specify file upload permissions
CKEDITOR_5_FILE_UPLOAD_PERMISSION = "staff"  # Possible values: "staff", "authenticated", "any"