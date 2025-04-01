# INSTALLED_APPS configuration list. Contains Django default apps and your own applications.
import os

from sympy import false

INSTALLED_APPS = [
    # Django default applications configuration
    'django.contrib.admin',  # Django admin site for managing your models and data through a UI
    'django.contrib.auth',   # Authentication system for user login, password management, and permissions
    'django.contrib.contenttypes',  # Content type framework for handling generic relationships between models
    'django.contrib.sessions',  # Session management for storing data during a user's visit across requests
    'django.contrib.messages',  # Message framework for passing notifications between requests
    'django.contrib.staticfiles',  # Static files handling (CSS, JavaScript, images)


    'whitenoise.runserver_nostatic', # white noise for azure

    # Your custom applications
    'csvhandler',  # My custom app for handling CSV file processing
    'rest_framework',  # Django REST Framework for building RESTful APIs
    'corsheaders',  # Middleware for handling cross-origin requests (CORS)
    'myproject'  # The main project app (if any)
]

# MIDDLEWARE configuration list, which handles request and response processing
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Middleware to allow cross-origin requests

    # Django default middleware for security, session, authentication, and other functionalities
    'django.middleware.security.SecurityMiddleware',  # Security middleware to handle HTTP security headers
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # Manages sessions between requests for user data
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Handles user authentication across requests
    'django.contrib.messages.middleware.MessageMiddleware',  # Handles message notifications across requests
    'django.middleware.common.CommonMiddleware',  # Provides various common middleware functionalities like URL rewriting
    'django.middleware.csrf.CsrfViewMiddleware',  # CSRF protection middleware to prevent cross-site request forgery
    'django.middleware.locale.LocaleMiddleware',  # Manages user language preferences
    'django.middleware.http.ConditionalGetMiddleware',  # Handles conditional GET requests to reduce bandwidth
    'django.middleware.gzip.GZipMiddleware',  # Compresses responses using GZIP for improved performance
]

# TEMPLATES configuration for rendering HTML files with context
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # Use Django's template engine
        'DIRS': [],  # If you have custom template directories, you can list them here
        'APP_DIRS': True,  # Enable searching for templates in each app's "templates" folder
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',  # Adds debug context to templates
                'django.template.context_processors.request',  # Adds request context (e.g., user info)
                'django.contrib.auth.context_processors.auth',  # Adds authenticated user context
                'django.contrib.messages.context_processors.messages',  # Adds message notifications context
            ],
        },
    },
]

# Allow some front end to access back end in Azure
CSRF_TRUSTED_ORIGINS = [
    "https://icy-tree-0067c3610.6.azurestaticapps.net"
]

CSRF_COOKIE_SECURE = True  # 仅在 HTTPS 传输


# STATIC_URL configuration, used for serving staticfiles files
STATIC_URL = './static/'  # The URL path for staticfiles files (CSS, JS, images)
STATIC_ROOT = os.path.join('./', 'staticfiles')

# Optional: If you need to load staticfiles files in development, you can specify directories here
# if DEBUG:
#     STATICFILES_DIRS = [
#         BASE_DIR / "staticfiles",  # Your staticfiles files directory
#     ]

# CORS configuration - Allow cross-origin requests from all domains (useful for development)
CORS_ALLOW_ALL_ORIGINS = True  # Allow requests from all origins, should be more restrictive in production

# ALLOWED_HOSTS defines which domains can access your Django app (use '*' for all domains in development)
ALLOWED_HOSTS = ['*']  # Allow all hosts in development, but should be restricted to specific domain names in production


# DEBUG setting - turns on debugging and detailed error messages (set to False in production)
DEBUG = false  # Enable debug mode for more detailed error messages during development

# ROOT_URLCONF configuration to specify the root URL configuration module
ROOT_URLCONF = 'myproject.urls'  # Defines the URL routing for the project

# SECRET_KEY is used for cryptographic operations such as signing cookies, tokens, etc. (keep it secure)
SECRET_KEY = '147258j'  # Change this to a secure, random key in production

# DATABASE configuration for connecting to the database
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',  # Database myproject, here we use PostgreSQL (change to MySQL if needed)
#         'NAME': 'postgres',  # The name of the database
#         'USER': 'postgres',  # Database username
#         'PASSWORD': 'Thisiswangtao',  # Database password
#         'HOST': 'database-1-instance-1.c1gce6c08np7.ap-southeast-2.rds.amazonaws.com',  # Database host (RDS endpoint for example)
#         'PORT': '5432',  # Database port (default PostgreSQL port is 5432)
#     }
# }

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# import os
# import sys
#
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(os.path.join(BASE_DIR, "myproject"))  # 确保 csvhandler 可被找到


