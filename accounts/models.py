<<<<<<< HEAD
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('super_admin', 'Super Admin'),
        ('salon_owner', 'Salon Owner'),
        ('customer', 'Customer'),
    )
    
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='customer')
    phone_number = models.CharField(max_length=15, unique=True, null=True, blank=True)
    
    def __str__(self):
        return self.email

class SalonOwnerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='salon_owner_profile')
    salon_name = models.CharField(max_length=200, blank=True)
    address = models.TextField(blank=True)
    is_approved = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.email} - {self.salon_name}"

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer_profile')
    date_of_birth = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.user.email
        
=======
from django.db import models

# Create your models here.
>>>>>>> 3b4d7d603705a8b1dab8e344cea9f1146bbc2988
