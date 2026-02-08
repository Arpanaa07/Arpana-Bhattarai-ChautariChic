from django.contrib import admin
<<<<<<< HEAD
from django.contrib.auth.admin import UserAdmin
from .models import User, SalonOwnerProfile, CustomerProfile

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'user_type', 'is_staff')
    list_filter = ('user_type', 'is_staff', 'is_superuser')
    
    # customizing fieldsets
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'user_type')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # creating a new user in admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'user_type', 'password1', 'password2'),
        }),
    )
    
    #  match custom User model
    ordering = ('email',)
    search_fields = ('email', 'first_name', 'last_name')

#  unregister 
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass  

# register 
admin.site.register(User, CustomUserAdmin)
admin.site.register(SalonOwnerProfile)
admin.site.register(CustomerProfile)

=======

# Register your models here.
>>>>>>> 3b4d7d603705a8b1dab8e344cea9f1146bbc2988
