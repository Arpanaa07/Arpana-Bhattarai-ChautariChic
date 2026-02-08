from django import forms
from .models import User, SalonOwnerProfile, CustomerProfile

class UserRegistrationForm(forms.ModelForm):
    # We add password fields manually to the form to handle confirmation
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-input',
        'placeholder': 'Create a password'
    }))
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-input',
        'placeholder': 'Confirm your password'
    }), label="Confirm Password")

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone_number', 'user_type']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'you@example.com'}),
            'first_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Last Name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone Number'}),
            'user_type': forms.Select(attrs={'class': 'form-input'}),
        }

    # This function checks if passwords match
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords do not match!")
        return cleaned_data

class UserLoginForm(forms.Form):
    # Simple email and password form for login
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-input',
        'placeholder': 'you@example.com'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-input',
        'placeholder': 'Enter your password'
    }))
