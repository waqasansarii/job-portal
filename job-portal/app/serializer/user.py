from django.contrib.auth.hashers import make_password

from rest_framework import serializers 

from ..models import User,Profile


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['email','role','password']
    
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)    
        

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
       
        

class UserSerializer(serializers.ModelSerializer):
    # profile = serializers.PrimaryKeyRelatedField(queryset = Profile.objects.all(),source ='profile_user')
    class Meta:
        model = User
        fields = ['id','role']
        
        
class ProfileSerializer (serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model =  Profile
        fields =['first_name','last_name','email','gender','dob','company_name'
                 ,'company_size','country','city','logo','user','created_at']
    
    # Customize the output to include the `user` field
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = UserSerializer(instance.user).data  # Add `user` data in output only
        return representation   

class UserProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True,source='profile_user',many=True)
    class Meta:
        model = User
        fields=['profile']        
        