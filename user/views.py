from django.shortcuts import render
from user.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics
from user.serializer import UserSerializer, CreateUserSerializer, CustomTokenObtainPairSerializer
from user.authentication import AuthenticationService
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from django.db.models import Prefetch
from borrowing.models import Borrowing
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model


User = get_user_model()


class SignInView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        auth_service = AuthenticationService()
        signin = auth_service.signin(username, password)

        if not signin:
            raise AuthenticationFailed(
                "Credenciais inválidas.", code=status.HTTP_401_UNAUTHORIZED
            )

        # serializar usuário
        user = UserSerializer(signin).data
        refresh = RefreshToken.for_user(signin)


        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "username": user.get("username")
                
            },
            status=status.HTTP_200_OK,
        )


class UserCreate(generics.ListCreateAPIView):
    
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    
    serializer_class = CreateUserSerializer
    
    
class UserList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    
class UserUpdate(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
   
    
class UserDelete(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    
class UserWithActiveBorrowingList(generics.ListAPIView):
    serializer_class = UserSerializer 
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filtra usuários que possuem pelo menos um empréstimo com status 'OUT'
        return User.objects.filter(
            borrowing__status='OUT'
        ).distinct()