

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
    user = request.user  # Get the currently logged-in user
    return render(request, 'account/profile.html', {'user': user})