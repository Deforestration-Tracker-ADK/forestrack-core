from helpers.email_sender.email_sender import send_email


def vio_email_verify(email, data):
    subject = "Vio Email Verification - ForestRack"

    html = '<strong>Hello there Vio Please verify your email using the following link</strong> ' \
           f'link {data["email_verify_link"]}'

    send_email(email, subject, html)
