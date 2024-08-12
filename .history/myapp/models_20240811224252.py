from django.db import models

class Register(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=128)
    confirm_password = models.CharField(max_length=128)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self):
        return self.username
class Login(models.Model):
    login_id = models.AutoField(primary_key=True)
    reg_id = models.ForeignKey(Register, on_delete=models.CASCADE, to_field='reg_id')
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.email


    def __str__(self):
        return self.email
