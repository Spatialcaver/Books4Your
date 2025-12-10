from rest_framework import serializers
from book.models import Book
from author.models import Author

from author.serializer import AuthorSerializer



class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    
    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ['id']
        
       
    def create(self, validated_data):
       
        author_data = validated_data.pop('author')
        
       
        author_instance = Author.objects.create(**author_data)
        
       
        book_instance = Book.objects.create(author=author_instance, **validated_data)
        
        return book_instance