from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = None
    first_name=None
    last_name = None
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    ROLES_CHOICE = [
        (0,'job-seeker'),
        (1,'employer'),
        # (2,'developer'),
        # (3,'tester')
    ]
    role = models.PositiveIntegerField(choices=ROLES_CHOICE, default=0)
    

class Profile(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.TextField(null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    GENDER = [
        ('M','Male'),
        ('F','Female')
    ]
    gender = models.CharField(choices=GENDER,default=0,max_length=50)
    dob = models.DateField(null=True,blank=True)
    company_name = models.CharField(max_length=200)
    company_size = models.IntegerField()
    country = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    logo = models.FileField(upload_to="profiles/", null=True, blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='profile_user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.first_name + ' ' + self.last_name
    

# class Task(models.Model):
    
#     Priority_choice = [
#         ('Low','Low'),
#         ('Medium','Medium'),
#         ('High','High')
#     ]
    
#     Status_Choice = [
#         ('Open','Open'),
#         ('In Progress','In Progress'),
#         ('Done','Done')
#     ]
    
#     title= models.CharField(max_length=200)
#     description= models.TextField(null=True,blank=True)
#     created_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='task_user')
#     assignee = models.ForeignKey(User,on_delete=models.CASCADE,related_name='task_assigne',null=True,blank=True)
#     project = models.ForeignKey(Project,on_delete=models.CASCADE,related_name='task_project')
#     images = models.FileField(upload_to='tasks/',null=True,blank=True)
#     priority = models.CharField(max_length=20,choices=Priority_choice,default='Low')
#     status = models.CharField(max_length=20,choices=Status_Choice, default='Open')
#     due_date = models.DateTimeField(null=True,blank=True)
    
#     def __str__(self):
#         return self.title
        
        
# class Comment(models.Model):
#     content = models.TextField()
#     created_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='comment_user')
#     task = models.ForeignKey(Task,on_delete=models.CASCADE,related_name='comment_task')
#     created_at = models.DateTimeField(auto_now_add=True)
        
    