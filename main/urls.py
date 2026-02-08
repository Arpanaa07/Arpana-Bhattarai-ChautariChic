# main/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Example path
    path('', views.home, name='home'),
]
