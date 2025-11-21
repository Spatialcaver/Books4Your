from rest_framework import serializers
from user.models import User
from django.contrib.auth import get_user_model
from borrowing.models import Borrowing
from django.utils import timezone
from author.models import Author
from django.db.models import Count


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = '__all__' 
        read_only_fields = ['id']
        
        
            
        
        
class CreateBorrowingSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Borrowing
        fields = ["user","book", "return_date"] 
        read_only_fields = ['id', 'borrow_date'] 
        
    def validate(self, data):
 
        request = self.context.get('request')
        authenticated_user = request.user
        
        
        user_to_borrow_for = data.get('user') 
        book = data['book']
        return_date = data.get('return_date')
        
       
        if not (authenticated_user.is_staff or authenticated_user.is_superuser):
            
            # Usuário comum só pode criar empréstimos para si mesmo.
            if user_to_borrow_for != authenticated_user:
                raise serializers.ValidationError(
                    {"user": "Usuários comuns só podem criar empréstimos para si mesmos."}
                )
            
         
            data['user'] = authenticated_user

      
        user = data['user']
        
      
        if user.status != 'active':
            raise serializers.ValidationError(
                {"user": f"Usuário '{user.username}' está inativo e não pode realizar empréstimos."}
            )

        # Regra: Limite de 5 Livros
        active_borrowings_count = Borrowing.objects.filter(
            user=user, 
            status='OUT'
        ).count()
        
        if active_borrowings_count >= 5:
            raise serializers.ValidationError(
                {"user": f"O usuário '{user.username}' já possui {active_borrowings_count} livros emprestados e excedeu o limite de cinco."}
            )
        
        # Regra: Livro Disponível/Reservado
        if book.status in ['Borrowed', 'Reserved']:
             raise serializers.ValidationError(
                {"book": f"O livro '{book.title}' está {book.status} e não pode ser emprestado."}
            )
            
        # Regra: Data de Devolução Válida
        today = timezone.now().date()
        
        if return_date and return_date <= today:
            raise serializers.ValidationError(
                {"return_date": "A data de devolução deve ser posterior à data de empréstimo (data atual)."}
            )

        return data
    
class UpdateBorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = ["return_date"]
        read_only_fields = ["borrow_date",'id']