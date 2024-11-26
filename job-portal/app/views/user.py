from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView,RetrieveUpdateAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.exceptions import NotFound
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema

from ..serializer.user import (
SignupSerializer,LoginSerializer,ProfileJobSeekerSerializer,
ProfileSerializer,UserSerializer,VerifySerializer,ChangePasswordSerializer,
ForgotPasswordSerializer,ResetPasswordSerializer
)
from ..models import User,Profile,ProfileJobSeeker,PasswordReset
from ..permissions import IsEmployeerOrReadOnly,IsJobSeeker
from ..utils import generate_otp,verify_otp,Util


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
    

class VerifyOtpView(APIView):
    @swagger_auto_schema( request_body=VerifySerializer)
    def post(self,req:Request):
        try:
            serializer = VerifySerializer(data=req.data)
            if serializer.is_valid():
                try:
                    user = User.objects.get(email=serializer.validated_data['email'])
                    if user.is_verified:
                        return Response({'success':'You are already verified'},status.HTTP_200_OK)
                    if serializer.validated_data['otp'] != user.email_otp:
                        return Response({'error':'given otp is wrong'},status.HTTP_200_OK)
                    # print(user)
                    verify = verify_otp(user.email_otp,serializer.validated_data['otp'],user.totp)
                    if verify:
                        user.is_verified = True
                        user.save()
                        return Response('your account has been verified',status.HTTP_201_CREATED)
                    else:
                        return Response({'error':'otp is expired'},status.HTTP_200_OK)
                        
                except User.DoesNotExist:
                    return Response({'error':'Wrong email'},status.HTTP_200_OK) 
            else:
                return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)       
            
        except Exception as e:
            return Response({'data':str(e)})


class LoginView(APIView):
    
    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self,request:Request):
        data = request.data
        serializer = LoginSerializer(data=data)   
        if serializer.is_valid():     
            password = serializer.validated_data['password']
            # user1 = User.objects.filter(email=serializer.validated_data['email'],password=password).first()
            # password = make_password(serializer.validated_data['password'])
            user = authenticate(request, email= serializer.validated_data['email'],password=password)
            # print(user,'user',user1.email,user1.role,user1.is_verified)
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


class ChangePasswordView(APIView):
    permission_classes=[IsAuthenticated]
    @swagger_auto_schema(request_body=ChangePasswordSerializer)
    def post(self,req:Request):
        data = req.data
        serializer = ChangePasswordSerializer(data=data)
        if serializer.is_valid():
            is_valid_password = check_password(
                serializer.validated_data['current_password'],
                req.user.password
                )
            
            if is_valid_password:
                new_password = serializer.validated_data['new_password']
                repeat_password = serializer.validated_data['repeat_password']
                
                if new_password != repeat_password:
                    return Response(
                        {'error':'New password and confirm password should be same'},
                        status.HTTP_400_BAD_REQUEST)
                
                try:
                    new_password_hash = make_password(new_password)
                    user = User.objects.get(id = req.user.id)
                    user.password = new_password_hash
                    user.save()
                    return Response({'data':'Password has been changed'},status.HTTP_201_CREATED)
                
                except Exception as e:
                    return Response({'error':str(e)},status.HTTP_400_BAD_REQUEST)
                    
            return Response('wrong password',status.HTTP_200_OK)
        
        else:
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)

class ForgotPasswordView(APIView):
    @swagger_auto_schema(request_body=ForgotPasswordSerializer)
    def post(self,req:Request):
        data = req.data
        serializer = ForgotPasswordSerializer(data=data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                # check = check_password('1234567','pbkdf2_sha256$870000$be1D6ttubgvrkswzlViVoh$2QBiQV9RNdo9oEWDeTPeJBVQ3nhaCxckDYfYSbaiK3k=')
                # print(user.password,check)
                token_generator = PasswordResetTokenGenerator()
                token = token_generator.make_token(user)
                reset = PasswordReset.objects.create(email=email,token=token)
                reset.save()
                email_obj = {
                    'subject':'Reset password link',
                    'body':f'Please follow this link to reset your password http://localhost:8000/reset/{token}',
                    'to_email':[email]
                }
                Util.send_email(email_obj)
                return Response({'success':'Reset password link has been sent on given email'},status.HTTP_201_CREATED)
            except User.DoesNotExist:
                return Response({'error':'User is not found with given email'},status.HTTP_404_NOT_FOUND)
            
        else:
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)
        

class ResetPasswordView(APIView):
    @swagger_auto_schema(request_body=ResetPasswordSerializer)
    def post(self,req:Request,token):
        data = req.data
        serializer = ResetPasswordSerializer(data=data)
        if serializer.is_valid():
            new_password = serializer.validated_data['new_password']
            confirm_password = serializer.validated_data['confirm_password']
            if new_password != confirm_password:
                return Response({'error':'Passwords do not match'},status.HTTP_400_BAD_REQUEST)
            reset_token = PasswordReset.objects.filter(token=token).first()
            if not reset_token:
                return Response({'error':'Invalid token'},status.HTTP_400_BAD_REQUEST)
            try:
                user = User.objects.get(email=reset_token.email)
                user.set_password(new_password)
                user.save()
                reset_token.delete()
                return Response({'success':'Your password has been changed'},status.HTTP_201_CREATED)
            except User.DoesNotExist:
                return Response({'error':'User does not exist '},status.HTTP_400_BAD_REQUEST)    
            
        else:
            return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)        
                 
        
class LogoutView(APIView):
    
    def post(self,req:Request):
        # user = req.user
        # data = UserSerializer(user)
        logout(req)
        return Response('logout success',status.HTTP_200_OK)

class UserView(APIView):
    permission_classes=[IsAuthenticated]
    def get(self,req:Request):
        user = req.user
        data = UserSerializer(user)    
        return Response(data.data,status.HTTP_200_OK)
             

class ProfileView (RetrieveUpdateAPIView):
    queryset = Profile.objects.select_related('user').all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated,IsEmployeerOrReadOnly]
    def get_object(self):
        user = self.request.user
        try:
            print('user obj',user.id)
            return Profile.objects.select_related('user').get(user=user.id)
        except Profile.DoesNotExist:
            raise NotFound('Profile does not exist for the logged-in user.')
        
    def update(self, request, *args, **kwargs):
        print(request.user)
        try:
            profile = self.get_object()
            print('profile update function',profile)
            return super().update(request, *args, **kwargs)
        except NotFound:
            print('except section is running')
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                print('request user id',request.user.id)
                serializer.save(email=request.user.email)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)
                    

class JobSeekerProfileView(RetrieveUpdateAPIView):
    queryset = ProfileJobSeeker.objects.all()
    serializer_class = ProfileJobSeekerSerializer  
    permission_classes = [IsAuthenticated,IsJobSeeker]
    
    def get_object(self):
        try :
           profile = ProfileJobSeeker.objects.select_related('user').get(user=self.request.user.id)
           data = ProfileJobSeekerSerializer(profile)
        #    return Response(data.data,status.HTTP_200_OK)
           return profile
        except ProfileJobSeeker.DoesNotExist:
            raise NotFound('Profile does not exists')   
    
    def update(self, request, *args, **kwargs):
        try:
            profile = self.get_object()
            return super().update(request, *args, **kwargs)
        except NotFound:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save(email=request.user.email)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors,status.HTTP_400_BAD_REQUEST)
                    
        
                      