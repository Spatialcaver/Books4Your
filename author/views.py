from rest_framework import status
from rest_framework.views import APIView
from author.models import Author
from author.serializer import AuthorSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from drf_spectacular.utils import    extend_schema
  


class CreateAuthorView(APIView):
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        request=AuthorSerializer,
        responses={201: AuthorSerializer},
        description="Create a new author",
        tags=["Author"],
    )
    
    def post(self, request, *args, **kwargs):
     serializer_class = AuthorSerializer(data=request.data)
     
     try:
         serializer_class.is_valid(raise_exception=True)
         serializer_class.save()
         return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        
       
     except Exception as e:
         return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    
class ListAuthorView(APIView):
    permission_classes = [AllowAny]
    @extend_schema(
            responses={200: AuthorSerializer},
            description="List all authors",
            tags=["Author"],
        )
        
    def get(self, request, *args, **kwargs):
        queryset = Author.objects.all()
        
        serializer_class = AuthorSerializer
        
        try:
            serializer = serializer_class(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
class UpdateAuthorView(APIView):
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        request=AuthorSerializer,
        responses={200: AuthorSerializer},
        description="Update an existing author",
        tags=["Author"],
    )
    
    def put(self, request, *args, **kwargs):
        serializer_class = AuthorSerializer(data=request.data)
        try:
            serializer_class.is_valid(raise_exception=True)
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        request=AuthorSerializer,
        responses={200: AuthorSerializer},
        description="Update an existing author",
        tags=["Author"],
    )
    def patch(self, request, *args, **kwargs):
        serializer_class = AuthorSerializer(data=request.data, partial=True)
        try:
            serializer_class.is_valid(raise_exception=True)
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
