from django.contrib import admin
from user.models import User



class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'full_name', 'email', 'status', 'birth_date')
    search_fields = ('id', 'username', 'full_name', 'email')
    
    
admin.site.register(User, UserAdmin)