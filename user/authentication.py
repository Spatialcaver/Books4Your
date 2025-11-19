from user.models import User
from django.contrib.auth.hashers import make_password, check_password


class AuthenticationService:
    def signin(self, username, password):
        try:
            user = User.objects.get(username=username)
            if check_password(password, user.password):
                return user
            else:
                return False
        except User.DoesNotExist:
            return False
        