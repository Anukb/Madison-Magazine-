from django.urls import path
from .views import register_view, login_view, home_view, forgot_password_view

urlpatterns = [
    path('', home_view, name='home'),  # Route for the homepage
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('forgot-password/', forgot_password_view, name='forgot_password'),  # Route for forgot password
    # Add other URL patterns here if needed
]