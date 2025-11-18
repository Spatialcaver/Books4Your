from django.contrib import admin
from borrowing.models import Borrowing



class BorrowingAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'borrow_date', 'return_date')
    search_fields = ('user__username', 'book__title', 'return_date')



admin.site.register(Borrowing, BorrowingAdmin)