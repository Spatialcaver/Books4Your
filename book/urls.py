from django.urls import  path
from book.views import CreateBookView, UpdateBookView, DeleteBookView, ListBookView


urlpatterns = [

    path('create/', CreateBookView.as_view(), name='create-book'), 
    path('list/', ListBookView.as_view(), name='list-books'), 
    path('update/<int:pk>/', UpdateBookView.as_view(), name='update-book'),
    path('delete/<int:pk>/', DeleteBookView.as_view(), name='delete-book'),
   
]
