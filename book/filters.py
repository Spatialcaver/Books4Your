import django_filters
from .models import Book

class BookFilter(django_filters.FilterSet):
    
    author_id= django_filters.UUIDFilter(field_name='author__id')
    
    author_name = django_filters.CharFilter(field_name='author__name', lookup_expr='icontains')
    
    category = django_filters.CharFilter(field_name='category')
    
    status = django_filters.CharFilter(field_name='status')
    
    
    class Meta:
        model = Book
        fields = ['author_id', 'author_name', 'category', 'status']