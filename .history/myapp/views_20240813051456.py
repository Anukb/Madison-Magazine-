from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from .models import Register, Login

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        # Basic validation
        if not username or not email or not password or not confirm_password:
            messages.error(request, 'Please fill out all fields.')
        elif password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        elif Register.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        elif Register.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
        else:
            # Create new user
            register = Register(
                username=username,
                email=email,
                password=password,
                confirm_password=confirm_password,
                first_name=first_name,
                last_name=last_name
            )
            register.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')




def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        # Implement your password reset logic here
        messages.info(request, 'Password reset instructions have been sent to your email address.')
        return redirect('login')
    return render(request, 'account/forgot_password.html')

def home_view(request):
    return render(request, 'home.html')

def subscribe_view(request):
    return render(request, 'subscription.html')

def payment_view(request):
    plan = request.GET.get('plan', '')
    return render(request, 'payment.html', {'plan': plan})

def process_payment_view(request):
    if request.method == 'POST':
        # Process the payment logic here
        pass
    return redirect('home')