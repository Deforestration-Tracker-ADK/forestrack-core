import os

from django.core.mail import EmailMultiAlternatives
from dotenv import load_dotenv

load_dotenv()


def send_email(email, subject, text, html):
    text_content = text
    html_content = html
    msg = EmailMultiAlternatives(subject, text_content, os.environ.get('COMPANY_EMAIL'), [email])
    msg.attach_alternative(html_content, "text/html")
    try:
        print(os.environ.get('COMPANY_EMAIL'))
        print(email)
        response = msg.send()
        print(response)
    except Exception as e:
        print(e)
