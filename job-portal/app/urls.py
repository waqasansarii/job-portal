from django.urls import path 
from rest_framework.routers import DefaultRouter
from .views.user import SignupView,LoginView,ProfileView,LogoutView,UserView,JobSeekerProfileView
from .views.job import JobView

router = DefaultRouter()
router.register('jobs',JobView)

urlpatterns = [
    path('users/signup',SignupView.as_view()),
    path('users/login',LoginView.as_view()),
    path('users/logout',LogoutView.as_view()),
    path('users',UserView.as_view()),
    path('employer/profile',ProfileView.as_view()),
    path('job-seeker/profile',JobSeekerProfileView.as_view())
    # path('jobs',JobView.as_view())
] + router.urls