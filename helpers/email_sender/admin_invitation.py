from django.template.loader import render_to_string
from django.utils.html import strip_tags

from helpers.email_sender.email_sender import send_email


def admin_invitation_email(email, data):
    subject = "Admin invitation to system - ForestRack"
    html_content = render_to_string('admin_invitation.html', {"registerURL": data["email_verify_link"],
                                                              "email": data["email"],
                                                              "password": data[
                                                                  "password"]})  # render with dynamic value
    text_content = strip_tags(html_content)

    send_email(email, subject, text_content, html_content)
