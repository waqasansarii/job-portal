from rest_framework import serializers

from ..models import Jobs,Applications
from .user import ProfileSerializer

class JobSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    profile = serializers.SerializerMethodField()
    class Meta:
        model = Jobs
        fields =['id','title','description','status','skills','job_type','salary_range','user','profile','created_at']
        
    def get_profile(self,obj):
        profile = getattr(obj.user,'profile_user',None)
        # profile = obj.user.profile_user
        if profile:
            return ProfileSerializer(profile).data
        return None
            
    def to_representation(self, instance):
        representation = super().to_representation(instance) 
        
        # hide salary range field if user is not logged in 
        if self.context['request'].user.is_authenticated == False:
            representation.pop('salary_range')
            return representation
        return representation  
    
    

class JobStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model =Jobs
        fields = ['status']    
        

class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jobs
        fields =['id','title','description','status','skills','job_type','salary_range','user','created_at']
        

class ApplicationSerializer(serializers.ModelSerializer):
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    applicant = serializers.SerializerMethodField()
    class Meta:
        model = Applications
        fields=['user','created_at','job','status','applicant']        
        read_only_fields = ['job', 'status','user']
    
    def get_applicant(self,obj):
        profile = getattr(obj.user,'profile_user',None)
        if profile:
            return ProfileSerializer(profile).data
        return None    
        
    def to_representation(self, instance):
        reperesetation= super().to_representation(instance)   
        reperesetation['job'] = JobApplicationSerializer(instance.job).data
        return reperesetation 
        
        