from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate,login

from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView,ListAPIView,UpdateAPIView,ListCreateAPIView,RetrieveUpdateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.exceptions import NotFound
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema


from ..serializer.user import SignupSerializer,LoginSerializer,UserSerializer,ProfileSerializer
from ..models import User,Profile


# class SignupView(APIView):
    
#     def post(self,request:Request):
#         data = request.data
#         serializer = SignupSerializer(data=data)
#         if serializer.is_valid():
#             serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
#             serializer.save()
#             return Response(serializer.data,status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)
        
class SignupView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    
class LoginView(APIView):
    
    @swagger_auto_schema( request_body=LoginSerializer)
    def post(self,request:Request):
        data = request.data
        serializer = LoginSerializer(data=data)   
        if serializer.is_valid():     
            password = serializer.validated_data['password']
            # password = make_password(serializer.validated_data['password'])
            user = authenticate(request, email= serializer.validated_data['email'],password=password)
            print(user,'user')
            if user is not None:
                login(request,user)
                # refresh_token = RefreshToken.for_user(user)
                return Response('login success',status.HTTP_200_OK)
                # return Response({
                #     "refresh_token":str(refresh_token),
                #     "access_token": str(refresh_token.access_token),
                #     "msg":"logged in successfully"
                #     },status.HTTP_200_OK)
            else:
                return Response('Invalid credentials',status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST) 
        
# class UserView(APIView):
#     def get(self,req:Request):
#         user = req.user
#         data = UserSerializer(user)
#         return Response(data.data,status.HTTP_200_OK)
                   

class ProfileView (RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]
    # http_method_names=['PUT']
    def get_object(self):
        user = self.request.user
        try:
            print('user obj',user.id)
            return Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            raise NotFound('Profile does not exist for the logged-in user.')
        # return super().get_object()
    def update(self, request, *args, **kwargs):
        print(request.user)
        # print(request)
        # print(self.id)
        try:
            profile = self.get_object()
            print('profile update function',profile)
            return super().update(request, *args, **kwargs)
        except NotFound:
            print('except section is running')
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                
            # serializer.is_valid(raise_exception=True)
                serializer.save(user=1)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)
                    