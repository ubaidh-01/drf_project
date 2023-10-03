from rest_framework import serializers
from django.contrib.auth.models import User

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

from.models import Post
from .models import User



# REGISTER SERIALIZER
class RegisterSerializer(serializers.Serializer):
    first_name  = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()
    password  =serializers.CharField()

    def validate(self, data):
        if User.objects.filter(email = data['email']).exists():
            raise serializers.ValidationError("email Already exists !")
        
        return data
    
    def create(self, validated_data):
        user = User.objects.create(
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            email = validated_data['email'].lower()
            )
        user.set_password(validated_data['password'])
        user.save()
        return user


# LOGIN SERIALIZER
class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password  = serializers.CharField()

    def validate(self, data):
        if not User.objects.filter(email = data['email']).exists():
            raise serializers.ValidationError("Account not found !")
        
        return data
    
    def get_jwt_token(self, data):
        user  = authenticate(email = data['email'],
                             password = data['password'],)
        if not user:
            return {
                'message' : 'Invalid Credentials',
                'data' : {}
            }
        refresh = RefreshToken.for_user(user)
        return {
                'message' : 'Login Successfull !',
                'data' : { 'token': {'refresh': str(refresh),'access': str(refresh.access_token),}}
            }
        


# USER SERIALIZER
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']



# POST SERIALIZER
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ['created_at', 'updated_at']
