from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# ======================
# 🔐 SECURITY
# ======================
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-change-me')

DEBUG = os.getenv('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['*']  # en prod mets ton domaine

CSRF_TRUSTED_ORIGINS = [
    'https://cti-projet.onrender.com'
]

# ======================
# 📦 APPS
# ======================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # tes apps
    'accounts',
    'academics',
    'courses',
    'evaluations',
    'deliberation',
    'payments',
    'reports',
]

# ======================
# ⚙️ MIDDLEWARE
# ======================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # 🔥 IMPORTANT pour production
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ======================
# 🌐 URLS
# ======================
ROOT_URLCONF = 'cti_project.urls'

# ======================
# 🧩 TEMPLATES
# ======================
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
                'accounts.context_processors.user_roles',
            ],
        },
    },
]

WSGI_APPLICATION = 'cti_project.wsgi.application'

# ======================
# 🛢️ DATABASE (POSTGRES DOCKER)
# ======================
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'cti_db'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'postgress'),
        'HOST': os.getenv('DB_HOST', 'db'),  # docker service
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# ======================
# 🔑 PASSWORD VALIDATION
# ======================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ======================
# 🌍 INTERNATIONAL
# ======================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ======================
# 📁 STATIC FILES
# ======================
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# 🔥 production static
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ======================
# 🔐 AUTH
# ======================
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/login/'

# ======================
# ⚡ PERFORMANCE
# ======================
DATA_UPLOAD_MAX_NUMBER_FIELDS = 50000

# ======================
# 🔐 SECURITY HEADERS
# ======================
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True

# ======================
# 🪵 LOGGING
# ======================
LOGGING = {
    'version': 1,
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'security.log',
        },
    },
    'loggers': {
        'django.security': {
            'handlers': ['file'],
            'level': 'WARNING',
        },
    },
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ======================
# 📧 EMAIL (⚠️ à sécuriser)
# ======================
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = os.getenv('EMAIL_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASSWORD')