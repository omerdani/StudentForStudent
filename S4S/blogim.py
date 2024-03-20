
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
    current_user = None
    if 'user_id' in request.session and 'user_type' in request.session:
        user_id = request.session['user_id']
        user_type = request.session['user_type']
        if user_type == 'candidate':
            user = Candidate.objects.get(id=user_id)
        elif user_type == 'student':
            user = Student.objects.get(id=user_id)
        elif user_type == 'graduate':
            user = Graduate.objects.get(id=user_id)
        current_user = user.first_name + ' ' + user.last_name
    return render(request, 'blog.detail.html', {'blog': blog, 'posts2': posts2, 'current_user': current_user})
def create_post(request, blog_id):
    user_id = request.session.get('user_id', 'No user logged in')
    user_type = request.session.get('user_type', 'No user type')
    first_name = 'No first name'
    last_name = 'No last name'
    user = None

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
        user_name = first_name + ' ' + last_name
        content = request.POST.get('content')

        post = Post2(title=title, content=content, user_name=user_name, blog_id=blog_id)

        if user_type == 'candidate':
            post.candidate = user
        elif user_type == 'student':
            post.student = user
        elif user_type == 'graduate':
            post.graduate = user

        post.save()

        return redirect('blog_detail', blog_id=blog_id)
    else:
        posts = Post2.objects.filter(blog_id=blog_id)
        return render(request, 'blog.detail.html', {'posts': posts, 'user': user})

def edit_post(request, post_id):
    # Get the post
    post = Post2.objects.get(id=post_id)

    # Check if the request method is POST
    if request.method == 'POST':
        # Update the post
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()

        # Redirect to the blog detail page
        return redirect('blog_detail', blog_id=post.blog.id)

    # If the request method is not POST, render the edit post form with the current post details
    return render(request, 'edit_post.html', {'post': post})



def delete_post(request, post_id):
    if request.method == 'POST':
        post = Post2.objects.get(pk=post_id)
        blog_id = post.blog.id  # Save the blog id before deleting the post
        post.delete()
        posts = Post2.objects.all()
        return redirect('blog_detail', blog_id=blog_id)  # Redirect to the blog detail page