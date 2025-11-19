from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from user.views import UserCreate, UserList, UserUpdate, UserDelete

urlpatterns = [
    path('create/', UserCreate.as_view(), name='user-create'),
    path('list/', UserList.as_view(), name='user-list'),
    path('update/<int:pk>/', UserUpdate.as_view(), name='user-update'),
    path('delete/<int:pk>/', UserDelete.as_view(), name='user-delete'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
]
