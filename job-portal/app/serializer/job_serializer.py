from rest_framework import serializers

from ..models import Profile,Jobs
from .user import UserSerializer

class JobSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Jobs
        fields =['id','title','description','status','skills','job_type','salary_range','user','created_at']
        
    def to_representation(self, instance):
        representation = super().to_representation(instance) 
        representation['user'] =  UserSerializer(instance.user).data
        
        # hide salary range field if user is not logged in 
        if self.context['request'].user.is_authenticated == False:
            representation.pop('salary_range')
            return representation
        return representation  
    
    

class JobStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model =Jobs
        fields = ['status']    