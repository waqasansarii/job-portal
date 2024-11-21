from rest_framework.permissions import BasePermission,SAFE_METHODS


class IsEmployeerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        
        if request.user.is_authenticated:
            # allowing to call get method to everyone 
            if request.method in SAFE_METHODS:
                return True
           
        #    post,put,delete method only for employer and owner 
            if request.user.role == 1:
               return True
            return False
        
            # allowing to call get method to everyone 
        return request.method in SAFE_METHODS

class IsJobSeeker(BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 0:
            return True
        return False
        # return super().has_permission(request, view)    
    

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        # print('has object',obj.user.id,request.user.id)
        if request in SAFE_METHODS:
            return True
        
        # put,delete method only for owner 
        if obj.user.id == request.user.id:
            return True
        return False