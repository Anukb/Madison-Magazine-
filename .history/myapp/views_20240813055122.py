from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from .models import Register, Login
from django.http import HttpResponseBadRequest
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
            return redirect('profile')

from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Register, Login
from django.contrib.auth import login as auth_login

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # Retrieve the user from the Register model
            register = Register.objects.get(email=email)

            # Check if the password matches using hashing
            if check_password(password, register.password):
                # Create a Login entry
                login_entry = Login(reg_id=register, email=register.email)
                login_entry.save()
                print(f"Login object saved: {login_entry}")  # Debugging statement

                # Log in the user (create a session)
                auth_login(request, register)

                # Redirect to the home page
                return redirect('home')
            else:
                messages.error(request, 'Invalid email or password.')
                print("Password mismatch")  # Debugging statement

        except Register.DoesNotExist:
            messages.error(request, 'User does not exist.')
            print("User does not exist")  # Debugging statement

        except Exception as e:
            messages.error(request, 'An error occurred during login.')
            print(f"Exception occurred: {e}")  # Debugging statement

    return render(request, 'account/login.html')



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
def profile_view(request):
    try:
        # Retrieve the user from the Register model using email
        user = Register.objects.get(email=request.user.email)
        return render(request, 'account/profile.html', {'user': user})
    except Register.DoesNotExist:
        messages.error(request, 'User does not exist.')
        return redirect('home')