from django_filters import rest_framework as filters
from .models import Jobs

class JobFilters(filters.FilterSet):
    job_type = filters.ChoiceFilter(field_name='job_type',lookup_expr='exact',choices=Jobs.Job_type)
    city = filters.CharFilter(field_name='user__profile_user__city',lookup_expr='icontains')
    country = filters.CharFilter(field_name='user__profile_user__country',lookup_expr='icontains')
    company_name = filters.CharFilter(field_name='user__profile_user__company_name',lookup_expr='icontains')
    
    class Meta:
        model = Jobs
        fields=['job_type','city','country','company_name']