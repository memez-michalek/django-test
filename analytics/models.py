from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    api_token = models.CharField(max_length=100, blank=True, unique=True)

class Event(models.Model):
    name = models.CharField(max_length=255, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    additional_data = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
