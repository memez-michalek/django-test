from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
#from rest_framework.authtoken.models import Token
from django.utils.translation import gettext_lazy as _
import os
import binascii

class Event(models.Model):
    name = models.CharField(max_length=255, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    additional_data = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
