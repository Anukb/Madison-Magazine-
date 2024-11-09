from django.urls import path, include  # Import include here
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
  
]

