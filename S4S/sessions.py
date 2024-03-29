from django.http import HttpResponse
from django.contrib.sessions.models import Session
from datetime import datetime, timezone
from S4S.models import Candidate, Student, Graduate, User
from django.contrib.auth.models import User

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
        elif user_type == 'superuser':
            user = User.objects.get(id=user_id)
        first_name = user.first_name
        last_name = user.last_name

    try:
        session = Session.objects.get(session_key=session_key)
        session_length = session.expire_date - datetime.now(timezone.utc)
    except Session.DoesNotExist:
        session_length = 'Session does not exist'

    return HttpResponse(f"User ID: {user_id}, User Type: {user_type}, First Name: {first_name}, Last Name: {last_name} , Email : {user.email}, Session Length: {session_length}")
def active_sessions(request):
    session_key_list = []
    for session in Session.objects.all():
        if '_auth_user_id' in session.get_decoded():  # check if user is logged in
            session_key_list.append(session.session_key)
    return HttpResponse(f"Active sessions: {session_key_list}")