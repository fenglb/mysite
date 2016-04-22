import smtplib
from django.core.mail import EmailMultiAlternatives

def sendEmail( to_emails, from_email, subject, content ):
    if not isinstance(to_emails, list):
        to_emails = [to_emails,]

    text_content = 'This is an important message.'
    msg = EmailMultiAlternatives(subject, text_content, from_email, to_emails )
    msg.attach_alternative(content, "text/html")
    try:
        msg.send()
        return True
    except smtplib.SMTPException:
        return False

