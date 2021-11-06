from django.template.loader import render_to_string
from django.utils.html import strip_tags

from helpers.email_sender.email_sender import send_email


def vio_email_verify(email, data):
    subject = "Vio Email Verification - ForestRack"
    html_content = render_to_string('vol_vio_email_verify.html',
                                    {"registerURL": data["email_verify_link"]})  # render with dynamic value
    text_content = strip_tags(html_content)

    send_email(email, subject, text_content, html_content)
