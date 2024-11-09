from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from .models import Article, Comment, Profile
from django.http import HttpResponse
from social_django.utils import psa
from social_django.views import auth, complete

def auth_view(request):
    if request.method == 'POST':
        if 'login' in request.POST:
            # Handle login
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('home')
            else:
                return render(request, 'account/login.html', {'error_message': 'Invalid username or password'})
        
        if 'register' in request.POST:
            # Handle registration
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')

            if password != confirm_password:
                return render(request, 'account/login.html', {'error_message': 'Passwords do not match'})
            
            if User.objects.filter(username=username).exists():
                return render(request, 'account/login.html', {'error_message': 'Username already exists'})

            user = User(
                username=username,
                email=email,
                password=make_password(password),
                first_name=first_name,
                last_name=last_name
            )
            user.save()
            auth_login(request, user)
            return redirect('home')

    return render(request, 'account/login.html')

def google_auth_view(request):
    return auth(request, 'google-oauth2')

def google_auth_complete_view(request):
    return complete(request, 'google-oauth2')

def facebook_auth_view(request):
    return HttpResponse("Facebook authentication logic will be implemented here.")

def apple_auth_view(request):
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
