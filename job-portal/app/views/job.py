from django.db import transaction

from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
# from requests import request
import requests


from ..permissions import IsEmployeerOrReadOnly,IsOwner,IsJobSeeker
from ..serializer.job_serializer import JobSerializer,JobStatusSerializer
from ..serializer.application_serializer import (
ApplicationSerializer,ApplicationStatusSerializer,NotificationSerializer
)
from ..models import Jobs,Applications,Notifications
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
        
        headers = {'x-api-key': 'CAAUXWY2gxx3sHYGMhPhJjt8jEaEH0Z5', 'Content-Type': 'application/json',           # Specify JSON content type
        'Accept': 'application/json'}
        response = requests.get('https://api.stb.gov.sg/content/attractions/v2/search?searchType=keyword&searchValues=singapore', headers=headers)
        if response.status_code!=200:
            print(response.text,response.status_code)
        
        try:
            data = response.json()
            print(data)
        except ValueError:
            print("Error: Unable to parse JSON - response content:", response.text)
            return Response({'error': 'Failed to parse JSON from API response'}, status=500)    
            
        # print('running',response.json())
        query = self.queryset.filter(user= request.user.id).all()
        serializer = self.get_serializer(query,many=True)
        return Response({'our':serializer.data,'api':data},status.HTTP_200_OK)
    
    
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
            # print('jobssssssssssss',jobs.user)
            # notify_obj = {
            #             'content':f'''{req.user} is applied on {jobs.title}''',
            #             'sender': req.user,
            #             'reciever': jobs.user,
            #             'job' : jobs
            #         }
            # print(**notify_obj)
            if Applications.objects.filter(user=req.user.id,job=jobs).exists():
                return Response({'data':'You have already applied on it'},status.HTTP_200_OK)
            application = self.get_serializer(data=req.data)
            if application.is_valid():
                try:
                    with transaction.atomic():
                        notify_obj = {
                        'content':f'''{req.user} is applied on {jobs.title}''',
                        'sender': req.user if req.user.role==0 else jobs.user,
                        'reciever': jobs.user if req.user.role==1 else req.user,
                        'job' : jobs
                        }
                    # print(notify)
                        application.save(status='Applied',job=jobs,user=req.user)
                        Notifications.objects.create(**notify_obj)
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
        
    @action(
        detail=False,
        methods=['GET'],
        url_path='notifications',
        url_name='Notifications',
        serializer_class = NotificationSerializer,
        permission_classes=[IsAuthenticated],
        
        filterset_class=None
    )
    def Notifications(self,req:Request):
        try:
            notifications = Notifications.objects.select_related(
            'job','sender__profile_user','reciever__profile_user'
            ).filter(reciever=req.user).all()
            notifications = self.get_serializer(notifications,many=True)
            return Response(notifications.data,status.HTTP_200_OK)
        except Exception as e:
            return Response({'data':str(e)})    
        
