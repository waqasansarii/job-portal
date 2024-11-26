from django.urls import path 
from rest_framework.routers import DefaultRouter
from .views.user import (
    SignupView,LoginView,ProfileView,LogoutView,UserView,
    JobSeekerProfileView,VerifyOtpView,ChangePasswordView,
    ForgotPasswordView,ResetPasswordView
    )
from .views.job import JobView

router = DefaultRouter()
router.register('jobs',JobView)

urlpatterns = [
    path('users/signup',SignupView.as_view()),
    path('users/verify',VerifyOtpView.as_view()),
    path('users/login',LoginView.as_view()),
    path('users/logout',LogoutView.as_view()),
    path('users/forgot-password',ForgotPasswordView.as_view()),
    path('users/reset/<token>',ResetPasswordView.as_view()),
    path('users/change-password',ChangePasswordView.as_view()),
    path('users',UserView.as_view()),
    path('employer/profile',ProfileView.as_view()),
    path('job-seeker/profile',JobSeekerProfileView.as_view())
] + router.urls