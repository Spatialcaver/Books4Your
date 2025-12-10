from django.shortcuts import render
from book.models import Book
from rest_framework import status, generics
from book.serializer import BookSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend 
from rest_framework.response import Response
from .filters import BookFilter



class CreateBookView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    
    queryset = Book.objects.all()
    
    serializer_class = BookSerializer
    
    def post(self, request, *args, **kwargs):
        try:
            serializer_class = self.get_serializer_class(data=request.data)
            serializer_class.is_valid(raise_exception=True)
            self.perform_create(serializer_class)
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
    
    
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST) 
    

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
    
    queryset = Book.objects.select_related('author').all()
    
    serializer_class = BookSerializer
    
    OrderingFilter = ['title', 'publication_date', 'author__name','category', 'author', 'status']