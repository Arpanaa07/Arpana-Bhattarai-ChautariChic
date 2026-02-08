from django import forms
from .models import Booking
from salon.models import Service, Staff

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['service', 'staff', 'date', 'time', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-input'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-input', 'placeholder': 'Optional notes for your stylist...'}),
            'service': forms.Select(attrs={'class': 'form-input'}),
            'staff': forms.Select(attrs={'class': 'form-input'}),
        }

    def __init__(self, *args, **kwargs):
        salon = kwargs.pop('salon', None)
        super().__init__(*args, **kwargs)
        if salon:
            self.fields['service'].queryset = Service.objects.filter(salon=salon, is_active=True)
            self.fields['staff'].queryset = Staff.objects.filter(salon=salon, is_active=True)
