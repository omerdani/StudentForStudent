from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
post_id = 1


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

class Post(models.Model):
    global post_id
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    id = models.IntegerField(default=post_id, primary_key=True)


    def __str__(self):
        return self.title
class Post2(models.Model):
    title = models.CharField(max_length=100)
    user_name = models.CharField(default="none", max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    id = models.IntegerField(default=post_id, primary_key=True)

    def __str__(self):
        return self.title