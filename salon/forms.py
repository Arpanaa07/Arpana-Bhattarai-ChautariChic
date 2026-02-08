from django import forms
from .models import Salon, SalonPhoto, ServiceCategory, Service, Staff

class SalonRegistrationForm(forms.ModelForm):
    class Meta:
        model = Salon
        fields = [
            'name', 'description', 'location', 'contact_number', 
            'opening_time', 'closing_time', 'logo'
        ]
        widgets = {
            'opening_time': forms.TimeInput(attrs={'type': 'time'}),
            'closing_time': forms.TimeInput(attrs={'type': 'time'}),
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class SalonPhotoForm(forms.ModelForm):
    class Meta:
        model = SalonPhoto
        fields = ['image']

class ServiceCategoryForm(forms.ModelForm):
    class Meta:
        model = ServiceCategory
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Hair Care, Skin Care'}),
        }

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['category', 'name', 'price', 'duration', 'description', 'image', 'is_active']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-input'}),
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Service Name'}),
            'price': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Price in Rs.'}),
            'duration': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': 'Minutes'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Describe the service...'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        salon = kwargs.pop('salon', None)
        super().__init__(*args, **kwargs)
        if salon:
            self.fields['category'].queryset = ServiceCategory.objects.filter(salon=salon)

class StaffForm(forms.ModelForm):
    DAYS_CHOICES = [
        ('Mon', 'Monday'),
        ('Tue', 'Tuesday'),
        ('Wed', 'Wednesday'),
        ('Thu', 'Thursday'),
        ('Fri', 'Friday'),
        ('Sat', 'Saturday'),
        ('Sun', 'Sunday'),
    ]
    
    working_days_list = forms.MultipleChoiceField(
        choices=DAYS_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input-group'}),
        required=True
    )

    class Meta:
        model = Staff
        fields = ['name', 'role', 'phone', 'photo', 'available_from', 'available_to', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Full Name'}),
            'role': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Senior Stylist'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Contact Number'}),
            'available_from': forms.TimeInput(attrs={'class': 'form-input', 'type': 'time'}),
            'available_to': forms.TimeInput(attrs={'class': 'form-input', 'type': 'time'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.working_days:
            # Pre-populate the working_days_list from the comma-separated string
            self.fields['working_days_list'].initial = self.instance.working_days.split(',')

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Convert list of days to comma-separated string
        instance.working_days = ','.join(self.cleaned_data['working_days_list'])
        if commit:
            instance.save()
        return instance
