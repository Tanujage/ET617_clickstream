from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.username} ({self.email})"


from django.contrib.auth import get_user_model
User = get_user_model()
from django.conf import settings

class ClickEvent(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
    path = models.CharField(max_length=500, blank=True)
    event_type = models.CharField(max_length=100, blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    user_agent = models.CharField(max_length=500, blank=True)
    ip_address = models.CharField(max_length=100, blank=True)
    meta = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.event_type} @ {self.path} by {self.user or 'anon'}"
