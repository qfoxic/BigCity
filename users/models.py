from django.contrib.auth.models import AbstractUser
from django.db import models


GENDER = [
    ['m', 'Male'],
    ['f', 'Female']
]


class Users(AbstractUser):
    resume = models.CharField(max_length=100000, null=True, blank=True)
    phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=1, choices=GENDER, default='m')
    city = models.CharField(max_length=20, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    street = models.CharField(max_length=100, null=True, blank=True)
    lng = models.CharField(max_length=50, null=True, blank=True)
    lat = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=50, null=True, blank=True)
