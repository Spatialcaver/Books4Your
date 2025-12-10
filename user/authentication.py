from user.models import User
from user.serializer import UserSerializer
from django.contrib.auth.hashers import make_password, check_password
from drf_spectacular.utils import extend_schema

class AuthenticationService:
    
    @extend_schema(
        request=None,
        responses={200: UserSerializer},
        description="Authenticate a user", 
        tags=["Authentication"]
    )
    def signin(self, username, password):
        try:
            user = User.objects.get(username=username)
            if check_password(password, user.password):
                return user
            else:
                return False
        except User.DoesNotExist:
            return False
        