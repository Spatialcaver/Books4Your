from django.db import models
import uuid
from user import User
from book import Book


class Borrowing(models.Model):
        id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
        user = models.ForeignKey(User, on_delete=models.CASCADE)
        book = models.ForeignKey(Book, on_delete=models.CASCADE)
        borrow_date = models.DateField(auto_now_add=True)
        return_date = models.DateField(blank=True, null=True)
        
        def __str__(self):
            return f"{self.user} borrowed {self.book} on {self.borrow_date}"