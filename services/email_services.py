from mailtrap import Address, Mail, MailtrapClient
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.environ.get("API_KEY")


def send_verification_email(email_to, token):
    # Create a Mailtrap mail object
    mail = Mail(
        sender=Address(email="mailtrap@example.com", name="Mailtrap Test"),
        to=[Address(email=email_to)],
        subject="Verify your email",
        text=f"Hi,\nPlease click on the link below to verify your email address:\nhttp://127.0.0.1:8000/verify_email?token={token}",
    )

    # Create a Mailtrap client and send the email
    client = MailtrapClient(token=API_KEY)
    response = client.send(mail)

    if response.status_code != 200:
        return f"Failed to send email: {response.text}"

    return f"Verification email sent to {email_to}"
