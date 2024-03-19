
from django.shortcuts import render
from .models import Blog, Post2, Candidate, Student, Graduate
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.sessions.models import Session
from datetime import datetime, timezone
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


def blog_detail(request, blog_id):
    blog = Blog.objects.get(pk=blog_id)
    posts2 = Post2.objects.filter(blog=blog)
    return render(request, 'blog.detail.html', {'blog': blog, 'posts2': posts2})

def create_post(request, blog_id):
    user_id = request.session.get('user_id', 'No user logged in')
    user_type = request.session.get('user_type', 'No user type')
    first_name = 'No first name'
    last_name = 'No last name'

    if user_id and user_type:
        if user_type == 'candidate':
            user = Candidate.objects.get(id=user_id)
        elif user_type == 'student':
            user = Student.objects.get(id=user_id)
        elif user_type == 'graduate':
            user = Graduate.objects.get(id=user_id)
        first_name = user.first_name
        last_name = user.last_name
    if request.method == 'POST':
        title = request.POST.get('title')
        # Get the first name from the session
        user_name = first_name
        content = request.POST.get('content')
        Post2.objects.create(title=title, content=content, user_name=user_name, blog_id=blog_id)
        return redirect('blog_detail', blog_id=blog_id)
    else:
        posts = Post2.objects.filter(blog_id=blog_id)
        return render(request, 'blog.detail.html', {'posts': posts},{'user': user})

def delete_post_Admin(request, post_id):           #the admin can delete every post
    if request.method == 'POST':
        post = Post2.objects.get(pk=post_id)
        post.delete()
        posts = Post2.objects.all()
    return render(request, 'after_login_forum.html',{'posts': posts})

