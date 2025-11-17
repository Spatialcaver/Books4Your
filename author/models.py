from django.db import models
import uuid

class Author(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, blank=False, null=False)
    biography = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=False, null=False)
    nationality = models.CharField(max_length=50, blank=False, null=False)
    
    
    
    def __str__(self):
        return F'{self.id} {self.name}'