import os

from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

load_dotenv()


def send_email(email, subject, html):
    message = Mail(
        from_email=os.environ.get('COMPANY_EMAIL'),
        to_emails=email,
        subject=subject,
        html_content=html)
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        if not os.environ.get('TESTING', False):
            response = sg.send(message)
        # print(response.status_code)
        # print(response.body)
        # print(response.headers)
    except Exception as e:
        print(e.message)
