from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _  # Import the translation function
from django.conf import settings


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [first_name, last_name]

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Change this to a unique name
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
user_permissions = models.ManyToManyField(
    'auth.Permission',
    related_name='customuser_permissions_set',  # Use a unique related name
    blank=True,
    help_text='Specific permissions for this user.',
    verbose_name='user permissions'
)


def __str__(self):
    return self.email

class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Updated to use CustomUser
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    publication_status = models.CharField(max_length=20, choices=[
        ('draft', 'Draft'),
        ('published', 'Published'),
    ])
    categories = models.ManyToManyField('Category', blank=True)


class Category(models.Model):
    name = models.CharField(max_length=100)


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Updated to use CustomUser
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_approved = models.BooleanField(default=False)

class Complaint(models.Model):
    id = models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"Complaint by {self.user} - Resolved: {self.is_resolved}"


class Subscription(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Updated to use CustomUser
    plan = models.CharField(max_length=50)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()


class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Updated to use CustomUser
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)


class RatingReview(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Updated to use CustomUser
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    review = models.TextField(blank=True)

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Register(AbstractBaseUser, PermissionsMixin):
    reg_id = models.AutoField(primary_key=True)  # Use reg_id as the primary key
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = BaseUserManager()  # Use the default manager

    USERNAME_FIELD = 'email'  # Specify the field to use for authentication
    REQUIRED_FIELDS = ['first_name', 'last_name']  # Specify any additional fields required

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='register_set',  # Change this to a unique name
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='register_set',  # Change this to a unique name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

class Profile(models.Model):
    USER_TYPES = [
        ('reader', 'Reader'),
        ('editor', 'Editor'),
        ('admin', 'Administrator'),
    ]

    last_name = models.CharField(max_length=30)
    user = models.OneToOneField(Register, on_delete=models.CASCADE)  # Updated to use Register
    user_type = models.CharField(max_length=10, choices=USER_TYPES)
    preferences = models.JSONField(default=dict, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)

def __str__(self):
    return self.email