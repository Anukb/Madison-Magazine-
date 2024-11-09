from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('subscribe/', views.subscribe_view, name='subscribe'),
    path('payment/', views.payment_view, name='payment'),
    path('process_payment/', views.process_payment_view, name='process_payment'), path('profile/', views.profile_view, name='profile'),

]