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
    
    def update(self, instance, validated_data):
        author_data = validated_data.pop('author', None)
        
        # 1. Atualizar o objeto Book (instância)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        
        # 2. Atualizar o objeto Author aninhado (se houver dados)
        if author_data:
            # Pega a instância do Autor que já está ligada ao Livro
            author_instance = instance.author 
            
            # Atualiza os campos do Autor
            for key, value in author_data.items():
                setattr(author_instance, key, value)
            
            author_instance.save()

        instance.save()
        return instance