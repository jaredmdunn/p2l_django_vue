import sendgrid
from sendgrid.helpers.mail import Mail

from django.conf import settings


def send_email(to: str, subject: str, content: str, sender=settings.DEFAULT_FROM_EMAIL):
    """Sends an email using SendGrid from an authorized sender to another email

    Args:
        to (str): The email to send to.
        subject (str): The subject of the email.
        content (str): HTML content to be the body of the email.
        sender (str, optional): The authorized sender email. Default: settings.DEFAULT_FROM_EMAIL.
    """
    sg = sendgrid.SendGridAPIClient(settings.SENDGRID_API_KEY)
    mail = Mail(
        from_email=sender,
        to_emails=to,
        subject=subject,
        html_content=content
    )
    return sg.send(mail)
