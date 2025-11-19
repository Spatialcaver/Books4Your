from django.db import models
import uuid
from author.models import Author

STATUS_CHOICES = [
    ('Available', 'Available'), 
    ('Reserved', 'Reserved'),
    ('Borrowed', 'Borrowed')
]

CATEGORY_CHOICES = (
    # Ficção
    ('FIC', 'Ficção Literária'),
    ('FAN', 'Fantasia'),
    ('SCF', 'Ficção Científica'),
    ('THR', 'Suspense / Thriller'),
    ('MYT', 'Mistério / Policial'),
    ('ROM', 'Romance'),
    ('HOR', 'Terror / Horror'),
    ('JUV', 'Literatura Juvenil'),
    ('INF', 'Literatura Infantil'),
    ('POE', 'Poesia'),
    
    # Não Ficção
    ('HIS', 'História'),
    ('BIO', 'Biografia / Memórias'),
    ('SEL', 'Autoajuda / Desenvolvimento Pessoal'),
    ('FIL', 'Filosofia'),
    ('REL', 'Religião / Espiritualidade'),
    ('ART', 'Artes / Design / Fotografia'),
    ('CUL', 'Culinária'),
    ('CIJ', 'Ciências Sociais e Jurídicas'),
    ('CIE', 'Ciências Exatas e Naturais'),
    ('TEC', 'Tecnologia / Computação'),
)


LANGUAGE_CHOICES = (
    # Línguas Europeias
    ('PT', 'Português'),
    ('PT-BR', 'Português (Brasil)'),
    ('EN', 'Inglês'),
    ('ES', 'Espanhol'),
    ('FR', 'Francês'),
    ('DE', 'Alemão'),
    ('IT', 'Italiano'),
    ('RU', 'Russo'),
    ('NL', 'Holandês'),
    ('SV', 'Sueco'),
    ('DA', 'Dinamarquês'),
    ('NO', 'Norueguês'),
    ('FI', 'Finlandês'),
    ('PL', 'Polaco'),
    ('RO', 'Romeno'),
    ('EL', 'Grego'),
    ('HU', 'Húngaro'),
    ('CS', 'Checo'),
    ('TR', 'Turco'),
    ('UK', 'Ucraniano'),
    
    # Línguas Asiáticas
    ('ZH', 'Chinês (Mandarim)'),
    ('JA', 'Japonês'),
    ('KO', 'Coreano'),
    ('HI', 'Hindi'),
    ('AR', 'Árabe'),
    ('ID', 'Indonésio'),
    ('TH', 'Tailandês'),
    ('VI', 'Vietnamita'),
    ('HE', 'Hebraico'),
    ('FA', 'Persa (Farsi)'),
    ('ML', 'Malaiala'),
    ('BN', 'Bengali'),
    
    # Outras Línguas Relevantes
    ('AF', 'Africâner'),
    ('SW', 'Suaíli'),
    ('CA', 'Catalão'),
    ('GA', 'Irlandês'),
    ('IS', 'Islandês'),
    ('LA', 'Latim'),  # Relevante para textos antigos/académicos
)

class Book (models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, )
    title = models.CharField(max_length=100, blank=False, null=False)
    subtitle = models.CharField(max_length=100, blank=True, null=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    book_description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, blank=False, null=False)
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
    
    
    read_only_fields = ['id']

    
    def __str__(self):
        return f'{self.title} - by ({self.author.name})'   
    