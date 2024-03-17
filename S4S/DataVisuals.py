from django.shortcuts import render, redirect
from .models import Candidate, Student, Graduate, Post, Post2
#from .models import post_id
def display_data(request):
    candidates = Candidate.objects.all()
    students = Student.objects.all()
    graduates = Graduate.objects.all()
    posts = Post.objects.all()
    posts2 = Post2.objects.all()
    return render(request, 'display_data.html', {'candidates': candidates, 'students': students,
                                                 'graduates': graduates, 'posts': posts, 'posts2': posts2} )
