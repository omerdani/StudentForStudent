# Create your views here.
import datetime

from django.shortcuts import render, redirect
from .models import Candidate, Student, Graduate, Post, Post2
from .models import post_id
def signup(request):
    if request.method == 'POST':
        status = request.POST.get('status')
        first_name = request.POST.get('name')
        last_name = request.POST.get('lastName')
        email = request.POST.get('email')
        password = request.POST.get('password')


        if Candidate.objects.filter(email=email).exists() or \
                Student.objects.filter(email=email).exists() or \
                Graduate.objects.filter(email=email).exists():

            return render(request, 'SignUp.html', {'error_message': 'User with this email already exists.'})

        if status == 'Candidate':
            Candidate.objects.create(first_name=first_name, last_name=last_name, email=email, password=password)
        elif status == 'Student':
            select_year = request.POST.get('year')
            Student.objects.create(first_name=first_name, last_name=last_name, select_year=select_year, email=email, password=password)
        elif status == 'Graduate':
            work_place = request.POST.get('workplace')
            Graduate.objects.create(first_name=first_name, last_name=last_name, work_place=work_place, email=email, password=password)

        return render(request,'Login.html')

    return render(request, 'SignUp.html')

def display_data(request):
    candidates = Candidate.objects.all()
    students = Student.objects.all()
    graduates = Graduate.objects.all()
    posts = Post2.objects.all()
    return render(request, 'display_data.html', {'candidates': candidates, 'students': students,
                                                 'graduates': graduates, 'posts': posts})

def login(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')

        candidate = Candidate.objects.filter(email=email).first()
        student = Student.objects.filter(email=email).first()
        graduate = Graduate.objects.filter(email=email).first()
        if candidate and candidate.password == password:
            return redirect('')
        elif student and student.password == password:
            return redirect('')
        elif graduate and graduate.password == password:
            return redirect('')
        else:
            return render(request, 'Login.html', {'error': 'Invalid email or password.'})
    else:
        return render(request, 'Login.html')

def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        user_name = request.POST.get('user_name')
        content = request.POST.get('content')
        Post2.objects.create(title=title, content=content,user_name=user_name)
        posts = Post2.objects.all()
        global post_id
        post_id+=1
        return render(request, 'after_login_forum.html',{'posts': posts})
    else:
        posts = Post2.objects.all()
        return render(request, 'after_login_forum.html',{'posts': posts})

def delete_post_Admin(request, post_id):           #the admin can delete every post
    if request.method == 'POST':
        post = Post2.objects.get(pk=post_id)
        post.delete()
        posts = Post2.objects.all()
    return render(request, 'after_login_forum.html',{'posts': posts})

def home(request):
    return render(request, 'Home.html')

def forgotpassword(request):
    return render(request, 'ForgotPassword.html')
def mavo(request):
    return render(request, 'Mavo.html')
def mainforum2(request):
    return render(request, 'after_login_forum.html')
def mainforum(request):
    return render(request, 'MainForum.html')