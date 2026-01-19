from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Profile
from django.http import HttpResponse
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer, UserProfileSerializer  # ✅ Only import what's defined

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate



from rest_framework.generics import UpdateAPIView, DestroyAPIView
from .serializers import UpdateUsernameSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class UpdateUsernameView(UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = UpdateUsernameSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_object(self):
        return self.request.user  # Updates username of logged-in user
    


class DeleteUserProfileView(DestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserProfileSerializer
    lookup_field = 'id'  # allow URL like: /api/delete-user/3/
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": f"User with ID {kwargs['id']} deleted successfully"},
            status=status.HTTP_200_OK
        )

class LoginAPIView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)


# Home view
def home(request):
    return HttpResponse("Welcome to Django Auth API")

# ✅ Register/List Users API (No JWT required here, since this is for sign up)
class UserProfileListCreate(ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = UserProfileSerializer

# ✅ Protected View Example: List all profiles (Requires JWT)
class ProtectedProfileList(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Profile.objects.all()
    serializer_class = UserProfileSerializer

# Custom Token Obtain Pair View

from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    


