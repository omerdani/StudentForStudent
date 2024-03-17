
from django.shortcuts import render
from .models import Blog, Post2

def blog_detail(request, blog_id):
    blog = Blog.objects.get(pk=blog_id)
    posts2 = Post2.objects.filter(blog=blog)
    return render(request, 'blog.detail.html', {'blog': blog, 'posts2': posts2})
