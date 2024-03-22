from django.contrib.auth.backends import ModelBackend
from lms_login_api.models import CustomUser  # Import your custom user model

class CustomUserAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = CustomUser.objects.get(username=username)
            if user.check_password(password):
                return user
        except CustomUser.DoesNotExist:
            return None
