from rest_framework import serializers
from user.models import User
from django.contrib.auth import get_user_model
from borrowing.models import Borrowing


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = '__all__' 
        read_only_fields = ['id']
        
        
class CreateBorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ["user", "book", "borrow_date","return_date"]
        read_only_fields = ['id']

class UpdateBorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ["borrow_date","return_date"]
        read_only_fields = ['id']