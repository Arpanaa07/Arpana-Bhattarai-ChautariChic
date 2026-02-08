from django.db import models
from django.conf import settings

class Salon(models.Model):
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='salon'
    )
    name = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=20)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    logo = models.ImageField(upload_to='salon_logos/', null=True, blank=True)
    is_approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class SalonPhoto(models.Model):
    salon = models.ForeignKey(
        Salon, 
        on_delete=models.CASCADE, 
        related_name='photos'
    )
    image = models.ImageField(upload_to='salon_photos/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Photo for {self.salon.name}"

class ServiceCategory(models.Model):
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Service Categories"
        unique_together = ('salon', 'name')

    def __str__(self):
        return f"{self.name} ({self.salon.name})"

class Service(models.Model):
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='services')
    category = models.ForeignKey(ServiceCategory, on_delete=models.CASCADE, related_name='services')
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='service_images/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.salon.name}"

class Staff(models.Model):
    salon = models.ForeignKey(Salon, on_delete=models.CASCADE, related_name='staff')
    name = models.CharField(max_length=150)
    role = models.CharField(max_length=100, help_text="e.g. Hairdresser, Makeup Artist")
    phone = models.CharField(max_length=20)
    photo = models.ImageField(upload_to='staff_photos/', null=True, blank=True)
    available_from = models.TimeField()
    available_to = models.TimeField()
    working_days = models.CharField(max_length=100, help_text="Comma-separated days, e.g. Mon,Tue,Wed")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Staff"

    def __str__(self):
        return f"{self.name} ({self.role}) - {self.salon.name}"
