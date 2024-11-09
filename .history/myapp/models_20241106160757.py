from django.db import models
from django.utils import timezone

from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class Articles(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    author = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')  # Saves images to 'media/images/' directory
    description = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
