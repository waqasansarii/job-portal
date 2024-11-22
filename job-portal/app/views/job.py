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
from ..serializer.job_serializer import JobSerializer,JobStatusSerializer,ApplicationSerializer,ApplicationStatusSerializer
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
        try:
            job = self.queryset.filter(id=pk,user=req.user).first()
            if not job:
                return Response({'error':'Job does not exists'},status.HTTP_200_OK)
            serializer = self.get_serializer(job,data=req.data)
            if serializer.is_valid():
                serializer.save(user=req.user)
                return Response(serializer.data,status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error':str(e)},status.HTTP_400_BAD_REQUEST)    

    
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
        

    @action(
        detail=False,
        methods=['GET'],
        url_path='my-applications',
        permission_classes=[IsAuthenticated],
        serializer_class=ApplicationSerializer,
        filterset_class=None
        # page_size=None
    )
    def my_applications(self, request):
        try:
            queryset = Applications.objects.select_related('user__profile_user', 'job').filter(user=request.user).all()
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST) 
        
        
    @action(
        detail=True,
        methods=['GET'],
        url_path='applicants',
        permission_classes=[IsAuthenticated],
        serializer_class=ApplicationSerializer,
        filterset_class=None
        # page_size=None
    )
    def applicants(self,request,pk):
        try:
            queryset = Applications.objects.select_related(
                'user__profile_user', 'job'
                ).filter(
                    job=pk,job__user=request.user
                ).all()
                
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)   
  
  
    @action(
        detail=True,
        methods=['PUT'],
        url_path='applicants/(?P<applicant_id>[^/.]+)/status',
        permission_classes=[IsAuthenticated,IsEmployeerOrReadOnly],
        serializer_class=ApplicationStatusSerializer,
        filterset_class=None
        # page_size=None
    )
    def update_status(self,request:Request,pk,applicant_id):
        try:
            application = Applications.objects.select_related(
                'user__profile_user', 'job'
                ).filter(
                    job=pk,job__user=request.user,id=applicant_id
                ).first()
            if not application:
                return Response({'error': 'Application does not exists'}, status=status.HTTP_400_BAD_REQUEST)   
                
            # print(application)    
            serializer = self.get_serializer(application,data=request.data)
            if serializer.is_valid():
                try:
                    serializer.save()
                    return Response(serializer.data,status.HTTP_201_CREATED)
                except Exception as e:
                    return Response(str(e),status.HTTP_400_BAD_REQUEST)
            else:
                return Response(application.errors,status.HTTP_400_BAD_REQUEST)   
        except application.DoesNotExist:
            return Response({'error': 'Application does not exists'}, status=status.HTTP_400_BAD_REQUEST)   
