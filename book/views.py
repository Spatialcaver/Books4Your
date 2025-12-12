from book.models import Book
from rest_framework.views import APIView
from rest_framework import status
from book.serializer import BookSerializer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend 
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema

from .filters import BookFilter


class CreateBookView(APIView):
    permission_classes = [IsAuthenticated]  
    
    @extend_schema(
        request=BookSerializer,
        responses={
            status.HTTP_201_CREATED: BookSerializer,
            status.HTTP_400_BAD_REQUEST: {"type": "object", "properties": {"error": {"type": "string"}}},
        }
    )
    def post(self, request, *args, **kwargs):
        serializer_class = BookSerializer(data=request.data)
        
        try:
            serializer_class.is_valid(raise_exception=True)
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST) 


class UpdateBookView(APIView):
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        request=BookSerializer,
        responses={status.HTTP_200_OK: BookSerializer}
    )
    def put(self, request, pk, *args, **kwargs):
        book = get_object_or_404(Book, pk=pk)
        serializer_class = BookSerializer(book, data=request.data)
        
        try:
            serializer_class.is_valid(raise_exception=True)
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @extend_schema(
        request=BookSerializer, 
        responses={status.HTTP_200_OK: BookSerializer}
    )
    def patch(self, request, pk, *args, **kwargs):
        book = get_object_or_404(Book, pk=pk)
        serializer_class = BookSerializer(book, data=request.data, partial=True)
        
        try:
            serializer_class.is_valid(raise_exception=True)
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ListBookView(APIView):
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        responses={status.HTTP_200_OK: BookSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs): 
        book = Book.objects.all()
        serializer = BookSerializer(book, many=True)
        return Response(serializer.data)


class DeleteBookView(APIView):
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        responses={status.HTTP_204_NO_CONTENT: None}
    )
    def delete(self, request, pk, *args, **kwargs):
        try:
            book = get_object_or_404(Book, pk=pk)
            book.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)