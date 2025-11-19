from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from borrowing.views import BorrowingListView, NewBorrowingView, UpdateBorrowingView
urlpatterns = [
    path('create/', NewBorrowingView.as_view(), name='borrowing-create'),
    path('list/', BorrowingListView.as_view(), name='borrowing-list'),
    path('update/<int:pk>/', UpdateBorrowingView.as_view(), name='borrowing-update')
  
]