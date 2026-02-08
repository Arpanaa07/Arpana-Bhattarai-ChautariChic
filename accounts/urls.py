from django.urls import path
from . import views

urlpatterns = [
<<<<<<< HEAD
    # Main authentication URLs
    path('', views.HomeView.as_view(), name='home'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login_page'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
]
=======
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
>>>>>>> 3b4d7d603705a8b1dab8e344cea9f1146bbc2988
