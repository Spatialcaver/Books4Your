from rest_framework import serializers
from user.models import User
from django.contrib.auth import get_user_model
from borrowing.models import Borrowing
from django.utils import timezone
from author.models import Author


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
        
        
        
        def validate(self, data):
            user = self.context['request'].user
            book = data['book']
            return_date = data.get('return_date')
            
            
            if user.status != 'active':
                raise serializers.ValidationError(
                    "Usuário inativo não pode realizar empréstimos de livros."
                )

            # Regra 2: Limite de 5 Livros por Usuário
            active_borrowings_count = Borrowing.objects.filter(
                user=user, 
                status='OUT'
            ).count()
            
            if active_borrowings_count >= 5:
                raise serializers.ValidationError(
                    f"Você já possui {active_borrowings_count} livros emprestados e excedeu o limite de cinco."
                )
            
            # Regra 3: Livro Disponível (não Borrowed ou Reserved)
            if book.status in ['Borrowed', 'Reserved']:
                raise serializers.ValidationError(
                    f"O livro '{book.title}' está {book.status} e não pode ser emprestado."
                )
                
            # Regra 4: Data de Devolução Válida (posterior à data de empréstimo/hoje)
            today = timezone.now().date()
            
            # A data de empréstimo é auto_now_add, então comparamos com a data atual
            if return_date and return_date <= today:
                raise serializers.ValidationError(
                    "A data de devolução deve ser posterior à data de empréstimo (data atual)."
                )

            return data

class UpdateBorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ["borrow_date","return_date"]
        read_only_fields = ['id']