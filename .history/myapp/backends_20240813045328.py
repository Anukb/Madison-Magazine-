from django.contrib.auth.backends import BaseBackend
from .models import Register

class RegisterBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        try:
            register = Register.objects.get(email=email, password=password)
            return register
        except Register.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Register.objects.get(pk=user_id)
        except Register.DoesNotExist:
            return None