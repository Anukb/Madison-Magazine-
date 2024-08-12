from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Register

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
