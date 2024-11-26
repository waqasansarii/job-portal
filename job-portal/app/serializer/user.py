from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail,BadHeaderError
from django.conf import settings

from rest_framework import serializers 
from rest_framework.response import Response

from ..models import User,Profile,ProfileJobSeeker
from ..utils import generate_otp,verify_otp


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
    # profile = serializers.PrimaryKeyRelatedField(queryset = Profile.objects.all(),source ='profile_user')
    class Meta:
        model = User
        fields = ['id','role','email']
        
 
        
class ProfileSerializer (serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model =  Profile
        fields =['first_name','last_name','email','gender','dob','company_name'
                 ,'company_size','country','city','logo','user','created_at']
        # depth = 1
    
    # Customize the output to include the `user` field
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data  # Add `user` data in output only
        return representation   


class ProfileJobSeekerSerializer (serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model =  ProfileJobSeeker
        fields =['first_name','last_name','gender','dob','qualification'
                 ,'cv','country','city','profile_image','user','created_at']
        # depth = 1
    
    # Customize the output to include the `user` field
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data  # Add `user` data in output only
        # representation['email'] = instance.user.email  # Add `user` data in output only
        return representation   


class UserProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True,source='profile_user',many=True)
    class Meta:
        model = User
        fields=['profile']        
        