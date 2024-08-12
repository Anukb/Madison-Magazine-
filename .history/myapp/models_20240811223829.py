from django.db import models
from django.contrib.auth.models import User

class Register(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=254, unique=True)
    date_of_birth = models.Date

    def __str__(self):
        return self.email

class Login(models.Model):
    register_id = models.ForeignKey(Register, on_delete=models.CASCADE, to_field='id')
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email