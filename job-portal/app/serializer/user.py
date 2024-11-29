from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail,BadHeaderError
from django.conf import settings

from rest_framework import serializers 
from rest_framework.response import Response

from ..models import User,Profile,ProfileJobSeeker
from ..utils import generate_otp,verify_otp
from ..cloudinary import CloudinaryImage


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,min_length=6)
    # email_otp = serializers.CharField()
    is_verified = serializers.BooleanField(read_only=True)
    class Meta:
        model = User
        fields = ['email','role','password','is_verified']
    
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        email_otp = generate_otp()
        print(email_otp)
        validated_data['email_otp'] = email_otp['otp']
        validated_data['totp'] = email_otp['totp']
        try :
            send_mail(
            'Account verification code',
            f'Your OTP for email verification is: {email_otp['otp']}',
            settings.EMAIL_HOST_USER,
            [validated_data['email']],
            fail_silently=False,
            )
        except BadHeaderError:
            return Response("Invalid header found.")    
        
        return super().create(validated_data)    


class VerifySerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()        


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
       

class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True,min_length=6)       
    new_password = serializers.CharField(write_only=True,min_length=6)       
    repeat_password = serializers.CharField(write_only=True,min_length=6)       
        

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','role','email','is_verified']
        
 
        
class ProfileSerializer (serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    email = serializers.EmailField(read_only=True)
    class Meta:
        model =  Profile
        fields =['first_name','last_name','email','gender','dob','company_name'
                 ,'company_size','country','city','logo','user','created_at']
    
    def update(self, instance, validated_data):

        if 'logo' in validated_data and validated_data['logo'] is not None:
            logo_url = CloudinaryImage.upload_file(validated_data['logo'], f"logo_{instance.user.id}")
            validated_data['logo'] = logo_url['result']['secure_url']
            
        return super().update(instance, validated_data)
            
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data 
        logo_url = representation.get('logo').replace('http://127.0.0.1:8000/https%3A/', 'https://')
        representation['logo'] = logo_url
        return representation   


class ProfileJobSeekerSerializer (serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    email = serializers.EmailField(read_only=True)
    class Meta:
        model =  ProfileJobSeeker
        fields =['first_name','last_name','gender','dob','qualification'
                 ,'cv','country','city','profile_image','user','email','created_at']
    

    def update(self, instance, validated_data):
        # print('serializer update')

        if 'profile_image' in validated_data and validated_data['profile_image'] is not None:
            logo_url = CloudinaryImage.upload_file(validated_data['profile_image'], f"profile_{instance.user.id}_image")
            validated_data['profile_image'] = logo_url['result']['secure_url']
        
        if 'cv' in validated_data and validated_data['cv'] is not None:
            cv_url = CloudinaryImage.upload_file(validated_data['cv'], f"cv_{instance.user.id}")
            validated_data['cv'] = cv_url['result']['secure_url']    
        # print('validated data',validated_data)    
        # print('serializer update',validated_data)
        return super().update(instance, validated_data)
            
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data 
        if 'profile_image' in representation and representation['profile_image'] is not None:
            logo_url = representation.get('profile_image').replace('http://127.0.0.1:8000/https%3A/', 'https://')
            representation['profile_image'] = logo_url
            
        if 'cv' in representation and representation['cv'] is not None:
            cv_url = representation.get('cv').replace('http://127.0.0.1:8000/https%3A/', 'https://')
            representation['cv'] = cv_url
        return representation    


class UserProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True,source='profile_user',many=True)
    class Meta:
        model = User
        fields=['profile']        
        

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    # token = serializers.CharField(read_only=True)  
    

class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(min_length=6) 
    confirm_password = serializers.CharField()         