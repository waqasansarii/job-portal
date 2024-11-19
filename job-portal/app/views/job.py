from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.pagination import PageNumberPagination

from ..permissions import IsEmployeerOrReadOnly,IsOwner
from ..serializer.job_serializer import JobSerializer,JobStatusSerializer
from ..models import Jobs


class JobView(ModelViewSet,PageNumberPagination):
    queryset = Jobs.objects.select_related('user').all()
    serializer_class = JobSerializer
    permission_classes = [IsOwner,IsEmployeerOrReadOnly]
    page_size = 20  # Number of items per page
    page_size_query_param = 'page_size'  # Allow clients to set the page size
    max_page_size = 100  # Maximum page size allowed

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
    
    
        
        
    
    
