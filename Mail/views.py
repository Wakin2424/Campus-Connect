from django.shortcuts import render
from django.core.mail import send_mail, EmailMultiAlternatives

from Auth import models

# Create your views here.
def registrationRequest(request):
    pass 

def postTransactionMessage():
    pass

def clientNotification():
    pass

def sendForgotPasswordURL(url, user_email):
    subject = "Reset Password - Campus Connect"
    to = user_email

    message = f""

    html_content = """
    
    """

    msg = EmailMultiAlternatives(subject, message, None, to)
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
    pass