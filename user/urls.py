from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from user.views import UserCreate,UserList, UserUpdate, UserDelete, UserWithActiveBorrowingList
from user.serializer import CustomTokenObtainPairSerializer

urlpatterns = [
    path('create/', UserCreate.as_view(), name='user-create'),
    path('list/', UserList.as_view(), name='user-list'),
    path('update/<int:pk>/', UserUpdate.as_view(), name='user-update'),
    path('delete/<int:pk>/', UserDelete.as_view(), name='user-delete'),
    path('borrowing/', UserWithActiveBorrowingList.as_view(), name='user-borrowing'),
    path('signin/', TokenObtainPairView.as_view(serializer_class=CustomTokenObtainPairSerializer), name='user-signin'),
]
