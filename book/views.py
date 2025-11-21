from django.shortcuts import render
from book.models import Book
from rest_framework import status, generics
from book.serializer import BookSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend 
from .filters import BookFilter



class CreateBookView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    
    queryset = Book.objects.all()
    
    serializer_class = BookSerializer

class UpdateBookView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    
    queryset = Book.objects.all()
    
    serializer_class = BookSerializer

class DeleteBookView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    
    queryset = Book.objects.all()
    
    serializer_class = BookSerializer
    
class ListBookView(generics.ListAPIView):
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilter
    permission_classes = [AllowAny]
    
    queryset = Book.objects.all()
    
    serializer_class = BookSerializer
    
    OrderingFilter = ['title', 'publication_date', 'author__name','category', 'author', 'status']