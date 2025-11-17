from django.db import models
import uuid
from author import Author

STATUS_CHOICES = [
    ('Available', 'Available'), 
    ('Reserved', 'Reserved'),
    ('Borrowed', 'Borrowed')
]


LANGUAGE_CHOICES = (
    ('PT', 'Português'),
    ('EN', 'Inglês'),
    ('ES', 'Espanhol'),
    ('FR', 'Francês'),
    ('DE', 'Alemão'),
    ('IT', 'Italiano'),
   
)


class Book (models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=30, blank=False, null=False)
    subtitle = models.CharField(max_length=100, blank=True, null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    book_description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=50, blank=False, null=False)
    publisher = models.CharField(max_length=100, blank=False, null=False)
    publication_date = models.DateField(blank=False, null=False)
    ISBN = models.CharField(unique=True, max_length=13, blank=False, null=False) #identificador unico
    page_count = models.IntegerField(blank=False, null=False)
    last_edition = models.DateField(blank=False, null=False)
    language = models.CharField(max_length=50,choices=LANGUAGE_CHOICES, blank=False, null=False)
    cover_url = models.URLField(blank=True, null=True) #imagem da capa
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status =models.CharField(max_length=10, choices=STATUS_CHOICES, default='Available', verbose_name='Book Status')
    