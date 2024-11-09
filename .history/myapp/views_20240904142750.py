from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from social_django.utils import psa
from social_django.views import auth as social_auth, complete as social_complete
from django.utils import timezone

from .models import Article, Comment, Profile

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'account/login.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'account/login.html')

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

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, 'account/login.html')
    return render(request, 'account/login.html')

def google_auth_view(request):
    return social_auth(request, 'google-oauth2')

def google_auth_complete_view(request):
    return social_complete(request, 'google-oauth2')

def facebook_auth_view(request):
    # Placeholder for Facebook authentication logic
    return HttpResponse("Facebook authentication logic will be implemented here.")

def apple_auth_view(request):
    # Placeholder for Apple authentication logic
    return HttpResponse("Apple authentication logic will be implemented here.")

@psa('social:complete')
def auth_by_google(request, backend):
    return redirect('/')

def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        # Utilize Django's built-in password reset functionality
        from django.contrib.auth.forms import PasswordResetForm
        form = PasswordResetForm(data={'email': email})
        if form.is_valid():
            form.save(request=request)
            messages.info(request, 'Password reset instructions have been sent to your email address.')
            return redirect('login')
        else:
            messages.error(request, 'Enter a valid email address.')
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
        # Implement payment processing logic here
        pass
    return redirect('home')

@login_required
def profile_view(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, 'account/profile.html', {'profile': profile})

@login_required
def create_article_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        article = Article.objects.create(title=title, content=content, author=request.user)
        messages.success(request, 'Article created successfully.')
        return redirect('home')
    return render(request, 'account/create_article.html')

@login_required
def comment_view(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        comment = Comment.objects.create(article=article, author=request.user, content=content)
        messages.success(request, 'Comment added successfully.')
        return redirect('article_detail', article_id=article.id)
    return render(request, 'account/comment.html', {'article': article})
