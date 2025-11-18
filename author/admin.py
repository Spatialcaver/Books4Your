from django.contrib import admin
from author.models import Author

# Register your models here.

class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'birth_date')
    search_fields = ('name',)

admin.site.register(Author, AuthorAdmin)