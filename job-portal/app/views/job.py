from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema

from ..permissions import IsEmployeerOrReadOnly,IsOwner,IsJobSeeker
from ..serializer.job_serializer import JobSerializer,JobStatusSerializer,ApplicationSerializer
from ..models import Jobs,Applications
from ..filters import JobFilters


class JobView(ModelViewSet,PageNumberPagination):
    queryset = Jobs.objects.select_related('user__profile_user').all()
    serializer_class = JobSerializer
    permission_classes = [IsOwner,IsEmployeerOrReadOnly]
    page_size = 20  # Number of items per page
    page_size_query_param = 'page_size'  # Allow clients to set the page size
    max_page_size = 100  # Maximum page size allowed
    filter_backends=[DjangoFilterBackend]
    filterset_class= JobFilters
    
    # def get_object(self):
        
    #     return super().get_object()
    

    @action(
        detail=False,
        methods=['GET'],
        url_path='my-jobs',
        url_name='my_jobs',
        permission_classes=[IsAuthenticated]
        )
    def my_jobs(self,request:Request):
        print('running')
        query = self.queryset.filter(user= request.user.id).all()
        serializer = self.get_serializer(query,many=True)
        return Response(serializer.data,status.HTTP_200_OK)
    
    
    @action(
        detail=True,
        methods=['PUT'],
        url_path='toggle-status',
        serializer_class=JobStatusSerializer
        )
    def toggle_status(self,req:Request,pk):
        obj = self.get_object()
        # calling IsOwner permission 
        self.check_object_permissions(req,obj)
        obj.status = req.data.get('status')
        obj.save()
        job = JobSerializer(obj)
        return Response(job.data,status.HTTP_201_CREATED)
    
    @action(
        detail=True,
        url_path='apply',
        methods=['PUT'],
        serializer_class=ApplicationSerializer,
        permission_classes=[IsAuthenticated,IsJobSeeker]
        )
    def apply(self,req:Request,pk):
        try: 
            jobs = Jobs.objects.select_related('user__profile_user').get(id=pk)
        
            if Applications.objects.filter(user=req.user.id,job=jobs).exists():
                return Response({'error':'You have already applied on it'},status.HTTP_200_OK)
            application = self.get_serializer(data=req.data)
            if application.is_valid():
                try:
                    application.save(status='Applied',job=jobs,user=req.user)
                    return Response(application.data,status.HTTP_201_CREATED)
                except Exception as e:
                    return Response(str(e),status.HTTP_400_BAD_REQUEST)
            else :
                return Response({'error':application.errors},status.HTTP_400_BAD_REQUEST)
        except Jobs.DoesNotExist:
            return Response({'error':'invalid job id'},status.HTTP_400_BAD_REQUEST)  
        
    def filter_queryset(self, queryset):
        # return super().filter_queryset(queryset):
        """
        Apply filters only when not in the `my_applications` action.
        """
        # queryset = super().get_queryset()
        if self.action != 'my_applications':
            queryset = self.filter_queryset(queryset)  # Apply global filters
        return queryset
    
    def get_filterset_class(self):
        """
        Dynamically assign filter set class based on action.
        """
        if self.action == 'my_applications':
            return {}  # Custom filter for `my_jobs`
        return None 

    @action(
        detail=False,
        methods=['GET'],
        url_path='my-applications',
        permission_classes=[IsAuthenticated],
        serializer_class=ApplicationSerializer,
        
    )
    @swagger_auto_schema(
        operation_description="Get a list of applications for the authenticated user",
        manual_parameters=[],  # This will hide the query filters from Swagger documentation
        # field_inspectors=None,
        filter_inspectors=None,
        # paginator_inspectors=None
    )
    def my_applications(self, request):
        
                # Temporarily bypass the filter backends in this specific action
        # original_filter_backends = self.filter_backends
        self.filter_backends = None  # Remove filters temporarily
        # self.filterset_class=None
        # filterset = self.get_filterset_class(None)
        try:
            # Custom queryset to bypass any global filtering
            queryset = Applications.objects.select_related('user__profile_user', 'job').filter(user=request.user).all()
            # filtered = self.filter_queryset(queryset)
            
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)  
        
        # finally:
        #      self.filter_backends = original_filter_backends      
    
    
        
        
    
    
