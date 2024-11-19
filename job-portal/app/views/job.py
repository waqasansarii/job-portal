from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated

from ..permissions import IsEmployeer
from ..serializer.job_serializer import JobSerializer
from ..models import Jobs


class JobView(ModelViewSet):
    queryset = Jobs.objects.all()
    serializer_class = JobSerializer
    permission_classes = [IsAuthenticated,IsEmployeer]
    
    # def get_object(self):
    #     jobs = self.queryset
    #     return super().get_object()
    
    
