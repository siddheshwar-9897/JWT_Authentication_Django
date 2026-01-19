from rest_framework import serializers
from .models import Profile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}  # Prevent password from being returned
        }

    def create(self, validated_data):
        password = validated_data.pop('password')  # Get and remove plain password
        user = Profile(**validated_data)
        user.set_password(password)  # Hash the password ✅
        user.save()
        return user


class UpdateUsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['username']  # Only username is updatable here


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(request=self.context.get('request'), email=email, password=password)

        if not user:
            raise serializers.ValidationError("Invalid email or password")

        refresh = self.get_token(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user_id': user.id,
            'email': user.email,
            'username': user.username
        }

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['username'] = user.username
        return token
