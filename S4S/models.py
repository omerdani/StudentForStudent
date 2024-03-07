from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.

class UserProfile(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

class Candidate(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=100)
class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    select_year = models.IntegerField()
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=100)

class Graduate(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    work_place = models.CharField(max_length=20)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=100)

class ForgotPassword(models.Model):
    email = models.EmailField(max_length=254)