
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



from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from .models import Comment, CommentLike, Candidate, Student, Graduate, Admin


def has_liked_comment(request, comment_id):
    comment = Comment.objects.get(pk=comment_id)
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
        comment.has_liked_comment = False
    else:
        CommentLike.objects.create(**{f'user_{user_type}': user, 'comment': comment})
        comment.likes_count += 1
        comment.has_liked_comment = True

    comment.save()
    return redirect(reverse('post_detail', args=[comment.post.id]))
def comment_detail(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    user_id = request.session.get('user_id')
    user_type = request.session.get('user_type')

    if user_type == 'candidate':
        user = Candidate.objects.get(id=user_id)
    elif user_type == 'student':
        user = Student.objects.get(id=user_id)
    elif user_type == 'graduate':
        user = Graduate.objects.get(id=user_id)
    elif user_type == 'admin':
        user = Admin.objects.get(id=user_id)

    user_has_liked_comment = CommentLike.objects.filter(comment=comment, **{f'user_{user_type}': user}).exists()
    return render(request, 'comment_detail.html', {'comment': comment, 'has_liked_comment': user_has_liked_comment})