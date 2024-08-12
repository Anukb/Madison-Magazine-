from django.db import models

class Register(models.Model):
    
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=128)
    confirm_password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self):
        return self.username
    

class Login(models.Model):
    user = models.OneToOneField(Register, on_delete=models.CASCADE)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.user.username

