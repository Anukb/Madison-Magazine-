from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from .models import Register
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

from django.shortcuts import render, redirect
 import RegistrationForm  # Ensure you have the correct import for your form

def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to login page or any other page after successful registration
            return redirect('login')  # Ensure 'login' matches the name of your login URL
    else:
        form = RegistrationForm()
    
    # Use 'login.html' instead of 'account/register.html'
    return render(request, 'account/login.html', {'form': form})
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'account/login.html')

def forgot_password_view(request):
    # This is a placeholder view for forgot password functionality
    if request.method == 'POST':
        email = request.POST.get('email')
        # Implement your password reset logic here
        messages.info(request, 'Password reset instructions have been sent to your email address.')
        return redirect('login')
    return render(request, 'account/forgot_password.html')

def home_view(request):
    return render(request, 'home.html')
