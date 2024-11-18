# myproject/urls.py
from django.urls import path, include

urlpatterns = [
    path('api/', include('csvhandler.urls')),  # CSV handles API routing
]


