import os

import sendgrid
from dotenv import load_dotenv
from sendgrid import Email, To, Content, Mail

load_dotenv()


def send_email(email, subject, text, html):
    # text_content = text
    html_content = html
    # msg = EmailMultiAlternatives(subject, text_content, os.environ.get('COMPANY_EMAIL'), [email])
    # msg.attach_alternative(html_content, "text/html")
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    from_email = Email(os.environ.get('COMPANY_EMAIL'))
    to_email = To(email)
    subject = subject
    content = Content("text/html", html_content)
    mail = Mail(from_email, to_email, subject, content)
    try:
        response = sg.client.mail.send.post(request_body=mail.get())
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)
