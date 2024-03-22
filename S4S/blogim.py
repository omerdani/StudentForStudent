
from django.shortcuts import render
from .models import Blog, Post2, Candidate, Student, Graduate,Comment
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from .forms import CommentForm

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

    post = Post2.objects.get(id=post_id)
    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()

        return redirect('blog_detail', blog_id=post.blog.id)


    return render(request, 'edit_post.html', {'post': post})


def delete_post(request, post_id):
    if request.method == 'POST':
        post = Post2.objects.get(pk=post_id)
        blog_id = post.blog.id
        post.delete()
        posts = Post2.objects.all()
        return redirect('blog_detail', blog_id=blog_id)

from django.shortcuts import render, get_object_or_404, redirect
from .models import Post2, Comment
from .forms import CommentForm

def post_detail(request, post_id):
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

    post = get_object_or_404(Post2, pk=post_id)
    blog = post.blog

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = first_name + ' ' + last_name
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()
    context = {'post': post, 'blog': blog, 'form': form}
    return render(request, 'post_detail.html', context)


def add_like(request, post_id):
    post = get_object_or_404(Post2, pk=post_id)
    post.likes_count += 1
    post.save()
    return redirect('post_detail', post_id=post_id)

