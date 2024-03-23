from django.http import JsonResponse
from .models import Notification, Candidate, Student, Graduate
from django.shortcuts import get_object_or_404, redirect,render
def unseen_count(request):
    user_id = request.session.get('user_id', 'No user logged in')
    user_type = request.session.get('user_type', 'No user type')
    user = None
    if user_id and user_type:
        if user_type == 'candidate':
            user = Candidate.objects.get(id=user_id)
        elif user_type == 'student':
            user = Student.objects.get(id=user_id)
        elif user_type == 'graduate':
            user = Graduate.objects.get(id=user_id)
    unseen_count = 0
    if user:
        if user_type == 'candidate':
            unseen_count = Notification.objects.filter(candidate=user, seen=False).count()
        elif user_type == 'student':
            unseen_count = Notification.objects.filter(student=user, seen=False).count()
        elif user_type == 'graduate':
            unseen_count = Notification.objects.filter(graduate=user, seen=False).count()
    return JsonResponse({'unseen_count': unseen_count})


def mark_notification_seen(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    notification.seen = True
    notification.save()
    return redirect('notifications')
def notifications(request):
    user_id = request.session.get('user_id', 'No user logged in')
    user_type = request.session.get('user_type', 'No user type')
    user = None
    if user_id and user_type:
        if user_type == 'candidate':
            user = Candidate.objects.get(id=user_id)
        elif user_type == 'student':
            user = Student.objects.get(id=user_id)
        elif user_type == 'graduate':
            user = Graduate.objects.get(id=user_id)
    notifications = []
    if user:
        if user_type == 'candidate':
            notifications = Notification.objects.filter(candidate=user)
        elif user_type == 'student':
            notifications = Notification.objects.filter(student=user)
        elif user_type == 'graduate':
            notifications = Notification.objects.filter(graduate=user)
    context = {'notifications': notifications}
    return render(request, 'notifications.html', context)