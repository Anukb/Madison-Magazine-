from django.shortcuts import render, redirect
from django.contrib import messages
from .models import reg,log

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        # Create a new Register instance
        register = Register(username=username, email=email, password=password,
                            confirm_password=confirm_password, first_name=first_name,
                            last_name=last_name)
        register.save()
        
        messages.success(request, 'Registration successful. You can now log in.')
        return redirect('login')  # Redirect to the login page after registration
    
    return render(request, 'registration/register.html')
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate the user using Django's User model
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')  # Redirect to a success page or home page
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'account/login.html')
from django.shortcuts import render

def home_view(request):
    return render(request, 'home.html')


