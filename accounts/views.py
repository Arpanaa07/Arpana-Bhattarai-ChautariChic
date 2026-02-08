from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.views import View
from .forms import UserRegistrationForm, UserLoginForm
from .models import User, SalonOwnerProfile, CustomerProfile
from salon.models import Salon

# The HomeView handles the landing page and redirects logged-in users to their correct dashboard
class HomeView(View):
    def get(self, request):
        # If user is logged in, redirect them based on their role
        if request.user.is_authenticated:
            if request.user.user_type == 'super_admin' or request.user.is_superuser:
                return redirect('salon:superadmin_dashboard')
            elif request.user.user_type == 'salon_owner':
                return redirect('salon:dashboard')
            else:
                # Customers stay on home or go to personal dashboard
                return render(request, 'home.html', {'user': request.user})
        
        # If not logged in, show the landing/home page
        return render(request, 'home.html')

# Handles new user registration (Customer or Salon Owner)
class RegisterView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            # Create the user but don't save to DB yet
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.username = user.email # Use email as username
            user.save()

            # Create profiles based on user type
            if user.user_type == 'salon_owner':
                SalonOwnerProfile.objects.create(user=user)
                messages.success(request, "Salon account created! Now register your salon details and wait for admin approval.")
            else:
                CustomerProfile.objects.create(user=user)
                messages.success(request, "Customer registration successful! Please log in.")
            
            return redirect('login_page')
        
        # If form is not valid, show errors on the same page
        return render(request, 'register.html', {'form': form})

# Handles user login with role-based redirection and approval checks
class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('home')
        form = UserLoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)

            if user is not None:
                # Special check for Salon Owners: Salon must be approved
                if user.user_type == 'salon_owner':
                    # Check if they have a salon and if it's approved
                    try:
                        salon = user.salon
                        if not salon.is_approved:
                            messages.warning(request, "Your salon is pending approval. Please wait for the admin to approve it.")
                            return redirect('login_page')
                    except Salon.DoesNotExist:
                        # They haven't created a salon yet, let them log in to create one
                        pass

                # If all checks pass, log the user in
                login(request, user)
                messages.success(request, f"Welcome back, {user.first_name}! Login successful.")
                return redirect('home')
            else:
                messages.error(request, "Invalid email or password. Please try again.")
        
        return render(request, 'login.html', {'form': form})

# Handles user logout
class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.info(request, "You have been logged out successfully.")
        return redirect('login_page')
