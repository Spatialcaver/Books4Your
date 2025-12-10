from borrowing.models import Borrowing
from borrowing.serializer import CreateBorrowingSerializer, UpdateBorrowingSerializer, BorrowingSerializer
from rest_framework import  generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema





class NewBorrowingView(APIView):
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        request=CreateBorrowingSerializer,
        responses={201: CreateBorrowingSerializer, 
        status.HTTP_400_BAD_REQUEST: {"type": "object", "properties": {"error": {"type": "string"}}}
        
        }
    )
    
    def post(self, request):
        serializer_class = CreateBorrowingSerializer(data=request.data)
    
        try:
            serializer_class.is_valid(raise_exception=True)
            serializer_class.save(user=request.user)
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
       
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    

class UpdateBorrowingView(APIView):
    serializer_class = UpdateBorrowingSerializer
    permission_classes = [IsAuthenticated]
    
    
    @extend_schema( 
        request=UpdateBorrowingSerializer,
        responses={200: UpdateBorrowingSerializer, 
        status.HTTP_400_BAD_REQUEST: {"type": "object", "properties": {"error": {"type": "string"}}}
        
        }
                   )
    
    def put(self, request, pk):
        serializer_class = UpdateBorrowingSerializer
        

        try:
            serializer_class.is_valid(raise_exception=True)
            serializer_class.save()
            
            return Response(serializer_class.data, status=status.HTTP_200_OK)
    
    
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        
        
    @extend_schema(
        request=UpdateBorrowingSerializer,
        responses={200: UpdateBorrowingSerializer, 
        status.HTTP_400_BAD_REQUEST: {"type": "object", "properties": {"error": {"type": "string"}}}
        
        }
                   )   
        
    def patch(self, request, pk):
        serializer_class = UpdateBorrowingSerializer
        
        try:
            serializer_class.is_valid(raise_exception=True)
            serializer_class.save()
            
            return Response(serializer_class.data, status=status.HTTP_200_OK)
    
    
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        
    def patch(self, request, pk):
        serializer_class = UpdateBorrowingSerializer
        
        try:
            serializer_class.is_valid(raise_exception=True)
            serializer_class.save()
            
            return Response(serializer_class.data, status=status.HTTP_200_OK)
    
    
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class BorrowingListView(APIView):
    serializer_class = BorrowingSerializer
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        request=BorrowingSerializer,
        responses={200: BorrowingSerializer, 
        status.HTTP_400_BAD_REQUEST: {"type": "object", "properties": {"error": {"type": "string"}}}
        
        }
    )
    
    def get_queryset(self):
        user = self.request.user
        
        try:
            if user.is_superuser:
                return Borrowing.objects.all()
            
            else:
                return Response(Borrowing.objects.filter(user=self.request.user, status=status.HTTP_200_OK))
            
        except:
            return Response ("You do not have permission to perform this action.", status=status.HTTP_400_BAD_REQUEST)
    
    
class OverdueBorrowingListView(APIView):
    permission_classes = [IsAuthenticated] 
    
    @extend_schema( 
                  request=BorrowingSerializer,
                  responses={200: BorrowingSerializer, 
                  status.HTTP_400_BAD_REQUEST: {"type": "object", "properties": {"error": {"type": "string"}}}
                  
                  }
                   )
    
    def get_queryset(self):
        serializer_class = BorrowingSerializer
        
        try:
            return Response(Borrowing.objects.filter(
                status='OUT', 
                return_date__lt=timezone.now().date()
            ).order_by('return_date'), status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)