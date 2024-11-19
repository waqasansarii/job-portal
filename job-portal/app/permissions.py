from rest_framework.permissions import BasePermission,SAFE_METHODS


class IsEmployeerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        # if request.method in ['Post']:
        #     pass
        if request.user.is_authenticated:
            if request.method in SAFE_METHODS:
                return True
        
            if request.user.role == 1:
               return True
            return False
        return request.method in SAFE_METHODS
    

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        print('has object',obj.user.id,request.user.id)
        if request in SAFE_METHODS:
            return True
        if obj.user.id == request.user.id:
            return True
        return False
        # return super().has_object_permission(request, view, obj)    