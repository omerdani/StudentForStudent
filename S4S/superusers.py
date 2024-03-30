from django.shortcuts import render, redirect
from S4S.models import Post2, Candidate, Student, Graduate
from django.contrib.auth.models import User

def superuser_home(request):

    user_id = request.session.get('user_id')
    user_type = request.session.get('user_type')
    if user_id and user_type == 'admin':

        return render(request, 'superuser_home.html')
    else:

        return redirect('login')

def delete_post_Admin(request, post_id):
        if request.method == 'POST':
            post = Post2.objects.get(pk=post_id)
            post.delete()
            posts = Post2.objects.all()
        return render(request, 'after_login_forum.html', {'posts': posts})


def manage_users(request):
    candidates = Candidate.objects.all()
    students = Student.objects.all()
    graduates = Graduate.objects.all()

    return render(request, 'manage_users.html', {'candidates': candidates, 'students': students,
                                                 'graduates': graduates})

def delete_user(request, user_id):
    if request.method == 'POST':
        status = request.POST.get('status')
        if status == 'candidate':
            candidate = Candidate.objects.get(pk=user_id)
            candidate.delete()
        elif status == 'student':
            student = Student.objects.get(pk=user_id)
            student.delete()
        elif status == 'graduate':
            graduate = Graduate.objects.get(pk=user_id)
            graduate.delete()
        return redirect('manage_users')