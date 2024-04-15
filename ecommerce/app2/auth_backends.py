from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class AdminAuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(username=username, is_active=True, is_staff=True)
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        return None