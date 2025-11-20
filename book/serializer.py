from rest_framework import serializers
from book.models import Book
from author.serializer import AuthorSerializer



class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    
    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ['id']
        
       
    