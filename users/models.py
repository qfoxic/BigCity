from django.contrib.auth.models import AbstractUser
from django.db import models


class Users(AbstractUser):
    resume = models.CharField(max_length=100000, null=True, blank=True)