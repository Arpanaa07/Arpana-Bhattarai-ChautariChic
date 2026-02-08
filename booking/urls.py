from django.urls import path
from . import views

app_name = 'booking'

urlpatterns = [
    path('book/<int:salon_id>/', views.BookServiceView.as_view(), name='book_service'),
    path('my-bookings/', views.MyBookingsView.as_view(), name='my_bookings'),
    path('salon/appointments/', views.SalonAppointmentsView.as_view(), name='salon_appointments'),
    path('salon/appointments/<int:pk>/update/<str:status>/', views.UpdateBookingStatusView.as_view(), name='update_status'),
]
