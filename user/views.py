from django.shortcuts import render
from user.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics
from user.serializer import UserSerializer, CreateUserSerializer, CustomTokenObtainPairSerializer
from user.authentication import AuthenticationService
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from borrowing.models import Borrowing
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from drf_spectacular.utils import    extend_schema


User = get_user_model()


class SignInView(APIView):

    permission_classes = [AllowAny]
    
    @extend_schema(
        request=CreateUserSerializer,
        responses={201: CreateUserSerializer},
        description="Create a new user", 
        tags=["User"]
    )

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


class UserCreate(APIView):
    permission_classes = [AllowAny]
    
    @extend_schema(
        request=CreateUserSerializer,
        responses={201: CreateUserSerializer},
        description="Create a new user", 
        tags=["User"]
    )
    
    def post(self, request, *args, **kwargs):
        serializer_class = CreateUserSerializer(data=request.data)
        queryset = User.objects.all()
        
        try:
            serializer_class.is_valid(raise_exception=True)
            serializer_class.save()
        
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    
class UserList(APIView):
    permission_classes = [IsAuthenticated]
   
    @extend_schema(
            responses={200: UserSerializer(many=True)},
            description="List all users", 
            tags=["User"]
        )
   
    def get(self, request):
        queryset = User.objects.filter(is_active=True)
        serializer_class = UserSerializer
        
        try:
            serializer_class.is_valid(raise_exception=True)
            serializer_class.save()
        
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    
    
class UserUpdate(APIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    
    @extend_schema(
        request=UserSerializer,
        responses={200: UserSerializer},
        description="Update a user", 
        tags=["User"]
    )
    def put(self, request, *args, **kwargs):
        serializer_class = UserSerializer
        
        try:
            serializer_class.is_valid(raise_exception=True)
            serializer_class.save()
        
            return Response(serializer_class.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    
    @extend_schema(
        request=UserSerializer,
        responses={200: UserSerializer},
        description="Partially update a user", 
        tags=["User"]
    )
   
    def patch(self, request, *args, **kwargs):
        serializer_class = UserSerializer
        
        
        try:
            serializer_class.is_valid(raise_exception=True)
            serializer_class.save()
            
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserDelete(APIView):
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        request=UserSerializer,
        responses={200: UserSerializer},
        description="Delete a user", 
        tags=["User"]
    )
    
    def delete(self, request, *args, **kwargs):
        queryset = User.objects.all()
        serializer_class = UserSerializer
        try:
            serializer_class.is_valid(raise_exception=True)
            serializer_class.save()
        
            return Response(serializer_class.data, status=status.HTTP_200_OK)
    
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserWithActiveBorrowingList(APIView):
    serializer_class = UserSerializer 
    permission_classes = [IsAuthenticated]
    queryset = User.objects.filter(borrowing__status='OUT').distinct()

    @extend_schema(...)
    def get(self, request):
        
        borrowings_active = self.queryset.all()
        
        try:
            serializer = self.serializer_class(borrowings_active, many=True) 
        
            return Response({"Users with active loans": serializer.data}, status=status.HTTP_200_OK)
    
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)