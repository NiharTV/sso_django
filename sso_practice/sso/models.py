from django.db import models
from django.contrib.auth.models import AbstractUser, User


class User(AbstractUser):
    name=models.CharField(max_length=255)
    email=models.CharField(max_length=255, unique=True)
    password=models.CharField(max_length=255)
    username=None
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class BlackListedToken(models.Model):
    token = models.CharField(max_length=500)
    user = models.ForeignKey(User, related_name="token_user", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("token", "user")