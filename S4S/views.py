from django.shortcuts import render, redirect
from .models import UserProfile, UserRegistration, ForgotPassword
# Create your views here.

from django.shortcuts import render
from S4S.models import UserRegistration

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user
        user = UserRegistration(request, username=username, password=password)
        if user is not None:
            # Login successful, redirect to a success URL
            login(request, user)
            return redirect('success_url')  # Replace 'success_url' with your actual success URL
        else:
            # Authentication failed, redirect to a failure URL
            return redirect('failure_url')  # Replace 'failure_url' with your actual failure URL

    return render(request, 'Home.html')


# Similarly, define views for signup and forgot password forms

def home(request):
    return render(request, 'Home.html')

def signup(request):
    return render(request, 'SignUp.html')

def forgotpassword(request):
    return render(request, 'ForgotPassword.html')