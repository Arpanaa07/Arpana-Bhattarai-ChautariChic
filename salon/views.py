from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, UpdateView, DetailView, ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import get_user_model
from .models import Salon, SalonPhoto, ServiceCategory, Service, Staff
from .forms import SalonRegistrationForm, ServiceCategoryForm, ServiceForm, StaffForm
from booking.models import Booking

User = get_user_model()

# Mixin to ensure only Salon Owners can access certain pages
class SalonOwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.user_type == 'salon_owner'

# Mixin to ensure only Super Admins (or staff) can access administration pages
class SuperAdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and (self.request.user.user_type == 'super_admin' or self.request.user.is_superuser)

# View for owners to register their salon after creating a user account
class SalonRegisterView(LoginRequiredMixin, SalonOwnerRequiredMixin, CreateView):
    model = Salon
    form_class = SalonRegistrationForm
    template_name = 'salon/register.html'
    success_url = reverse_lazy('salon:dashboard')

    # If they already have a salon, don't let them register another one
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and Salon.objects.filter(owner=request.user).exists():
            return redirect('salon:dashboard')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.owner = self.request.user
        messages.success(self.request, "Salon registration submitted! Please wait for administrative approval.")
        return super().form_valid(form)

# Private dashboard for Salon Owners
class SalonDashboardView(LoginRequiredMixin, SalonOwnerRequiredMixin, DetailView):
    model = Salon
    template_name = 'salon/dashboard.html'
    context_object_name = 'salon'

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except:
            # If they don't have a salon yet, send them to register one
            messages.info(request, "Please register your salon details first.")
            return redirect('salon:register')
        
        # Check if approved before showing full dashboard
        if not self.object.is_approved:
            messages.warning(request, "Your salon is still pending approval. Some features are hidden.")
            
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        salon = self.object
        context['total_bookings_count'] = salon.bookings.count()
        context['active_services_count'] = salon.services.filter(is_active=True).count()
        context['staff_count'] = salon.staff.count()
        context['recent_bookings'] = salon.bookings.all().order_by('-created_at')[:5]
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Salon, owner=self.request.user)

# View for owners to edit their salon profile
class SalonEditView(LoginRequiredMixin, SalonOwnerRequiredMixin, UpdateView):
    model = Salon
    form_class = SalonRegistrationForm
    template_name = 'salon/edit_salon.html'
    success_url = reverse_lazy('salon:dashboard')

    def get_object(self, queryset=None):
        return get_object_or_404(Salon, owner=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, "Salon profile updated successfully.")
        return super().form_valid(form)

# Administration Dashboard for Super Admins to moderate salons
class SuperAdminDashboardView(LoginRequiredMixin, SuperAdminRequiredMixin, ListView):
    model = Salon
    template_name = 'salon/superadmin_dashboard.html'
    context_object_name = 'salons'
    queryset = Salon.objects.all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_users'] = User.objects.count()
        context['pending_salons_count'] = Salon.objects.filter(is_approved=False).count()
        context['total_bookings'] = Booking.objects.count()
        return context

# Admin View to List All Salons
class AdminSalonListView(LoginRequiredMixin, SuperAdminRequiredMixin, ListView):
    model = Salon
    template_name = 'salon/admin_salon_list.html'
    context_object_name = 'salons'
    queryset = Salon.objects.all().order_by('-created_at')

# Admin View to List All Users
class AdminUserListView(LoginRequiredMixin, SuperAdminRequiredMixin, ListView):
    model = User
    template_name = 'salon/admin_user_list.html'
    context_object_name = 'users'
    queryset = User.objects.all().order_by('-date_joined')

# Action to Approve a Salon
class ApproveSalonView(LoginRequiredMixin, SuperAdminRequiredMixin, View):
    def post(self, request, pk):
        salon = get_object_or_404(Salon, pk=pk)
        salon.is_approved = True
        salon.save()
        messages.success(request, f"Salon '{salon.name}' has been approved.")
        return redirect('salon:superadmin_dashboard')

# Action to Reject/Unapprove a Salon
class RejectSalonView(LoginRequiredMixin, SuperAdminRequiredMixin, View):
    def post(self, request, pk):
        salon = get_object_or_404(Salon, pk=pk)
        salon.is_approved = False
        salon.save()
        messages.warning(request, f"Salon '{salon.name}' has been rejected.")
        return redirect('salon:superadmin_dashboard')

# Action to Toggle Salon Visibility (Active/Inactive)
class ToggleSalonActiveView(LoginRequiredMixin, SuperAdminRequiredMixin, View):
    def post(self, request, pk):
        salon = get_object_or_404(Salon, pk=pk)
        salon.is_active = not salon.is_active
        salon.save()
        status = "enabled" if salon.is_active else "disabled"
        messages.info(request, f"Salon '{salon.name}' is now {status}.")
        return redirect('salon:superadmin_dashboard')
# --- Service Category Management ---

class CategoryListView(LoginRequiredMixin, SalonOwnerRequiredMixin, ListView):
    model = ServiceCategory
    template_name = 'salon/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        salon = get_object_or_404(Salon, owner=self.request.user)
        return ServiceCategory.objects.filter(salon=salon)

class CategoryCreateView(LoginRequiredMixin, SalonOwnerRequiredMixin, CreateView):
    model = ServiceCategory
    form_class = ServiceCategoryForm
    template_name = 'salon/category_form.html'
    success_url = reverse_lazy('salon:category_list')

    def form_valid(self, form):
        form.instance.salon = get_object_or_404(Salon, owner=self.request.user)
        messages.success(self.request, "Category created successfully.")
        return super().form_valid(form)

class CategoryUpdateView(LoginRequiredMixin, SalonOwnerRequiredMixin, UpdateView):
    model = ServiceCategory
    form_class = ServiceCategoryForm
    template_name = 'salon/category_form.html'
    success_url = reverse_lazy('salon:category_list')

    def get_queryset(self):
        salon = get_object_or_404(Salon, owner=self.request.user)
        return ServiceCategory.objects.filter(salon=salon)

class CategoryDeleteView(LoginRequiredMixin, SalonOwnerRequiredMixin, View):
    def post(self, request, pk):
        salon = get_object_or_404(Salon, owner=request.user)
        category = get_object_or_404(ServiceCategory, pk=pk, salon=salon)
        category.delete()
        messages.success(request, "Category deleted successfully.")
        return redirect('salon:category_list')

# --- Service Management ---

class ServiceListView(LoginRequiredMixin, SalonOwnerRequiredMixin, ListView):
    model = Service
    template_name = 'salon/service_list.html'
    context_object_name = 'services'

    def get_queryset(self):
        salon = get_object_or_404(Salon, owner=self.request.user)
        return Service.objects.filter(salon=salon).select_related('category')

class ServiceCreateView(LoginRequiredMixin, SalonOwnerRequiredMixin, CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'salon/service_form.html'
    success_url = reverse_lazy('salon:service_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['salon'] = get_object_or_404(Salon, owner=self.request.user)
        return kwargs

    def form_valid(self, form):
        form.instance.salon = get_object_or_404(Salon, owner=self.request.user)
        messages.success(self.request, "Service added successfully.")
        return super().form_valid(form)

class ServiceUpdateView(LoginRequiredMixin, SalonOwnerRequiredMixin, UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = 'salon/service_form.html'
    success_url = reverse_lazy('salon:service_list')

    def get_queryset(self):
        salon = get_object_or_404(Salon, owner=self.request.user)
        return Service.objects.filter(salon=salon)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['salon'] = get_object_or_404(Salon, owner=self.request.user)
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, "Service updated successfully.")
        return super().form_valid(form)

class ServiceDeleteView(LoginRequiredMixin, SalonOwnerRequiredMixin, View):
    def post(self, request, pk):
        salon = get_object_or_404(Salon, owner=request.user)
        service = get_object_or_404(Service, pk=pk, salon=salon)
        service.delete()
        messages.success(request, "Service deleted successfully.")
        return redirect('salon:service_list')

# --- Staff Management ---

class StaffListView(LoginRequiredMixin, SalonOwnerRequiredMixin, ListView):
    model = Staff
    template_name = 'salon/staff_list.html'
    context_object_name = 'staff_members'

    def get_queryset(self):
        salon = get_object_or_404(Salon, owner=self.request.user)
        return Staff.objects.filter(salon=salon).order_by('name')

class StaffCreateView(LoginRequiredMixin, SalonOwnerRequiredMixin, CreateView):
    model = Staff
    form_class = StaffForm
    template_name = 'salon/staff_form.html'
    success_url = reverse_lazy('salon:staff_list')

    def form_valid(self, form):
        form.instance.salon = get_object_or_404(Salon, owner=self.request.user)
        messages.success(self.request, f"Staff member '{form.instance.name}' added successfully.")
        return super().form_valid(form)

class StaffUpdateView(LoginRequiredMixin, SalonOwnerRequiredMixin, UpdateView):
    model = Staff
    form_class = StaffForm
    template_name = 'salon/staff_form.html'
    success_url = reverse_lazy('salon:staff_list')

    def get_queryset(self):
        salon = get_object_or_404(Salon, owner=self.request.user)
        return Staff.objects.filter(salon=salon)

    def form_valid(self, form):
        messages.success(self.request, "Staff profile updated successfully.")
        return super().form_valid(form)

class StaffDeleteView(LoginRequiredMixin, SalonOwnerRequiredMixin, View):
    def post(self, request, pk):
        salon = get_object_or_404(Salon, owner=request.user)
        member = get_object_or_404(Staff, pk=pk, salon=salon)
        name = member.name
        member.delete()
        return redirect('salon:staff_list')

# --- Public Customer Views ---

class PublicSalonListView(ListView):
    model = Salon
    template_name = 'salon/public_salon_list.html'
    context_object_name = 'salons'
    
    def get_queryset(self):
        # Show all approved and active salons
        return Salon.objects.filter(is_approved=True, is_active=True).order_by('name')

class PublicSalonDetailView(DetailView):
    model = Salon
    template_name = 'salon/public_salon_detail.html'
    context_object_name = 'salon'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        salon = self.object
        # Group services by category for display
        services = salon.services.filter(is_active=True).select_related('category').order_by('category__name', 'name')
        
        # Grouping logic
        grouped_services = {}
        for service in services:
            cat_name = service.category.name if service.category else "Uncategorized"
            if cat_name not in grouped_services:
                grouped_services[cat_name] = []
            grouped_services[cat_name].append(service)
            
        context['grouped_services'] = grouped_services
        context['staff_members'] = salon.staff.filter(is_active=True)
        return context
