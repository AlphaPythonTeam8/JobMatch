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
        text=f"Hi,\nPlease click on the link below to verify your email address:\nhttp://http://127.0.0.1:8000/verify_email?token={token}",
    )

    # Create a Mailtrap client and send the email
    client = MailtrapClient(token=API_KEY)
    client.send(mail)

    print(f'Verification email sent to {email_to}')
