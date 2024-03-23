from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Post2, Candidate, Student, Graduate
from django.shortcuts import redirect
from django import forms
from django.contrib.auth.models import User


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
def my_profile(request):
    user_id = request.session.get('user_id', None)
    user_type = request.session.get('user_type', None)
    user = None
    posts = None

    if user_id and user_type:
        if user_type == 'candidate':
            user = Candidate.objects.get(id=user_id)
            posts = Post2.objects.filter(candidate=user)
        elif user_type == 'student':
            user = Student.objects.get(id=user_id)
            posts = Post2.objects.filter(student=user)
            year= Student.objects.get(id=user_id).select_year
        elif user_type == 'graduate':
            user = Graduate.objects.get(id=user_id)
            posts = Post2.objects.filter(graduate=user)

    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('My_Profile')
    else:
        form = EditProfileForm(instance=user)

    return render(request, 'My_Profile.html', {'user': user, 'posts': posts, 'form': form, 'user_type': user_type})