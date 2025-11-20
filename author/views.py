from rest_framework import generics
from author.models import Author
from author.serializer import AuthorSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny


class CreateAuthorView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    
    queryset = Author.objects.all()
    
    serializer_class = AuthorSerializer
    
       
    
class ListAuthorView(generics.ListAPIView):
    permission_classes = [AllowAny]
    
    queryset = Author.objects.all()
    
    serializer_class = AuthorSerializer
    
    
class UpdateAuthorView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    
    queryset = Author.objects.all()
    
    serializer_class = AuthorSerializer
    




