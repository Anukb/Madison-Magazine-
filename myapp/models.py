from django.db import models
from django.utils import timezone
class Register(models.Model):
    reg_id = models.AutoField(primary_key=True)  # Primary key for Register
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=128)
    confirm_password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self):
        return self.username

class Login(models.Model):
    log_id = models.AutoField(primary_key=True)  # Primary key for Login
    reg_id = models.ForeignKey(Register, on_delete=models.CASCADE, to_field='reg_id')  # Foreign key to Register
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.email

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
# class Subscription_Billing(models.Model):
#     first_name=models.CharField(max_length=100)
#     last_name=models.CharField(max_length=100)
#     address=models.CharField(max_length=100)
#     city=models.CharField(max_length=100)
#     state=models.CharField(max_length=100)
#     post_code=models.IntegerField()
#     country=models.CharField(max_length=100)
#     phone=models.IntegerField()
#     mail=models.EmailField(max_length=254, unique=True)
#     price=models.IntegerField(default=15)
#     duration=models.CharField(max_length=100)

#     def __str__(self):
#         return self.first_name