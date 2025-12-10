from book.models import Book
from rest_framework.views import APIView
from rest_framework import status
from book.serializer import BookSerializer
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend 
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import    extend_schema
  

from .filters import BookFilter

@extend_schema(
    
    request=BookSerializer,
    
    responses={
        status.HTTP_201_CREATED: BookSerializer, # Sucesso 201 com dados do livro
        status.HTTP_400_BAD_REQUEST: {"type": "object", "properties": {"error": {"type": "string"}}},
    }
)

class CreateBookView(APIView):
    permission_classes = [IsAuthenticated]  
    
    def post(self, request, *args, **kwargs):
        serializer_class = BookSerializer(data=request.data)
       
        

        try:
            serializer_class.is_valid(raise_exception=True)
            serializer_class.save()
          
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
    
    
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST) 
        
        
   
    
        

class UpdateBookView(APIView):
   

    @extend_schema(
        # PUT espera um BookSerializer na requisição e retorna um BookSerializer no response
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
        # patch não espera corpo de requisição, retorna 200 ok
        request=None, 
        responses={status.HTTP_200_OK: None}
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
    @extend_schema(
        # GET retorna o objeto (BookSerializer)
        responses={status.HTTP_200_OK: BookSerializer}
    )
    def get(self, request, pk, *args, **kwargs): 
        filter_backends = [DjangoFilterBackend]
        filterset_class = BookFilter
        permission_classes = [IsAuthenticated]
                
        book = get_object_or_404(Book, pk=pk)
        serializer = BookSerializer(book)
        
        ordering_fields = ['title', 'publication_date', 'author__name','category', 'author', 'status']
       
        return Response(serializer.data)
   
   
   
class DeleteBookView(APIView):
    @extend_schema(
        request=BookSerializer,
        responses={status.HTTP_200_OK: BookSerializer}
    )     
    
    def delete(self, request, pk, *args, **kwargs):
        
        try:
            book = get_object_or_404(Book, pk=pk)
            book.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)