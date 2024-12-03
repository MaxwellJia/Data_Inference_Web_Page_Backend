# myproject/urls.py
from django.urls import path, include

from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('api/', include('csvhandler.urls')),  # CSV handles API routing
    path('admin/', admin.site.urls),
]


