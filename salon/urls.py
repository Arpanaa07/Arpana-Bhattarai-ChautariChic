from django.urls import path
from . import views

app_name = 'salon'

urlpatterns = [
    path('register/', views.SalonRegisterView.as_view(), name='register'),
    path('dashboard/', views.SalonDashboardView.as_view(), name='dashboard'),
    path('edit/', views.SalonEditView.as_view(), name='edit'),
    path('admin/dashboard/', views.SuperAdminDashboardView.as_view(), name='superadmin_dashboard'),
    path('admin/approve/<int:pk>/', views.ApproveSalonView.as_view(), name='approve_salon'),
    path('admin/reject/<int:pk>/', views.RejectSalonView.as_view(), name='reject_salon'),
    path('admin/toggle-active/<int:pk>/', views.ToggleSalonActiveView.as_view(), name='toggle_salon_active'),
    path('admin/salons/', views.AdminSalonListView.as_view(), name='admin_salon_list'),
    path('admin/users/', views.AdminUserListView.as_view(), name='admin_user_list'),

    # Service Category Management
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/add/', views.CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/edit/', views.CategoryUpdateView.as_view(), name='category_edit'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category_delete'),

    # Service Management
    path('services/', views.ServiceListView.as_view(), name='service_list'),
    path('services/add/', views.ServiceCreateView.as_view(), name='service_create'),
    path('services/<int:pk>/edit/', views.ServiceUpdateView.as_view(), name='service_edit'),
    path('services/<int:pk>/delete/', views.ServiceDeleteView.as_view(), name='service_delete'),

    # Staff Management
    path('staff/', views.StaffListView.as_view(), name='staff_list'),
    path('staff/add/', views.StaffCreateView.as_view(), name='staff_create'),
    path('staff/<int:pk>/edit/', views.StaffUpdateView.as_view(), name='staff_edit'),
    path('staff/<int:pk>/delete/', views.StaffDeleteView.as_view(), name='staff_delete'),
    path('staff/<int:pk>/delete/', views.StaffDeleteView.as_view(), name='staff_delete'),

    # Public Customer Views
    path('salons/', views.PublicSalonListView.as_view(), name='public_salon_list'),
    path('salons/<int:pk>/', views.PublicSalonDetailView.as_view(), name='public_salon_detail'),
]
