from django.urls import path
from .views import register_view, login_view, home_view

urlpatterns = [
    path('', home_view, name='home'),  # Route for the homepage
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    # Add other URL patterns here if needed
]
