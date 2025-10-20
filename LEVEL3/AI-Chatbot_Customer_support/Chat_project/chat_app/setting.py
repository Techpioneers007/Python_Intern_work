import os
try:
    from dotenv import load_dotenv
except Exception:
    # Minimal fallback to load simple KEY=VALUE .env files when python-dotenv is not installed.
    def load_dotenv(dotenv_path=None):
        path = dotenv_path or '.env'
        try:
            with open(path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue
                    if '=' not in line:
                        continue
                    key, val = line.split('=', 1)
                    key = key.strip()
                    val = val.strip().strip('"').strip("'")
                    if key and key not in os.environ:
                        os.environ[key] = val
        except FileNotFoundError:
            # No .env file present; nothing to load.
            pass
from pathlib import Path

# --- 1. ENVIRONMENT LOADING (Your Code Snippet) ---
# Load environment variables from .env file (must be at the very top)
load_dotenv() 

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# --- 2. CORE SECURITY SETTINGS ---

# IMPORTANT: You must change this in production!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-n2b7=5g@1*k1d0g7k*6k7g$c8n2l9j4x2p8g0v!c9d7q5e3t0f0y')

DEBUG = True

# Allows access from Codespaces development URLs
ALLOWED_HOSTS = ['*'] 


# --- 3. APPLICATION DEFINITION ---

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party Apps for the API
    'rest_framework',
    'corsheaders',

    # Your Chatbot Application
    'chat_app', 
]

MIDDLEWARE = [
    # CORS middleware MUST be placed before CommonMiddleware
    'corsheaders.middleware.CorsMiddleware', 
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# --- 4. CORS CONFIGURATION (Crucial for Codespaces) ---
# Allows any domain to access your API endpoints for development testing.
# This setting is required since your HTML file is served separately from Django.
CORS_ALLOW_ALL_ORIGINS = True


# --- 5. URLS AND TEMPLATES (Standard Django) ---

ROOT_URLCONF = 'myproject.urls'

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

WSGI_APPLICATION = 'myproject.wsgi.application'


# --- 6. DATABASE (Standard SQLite) ---

DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': 'chatbot_db',  # Your desired MongoDB database name
        'CLIENT': {
            'host': 'mongodb://localhost:27017/',
            # IMPORTANT: If your MongoDB is hosted elsewhere (e.g., MongoDB Atlas),
            # replace 'mongodb://localhost:27017/' with your full connection string
            'authMechanism': 'SCRAM-SHA-1', # Default auth mechanism for MongoDB
        }
    }
}

# --- 7. PASSWORD VALIDATION & INTERNATIONALIZATION (Standard Django) ---

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# --- 8. STATIC FILES (Standard Django) ---

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'