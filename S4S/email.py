import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.http import HttpResponseBadRequest
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import random
import string
from .models import Candidate, Student, Graduate
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages


def send_email(to_email):
    # Generate a unique code
    reset_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    smtp_server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    smtp_server.starttls()
    smtp_server.login("s4s.sami.forum@gmail.com", "wpkw qfjd xxyg pwhe")
    msg = MIMEMultipart()

    msg['From'] = "s4s.sami.forum@gmail.com"
    msg['To'] = to_email
    msg['Subject'] = "Reset your password"

    msg.attach(MIMEText(f'Your reset code is: {reset_code}', 'plain'))
    smtp_server.send_message(msg)
    smtp_server.quit()
    return reset_code


@csrf_exempt
def send_test_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            try:

                if Candidate.objects.filter(email=email).exists():
                    user = Candidate.objects.get(email=email)
                elif Student.objects.filter(email=email).exists():
                    user = Student.objects.get(email=email)
                elif Graduate.objects.filter(email=email).exists():
                    user = Graduate.objects.get(email=email)
                else:
                    raise ObjectDoesNotExist

                reset_code = send_email(email)
                user.reset_code = reset_code
                user.save()

                request.session['email'] = email

                return redirect('enter_code')

            except ObjectDoesNotExist:
                return HttpResponseBadRequest("Email does not exist")
        else:
            return HttpResponseBadRequest("Email is required")
    return render(request, 'sent_test_email.html')



@csrf_exempt
def enter_code(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        new_password = request.POST.get('new_password')
        email = request.session.get('email')

        print(f"Email from request: {email}")


        user = None
        if Candidate.objects.filter(email=email).exists():
            user = Candidate.objects.get(email=email)
        elif Student.objects.filter(email=email).exists():
            user = Student.objects.get(email=email)
        elif Graduate.objects.filter(email=email).exists():
            user = Graduate.objects.get(email=email)

        print(f"User object: {user}")

        if user is None:
            return HttpResponseBadRequest("Invalid email")

        if code == user.reset_code:
            user.password = new_password
            user.reset_code = None
            user.save()
            return render(request, 'Login.html')
        else:
            messages.error(request, 'הקוד שהוזן לא תואם את הקוד שנשלח למייל שלך, אנא נסה שוב.')
            return render(request, 'enter_code.html')
    return render(request, 'enter_code.html')