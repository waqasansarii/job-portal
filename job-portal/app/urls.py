from django.urls import path 
from rest_framework.routers import DefaultRouter
from .views.user import SignupView,LoginView,UserView,ProfileView

router = DefaultRouter()
# router.register('employer/profile',ProfileView)

urlpatterns = [
    path('users/signup',SignupView.as_view()),
    path('users/login',LoginView.as_view()),
    path('users/profile',UserView.as_view()),
    path('employer/profile',ProfileView.as_view()),
] + router.urls