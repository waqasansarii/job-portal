from rest_framework import serializers

from ..models import Profile,Jobs,User
from .user import UserSerializer,ProfileSerializer,UserProfileSerializer

class JobSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # user_profile = ProfileSerializer(source='user.profile_user',read_only=True)
    profile = serializers.SerializerMethodField()
    class Meta:
        model = Jobs
        fields =['id','title','description','status','skills','job_type','salary_range','user','profile','created_at']
        
    def get_profile(self,obj):
        # print('obj user',obj.user)
        profile = getattr(obj.user,'profile_user',None)
        # profile = obj.user.profile_user
        # print(profile)
        if profile:
            return ProfileSerializer(profile).data
        return None
            
    def to_representation(self, instance):
        representation = super().to_representation(instance) 
        # representation['user'] =  UserSerializer(instance.user).data
        
        # hide salary range field if user is not logged in 
        if self.context['request'].user.is_authenticated == False:
            representation.pop('salary_range')
            return representation
        return representation  
    
    

class JobStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model =Jobs
        fields = ['status']    