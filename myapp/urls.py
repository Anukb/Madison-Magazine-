# urls.py
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import   check_username, forgot_password_view, home_view, register_view, login_view, logout_view, profile_view, edit_profile_view, admin_login_view, admin_dashboard_view,add_category
from .views import delete_category, update_category, add_article, view_articles, article_detail

urlpatterns = [
    path('', home_view, name='home'),
    path('register/', register_view, name='register'),
    path('check_username/', check_username, name='check_username'),
    path('login/', login_view, name='login'),
    path('forgot-password/', forgot_password_view, name='forgot_password'),  # Add this line
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('profile/edit/', edit_profile_view, name='edit_profile'),
    path('admin_login/', admin_login_view, name='admin_login'),
    path("admin_dashboard/", admin_dashboard_view, name="admin_dashboard"),
    path('add_category/', add_category, name='add_category'),
    path('delete_category/<int:category_id>/', delete_category, name='delete_category'),
    path('update_category/<int:category_id>/', update_category, name='update_category'),
    path('add-article/', add_article, name='add_article'),
    path('articles/', view_articles, name='view_articles'),
    path('add/', add_article, name='add_article'),
    path('articles/', view_articles, name='view_articles'),
    path('article/<int:id>/', article_detail, name='article_detail'),

    path('articles/<int:id>/', article_detail, name='article_detail'),
      # Admin dashboard URL
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)