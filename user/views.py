from django.shortcuts import render
from user.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics
from user.serializer import UserSerializer, CreateUserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
import json


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