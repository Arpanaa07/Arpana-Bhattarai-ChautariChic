from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from accounts.views import HomeView, LoginView, LogoutView

urlpatterns = [
    # Admin Panel
    path('admin/', admin.site.urls),
    
    # Homepage
    path('', HomeView.as_view(), name='home'),
    
    # Simple Authentication
    path('login/', LoginView.as_view(), name='login_page'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # App URLs
    path('api/accounts/', include('accounts.urls')),
    path('salon/', include('salon.urls')),
    path('bookings/', include('booking.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)