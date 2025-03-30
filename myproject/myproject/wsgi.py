# wsgi.py
import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.py')

application = get_wsgi_application()

application = WhiteNoise(application, root="./../staticfiles")
application.add_files("./static", prefix="more-files/")