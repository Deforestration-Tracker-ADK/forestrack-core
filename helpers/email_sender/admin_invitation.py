from helpers.email_sender.email_sender import send_email


def admin_invitation_email(email, data):
    subject = "Admin invitation to system - ForestRack"

    html = '<strong>Hello there, Your invited as an admin to the Forestrack system</strong> ' \
           f'email:- {data["email"]} , password:- {data["password"]},Please verify your email using the following ' \
           f'link</strong> ' \
           f'link {data["email_verify_link"]}'

    send_email(email, subject, html)
