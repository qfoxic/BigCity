from django.contrib.auth.models import User
from django.db import models



class Users(User):
    resume = models.CharField(max_length=100000, null=True, blank=True)