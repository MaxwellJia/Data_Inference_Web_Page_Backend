
INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'csvhandler',             # New apps
    'rest_framework',         # REST API support
    'corsheaders',            # Cross-domain support
    'myproject'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # CROSS ORIGIN REQUESTS ARE ALLOWED
]

CORS_ALLOW_ALL_ORIGINS = True # Cross-origin requests from all sources are allowed, which is convenient for development, but the production environment needs to be more stringent
ALLOWED_HOSTS = ['*'] # All hosts should be allowed to access, and the production environment should specify a specific domain name
DEBUG = True # Turn on the debug mode, display a detailed error message, and the production environment should be shut down
ROOT_URLCONF = 'myproject.urls' # Configure the URL of the project and define the routing rules
SECRET_KEY = '123456' # Keys used for operations such as encryption, production environments should use more complex and confidential keys



