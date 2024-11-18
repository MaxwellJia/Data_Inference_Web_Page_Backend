# csvhandler/urls.py
from django.urls import path
from .views import CSVUploadView, CSVTypesView, CSVSaveViewAndDownload

urlpatterns = [
    path('upload/', CSVUploadView.as_view(), name='csv-upload'),
    path('types/', CSVTypesView.as_view(), name='csv-types'),
    path('save-types/', CSVSaveViewAndDownload().as_view(), name='csv-save'),
]
