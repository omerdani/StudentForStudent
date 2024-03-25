from django.shortcuts import render, redirect
from S4S.models import Post2
def superuser_home(request):

    user_id = request.session.get('user_id')
    user_type = request.session.get('user_type')
    if user_id and user_type == 'superuser':

        return render(request, 'superuser_home.html')
    else:

        return redirect('login')

def delete_post_Admin(request, post_id):
        if request.method == 'POST':
            post = Post2.objects.get(pk=post_id)
            post.delete()
            posts = Post2.objects.all()
        return render(request, 'after_login_forum.html', {'posts': posts})