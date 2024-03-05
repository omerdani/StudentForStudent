from django.shortcuts import render, redirect
# Create your views here.
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from .models import Candidate, Student, Graduate
def signup(request):
    if request.method == 'POST':
        status = request.POST.get('status')
        first_name = request.POST.get('name')
        last_name = request.POST.get('lastName')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if a user with the same email already exists
        if Candidate.objects.filter(email=email).exists() or \
                Student.objects.filter(email=email).exists() or \
                Graduate.objects.filter(email=email).exists():
            # If user with the same email already exists, return to signup page with an error message
            return render(request, 'SignUp.html', {'error_message': 'User with this email already exists.'})

        if status == 'Candidate':
            Candidate.objects.create(first_name=first_name, last_name=last_name, email=email, password=password)
        elif status == 'Student':
            select_year = request.POST.get('year')
            Student.objects.create(first_name=first_name, last_name=last_name, select_year=select_year, email=email, password=password)
        elif status == 'Graduate':
            work_place = request.POST.get('workplace')
            Graduate.objects.create(first_name=first_name, last_name=last_name, work_place=work_place, email=email, password=password)

        # Redirect to some page after successful signup
        return redirect('signup_success')  # Replace 'signup_success' with your URL name for signup success page

    return render(request, 'SignUp.html')  # Replace 'SignUp.html' with the actual path to your HTML template

# Similarly, define views for signup and forgot password forms
def display_data(request):
    candidates = Candidate.objects.all()
    students = Student.objects.all()
    graduates = Graduate.objects.all()
    return render(request, 'display_data.html', {'candidates': candidates, 'students': students, 'graduates': graduates})
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # If authentication is successful, log in the user
            auth_login(request, user)
            # Redirect to the home page
            print(f"works")
            return redirect('home')  # Assuming 'home' is the URL name for the home page
        else:
            # If authentication fails, return an error message or render the login page again
            return render(request, 'Login.html', {'error_message': 'Invalid username or password'})

    return render(request, 'Login.html')

def home(request):
    return render(request, 'Home.html')

def forgotpassword(request):
    return render(request, 'ForgotPassword.html')