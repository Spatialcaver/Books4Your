from django.contrib import admin

from book.models import Book


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'subtitle', 'author', 'category', 'publisher', 'publication_date', 'ISBN', 'status')
    search_fields = ('title', 'author__name', 'ISBN', 'publisher')
    list_filter = ('category', 'language', 'status', 'id')
    read_only_fields = ['id']


admin.site.register(Book, BookAdmin)