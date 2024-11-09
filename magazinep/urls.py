from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),  # Your app's URLs
    # Remove the following line if you don't need Django's built-in auth URLs
    #path('accounts/', include('django.contrib.auth.urls')),  # Include built-in auth URLs
]
