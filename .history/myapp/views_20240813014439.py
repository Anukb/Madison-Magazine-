from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login as auth_login
from .models import Register, Login

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            register = Register.objects.get(username=username, password=password)
            print(f"Register object retrieved: {register}")  # Debugging statement
            
            login = Login(reg_id=register, email=register.email, password=register.password)
            login.save()
            print(f"Login object saved: {login}")  # Debugging statement
            
            auth_login(request, register)  # Assuming you have a custom authentication backend
            return redirect('home')
        except Register.DoesNotExist:
            messages.error(request, 'Invalid username or password.')
            print("Register object not found")  # Debugging statement
        except Exception as e:
            messages.error(request, 'An error occurred during login.')
            print(f"Exception occurred: {e}")  # Debugging statement
    
    return render(request, 'account/login.html')