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

def send_email(to_email):
    # Generate a unique code
    reset_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

    # set up the SMTP server
    smtp_server = smtplib.SMTP(host='smtp.gmail.com', port=587)
    smtp_server.starttls()

    # Login to the email server
    smtp_server.login("omerdaniel00@gmail.com", "prur xdcz dycw qypl")

    # create a message
    msg = MIMEMultipart()

    msg['From'] = "omerdaniel00@gmail.com"
    msg['To'] = to_email
    msg['Subject'] = "Reset your password"

    # add in the message body
    msg.attach(MIMEText(f'Your reset code is: {reset_code}', 'plain'))

    # send the message via the server
    smtp_server.send_message(msg)

    # close the connection
    smtp_server.quit()

    return reset_code


@csrf_exempt
@csrf_exempt
def send_test_email(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            try:
                # Check if the email exists in any of the user models
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
            user.save()
            return render(request, 'Login.html')
        else:
            return HttpResponseBadRequest("Invalid code")
    return render(request, 'enter_code.html')