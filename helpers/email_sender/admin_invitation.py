from helpers.email_sender.email_sender import send_email


def admin_invitation_email(email, data):
    subject = "Admin invitation to system - ForestRack"

    html = '<strong>Hello there, Your invited as an admin to the Forestrack system</strong> ' \
           f'email:- {data["email"]} , password:- {data["password"]}'

    send_email(email, subject, html)
