
from django.shortcuts import render
from .models import Blog, Post2, Candidate, Student,Like, Graduate,Comment, Notification,Admin
from django.shortcuts import redirect
from django.shortcuts import render, get_object_or_404
from .forms import CommentForm

from django.contrib.auth.models import User

def blog_detail(request, blog_id):
    blog = Blog.objects.get(pk=blog_id)
    posts2 = Post2.objects.filter(blog=blog)
    current_user = None
    user_type = None
    if 'user_id' in request.session and 'user_type' in request.session:
        user_id = request.session['user_id']
        user_type = request.session['user_type']
        if user_type == 'candidate':
            user = Candidate.objects.get(id=user_id)
        elif user_type == 'student':
            user = Student.objects.get(id=user_id)
        elif user_type == 'graduate':
            user = Graduate.objects.get(id=user_id)
        elif user_type == 'admin':  # Check if the user is an Admin
            user = Admin.objects.get(id=user_id)
        current_user = user.first_name + ' ' + user.last_name
    return render(request, 'blog.detail.html', {'blog': blog, 'posts2': posts2, 'current_user': current_user, 'user_type': user_type})
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
        elif user_type == 'admin':
            user = Admin.objects.get(id=user_id)
        first_name = user.first_name
        last_name = user.last_name

    if request.method == 'POST':
        title = request.POST.get('title')
        user_name = 'Admin' if user_type == 'admin' else first_name + ' ' + last_name
        content = request.POST.get('content')

        post = Post2(title=title, content=content, user_name=user_name, blog_id=blog_id)

        if user_type == 'candidate':
            post.candidate = user
        elif user_type == 'student':
            post.student = user
        elif user_type == 'graduate':
            post.graduate = user
        elif user_type == 'admin':
            post.admin = user

        post.save()

        return redirect('blog_detail', blog_id=blog_id)
    else:
        posts = Post2.objects.filter(blog_id=blog_id)

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
        elif user_type == 'admin':
            user = Admin.objects.get(id=user_id)

        first_name = user.first_name
        last_name = user.last_name

    post = get_object_or_404(Post2, pk=post_id)
    blog = post.blog
    current_user = first_name + ' ' + last_name
    has_liked = Like.objects.filter(**{f'user_{user_type}': user, 'post': post}).exists()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            if user_type == 'admin':
                comment.author = 'Admin'
            else:
                comment.author = first_name + ' ' + last_name
            comment.save()
            post.comment_count += 1
            post.save()
            post_owner_username = None
            if post.candidate:
                post_owner_username = post.candidate.first_name + ' ' + post.candidate.last_name
            elif post.student:
                post_owner_username = post.student.first_name + ' ' + post.student.last_name
            elif post.graduate:
                post_owner_username = post.graduate.first_name + ' ' + post.graduate.last_name
            elif post.admin:
                post_owner_username = post.admin.first_name + ' ' + post.admin.last_name

            if comment.author != post_owner_username:
                if post.candidate:
                    Notification.objects.create(candidate=post.candidate, post=post)
                elif post.student:
                    Notification.objects.create(student=post.student, post=post)
                elif post.graduate:
                    Notification.objects.create(graduate=post.graduate, post=post)
                elif post.admin:
                    Notification.objects.create(admin=post.admin, post=post)
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()
    context = {'post': post, 'blog': blog, 'form': form, 'current_user': current_user, 'has_liked': has_liked,'user_type': user_type}
    return render(request, 'post_detail.html', context)

def add_like(request, post_id):
    post = get_object_or_404(Post2, pk=post_id)
    post.likes_count += 1
    post.save()
    return redirect('post_detail', post_id=post_id)


def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    post_id = comment.post.id
    comment.post.comment_count -= 1
    comment.post.save()
    comment.delete()
    return redirect('post_detail', post_id=post_id)

def about_us(request):
    return render(request, 'About_us.html')

def about_us1(request):
    return render(request, 'About_us1.html')
