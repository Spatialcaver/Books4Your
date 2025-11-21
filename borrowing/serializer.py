from rest_framework import serializers
from user.models import User
from django.contrib.auth import get_user_model
from borrowing.models import Borrowing
from django.utils import timezone
from datetime import timedelta
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
    # Campo customizado para TRGGER a ação de renovação
    renew = serializers.BooleanField(write_only=True, required=False, label="Renovar por 7 dias")

    class Meta:
        model = Borrowing
        # return_date e status são permitidos para atualização normal ou renovação
        fields = ["return_date", "status", "renew"] 
        read_only_fields = ["borrow_date", 'id']

    def validate(self, data):
        instance = self.instance 
        authenticated_user = self.context['request'].user
        
        # Lógica de Validação SÓ se a flag 'renew' estiver presente
        if data.get('renew', False):
            
            # 1. Regra de Autorização (Usuário vs. Admin)
            if instance.user != authenticated_user and not (authenticated_user.is_staff or authenticated_user.is_superuser):
                raise serializers.ValidationError(
                    {"detail": "Você não tem permissão para renovar empréstimos de outros usuários."}
                )

            # 2. Regra: O empréstimo deve estar ativo ('OUT')
            if instance.status != 'OUT':
                raise serializers.ValidationError(
                    {"status": "Este empréstimo não está ativo para renovação (status diferente de 'Emprestado')."}
                )
            
            # 3. Regra: O livro não pode estar reservado
            if instance.book.status == 'Reserved':
                raise serializers.ValidationError(
                    {"book": f"O livro '{instance.book.title}' está reservado e não pode ser renovado."}
                )
            
            # 4. Verifica se a data de devolução não está no passado (se houver)
            if instance.return_date and instance.return_date < timezone.now().date():
                 raise serializers.ValidationError(
                    {"return_date": "O prazo de devolução já expirou. O livro precisa ser devolvido (status 'RET') antes de renovar."}
                )
            
        return data

    def update(self, instance, validated_data):
        is_renewal = validated_data.pop('renew', False)

        if is_renewal:
            # Lógica de Renovação: Estende a data em 7 dias
            
            if instance.return_date:
                instance.return_date += timedelta(days=7)
            else:
                # Se for o primeiro prazo, define a partir de hoje
                instance.return_date = timezone.now().date() + timedelta(days=7)
                
            # Garante que a data de devolução seja o único campo salvo na renovação
            instance.save(update_fields=['return_date'])
            
            # O status e a return_date fornecidos pelo usuário são ignorados aqui para a renovação
            
        else:
            # Lógica de Atualização Normal (PATCH/PUT para status ou data manual)
            instance = super().update(instance, validated_data)
            
        return instance