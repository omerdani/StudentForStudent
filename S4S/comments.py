
from django.shortcuts import render, redirect
from .models import Comment,CommentLike
from django.shortcuts import get_object_or_404
from .models import Post, Candidate, Student, Graduate, Admin, Like, Comment
from django.http import HttpResponse
from django.urls import reverse


def edit_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if request.method == 'POST':
        comment.text = request.POST.get('text')
        comment.save()
        email = comment.user_email
        return redirect('post_detail', post_id=comment.post.id)

    return render(request, 'edit_comment.html', {'comment': comment})


from S4S.models import Comment, CommentLike, Candidate, Student, Graduate, Admin

def like_comment(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    post_id = comment.post.id
    user_id = request.session.get('user_id')
    user_type = request.session.get('user_type')

    if user_type == 'candidate':
        user = Candidate.objects.get(id=user_id)
        like = CommentLike.objects.filter(user_candidate=user, comment=comment)
    elif user_type == 'student':
        user = Student.objects.get(id=user_id)
        like = CommentLike.objects.filter(user_student=user, comment=comment)
    elif user_type == 'graduate':
        user = Graduate.objects.get(id=user_id)
        like = CommentLike.objects.filter(user_graduate=user, comment=comment)
    elif user_type == 'admin':
        user = Admin.objects.get(id=user_id)
        like = CommentLike.objects.filter(user_admin=user, comment=comment)

    if like:
        like.delete()
        comment.likes_count -= 1
    else:
        CommentLike.objects.create(**{f'user_{user_type}': user, 'comment': comment})
        comment.likes_count += 1

    comment.save()
    return redirect(reverse('post_detail', args=[post_id]))

from django.shortcuts import render
from .models import Comment, CommentLike, Candidate, Student, Graduate, Admin

def comment_detail(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    user_id = request.session.get('user_id')
    user_type = request.session.get('user_type')

    if user_type == 'candidate':
        user = Candidate.objects.get(id=user_id)
        has_liked_comment = CommentLike.objects.filter(user_candidate=user, comment=comment).exists()
    elif user_type == 'student':
        user = Student.objects.get(id=user_id)
        has_liked_comment = CommentLike.objects.filter(user_student=user, comment=comment).exists()
    elif user_type == 'graduate':
        user = Graduate.objects.get(id=user_id)
        has_liked_comment = CommentLike.objects.filter(user_graduate=user, comment=comment).exists()
    elif user_type == 'admin':
        user = Admin.objects.get(id=user_id)
        has_liked_comment = CommentLike.objects.filter(user_admin=user, comment=comment).exists()

    return render(request, 'comment_detail.html', {'has_liked_comment': has_liked_comment, 'comment': comment})
