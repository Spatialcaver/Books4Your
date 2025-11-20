from django.urls import  path
from author.views import ListAuthorView, CreateAuthorView, UpdateAuthorView


urlpatterns = [
    
    path('list/', ListAuthorView.as_view(), name='list-authors'),
    path('create/', CreateAuthorView.as_view(), name='create-author'),
    path('update/<int:pk>/', UpdateAuthorView.as_view(), name='update-author'),
]