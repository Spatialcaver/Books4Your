from django.shortcuts import render
from user.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from user.serializer import UserSerializer, CreateUserSerializer, CustomTokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from borrowing.models import Borrowing
from django.contrib.auth import get_user_model
from drf_spectacular.utils import    extend_schema
from django.shortcuts import get_object_or_404 


User = get_user_model()


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
   
    def get(self, request, *args, **kwargs):
        queryset = User.objects.filter(is_active=True)
        serializer = UserSerializer(queryset, many=True)
        
        try:
            return Response(serializer.data, status=status.HTTP_200_OK)
        
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
    def put(self, request, pk, *args, **kwargs):
    
        user = get_object_or_404(User, pk=pk)
        serializer_class = UserSerializer(data=request.data)
        
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

    def patch(self, request, pk, *args, **kwargs):
        user = get_object_or_404(User, pk=pk)
        serializer_class = UserSerializer(data=request.data, partial=True)
        
        
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
       
        try:
            user = get_object_or_404(User, pk=kwargs.get('pk'))
            
            if user != request.user and not request.user.is_superuser:
                 return Response(
                     {"error": "Você não tem permissão para deletar este usuário."}, 
                     status=status.HTTP_403_FORBIDDEN
                 )
                 
            user.delete()
        
            return Response("User deleted successfully", status=status.HTTP_200_OK)
    
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserWithActiveBorrowingList(APIView):
    serializer_class = UserSerializer 
    permission_classes = [IsAuthenticated]
    queryset = User.objects.filter(borrowing__status='OUT').distinct()

    @extend_schema(
        request= UserSerializer,
        responses={200: UserSerializer},
        description="List users with active borrowings", 
        tags=["User"]
    )
    def get(self, request, *args, **kwargs):
        
        borrowings_active = self.queryset.all()
        
        try:
            serializer = self.serializer_class(borrowings_active, many=True) 
        
            return Response({"Users with active loans": serializer.data}, status=status.HTTP_200_OK)
    
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)