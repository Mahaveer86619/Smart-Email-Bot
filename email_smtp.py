import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import socket

from configs import SMTP_SERVER, SMTP_PORT


def send_email_smtp(recipients, subject, body, sender_email, smtp_password):
    """
    Send an email via SMTP.

    Args:
        recipients (list[str] or str): Recipient email(s).
        subject (str): Email subject.
        body (str): Email body (plain text).
        sender_email (str): Sender's email address.
        smtp_password (str): SMTP password.
    """
    if isinstance(recipients, str):
        recipients = [recipients]

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        # Validate SMTP_SERVER is a valid hostname or IP
        try:
            socket.gethostbyname(SMTP_SERVER)
        except socket.gaierror:
            raise ValueError(
                f"SMTP_SERVER '{SMTP_SERVER}' is not a valid hostname or IP address. Please check your configs."
            )

        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10) as smtp_server:
            smtp_server.ehlo()
            smtp_server.starttls()
            smtp_server.ehlo()
            smtp_server.login(sender_email, smtp_password)
            smtp_server.sendmail(sender_email, recipients, msg.as_string())
    except ValueError as e:
        print(e)
        raise
    except smtplib.SMTPException as e:
        print(f"SMTP error occurred: {e}")
        raise
    except OSError as e:
        print(
            f"Network error occurred: {e}. Check your SMTP_SERVER address and network connection."
        )
        raise
        print(
            f"Network error occurred: {e}. Check your SMTP_SERVER address and network connection."
        )
        raise
