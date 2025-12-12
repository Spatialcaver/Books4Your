from borrowing.models import Borrowing
from borrowing.serializer import CreateBorrowingSerializer, UpdateBorrowingSerializer, BorrowingSerializer
from rest_framework import  generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from user.models import User
from user.serializer import UserSerializer





class NewBorrowingView(APIView):
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        request=CreateBorrowingSerializer,
        responses={201: CreateBorrowingSerializer, 
        status.HTTP_400_BAD_REQUEST: {"type": "object", "properties": {"error": {"type": "string"}}}
        
        }
    )
    
    def post(self, request, *args, **kwargs):
        serializer_class = CreateBorrowingSerializer(data=request.data, context={'request': request})
    
        try:
            serializer_class.is_valid(raise_exception=True)
            serializer_class.save()
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
        borrowing = get_object_or_404(Borrowing, pk=pk)
        
        serializer = self.serializer_class(borrowing, data=request.data, context={'request': request})
        
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            return Response(serializer.data, status=status.HTTP_200_OK)
    
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        
   
    @extend_schema(
        request=UpdateBorrowingSerializer,
        responses={200: UpdateBorrowingSerializer, 
        status.HTTP_400_BAD_REQUEST: {"type": "object", "properties": {"error": {"type": "string"}}}
        }
    )   
    def patch(self, request, pk):
        borrowing = get_object_or_404(Borrowing, pk=pk)
        
        serializer = self.serializer_class(borrowing, data=request.data, partial=True, context={'request': request})
        
        try: 
            serializer.is_valid(raise_exception=True)
            serializer.save()
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        
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
    
    def get(self, request, *args, **kwargs):
        user = self.request.user
        
        if user.is_superuser:
            queryset = Borrowing.objects.all()
        
        else:
            queryset = Borrowing.objects.filter(user=self.request.user)
    
        try:
            serializer = self.serializer_class(queryset, many=True)
            return Response({"Emprestimos": serializer.data}, status=status.HTTP_200_OK)
        
        except:
            return Response ("You do not have permission to perform this action.", status=status.HTTP_400_BAD_REQUEST)
    
    
class OverdueBorrowingListView(APIView):
    serializer_class = BorrowingSerializer 
    permission_classes = [IsAuthenticated]
    
    queryset = Borrowing.objects.filter(
        status='OUT', 
        return_date__lt=timezone.now().date()
    ).distinct() 

    @extend_schema(
        request=BorrowingSerializer,
        responses={200: BorrowingSerializer, 
        status.HTTP_400_BAD_REQUEST: {"type": "object", "properties": {"error": {"type": "string"}}}
        }
    )
    def get(self, request, *args, **kwargs):
        
        users_with_overdue_borrowing = self.queryset.all()
            
        try:
            serializer = self.serializer_class(users_with_overdue_borrowing, many=True) 
        
            return Response({"Users with overdue loans": serializer.data}, status=status.HTTP_200_OK)
    
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)