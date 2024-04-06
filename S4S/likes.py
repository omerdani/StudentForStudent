
from django.shortcuts import redirect
from django.urls import reverse
from  S4S.models import Post2, Like, Candidate, Student, Graduate,Admin
def like_post(request, post_id):
    post = Post2.objects.get(pk=post_id)
    user_id = request.session.get('user_id')
    user_type = request.session.get('user_type')
    like = None
    user = None

    if user_type == 'candidate':
        user = Candidate.objects.get(id=user_id)
        like = Like.objects.filter(user_candidate=user, post=post)
    elif user_type == 'student':
        user = Student.objects.get(id=user_id)
        like = Like.objects.filter(user_student=user, post=post)
    elif user_type == 'graduate':
        user = Graduate.objects.get(id=user_id)
        like = Like.objects.filter(user_graduate=user, post=post)
    elif user_type == 'admin':
        user = Admin.objects.get(id=user_id)
        like = Like.objects.filter(user_admin=user, post=post)

    if like:
        like.delete()
        post.likes_count -= 1
    else:
        if user_type is not None:
            Like.objects.create(**{f'user_{user_type}': user, 'post': post})
        post.likes_count += 1

    post.save()
    return redirect(reverse('post_detail', args=[post_id]))