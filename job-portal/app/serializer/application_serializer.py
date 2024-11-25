from rest_framework import serializers

from ..models import Jobs,Applications,Notifications
from .user import ProfileSerializer
from .job_serializer import JobApplicationSerializer


class ApplicationSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    applicant = serializers.SerializerMethodField()
    class Meta:
        model = Applications
        fields=['id','user','created_at','job','status','applicant']        
        read_only_fields = ['job', 'status']
    
    def get_applicant(self,obj):
        profile = getattr(obj.user,'profile_user',None)
        if profile:
            return ProfileSerializer(profile).data
        return None    
        
    def to_representation(self, instance):
        reperesetation= super().to_representation(instance)   
        reperesetation['job'] = JobApplicationSerializer(instance.job).data
        return reperesetation 
        

class ApplicationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Applications
        fields=['status']  
        
        

class NotificationSerializer(serializers.ModelSerializer):
    # job = JobApplicationSerializer(read_only=True)
    applicant = serializers.SerializerMethodField()
    class Meta :
        model = Notifications
        fields = ['id','content','job','sender','reciever','applicant','created_at'] 
        
    def get_applicant(self,obj):
        profile = getattr(obj.sender,'profile_user',None)
        if profile:
            return ProfileSerializer(profile).data
        return None    
        
    def to_representation(self, instance):
        representation= super().to_representation(instance)
        print(self.context['request'].user.role)
        representation['job'] = JobApplicationSerializer(instance.job).data
        if self.context['request'].user.role !=1:
            representation.pop('applicant')
        # representation['user'] = ProfileSerializer(instance.sender).data
        representation.pop('reciever')
        representation.pop('sender')
        
        return representation
                        