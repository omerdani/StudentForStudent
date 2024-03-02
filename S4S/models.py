from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.

class UserProfile(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

class UserRegistration(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=100)

class ForgotPassword(models.Model):
    email = models.EmailField(max_length=254)

class MyModel(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField()