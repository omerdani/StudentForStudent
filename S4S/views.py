# Create your views here.
import datetime
from django.shortcuts import render, redirect
from .models import Candidate, Student, Graduate, Post, Post2, Like,Admin
from django.http import HttpResponse
from django.contrib.sessions.models import Session
from datetime import datetime, timezone
from django.contrib.auth.models import User


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
            workplace = request.POST.get('workplace')
            Graduate.objects.create(first_name=first_name, last_name=last_name, workplace=workplace, email=email, password=password)

        return render(request,'Login.html')

    return render(request, 'SignUp.html')


def login(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')

        candidate = Candidate.objects.filter(email=email).first()
        student = Student.objects.filter(email=email).first()
        graduate = Graduate.objects.filter(email=email).first()
        admin = Admin.objects.filter(email=email).first()

        if candidate and candidate.password == password:
            request.session['user_id'] = candidate.id
            request.session['user_type'] = 'candidate'
            return render(request, 'MainForum.html', {'user': candidate})
        elif student and student.password == password:
            request.session['user_id'] = student.id
            request.session['user_type'] = 'student'
            return render(request, 'MainForum.html', {'user': student})
        elif graduate and graduate.password == password:
            request.session['user_id'] = graduate.id
            request.session['user_type'] = 'graduate'
            return render(request, 'MainForum.html', {'user': graduate})
        elif admin and admin.password == password:
            request.session['user_id'] = admin.id
            request.session['user_type'] = 'admin'
            return render(request, 'superuser_home.html', {'user': admin})
        else:
            user = User.objects.filter(email=email).first()
            if user and user.check_password(password) and user.is_superuser:
                request.session['user_id'] = user.id
                request.session['user_type'] = 'superuser'
                return render(request, 'superuser_home.html', {'user': user})
            else:
                return render(request, 'Login.html')

    else:
        return render(request, 'Login.html')
def logout(request):
    request.session.flush()
    return redirect('login')


def home(request):
    user_id = request.session.get('user_id')
    user_type = request.session.get('user_type')

    if user_id and user_type:
        if user_type == 'candidate':
            user = Candidate.objects.get(id=user_id)
        elif user_type == 'student':
            user = Student.objects.get(id=user_id)
        elif user_type == 'graduate':
            user = Graduate.objects.get(id=user_id)
        elif user_type == 'admin':
            user = Admin.objects.get(id=user_id)
        else:

         return HttpResponse('Unexpected user type', status=400)
        return render(request, 'MainForum.html', {'user': user})
    else:
        return render(request, 'Home.html')


def forgotpassword(request):
    return render(request, 'ForgotPassword.html')
def mainforum2(request):
    return render(request, 'after_login_forum.html')
def mainforum(request):
    return render(request, 'MainForum.html')


