from django.contrib import admin
from .models import Salon, SalonPhoto

@admin.register(Salon)
class SalonAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'location', 'is_approved', 'is_active', 'created_at')
    list_filter = ('is_approved', 'is_active')
    search_fields = ('name', 'owner__email', 'location')

@admin.register(SalonPhoto)
class SalonPhotoAdmin(admin.ModelAdmin):
    list_display = ('salon', 'created_at')
