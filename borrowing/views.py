from borrowing.models import Borrowing
from borrowing.serializer import CreateBorrowingSerializer, UpdateBorrowingSerializer, BorrowingSerializer
from rest_framework import  generics
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone





class NewBorrowingView(generics.CreateAPIView):
    serializer_class = CreateBorrowingSerializer
    permission_classes = [IsAuthenticated]

    

class UpdateBorrowingView(generics.UpdateAPIView):
    serializer_class = UpdateBorrowingSerializer
    permission_classes = [IsAuthenticated]

class BorrowingListView(generics.ListAPIView):
    serializer_class = BorrowingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        
        if user.is_staff or user.is_superuser:
            return Borrowing.objects.all()
        
        return Borrowing.objects.filter(user=self.request.user)
    
    
class OverdueBorrowingListView(generics.ListAPIView):
    serializer_class = BorrowingSerializer
    permission_classes = [IsAuthenticated] 
    
    def get_queryset(self):
       
        return Borrowing.objects.filter(
            status='OUT', 
            return_date__lt=timezone.now().date()
        ).order_by('return_date')