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
    reset_code = models.CharField(max_length=10, null=True, blank=True)


class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    select_year = models.IntegerField()
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=100)
    reset_code = models.CharField(max_length=10, null=True, blank=True)


class Graduate(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    work_place = models.CharField(max_length=20)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=100)
    reset_code = models.CharField(max_length=10, null=True, blank=True)

class Admin(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
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
    title = models.CharField(max_length=100, default='')
    content = models.TextField(default='')
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title

class Post2(models.Model):
    title = models.CharField(max_length=100)
    user_name = models.CharField(default="none", max_length=100)
    user_email = models.EmailField(null=True)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE, null=True)
    candidate = models.ForeignKey('Candidate', on_delete=models.CASCADE, null=True, blank=True)
    student = models.ForeignKey('Student', on_delete=models.CASCADE, null=True, blank=True)
    graduate = models.ForeignKey('Graduate', on_delete=models.CASCADE, null=True, blank=True)
    admin = models.ForeignKey('Admin', on_delete=models.CASCADE, null=True, blank=True)
    comment_count = models.IntegerField(default=0)
    likes_count = models.IntegerField(default=0)


    def __str__(self):
        return self.title
class Comment(models.Model):
    post = models.ForeignKey(Post2, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    user_email = models.EmailField(null=True)
    likes_count = models.IntegerField(default=0)
    has_liked_comment = models.BooleanField(default=False)



class Notification(models.Model):
    candidate = models.ForeignKey('Candidate', on_delete=models.CASCADE, null=True, blank=True)
    student = models.ForeignKey('Student', on_delete=models.CASCADE, null=True, blank=True)
    graduate = models.ForeignKey('Graduate', on_delete=models.CASCADE, null=True, blank=True)
    admin = models.ForeignKey('Admin', on_delete=models.CASCADE, null=True, blank=True)
    post = models.ForeignKey(Post2, on_delete=models.CASCADE)
    seen = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    user_candidate = models.ForeignKey('Candidate', on_delete=models.CASCADE, null=True, blank=True)
    user_student = models.ForeignKey('Student', on_delete=models.CASCADE, null=True, blank=True)
    user_graduate = models.ForeignKey('Graduate', on_delete=models.CASCADE, null=True, blank=True)
    user_admin = models.ForeignKey('Admin', on_delete=models.CASCADE, null=True, blank=True)
    post = models.ForeignKey('Post2', on_delete=models.CASCADE)

class CommentLike(models.Model):
    user_candidate = models.ForeignKey('Candidate', on_delete=models.CASCADE, null=True, blank=True)
    user_student = models.ForeignKey('Student', on_delete=models.CASCADE, null=True, blank=True)
    user_graduate = models.ForeignKey('Graduate', on_delete=models.CASCADE, null=True, blank=True)
    user_admin = models.ForeignKey('Admin', on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE)