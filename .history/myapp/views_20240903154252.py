from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Register, Login, Article, Comment, Profile, Subscription, RatingReview, Notification
from django.http import HttpResponse, JsonResponse
from social_django.utils import psa
from social_django.views import auth, complete
from django.utils import timezone


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        # Basic validation
        if not all([username, email, password, confirm_password]):
            messages.error(request, 'Please fill out all fields.')
        elif password != confirm_password:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
        else:
            # Create new user with hashed password
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            user.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')
    
    return render(request, 'account/register.html')

def login_view(request):
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')  # Redirect to home or another page
        else:
            return render(request, 'accounts/login.html', {'error_message': 'Invalid username or password'})
    return render(request, 'accounts/login.html')


def google_auth_view(request):
    return auth(request, 'google-oauth2')

def google_auth_complete_view(request):
    return complete(request, 'google-oauth2')

def facebook_auth_view(request):
    # Implement Facebook authentication logic here
    return HttpResponse("Facebook authentication logic will be implemented here.")

def apple_auth_view(request):
    # Implement Apple authentication logic here
    return HttpResponse("Apple authentication logic will be implemented here.")

@psa('social:complete')
def auth_by_google(request, backend):
    return redirect('/')

def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        # Implement password reset logic here
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
        # Process payment logic here
        pass
    return redirect('home')

@login_required
def profile_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, 'account/profile.html', {'profile': profile})

def create_article_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if request.user.is_authenticated:
            author = request.user
            article = Article.objects.create(title=title, content=content, author=author)
            messages.success(request, 'Article created successfully.')
            return redirect('home')
        else:
            messages.error(request, 'You must be logged in to create an article.')
            return redirect('login')
    return render(request, 'account/create_article.html')

def comment_view(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if request.user.is_authenticated:
            author = request.user
            comment = Comment.objects.create(article=article, author=author, content=content)
            messages.success(request, 'Comment added successfully.')
            return redirect('article_detail', article_id=article.id)
        else:
            messages.error(request, 'You must be logged in to comment.')
            return redirect('login')
    return render(request, 'account/comment.html', {'article': article})