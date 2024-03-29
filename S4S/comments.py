
from django.shortcuts import render, redirect
from .models import Comment
def edit_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if request.method == 'POST':
        comment.text = request.POST.get('text')
        comment.save()
        email = comment.user_email
        return redirect('post_detail', post_id=comment.post.id)

    return render(request, 'edit_comment.html', {'comment': comment})