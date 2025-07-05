import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import socket

from configs import SENDER_EMAIL, SMTP_SERVER, SMTP_PORT, SMTP_PASSWORD


def send_email_smtp(recipients, subject, body):
    """
    Send an email via SMTP.

    Args:
        recipients (list[str] or str): Recipient email(s).
        subject (str): Email subject.
        body (str): Email body (plain text).
    """
    if isinstance(recipients, str):
        recipients = [recipients]

    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
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

        smtp_server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10)
        with smtp_server:
            smtp_server.ehlo()
            smtp_server.starttls()
            smtp_server.ehlo()
            smtp_server.login(SENDER_EMAIL, SMTP_PASSWORD)
            smtp_server.sendmail(SENDER_EMAIL, recipients, msg.as_string())
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
