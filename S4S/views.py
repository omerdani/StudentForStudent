# Create your views here.
import datetime
from django.shortcuts import render, redirect
from .models import Candidate, Student, Graduate, Post, Post2, Like
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
            work_place = request.POST.get('workplace')
            Graduate.objects.create(first_name=first_name, last_name=last_name, work_place=work_place, email=email, password=password)

        return render(request,'Login.html')

    return render(request, 'SignUp.html')


def login(request):
    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')

        print(f"Email: {email}, Password: {password}")

        candidate = Candidate.objects.filter(email=email).first()
        student = Student.objects.filter(email=email).first()
        graduate = Graduate.objects.filter(email=email).first()

        print(f"Candidate: {candidate}, Student: {student}, Graduate: {graduate}")

        if candidate and candidate.password == password:
            request.session['user_id'] = candidate.id
            request.session['user_type'] = 'candidate'
        elif student and student.password == password:
            request.session['user_id'] = student.id
            request.session['user_type'] = 'student'
        elif graduate and graduate.password == password:
            request.session['user_id'] = graduate.id
            request.session['user_type'] = 'graduate'
        else:
            user = User.objects.filter(email=email).first()
            if user and user.check_password(password) and user.is_superuser:  # Check if the user is a superuser and if the password is correct
                request.session['user_id'] = user.id
                request.session['user_type'] = 'superuser'
                return redirect('superuser_home')
            else:
                return render(request, 'Login.html')

        print(f"User ID: {request.session.get('user_id')}, User Type: {request.session.get('user_type')}")  # Print the user's ID and type

        return redirect('')
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
        return render(request, 'MainForum.html', {'user': user})
    else:
        return render(request, 'Home.html')


def forgotpassword(request):
    return render(request, 'ForgotPassword.html')
def mainforum2(request):
    return render(request, 'after_login_forum.html')
def mainforum(request):
    return render(request, 'MainForum.html')


