from django.db import models

class Register(models.Model):
    reg_id = models.AutoField(primary_key=True) # Primary key for Register
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=128)
    confirm_password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self):
        return self.username

class Login(models.Model):log_id = models.AutoField(primary_key=True)
    reg_id = models.ForeignKey(Register, on_delete=models.CASCADE)  # Foreign key to Register
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.email


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
