from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class UserProfile(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

class Blog(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(default='No description')

    def __str__(self):
        return self.title

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

class Forum(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(default='No description')

    def __str__(self):
        return self.title

class ForgotPassword(models.Model):
    email = models.EmailField(max_length=254)

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title

class Post2(models.Model):
    title = models.CharField(max_length=100)
    user_name = models.CharField(default="none", max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE, null=True)
    candidate = models.ForeignKey('Candidate', on_delete=models.CASCADE, null=True, blank=True)
    student = models.ForeignKey('Student', on_delete=models.CASCADE, null=True, blank=True)
    graduate = models.ForeignKey('Graduate', on_delete=models.CASCADE, null=True, blank=True)
    likes_count = models.IntegerField(default=0)
    dislikes_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title
class Comment(models.Model):
    post = models.ForeignKey(Post2, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)


