from django.shortcuts import render
from book.models import Book
from rest_framework import status, generics
from book.serializer import BookSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny



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
    permission_classes = [AllowAny]
    
    queryset = Book.objects.all()
    
    serializer_class = BookSerializer
    
    OrderingFilter = ['categoria', 'author', 'status']