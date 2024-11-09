from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from .models import Category, Articles
from django.shortcuts import get_object_or_404, redirect
import json
from django.core.files.storage import FileSystemStorage


def edit_profile_view(request):
    profile = request.user.profile  # Assuming Profile is linked to User via a OneToOneField

    if request.method == 'POST':
        # Update User fields
        request.user.first_name = request.POST.get('first_name')
        request.user.last_name = request.POST.get('last_name')
        request.user.email = request.POST.get('email')

        # Update Profile fields
        profile.user_type = request.POST.get('user_type')
        profile.bio = request.POST.get('bio')

        # Save the updates
        request.user.save()
        profile.save()

        messages.success(request, 'Your profile has been updated!')
        return redirect('profile')  # Redirect to the profile page

    return render(request, 'account/edit_profile.html', {'profile': profile})

@login_required
def profile_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        
        # Update user details
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        
        messages.success(request, 'Your profile has been updated.')
        return redirect('profile')

    return render(request, 'account/profile.html')

def home_view(request):
    articles = Articles.objects.all()  # Fetch all articles
    return render(request, 'home.html', {'articles': articles})


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        # Validate name is alphabetic
        if not first_name.isalpha() or not last_name.isalpha():
            messages.error(request, 'First name and last name should only contain alphabets.')
            return redirect('register')

        # Validate password match
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

        # Check for existing username or email
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('register')

        # Create the new user
        user = User.objects.create_user(username=username, email=email, password=password,
                                        first_name=first_name, last_name=last_name)
        user.save()

        messages.success(request, 'Registration successful. You can now log in.')
        return redirect('login')

    return render(request, 'account/register.html')


def check_username(request):
    username = request.GET.get('username')
    exists = User.objects.filter(username=username).exists()
    return JsonResponse({'exists': exists})  # Return a JSON response with the existence status


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid email or password.')
        except User.DoesNotExist:
            messages.error(request, 'No user found with that email address.')

    return render(request, 'account/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')


def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            # Generate a password reset link/token (you can customize this part)
            token = get_random_string(length=32)
            # Save the token to the user model or handle it as you need
            
            # Send email with reset link
            reset_link = f"http://yourdomain.com/reset-password/{token}/"  # Update with your domain
            send_mail(
                'Password Reset Request',
                f'Click the link to reset your password: {reset_link}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            messages.success(request, 'Password reset email has been sent.')
        except User.DoesNotExist:
            messages.error(request, 'No user found with that email address.')

    return render(request, 'accounts/forgot_password.html', {})

def admin_login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Check if the credentials are correct
        if username == "admin@gmail.com" and password == "admin":
            # Redirect to the admin dashboard if credentials are correct
            return redirect("admin_dashboard")  # Ensure 'admin_dashboard' URL is defined
        else:
            # Display an error message if credentials are incorrect
            messages.error(request, "Invalid username or password.")
            
    return render(request, "account/admin_login.html")

def admin_dashboard_view(request):
    categories = Category.objects.all()
    return render(request, 'account/admin_dashboard.html', {'categories': categories})

def add_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        category_description = request.POST.get('category_description')

        # Create a new category
        Category.objects.create(
            name=category_name,
            description=category_description  # Ensure this is correct
        )
        messages.success(request, "Category added successfully!")
        return redirect('admin_dashboard')
    return render(request, 'admin_dashboard.html')

def delete_category(request, category_id):
    if request.method == "POST":
        category = get_object_or_404(Category, id=category_id)
        category.delete()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False})

def update_category(request, category_id):
    if request.method == 'POST':
        # Extract the data sent from the request
        data = json.loads(request.body)
        name = data.get('name')
        
        try:
            category = Category.objects.get(id=category_id)
            category.name = name
            category.save()
            return JsonResponse({'success': True, 'message': 'Category updated successfully!'})
        except Category.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Category not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

def add_article(request):
    if request.method == 'POST':
        title = request.POST['title']
        category_id = request.POST['category']
        author = request.POST['author']
        description = request.POST['description']
        image = request.FILES['image']

        # Save the article
        article = Articles(
            title=title,
            category_id=category_id,
            author=author,
            description=description,
            image=image  # No need to manually save; Django handles this automatically
        )
        article.save()

        return redirect('view_articles')  # Redirect to a page showing the list of articles or success message

    # Get categories for the form
    categories = Category.objects.all()
    return render(request, 'add_article.html', {'categories': categories})

from django.shortcuts import render
from .models import Articles  # Make sure to import your Articles model

def view_articles(request):
    articles = Articles.objects.all()  # Retrieve all articles from the database
    return render(request, 'view_article.html', {'articles': articles})

def article_detail(request, id):
    article = Articles.objects.get(id=id)
    return render(request, 'article_detail.html', {'article': article})
