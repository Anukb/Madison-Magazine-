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

from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Register, Login

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Authenticate user
        user = authenticate(request, email=email, password=password)
        if user is not None:
            # User is authenticated
            try:
                register = Register.objects.get(email=email)
                print(f"Register object retrieved: {register}")  # Debugging statement

                # Create a Login entry
                login_entry = Login(reg_id=register, email=register.email, password=register.password)
                login_entry.save()
                print(f"Login object saved: {login_entry}")  # Debugging statement

                # Log in the user
                auth_login(request, user)

                # Redirect to the home page
                return redirect('home')

            except Register.DoesNotExist:
                messages.error(request, 'Register object not found.')
                print("Register object not found")  # Debugging statement

            except Exception as e:
                messages.error(request, 'An error occurred during login.')
                print(f"Exception occurred: {e}")  # Debugging statement

        else:
            messages.error(request, 'Invalid username or password.')
            print("Authentication failed")  # Debugging statement

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