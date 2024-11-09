from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import IntegrityError
from .models import Register

def register_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return render(request, 'account/register.html')

        try:
            # Create a new Register instance with plain text password
            new_user = Register(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
            new_user.save()
            messages.success(request, "Registration successful.")
            return redirect('login')
        except IntegrityError:
            messages.error(request, "Username or email already exists.")
            return render(request, 'account/register.html')

    return render(request, 'account/register.html')
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Register

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = Register.objects.get(email=email)
            if user.password == password:  # Direct comparison of plain text passwords
                # Handle user session management
                request.session['user_id'] = user.reg_id  # Save user ID in session
                return redirect('home')
            else:
                messages.error(request, 'Invalid email or password')
        except Register.DoesNotExist:
            messages.error(request, 'Invalid email or password')

    return render(request, 'account/login.html')


def home_view(request):
    return render(request, 'home.html')