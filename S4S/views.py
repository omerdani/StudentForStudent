from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'Home.html')

def signup(request):
    return render(request, 'SignUp.html')

def forgotpassword(request):
    return render(request, 'ForgotPassword.html')