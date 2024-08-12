from django.urls import path
from .views import register_view, login_view

urlpatterns = [
    path(' ', register_view, name='register'),
    path('login/', login_view, name='login'),
]
