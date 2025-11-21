from django.db import models , transaction
import uuid
from user.models import User
from book.models import Book
from django.core.exceptions import ValidationError 

BORROWING_STATUS_CHOICES = (
    ('OUT', 'Emprestado'),
    ('RET', 'Devolvido'),
    ('OVD', 'Atrasado'),
)

class Borrowing(models.Model):
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        book = models.ForeignKey(Book, on_delete=models.CASCADE)
        status = models.CharField(max_length=3, choices=BORROWING_STATUS_CHOICES, default='OUT')
        borrow_date = models.DateField(auto_now_add=True)
        return_date = models.DateField(blank=True, null=True)
        
        
        def save(self, *args, **kwargs):
            book = self.book
        
        # 1. VALIDAÇÃO DE DISPONIBILIDADE ANTES DE SALVAR (Para ADMIN e Model Save)
        # Verifica se é uma nova criação e se o status é 'Emprestado' ('OUT')
            is_new = self._state.adding
            
            if is_new and self.status == 'OUT':
                # Se o livro já estiver emprestado ou reservado, levanta um erro
                if book.status in ['Borrowed', 'Reserved']:
                    # ValidationError é traduzido em 500 na API, mas é o mecanismo de erro do modelo
                    raise ValidationError(
                        f"O livro '{book.title}' está {book.status} e não pode ser emprestado novamente."
                    )

            # 2. Execução Atômica e Sincronização (O restante do seu código)
            with transaction.atomic():
                
                # Se a validação passou, salva o empréstimo
                super().save(*args, **kwargs) 

                # Sincronização de status (DEVE ficar aqui, após o super().save())
                if self.status == 'OUT':
                    book.status = 'Borrowed'
                elif self.status == 'RET':
                    book.status = 'Available'
                
                book.save(update_fields=['status'])
        
        
        
        
       

       
        def __str__(self):
            return f"{self.user} borrowed {self.book} on {self.borrow_date}"