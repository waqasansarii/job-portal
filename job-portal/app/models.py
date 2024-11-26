from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = None
    first_name=None
    last_name = None
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    email_otp = models.CharField(max_length=6, null=True, blank=True)
    totp = models.CharField(max_length=32,null=True,blank=True)

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
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile_user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.first_name + ' ' + self.last_name
    

class ProfileJobSeeker(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.TextField(null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    GENDER = [
        ('M','Male'),
        ('F','Female')
    ]
    gender = models.CharField(choices=GENDER,default=0,max_length=50)
    dob = models.DateField(null=True,blank=True)
    qualification = models.TextField(null=True,blank=True)
    cv = models.FileField(upload_to="profiles/", null=True, blank=True)
    country = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    profile_image = models.FileField(upload_to="profiles/", null=True, blank=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile_job_user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.first_name + ' ' + self.last_name 
    
    

class Jobs(models.Model):
    Job_status=[
        ('Open','Open'),
        ('Closed','Closed'),
        ('On Hold','On Hold'),
        ('Filled','Filled')
    ]
    Job_type=[
        ('Full Time','Full Time'),
        ('Part time','Part time'),
        ('Contract','Contract')
    ]
        
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(choices=Job_status,max_length=200)
    skills = models.TextField()
    salary_range = models.CharField(max_length=250)
    job_type = models.CharField(max_length=200,choices=Job_type)
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='job_user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.title}"
    
    
class Applications(models.Model):
    STATUS=[
        ('Applied','Applied'),
        ('Approved','Approved'),
        ('Rejected','Rejected'),
        ('Hired','Hired')
    ]

    status = models.CharField(
        max_length=10,
        choices=STATUS,
        default=STATUS[0],
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='application_user')
    job = models.ForeignKey(Jobs,on_delete=models.CASCADE,related_name='application_job')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        unique_together = ('user', 'job')
        
    def __str__(self):
        return self.id 
    
class Notifications(models.Model):
    content = models.TextField()
    job = models.ForeignKey(Jobs,on_delete=models.CASCADE,related_name='notify_job')
    sender = models.ForeignKey(User,on_delete=models.CASCADE,related_name='notify_sender')
    reciever = models.ForeignKey(User,on_delete=models.CASCADE,related_name='notify_reciever')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
        
        
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
        
    