from borrowing.models import Borrowing
from borrowing.serializer import CreateBorrowingSerializer, UpdateBorrowingSerializer, BorrowingSerializer
from rest_framework import  generics
from rest_framework.permissions import IsAuthenticated




class NewBorrowingView(generics.CreateAPIView):
    serializer_class = CreateBorrowingSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UpdateBorrowingView(generics.UpdateAPIView):
    serializer_class = UpdateBorrowingSerializer
    permission_classes = [IsAuthenticated]

class BorrowingListView(generics.ListAPIView):
    serializer_class = BorrowingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Borrowing.objects.filter(user=self.request.user)