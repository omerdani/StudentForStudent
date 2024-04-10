from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Post2, Candidate, Student, Graduate
from django.shortcuts import redirect
from django import forms
from django.contrib.auth.models import User


class EditStudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'select_year']
class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
class EditGraduateProfileForm(forms.ModelForm):
    class Meta:
        model = Graduate
        fields = ['first_name', 'last_name', 'email', 'workplace']

def my_profile(request):
    user_id = request.session.get('user_id', None)
    user_type = request.session.get('user_type', None)
    user = None
    posts = None
    form = None

    if user_id and user_type:
        if user_type == 'candidate':
            user = Candidate.objects.get(id=user_id)
            posts = Post2.objects.filter(candidate=user)
            form = EditProfileForm(instance=user)
        elif user_type == 'student':
            user = Student.objects.get(id=user_id)
            posts = Post2.objects.filter(student=user)
            form = EditStudentProfileForm(instance=user)
        elif user_type == 'graduate':
            user = Graduate.objects.get(id=user_id)
            posts = Post2.objects.filter(graduate=user)
            form = EditGraduateProfileForm(instance=user)

    if request.method == 'POST':
        if user_type == 'student':
            form = EditStudentProfileForm(request.POST, instance=user)
        elif user_type == 'graduate':
            form = EditGraduateProfileForm(request.POST, instance=user)
        else:
            form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('My_Profile')

    return render(request, 'My_Profile.html', {'user': user, 'posts': posts, 'form': form, 'user_type': user_type})