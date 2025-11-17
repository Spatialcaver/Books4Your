import email
from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime



class User(AbstractUser):
    username = models.CharField(max_length=20, unique=True, blank=False, null=False )
    full_name = models.CharField(max_length=100, blank=False, null=False)
    password = models.CharField(max_length=128, blank=False, null=False)
    email = models.EmailField(max_length=254, unique=True, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    birth_date = models.DateField(blank=False, null=False)
    status = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    
    def __str__(self):
        return f"{self.username} {self.full_name} {self.status} {self.email}"
    
    
    
    


