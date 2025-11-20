from django.db import models , transaction
import uuid
from user.models import User
from book.models import Book

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
          
            with transaction.atomic():
              
                super().save(*args, **kwargs)

              
                book = self.book
                
                
                if self.status == 'OUT':
                    
                    book.status = 'Borrowed'
                
                elif self.status == 'RET':
                    
                    book.status = 'Available'
                
                book.save(update_fields=['status'])
            
       
        def __str__(self):
            return f"{self.user} borrowed {self.book} on {self.borrow_date}"