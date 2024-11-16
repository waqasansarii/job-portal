from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate

from rest_framework import serializers 
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from ..models import User,Profile


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    class Meta:
        model = User
        fields = ['first_name','last_name','role','email','password']
    
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        
        return super().create(validated_data)    
        

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    # first_name = serializers.CharField()
    # last_name = serializers.CharField()
    # class Meta:
    #     model = User
    #     fields = ['email','password']
    # def create(self, validated_data):
    #     print(validated_data,self.context['request'])
    #     password = validated_data['password']
    #         # password = make_password(serializer.validated_data['password'])
    #     user = authenticate(self.context['request'], email= validated_data['email'],password=password)
    #     print(user,'user')
    #     if user is not None:
    #         refresh_token = RefreshToken.for_user(user)
    #         res_data= {
    #                 "refresh_token":str(refresh_token),
    #                 "access_token": str(refresh_token.access_token),
    #                 "msg":"logged in successfully"
    #                 }
    #         return res_data
    #     else:
    #         return 'invalid credentials'
    #             # return Response('Invalid credentials',status.HTTP_400_BAD_REQUEST)
    #     # return super().create(validated_data)
        
        

class UserSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(write_only=True)
    # first_name = serializers.CharField()
    # last_name = serializers.CharField()
    class Meta:
        model = User
        fields = ['id','first_name','last_name','role','email']
        
        
class ProfileSerializer (serializers.ModelSerializer):
    class Meta:
        model =  Profile
        fields ='__all__'       
        
        