from django.contrib import admin
from django.urls import path
from .views import data_api



urlpatterns = [
    path('test-api/', data_api.as_view(), name='test-api'),
]