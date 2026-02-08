from django.urls import path
from . import views

urlpatterns = [
    # Main authentication URLs
    path('', views.HomeView.as_view(), name='home'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login_page'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]