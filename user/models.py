import email
from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime

STATUS_CHOICES = [
    ('active', 'Active'),
    ('inactive', 'Inactive'),
]

class User(AbstractUser):
    username = models.CharField(max_length=20, unique=True, blank=False, null=False )
    full_name = models.CharField(max_length=100, blank=False, null=False)
    password = models.CharField(max_length=128, blank=False, null=False)
    email = models.EmailField(max_length=254, unique=True, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    birth_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    REQUIRED_FIELDS = ['email', 'full_name',  'password']
    
    
    def __str__(self):
        return f"{self.full_name} - ({self.username})"
    
    
    
    


