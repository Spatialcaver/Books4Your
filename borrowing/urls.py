from django.urls import include, path
from borrowing.views import BorrowingListView, NewBorrowingView, UpdateBorrowingView, OverdueBorrowingListView
urlpatterns = [
    path('create/', NewBorrowingView.as_view(), name='borrowing-create'),
    path('list/', BorrowingListView.as_view(), name='borrowing-list'),
    path('renovate/<int:pk>/', UpdateBorrowingView.as_view(), name='borrowing-update'), 
    path('overdue/', OverdueBorrowingListView.as_view(), name='borrowing-overdue'),
  
]