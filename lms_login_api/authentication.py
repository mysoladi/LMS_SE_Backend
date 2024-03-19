from django.contrib.auth.backends import ModelBackend
from models import CustomUser

class CustomUserAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(username=username)
            print(user)
            if user.check_password(password):
                return user
        except CustomUser.DoesNotExist:
            return None