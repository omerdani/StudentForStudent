# Create your views here.
import datetime
from django.shortcuts import render, redirect
from .models import Candidate, Student, Graduate, Post, Post2
from django.http import HttpResponse
from django.contrib.sessions.models import Session
from datetime import datetime, timezone

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


from django.shortcuts import redirect

def login(request):
    user_id = request.session.get('user_id')
    user_type = request.session.get('user_type')

    # If user is already logged in, redirect to home page
    if user_id and user_type:
        return redirect('')

    if request.method == 'POST':
        email = request.POST.get('username')
        password = request.POST.get('password')

        candidate = Candidate.objects.filter(email=email).first()
        student = Student.objects.filter(email=email).first()
        graduate = Graduate.objects.filter(email=email).first()

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
            return render(request, 'Login.html')

        return redirect('')
    else:
        return render(request, 'Login.html')
def logout(request):
    request.session.flush()
    return redirect('login')
def delete_post_Admin(request, post_id):           #the admin can delete every post
    if request.method == 'POST':
        post = Post2.objects.get(pk=post_id)
        post.delete()
        posts = Post2.objects.all()
    return render(request, 'after_login_forum.html',{'posts': posts})


def check_session(request):
    user_id = request.session.get('user_id', 'No user logged in')
    user_type = request.session.get('user_type', 'No user type')
    session_key = request.session.session_key
    first_name = 'No first name'
    last_name = 'No last name'

    if user_id and user_type:
        if user_type == 'candidate':
            user = Candidate.objects.get(id=user_id)
        elif user_type == 'student':
            user = Student.objects.get(id=user_id)
        elif user_type == 'graduate':
            user = Graduate.objects.get(id=user_id)
        first_name = user.first_name
        last_name = user.last_name

    try:
        session = Session.objects.get(session_key=session_key)
        session_length = session.expire_date - datetime.now(timezone.utc)
    except Session.DoesNotExist:
        session_length = 'Session does not exist'

    return HttpResponse(f"User ID: {user_id}, User Type: {user_type}, First Name: {first_name}, Last Name: {last_name}, Session Length: {session_length}")
def active_sessions(request):
    session_key_list = []
    for session in Session.objects.all():
        if '_auth_user_id' in session.get_decoded():  # check if user is logged in
            session_key_list.append(session.session_key)
    return HttpResponse(f"Active sessions: {session_key_list}")
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