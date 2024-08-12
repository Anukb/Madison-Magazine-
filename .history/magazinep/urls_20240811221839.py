from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),  # Root path now points to madison_app.urls
    path('accounts/', include('myapp.urls')),  # Optional: if 'accounts/' is part of madison_app
]
