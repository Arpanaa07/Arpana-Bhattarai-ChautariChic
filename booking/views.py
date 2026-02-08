from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Booking
from .forms import BookingForm
from salon.models import Salon, Service
from django.utils import timezone

class BookServiceView(LoginRequiredMixin, CreateView):
    model = Booking
    form_class = BookingForm
    template_name = 'booking/book_service.html'
    success_url = reverse_lazy('booking:my_bookings')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        salon_id = self.kwargs.get('salon_id')
        kwargs['salon'] = get_object_or_404(Salon, pk=salon_id)
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        service_id = self.request.GET.get('service')
        if service_id:
            try:
                service = Service.objects.get(pk=service_id, salon__pk=self.kwargs.get('salon_id'))
                initial['service'] = service
            except Service.DoesNotExist:
                pass
        return initial

    def form_valid(self, form):
        salon_id = self.kwargs.get('salon_id')
        form.instance.customer = self.request.user
        form.instance.salon = get_object_or_404(Salon, pk=salon_id)
        messages.success(self.request, "Booking requested! Please wait for confirmation.")
        return super().form_valid(form)

class MyBookingsView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'booking/my_bookings_v2.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        return Booking.objects.filter(customer=self.request.user).order_by('-created_at')

class SalonAppointmentsView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'booking/salon_bookings.html'
    context_object_name = 'appointments'

    def get_queryset(self):
        salon = get_object_or_404(Salon, owner=self.request.user)
        return Booking.objects.filter(salon=salon).order_by('-date', '-time')

class UpdateBookingStatusView(LoginRequiredMixin, View):
    def post(self, request, pk, status):
        salon = get_object_or_404(Salon, owner=request.user)
        booking = get_object_or_404(Booking, pk=pk, salon=salon)
        
        if status.upper() in ['CONFIRMED', 'COMPLETED', 'CANCELLED']:
            booking.status = status.upper()
            booking.save()
            messages.success(request, f"Booking status updated to {status.capitalize()}.")
        
        return redirect('booking:salon_appointments')
