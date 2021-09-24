from helpers.email_sender.email_sender import send_email


def volunteer_email_verify(email, data):
    subject = "Volunteer Email Verification - ForestRack"

    html = '<strong>Hello there Volunteer Please verify your email using the following link</strong> ' \
           f'link {data["email_verify_link"]}'

    send_email(email, subject, html)
