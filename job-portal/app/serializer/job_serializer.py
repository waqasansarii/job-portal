from rest_framework import serializers

from ..models import Profile,Jobs
from .user import UserSerializer

class JobSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Jobs
        fields =['title','description','status','skills','job_type','salary_range','user','created_at']
        
    def to_representation(self, instance):
        representation = super().to_representation(instance) 
        representation['user'] =  UserSerializer(instance.user).data
        return representation  