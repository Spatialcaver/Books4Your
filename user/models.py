import email
from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import DateT



class User(AbstractUser):
    username = models.CharField(max_length=20, unique=True, blank=False, null=False )
    full_name = models.CharField(max_length=100, blank=False, null=False)
    password = models.CharField(max_length=128, blank=False, null=False)
    email = models.EmailField(max_length=254, unique=True, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    


