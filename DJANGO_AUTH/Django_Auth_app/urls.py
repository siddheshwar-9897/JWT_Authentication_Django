from django.urls import path
from .views import (
     LoginAPIView, home, UserProfileListCreate, ProtectedProfileList, CustomTokenObtainPairView, UpdateUsernameView, DeleteUserProfileView
)
# from .views import LoginView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('api/login/', LoginAPIView.as_view(), name='login'),
    path('', home, name='home'),
    path('api/register/', UserProfileListCreate.as_view(), name='register'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/profiles/', ProtectedProfileList.as_view(), name='profile_list'),
    path('api/update-username/', UpdateUsernameView.as_view(), name='update_username'),
    path('api/delete-user/<int:id>/', DeleteUserProfileView.as_view(), name='delete_user'),

]
